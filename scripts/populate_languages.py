#!/usr/bin/env python3
"""
Populate and synchronize per-language reference tables in MySQL (prog_toolbox).

For every language defined in ``scripts/language_data.py``:
- Creates the table if it does not already exist with the standard schema:
    (id, topic, description, example, syntax, created_at, updated_at)
- Populates core syntax, variables, decisions, loops, functions, OOP,
  design patterns, and popular project templates.
- Updates existing topic rows in place and appends new topics with sequential IDs,
  preserving existing IDs and backwards compatibility.

Credentials are read from ``scripts/.env`` or environment variables:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

Usage:
    python scripts/populate_languages.py            # run sync
    python scripts/populate_languages.py --dry-run  # preview only
    python scripts/populate_languages.py --langs python,js,typescript
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import language_data as ld  # noqa: E402


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
        sys.exit("DB_USER / DB_PASSWORD not set. Check scripts/.env or environment variables.")
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=user,
        password=password,
        database=os.environ.get("DB_NAME", "prog_toolbox"),
        charset="utf8mb4",
        autocommit=False,
    )


def parse_entries(slug: str, info: dict) -> list[dict]:
    entries: list[dict] = []
    lang_name = info["name"]
    raw_lines = info["data"].strip().splitlines()

    for raw in raw_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.replace("¶", "\n") for p in line.split("§")]
        if len(parts) == 3:
            key, example, syntax = parts
            if key in ld.STD:
                topic, desc_tmpl, category, kb = ld.STD[key]
                description = desc_tmpl.format(L=lang_name)
            else:
                topic = key
                description = f"{topic} in {lang_name}"
                category = "General"
        elif len(parts) >= 4:
            topic = parts[0]
            example = parts[1]
            syntax = parts[2]
            description = parts[3]
            category = parts[4] if len(parts) > 4 else "General"
        else:
            continue

        entries.append(
            {
                "topic": topic.strip(),
                "description": description.strip(),
                "example": example.strip(),
                "syntax": syntax.strip(),
            }
        )
    return entries


def sync_language(cur, slug: str, info: dict, dry_run: bool = False) -> tuple[int, int]:
    table = slug.lower()
    entries = parse_entries(slug, info)

    # 1. Create table if missing
    ddl = f"""
    CREATE TABLE IF NOT EXISTS `{table}` (
        `id` int NOT NULL AUTO_INCREMENT,
        `topic` varchar(255) DEFAULT NULL,
        `description` text,
        `example` text,
        `syntax` varchar(255) DEFAULT NULL,
        `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    if not dry_run:
        cur.execute(ddl)

    # 2. Check existing rows
    cur.execute(f"SHOW TABLES LIKE '{table}'")
    has_table = cur.fetchone() is not None
    existing = {}
    max_id = 0

    if has_table:
        cur.execute(f"SELECT id, topic FROM `{table}`")
        for row_id, topic in cur.fetchall():
            if topic:
                existing[topic.strip().lower()] = row_id
            if row_id and row_id > max_id:
                max_id = row_id

    updated = 0
    inserted = 0

    for item in entries:
        t_key = item["topic"].lower()
        if t_key in existing:
            row_id = existing[t_key]
            if not dry_run:
                cur.execute(
                    f"UPDATE `{table}` SET description = %s, example = %s, syntax = %s WHERE id = %s",
                    (item["description"], item["example"], item["syntax"], row_id),
                )
            updated += 1
        else:
            max_id += 1
            if not dry_run:
                cur.execute(
                    f"INSERT INTO `{table}` (id, topic, description, example, syntax) VALUES (%s, %s, %s, %s, %s)",
                    (max_id, item["topic"], item["description"], item["example"], item["syntax"]),
                )
            existing[t_key] = max_id
            inserted += 1

    return updated, inserted


def run_sync(dry_run: bool = False, langs: list[str] | None = None) -> tuple[int, int]:
    load_env(ROOT / ".env")
    conn = connect()

    if langs:
        targets = [s.strip().lower() for s in langs if s.strip()]
        selected = {k: v for k, v in ld.LANGS.items() if k in targets}
    else:
        selected = ld.LANGS

    total_up = 0
    total_in = 0

    mode_label = "[DRY-RUN] " if dry_run else ""
    print(f"{mode_label}Synchronizing {len(selected)} language tables in '{os.environ.get('DB_NAME', 'prog_toolbox')}':\n")

    try:
        with conn.cursor() as cur:
            for slug, info in selected.items():
                up, ins = sync_language(cur, slug, info, dry_run=dry_run)
                total_up += up
                total_in += ins
                status = f"{up} updated, {ins} inserted"
                print(f"  • {slug:<12} ({info['name']:<15}): {status:>22} (total {up + ins} topics)")

        if not dry_run:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print(f"\n{mode_label}Completed successfully: {total_up} topics updated, {total_in} topics inserted across {len(selected)} tables.")
    return total_up, total_in


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="simulate without writing to DB")
    ap.add_argument("--langs", type=str, default="", help="comma-separated list of slugs to sync (default: all)")
    args = ap.parse_args()

    targets = [s.strip().lower() for s in args.langs.split(",") if s.strip()] if args.langs else None
    run_sync(dry_run=args.dry_run, langs=targets)


if __name__ == "__main__":
    main()
