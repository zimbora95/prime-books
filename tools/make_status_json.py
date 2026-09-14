#!/usr/bin/env python3
"""Generate public/status.json - the point-of-situation data behind /status.

One row per catalogue book, grouped by year:

    {slug, subject, pages, input: {kind, file} | null, standardized: bool}

Sources, in order of authority:
  public/library.json        the catalogue (year, subject, slug, pages)
  public/inputs/             the ONE canonical input location
                             (<slug> - input.<ext>, since 2026-09-14)
  public/standardized.json   the manual sign-off map {slug: true|{...}}.
                             Absent/empty means nothing is standardised yet -
                             the page reports that honestly rather than
                             guessing from the presence of an input file.

Run after adding a book, an input, or flipping a standardised flag:

    .venv/bin/python tools/make_status_json.py
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUB = REPO / "public"
INPUTS = PUB / "inputs"
OUT = PUB / "status.json"
FLAGS = PUB / "standardized.json"
INPUT_RE = re.compile(r"^(?P<slug>[a-z0-9-]+) - input\.(?P<ext>[a-z0-9]+)$")


def input_map() -> dict:
    """slug -> {"kind": "XLSX", "file": "<name>"} for every book with a source."""
    found = {}
    if not INPUTS.is_dir():
        return found
    for p in sorted(INPUTS.iterdir()):
        if not p.is_file():
            continue
        m = INPUT_RE.match(p.name)
        if m:
            found[m.group("slug")] = {
                "kind": m.group("ext").upper(),
                "file": p.name,
            }
    return found


def flag_map() -> dict:
    """slug -> True for books signed off as standardised."""
    try:
        raw = json.loads(FLAGS.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(raw, dict):
        return {}
    out = {}
    for slug, val in raw.items():
        if isinstance(slug, str) and (val is True or isinstance(val, dict)):
            out[slug] = val if isinstance(val, dict) else True
    return out


def main() -> int:
    books = json.loads((PUB / "library.json").read_text(encoding="utf-8"))
    inputs = input_map()
    flags = flag_map()

    years: dict[int, list] = {}
    for b in books:
        slug = b["slug"]
        row = {
            "slug": slug,
            "subject": b.get("subject") or slug,
            "pages": int(b.get("pages") or 0),
            "input": inputs.get(slug),
            "standardized": bool(flags.get(slug)),
        }
        years.setdefault(int(b.get("year") or 0), []).append(row)

    ordered = []
    for y in sorted(years):
        rows = sorted(years[y], key=lambda r: (r["subject"].lower(), r["slug"]))
        ordered.append({
            "year": y,
            "books": rows,
            "withInput": sum(1 for r in rows if r["input"]),
            "standardized": sum(1 for r in rows if r["standardized"]),
            "pages": sum(r["pages"] for r in rows),
        })

    all_rows = [r for y in ordered for r in y["books"]]
    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "totals": {
            "books": len(all_rows),
            "pages": sum(r["pages"] for r in all_rows),
            "withInput": sum(1 for r in all_rows if r["input"]),
            "noInput": sum(1 for r in all_rows if not r["input"]),
            "standardized": sum(1 for r in all_rows if r["standardized"]),
            "years": len(ordered),
        },
        "years": ordered,
    }

    tmp = str(OUT) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, OUT)

    t = payload["totals"]
    print(f"{OUT.name}: {t['books']} books, {t['pages']} pages, "
          f"{t['withInput']} with input, {t['noInput']} without, "
          f"{t['standardized']} standardised, {t['years']} years")
    return 0


if __name__ == "__main__":
    sys.exit(main())
