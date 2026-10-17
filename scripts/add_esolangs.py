"""Scrape the saved angrykoala/awesome-esolangs page in assets/ and inject an
"Esoteric Programming Languages" section (same table format as the others)
into index.html. Safe to re-run: the generated section is replaced in place.

Usage:  python scripts/add_esolangs.py
"""
import glob
import html
import os
import re
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
START = "<!-- ESOLANGS SECTION -->"
END = "<!-- /ESOLANGS SECTION -->"
TOC_LINE = '<li><a href="#esolangs">9. Esoteric Programming Languages</a></li>'


def find_asset():
    hits = glob.glob(os.path.join(ROOT, "assets", "angrykoala_awesome-esolangs*.html"))
    if not hits:
        raise SystemExit("awesome-esolangs asset page not found in assets/")
    return hits[0]


def scrape_languages(page):
    m = re.search(r"<h2[^>]*>Languages</h2>.*?<ul[^>]*>(.*?)</ul>", page, re.S)
    if not m:
        raise SystemExit("Could not find the Languages list in the asset page")
    items = []
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
        a = re.match(r"\s*<a\s+href=[\"']?([^\s\"'>]+)[^>]*>(.*?)</a>(.*)", li, re.S)
        if not a:
            continue
        url = html.unescape(a.group(1))
        name = html.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip()
        desc = html.unescape(re.sub(r"<[^>]+>", "", a.group(3)))
        desc = re.sub(r"^\s*[-–—]\s*", "", desc).strip()
        items.append((name, url, desc))
    return items


def host_info(url):
    p = urlparse(url)
    host = p.netloc.lower().removeprefix("www.")
    if host == "esolangs.org":
        return "Esolangs Wiki", unquote(p.path.removeprefix("/wiki/"))
    if host == "github.com":
        return "GitHub", p.path.strip("/")
    return "Website", host + p.path.rstrip("/")


def row(name, url, desc):
    e = html.escape
    kind, ref = host_info(url)
    return (
        "<tr>"
        f"<td><strong>{e(name)}</strong><br>(Esolang)</td>"
        f"<td>{e(desc) or '&mdash;'}</td>"
        f'<td><span class="badge">{kind}</span></td>'
        f"<td><code>{e(ref)}</code></td>"
        f'<td><a href="{e(url, quote=True)}" target="_blank" rel="noopener" class="link-btn">Open</a></td>'
        "</tr>"
    )


def build_section(items):
    rows = "\n".join(row(*i) for i in items)
    return f"""{START}
    <section id="esolangs">
        <h2>9. Esoteric Programming Languages</h2>
        <p>{len(items)} esoteric languages curated from the <a class="faq-btn" href="https://github.com/angrykoala/awesome-esolangs" target="_blank" rel="noopener">awesome-esolangs</a> list: minimalist, joke, 2D, and art-driven languages.</p>
        <div class="table-wrapper">
            <table class="compact">
                <thead><tr><th>Language</th><th>Description</th><th>Hosted On</th><th>Project / Reference</th><th>Link</th></tr></thead>
                <tbody>
{rows}
                </tbody>
            </table>
        </div>
    </section>
    {END}"""


def main():
    with open(find_asset(), encoding="utf-8", errors="replace") as fh:
        items = scrape_languages(fh.read())
    with open(INDEX, encoding="utf-8", newline="") as fh:
        doc = fh.read()
    section = build_section(items)
    if START in doc:
        doc = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: section, doc, flags=re.S)
    else:
        idx = doc.rindex("</main>")
        doc = doc[:idx] + section + "\n\n" + doc[idx:]
    if 'href="#esolangs"' not in doc:
        doc = re.sub(r'(<li><a href="#syntax">[^<]*</a></li>)', lambda m: m.group(1) + "\n            " + TOC_LINE, doc, count=1)
    with open(INDEX, "w", encoding="utf-8", newline="") as fh:
        fh.write(doc)
    print(f"Injected {len(items)} esoteric languages into index.html")


if __name__ == "__main__":
    main()
