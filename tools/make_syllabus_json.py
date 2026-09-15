#!/usr/bin/env python3
"""Generate public/syllabus.json - every title's syllabus, unit by unit.

The /syllabus page is the mega overview: the same year/subject grouping as
/status, but with the whole scheme of work expanded under each subject, so the
teacher can read all of it in one scroll instead of clicking book by book.

One row per catalogue book:

    {slug, subject, pages, input: {kind, file} | null, source, units, extras}

`source` is honest and never inferred:
  "input"  the book's input is a SPREADSHEET and every row of it is on the page
           (public/inputs/<slug>.json, written by tools/inputs_to_json.py);
  "book"   no input table exists, so the section list was read from the BOOK's
           own contents page (public/book-sections.json, written by
           tools/make_book_sections_json.py) - the same list the reader's
           Sections panel shows;
  "pdf"    an input file exists but it is a PDF document and the book itself
           yielded no section list, so there is nothing to show but the file;
  "none"   no input file and no section list.

Where a spreadsheet exists, the Input is the source of truth: it is the school's
own scheme of work, and it is NOT the book's printed contents page (a different
source, parsed page by page, and the only thing available when there is no
spreadsheet). The two are never mixed inside one title.

Run after adding or editing any input spreadsheet:

    .venv/bin/python tools/inputs_to_json.py          # xlsx -> public/inputs/<slug>.json
    .venv/bin/python tools/make_book_sections_json.py # books -> public/book-sections.json
    .venv/bin/python tools/make_syllabus_json.py      # -> public/syllabus.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from title_norm import normalise_units  # noqa: E402  (the house title structure)

PUB = REPO / "public"
INPUTS = PUB / "inputs"
OUT = PUB / "syllabus.json"
SECTIONS_IN = PUB / "book-sections.json"
INPUT_RE = re.compile(r"^(?P<slug>[a-z0-9-]+) - input\.(?P<ext>[a-z0-9]+)$")

UNIT = "unit"
SUBUNIT = "subunit"
SECTION = "section"
FRONT = "front"  # anything that carries no unit/subunit name at all


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
            found[m.group("slug")] = {"kind": m.group("ext").upper(), "file": p.name}
    return found


def page_of(value):
    """A printed folio, or None. Blank cells are the norm - most schemes carry
    no page numbers at all - and a blank must never be rendered as 0."""
    s = str(value if value is not None else "").strip()
    if not s:
        return None
    m = re.search(r"(\d{1,4})", s)
    return int(m.group(1)) if m else None


def row_kind(value: str) -> str:
    v = (value or "").strip().lower()
    if v.startswith("unit"):
        return UNIT
    if v.startswith("subunit") or v.startswith("sub unit") or v.startswith("sub-unit"):
        return SUBUNIT
    if v.startswith("section"):
        return SECTION
    return FRONT


def parse_input(slug: str):
    """-> (units, extras) for a book whose input is a spreadsheet.

    units   [{title, page, subs: [{title, page}]}]  in input row order
    extras  [{title, page}]  rows that belong to no unit (the trailing term /
            revision / assessment blocks every scheme of work ends with)
    """
    path = INPUTS / f"{slug}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return [], []
    heads = data.get("headers") or []
    rows = data.get("rows") or []
    if not rows:
        return [], []
    type_key = next((h for h in heads if re.search(r"type|kind", str(h), re.I)), None)
    title_key = next((h for h in heads if re.search(r"title|name", str(h), re.I)), None)
    page_key = next((h for h in heads if re.fullmatch(r"\s*page\s*", str(h), re.I)), None)
    if not title_key:
        return [], []

    units, extras = [], []
    for r in rows:
        title = str(r.get(title_key) or "").strip()
        if not title:
            continue
        kind = row_kind(r.get(type_key)) if type_key else FRONT
        page = page_of(r.get(page_key)) if page_key else None
        if kind == UNIT:
            units.append({"title": title, "page": page, "subs": []})
        elif kind == SUBUNIT:
            if units:
                units[-1]["subs"].append({"title": title, "page": page})
            else:
                extras.append({"title": title, "page": page})
        else:
            extras.append({"title": title, "page": page})
    if units:
        units, _ = normalise_units(units, slug, "input")
    return units, extras


def clean_unit(u: dict) -> dict:
    """One unit as the page wants it: the label, the page, its subunits, and the
    extras that mark a row as something other than a unit ('term' dividers,
    'furniture' contents-page rows) or as a row listed more than once."""
    out = {"title": u.get("title") or "", "page": u.get("page")}
    for key in ("kind", "multi"):
        if u.get(key):
            out[key] = u[key]
    out["subs"] = []
    for s in u.get("subs") or []:
        sub = {"title": s.get("title") or "", "page": s.get("page")}
        if s.get("count"):
            sub["count"] = s["count"]
        out["subs"].append(sub)
    return out


def is_unit(u: dict) -> bool:
    """A term divider or a contents-page row is not a unit."""
    return not u.get("kind")


def book_sections() -> dict:
    """slug -> {"kind", "units"} from the book's own PDF, or {} when absent.

    Generated by tools/make_book_sections_json.py. Missing file is not an error:
    it only means the page falls back to "nothing on disk" for the titles that
    have no input spreadsheet.
    """
    try:
        raw = json.loads(SECTIONS_IN.read_text(encoding="utf-8"))
    except Exception:
        return {}
    books = raw.get("books")
    return books if isinstance(books, dict) else {}


def main() -> int:
    books = json.loads((PUB / "library.json").read_text(encoding="utf-8"))
    inputs = input_map()
    from_book = book_sections()

    years: dict[int, list] = {}
    for b in books:
        slug = b["slug"]
        inp = inputs.get(slug)
        units, extras = parse_input(slug) if inp and inp["kind"] != "PDF" else ([], [])
        kind = ""
        derived_from = ""
        if units:
            source = "input"
        else:
            # No spreadsheet: the book's own section list is what the reader
            # shows, so it is what the page shows. The input's rows are not
            # available in this case, so extras stay empty.
            entry = from_book.get(slug) or {}
            derived = entry.get("units") or []
            units = [clean_unit(u) for u in derived]
            if units:
                source = "book"
                kind = entry.get("kind") or ""
                derived_from = entry.get("source") or ""
            elif entry.get("kind") == "unreadable":
                # The book has a contents page, but the reader cannot read a
                # unit list out of it. Saying so is honest; dressing a bare "7"
                # up as a unit is not.
                source = "unreadable"
            elif inp:
                source = "pdf" if inp["kind"] == "PDF" else "none"
            else:
                source = "none"
        row = {
            "slug": slug,
            "subject": b.get("subject") or slug,
            "pages": int(b.get("pages") or 0),
            "input": inp,
            "source": source,
            "kind": kind,
            "derivedFrom": derived_from,
            "units": units,
            "extras": extras,
        }
        years.setdefault(int(b.get("year") or 0), []).append(row)

    ordered = []
    for y in sorted(years):
        rows = sorted(years[y], key=lambda r: (r["subject"].lower(), r["slug"]))
        for r in rows:
            r["subunitCount"] = sum(len(u["subs"]) for u in r["units"] if is_unit(u))
            r["unitCount"] = sum(1 for u in r["units"] if is_unit(u))
            r["nonUnits"] = sum(1 for u in r["units"] if not is_unit(u))
        ordered.append({
            "year": y,
            "books": rows,
            "units": sum(r["unitCount"] for r in rows),
            "subunits": sum(r["subunitCount"] for r in rows),
            "nonUnits": sum(r["nonUnits"] for r in rows),
            "withInput": sum(1 for r in rows if r["input"]),
            "withTable": sum(1 for r in rows if r["source"] == "input"),
            "withBook": sum(1 for r in rows if r["source"] == "book"),
        })

    all_rows = [r for y in ordered for r in y["books"]]
    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "totals": {
            "books": len(all_rows),
            "years": len(ordered),
            "units": sum(r["unitCount"] for r in all_rows),
            "subunits": sum(r["subunitCount"] for r in all_rows),
            "nonUnits": sum(r["nonUnits"] for r in all_rows),
            "sections": sum(len(r["extras"]) for r in all_rows),
            "withInput": sum(1 for r in all_rows if r["input"]),
            "withTable": sum(1 for r in all_rows if r["source"] == "input"),
            "withBook": sum(1 for r in all_rows if r["source"] == "book"),
            "pdfOnly": sum(1 for r in all_rows if r["source"] == "pdf"),
            "noInput": sum(1 for r in all_rows if not r["input"]),
            "unreadable": sum(1 for r in all_rows if r["source"] == "unreadable"),
            "nothing": sum(1 for r in all_rows if r["source"] in ("pdf", "none", "unreadable")),
        },
        "years": ordered,
    }

    tmp = str(OUT) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, OUT)

    t = payload["totals"]
    print(f"{OUT.name}: {t['books']} titles, {t['units']} units, "
          f"{t['subunits']} subunits, {t['sections']} standalone sections; "
          f"{t['withTable']} from an input table, {t['withBook']} from the book, "
          f"{t['nothing']} with neither ({t['pdfOnly']} of those have a PDF input)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
