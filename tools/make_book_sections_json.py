#!/usr/bin/env python3
"""Generate public/book-sections.json - the section list each BOOK carries.

Why this file exists: not every title has an input SPREADSHEET. Where the input
is a PDF (or missing), the syllabus page used to say "no unit table on disk" and
send the teacher off to the reader - who then showed a perfectly good section
list. That is a dead end in the middle of a page whose whole point is not having
to click.

THE READER IS THE SOURCE. This file is built from public/reader-sections.json,
which `tools/capture_reader_sections.cjs` writes by driving the real reader
(/book/<slug>#sections) once per title and reading the rows the panel shows. That
is the only way the page can honestly say "the same list you see under Sections".

A pymupdf reimplementation of the reader's parser (tools/book_sections.py) was
tried first and DISAGREED on real titles - it listed three Y2 Maths units the
reader does not show at all, missed a second Y8 English unit, and invented bare
page numbers as unit names for Y9 Humanities, where the reader shows nothing. So
the parse is only a FALLBACK for slugs the capture has not reached yet, and every
entry records which of the two produced it (`source`: "reader" | "pdf-parse").

Two rules the page depends on:
  * a list whose unit labels are not real words (a bare "7", a stray "21") is NOT
    reproduced: it is reported as an unreadable contents page instead of dressing
    junk up as a syllabus;
  * a list with no units at all is reported as such, exactly as the reader shows
    "No sections found in this book."

    .venv/bin/python tools/make_book_sections_json.py
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

from book_sections import sections  # noqa: E402  (the fallback parse)
from title_norm import normalise_units  # noqa: E402  (the house title structure)

PUB = REPO / "public"
LIB = PUB / "library"
CAPTURE = PUB / "reader-sections.json"
OUT = PUB / "book-sections.json"
INPUT_RE = re.compile(r"^(?P<slug>[a-z0-9-]+) - input\.(?P<ext>[a-z0-9]+)$")
WORDY = re.compile(r"[A-Za-z]{3}")


def kinds_from_src(src: str) -> str:
    s = (src or "").lower()
    if "contents page" in s:
        return "contents page"
    if "unit openings" in s:
        return "unit openings"
    if "scheme of work" in s:
        return "scheme of work"
    if s.startswith("error"):
        return "unreadable"
    return "none"


def group_rows(rows) -> list:
    """Reader rows -> units with their subunits, in the panel's own order."""
    units, cur = [], None
    for r in rows:
        label = (r.get("label") or "").strip()
        if not label:
            continue
        if r.get("unit"):
            cur = {"title": label, "page": r.get("page"), "subs": []}
            units.append(cur)
        elif cur is not None:
            cur["subs"].append({"title": label, "page": r.get("page")})
    return units


def from_reader(rows, src):
    kind = kinds_from_src(src)
    units = group_rows(rows)
    if not units:
        return [], kind if kind != "none" else "none"
    if any(not WORDY.search(u["title"]) for u in units):
        # bare numbers and stray fragments: not a syllabus, do not dress it up
        return [], "unreadable"
    return units, kind


def from_pdf(path: Path):
    """Fallback for a title the reader capture has not reached."""
    kind = {}
    try:
        secs = sections(path, js_style=True, kind_out=kind)
    except Exception as e:                                            # noqa: BLE001
        return [], "unreadable: " + str(e)[:60]
    units, cur = [], None
    for s in secs:
        if s["unit"]:
            cur = {"title": s["label"], "page": s["page"] + 1, "subs": []}
            units.append(cur)
        elif cur is not None:
            cur["subs"].append({"title": s["label"], "page": s["page"] + 1})
    if not units:
        return [], "none"
    if any(not WORDY.search(u["title"]) for u in units):
        return [], "unreadable"
    return units, ("unit openings" if kind.get("kind") == "openers" else "contents page")


def main() -> int:
    books = json.loads((PUB / "library.json").read_text(encoding="utf-8"))
    have_table = set()
    for p in sorted((PUB / "inputs").iterdir()):
        if p.is_file():
            m = INPUT_RE.match(p.name)
            if m and m.group("ext").lower() != "pdf":
                have_table.add(m.group("slug"))
    try:
        captured = json.loads(CAPTURE.read_text(encoding="utf-8")).get("books") or {}
    except Exception:
        captured = {}

    out = {}
    for b in books:
        slug = b["slug"]
        if slug in have_table:
            continue                      # the input table is this title's source
        cap = captured.get(slug)
        if cap is not None:
            units, kind = from_reader(cap.get("rows") or [], cap.get("src") or "")
            source = "reader"
        else:
            path = LIB / slug / "book.pdf"
            units, kind = from_pdf(path) if path.exists() else ([], "none")
            source = "pdf-parse"
        # The house structure, applied to whatever the reader/book produced: one
        # label standard, one numbering, term and contents-page rows marked as
        # the non-unit rows they are.
        units, notes = normalise_units(units, slug, "book")
        out[slug] = {"source": source, "kind": kind, "units": units,
                     "normalised": notes}
        print(f"  {slug:38} {len(units):3d} units "
              f"{sum(len(u['subs']) for u in units):4d} subs   {source:9} {kind}"
              + (f"   [{len(notes)} title fix(es)]" if notes else ""),
              flush=True)

    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "note": ("Section lists read from the reader's Sections panel "
                 "(tools/capture_reader_sections.cjs); 'pdf-parse' entries are the "
                 "pymupdf fallback for titles the capture has not reached. Pages "
                 "are the reader's own page numbers."),
        "captured": sorted(captured),
        "books": out,
    }
    tmp = str(OUT) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, OUT)

    with_units = [k for k, v in out.items() if v["units"]]
    from_reader_n = sum(1 for v in out.values() if v["source"] == "reader")
    unreadable = sum(1 for v in out.values() if v["kind"] == "unreadable")
    print(f"{OUT.name}: {len(out)} titles, {from_reader_n} from the reader, "
          f"{len(with_units)} with a list, {unreadable} unreadable contents pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
