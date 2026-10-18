#!/usr/bin/env python3
"""
Parse DevMatrix index.html and load every table row into the MySQL / MariaDB
database ``prog_toolbox``.

Schema (created automatically, safe to re-run - rows are upserted):

    toolbox_sections(id, slug, title, intro)
    toolbox_entries(id, section_id, group_name, sort_order, name, era,
                    popularity_level, popularity_note, faq_links, download_links)
    toolbox_fields(id, entry_id, field_name, field_value)

Every column of an HTML table that is not a name, a link column or the
popularity column is stored as one row in ``toolbox_fields`` so that tables
with different columns (tools, languages, .NET versions, syntax reference...)
share one schema.

Credentials are read from environment variables or a ``.env`` file placed next
to this script (git-ignored). Never commit the password.

    DB_HOST (default localhost)   DB_PORT (default 3306)
    DB_NAME (default prog_toolbox)  DB_USER   DB_PASSWORD

Usage:
    pip install -r scripts/requirements.txt
    python scripts/import_to_db.py                # parse + load
    python scripts/import_to_db.py --dry-run      # parse only, print summary
    python scripts/import_to_db.py --html path/to/index.html
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent
DEFAULT_HTML = ROOT.parent / "index.html"

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS toolbox_sections (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        slug VARCHAR(64) NOT NULL UNIQUE,
        title VARCHAR(255) NOT NULL,
        intro TEXT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS toolbox_entries (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        section_id INT UNSIGNED NOT NULL,
        group_name VARCHAR(255) NULL,
        sort_order INT NOT NULL DEFAULT 0,
        name VARCHAR(255) NOT NULL,
        era VARCHAR(128) NULL,
        popularity_level VARCHAR(32) NULL,
        popularity_note VARCHAR(255) NULL,
        faq_links TEXT NULL,
        download_links TEXT NULL,
        UNIQUE KEY uq_section_name (section_id, name),
        KEY idx_popularity (popularity_level),
        CONSTRAINT fk_entry_section FOREIGN KEY (section_id)
            REFERENCES toolbox_sections (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS toolbox_fields (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        entry_id INT UNSIGNED NOT NULL,
        field_name VARCHAR(128) NOT NULL,
        field_value MEDIUMTEXT NULL,
        UNIQUE KEY uq_entry_field (entry_id, field_name),
        CONSTRAINT fk_field_entry FOREIGN KEY (entry_id)
            REFERENCES toolbox_entries (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
]


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------
def cell_text(cell: Tag) -> str:
    """Cell text with <br> converted to newlines and whitespace tidied."""
    for br in cell.find_all("br"):
        br.replace_with("\n")
    text = cell.get_text(" ")
    lines = [" ".join(line.split()) for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def split_name_era(cell: Tag) -> tuple[str, str | None]:
    strong = cell.find(["strong", "button"])
    name = " ".join(strong.get_text().split()) if strong else cell_text(cell).split("\n")[0]
    rest = cell_text(cell).split("\n")[1:]
    era = " ".join(rest).strip()
    if era.startswith("(") and era.endswith(")"):
        era = era[1:-1]
    return name, (era or None)


def extract_links(cell: Tag, css_class: str) -> list[dict]:
    return [
        {"label": " ".join(a.get_text().split()), "url": a["href"]}
        for a in cell.find_all("a", class_=css_class)
        if a.get("href")
    ]


def parse_document(path: Path) -> list[dict]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    sections: list[dict] = []
    for sec in soup.select("main section[id]"):
        title_tag = sec.find("h2")
        intro_tag = sec.find("p")
        table = sec.find("table")
        if not title_tag or not table:
            continue
        headers = [" ".join(th.get_text().split()) for th in table.select("thead th")]
        entries: list[dict] = []
        group = None
        order = 0
        for tr in table.select("tbody tr"):
            cells = tr.find_all("td", recursive=False)
            if len(cells) == 1 and cells[0].get("colspan"):
                group = cell_text(cells[0]).strip("↓ ").strip()
                continue
            if len(cells) != len(headers):
                print(f"  ! skipped row with {len(cells)} cells in #{sec['id']}", file=sys.stderr)
                continue
            name, era = split_name_era(cells[0])
            entry = {
                "group_name": group,
                "sort_order": order,
                "name": name,
                "era": era,
                "popularity_level": None,
                "popularity_note": None,
                "faq_links": [],
                "download_links": [],
                "fields": {},
            }
            order += 1
            for header, cell in zip(headers[1:], cells[1:]):
                pop = cell.find("span", class_="pop")
                if pop:
                    entry["popularity_level"] = pop.get_text().strip()
                    note = cell.find("span", class_="pop-note")
                    entry["popularity_note"] = note.get_text().strip() if note else None
                    continue
                faq = extract_links(cell, "faq-btn")
                dl = extract_links(cell, "link-btn")
                if faq or dl:
                    entry["faq_links"] += faq
                    entry["download_links"] += dl
                    continue
                entry["fields"][header] = cell_text(cell)
            entries.append(entry)
        sections.append(
            {
                "slug": sec["id"],
                "title": " ".join(title_tag.get_text().split()),
                "intro": " ".join(intro_tag.get_text().split()) if intro_tag else None,
                "entries": entries,
            }
        )
    return sections


# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def connect():
    import pymysql

    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    if not user or password is None:
        sys.exit("DB_USER / DB_PASSWORD not set. Copy scripts/.env.example to scripts/.env and fill it in.")
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=user,
        password=password,
        database=os.environ.get("DB_NAME", "prog_toolbox"),
        charset="utf8mb4",
        autocommit=False,
    )


def save(conn, sections: list[dict]) -> tuple[int, int]:
    entry_count = field_count = 0
    with conn.cursor() as cur:
        for ddl in SCHEMA:
            cur.execute(ddl)
        for sec in sections:
            cur.execute(
                "INSERT INTO toolbox_sections (slug, title, intro) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE title = VALUES(title), intro = VALUES(intro)",
                (sec["slug"], sec["title"], sec["intro"]),
            )
            cur.execute("SELECT id FROM toolbox_sections WHERE slug = %s", (sec["slug"],))
            section_id = cur.fetchone()[0]
            for e in sec["entries"]:
                cur.execute(
                    "INSERT INTO toolbox_entries (section_id, group_name, sort_order, name, era, "
                    "popularity_level, popularity_note, faq_links, download_links) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE group_name = VALUES(group_name), sort_order = VALUES(sort_order), "
                    "era = VALUES(era), popularity_level = VALUES(popularity_level), "
                    "popularity_note = VALUES(popularity_note), faq_links = VALUES(faq_links), "
                    "download_links = VALUES(download_links)",
                    (
                        section_id, e["group_name"], e["sort_order"], e["name"], e["era"],
                        e["popularity_level"], e["popularity_note"],
                        json.dumps(e["faq_links"], ensure_ascii=False),
                        json.dumps(e["download_links"], ensure_ascii=False),
                    ),
                )
                cur.execute(
                    "SELECT id FROM toolbox_entries WHERE section_id = %s AND name = %s",
                    (section_id, e["name"]),
                )
                entry_id = cur.fetchone()[0]
                cur.execute("DELETE FROM toolbox_fields WHERE entry_id = %s", (entry_id,))
                for fname, fvalue in e["fields"].items():
                    cur.execute(
                        "INSERT INTO toolbox_fields (entry_id, field_name, field_value) VALUES (%s, %s, %s)",
                        (entry_id, fname, fvalue),
                    )
                    field_count += 1
                entry_count += 1
    conn.commit()
    return entry_count, field_count


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", type=Path, default=DEFAULT_HTML, help="path to index.html")
    ap.add_argument("--dry-run", action="store_true", help="parse only, do not touch the database")
    ap.add_argument("--with-languages", action="store_true", help="also synchronize all per-language reference tables")
    args = ap.parse_args()

    load_env(ROOT / ".env")
    sections = parse_document(args.html)
    total = sum(len(s["entries"]) for s in sections)
    print(f"Parsed {len(sections)} sections, {total} entries from {args.html}")
    for s in sections:
        print(f"  #{s['slug']:<10} {len(s['entries']):>4} entries  - {s['title']}")

    if args.dry_run:
        if args.with_languages:
            import populate_languages
            print("\n--- Synchronizing Language Reference Tables (dry-run) ---")
            populate_languages.run_sync(dry_run=True)
        return
    conn = connect()
    try:
        entries, fields = save(conn, sections)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"Saved {entries} entries and {fields} field values to {os.environ.get('DB_NAME', 'prog_toolbox')}.")

    if args.with_languages:
        import populate_languages
        print("\n--- Synchronizing Language Reference Tables ---")
        populate_languages.run_sync(dry_run=False)



if __name__ == "__main__":
    main()

