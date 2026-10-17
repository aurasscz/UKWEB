"""Projde složku lekce/ a zapíše lekce.json, ze kterého čte hlavní stránka.

Lekce je buď jeden soubor   lekce/<nazev>.html
nebo složka s obrázky       lekce/<nazev>/index.html  (+ cokoli dalšího)

Název se bere z <title>, popis z <meta name="description"> nebo z prvního
odstavce, datum z <meta name="ukweb-datum" content="RRRR-MM-DD">, jinak z data,
kdy byl soubor poprvé přidán do gitu.
"""

import datetime
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEKCE = ROOT / "lekce"
OUT = ROOT / "lekce.json"


def text_of(fragment: str) -> str:
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def meta(src: str, name: str) -> str | None:
    for tag in re.findall(r"<meta\b[^>]*>", src, flags=re.I):
        if re.search(rf"""name\s*=\s*["']?{re.escape(name)}["']?[\s/>]""", tag, flags=re.I):
            m = re.search(r"""content\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", tag, flags=re.I)
            if m:
                return html.unescape(next(g for g in m.groups() if g is not None)).strip()
    return None


def shorten(s: str, limit: int = 220) -> str:
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0].rstrip(",.;:–- ")
    return cut + "…"


def git_added(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%cI", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out[-1][:10] if out else None


def describe(page: Path, href: str, slug: str) -> dict:
    src = page.read_text(encoding="utf-8", errors="replace")

    m = re.search(r"<title[^>]*>(.*?)</title>", src, flags=re.S | re.I)
    title = text_of(m.group(1)) if m else ""
    if not title:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", src, flags=re.S | re.I)
        title = text_of(m.group(1)) if m else slug.replace("-", " ").capitalize()

    desc = meta(src, "description") or ""
    if not desc:
        body = re.sub(r"<(script|style)\b.*?</\1>", " ", src, flags=re.S | re.I)
        header = re.search(r"<header\b.*?</header>", body, flags=re.S | re.I)
        scope = header.group(0) if header else body
        for p in re.findall(r"<p\b[^>]*>(.*?)</p>", scope, flags=re.S | re.I):
            if len(text_of(p)) > 25:
                desc = text_of(p)
                break

    date = meta(src, "ukweb-datum") or git_added(page) or datetime.date.fromtimestamp(page.stat().st_mtime).isoformat()

    return {"slug": slug, "href": href, "title": title, "description": shorten(desc), "date": date}


def main() -> None:
    items = []
    for entry in sorted(LEKCE.iterdir()):
        if entry.name.startswith((".", "_")):
            continue
        if entry.is_file() and entry.suffix.lower() in (".html", ".htm"):
            items.append(describe(entry, f"lekce/{entry.name}", entry.stem))
        elif entry.is_dir() and (entry / "index.html").exists():
            items.append(describe(entry / "index.html", f"lekce/{entry.name}/index.html", entry.name))

    items.sort(key=lambda x: (x["date"], x["title"]), reverse=True)
    OUT.write_text(json.dumps({"lekce": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"lekce.json: {len(items)} lekcí")
    for it in items:
        print(f"  {it['date']}  {it['title']}  ({it['href']})")


if __name__ == "__main__":
    main()
