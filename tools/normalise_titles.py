#!/usr/bin/env python3
"""Standardise every unit/subunit title, in EVERY source, and show the changes.

Two sources, one structure (`tools/title_norm.py`):

  * the input SPREADSHEETS - public/inputs/<slug> - input.xlsx - which are the
    school's own scheme of work. `--write` edits the Title cells IN the
    spreadsheet, so the correction is permanent everywhere the workbook goes
    (downloads, the Input panel, every later rebuild), not just on one page.
    Backups are written to public/inputs/.backup-original/ the first time, and
    the whole tree is in git on top of that.
  * the BOOK-derived lists - public/book-sections.json - normalised where the
    page renders them; their source is a printed contents page, so the fix lives
    with the reading, not with a file on disk.

    .venv/bin/python tools/normalise_titles.py            # dry run, every change
    .venv/bin/python tools/normalise_titles.py --write     # spreadsheets + rebuild
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from title_norm import (normalise_title, normalise_units, lang_of,   # noqa: E402
                        squeeze)

PUB = REPO / "public"
INPUTS = PUB / "inputs"
BACKUP = INPUTS / ".backup-original"
SECTIONS = PUB / "book-sections.json"
SLUG_RE = re.compile(r"^(?P<slug>[a-z0-9-]+?)\s*-\s*input\.xlsx$", re.I)


def sheet_of(path: Path):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    head = [str(c.value or "").strip() for c in ws[1]]
    try:
        col = head.index("Title") + 1
    except ValueError:
        return None, None, None
    return wb, ws, col


def spreadsheet_changes():
    """-> [(slug, file, [(cell, before, after)])], every Title cell that moves."""
    out = []
    for path in sorted(INPUTS.glob("*.xlsx")):
        m = SLUG_RE.match(path.name)
        if not m:
            continue
        slug = m.group("slug").lower()
        wb, ws, col = sheet_of(path)
        if ws is None:
            print(f"  ! no Title column: {path.name}")
            continue
        changes = []
        for r in range(2, ws.max_row + 1):
            cell = ws.cell(row=r, column=col)
            before = str(cell.value or "").strip()
            if not before:
                continue
            after, _ = normalise_title(before, slug)
            if after and after != before:
                changes.append((r, before, after))
        if changes:
            out.append((slug, path, changes))
    return out


def book_changes():
    """-> [(slug, [(before, after)])] for the book-derived lists."""
    data = json.loads(SECTIONS.read_text(encoding="utf-8")).get("books") or {}
    out = []
    for slug, entry in sorted(data.items()):
        units = json.loads(json.dumps(entry.get("units") or []))
        before = flatten(units)
        normalise_units(units, slug, source="book")
        after = flatten(units)
        if before != after:
            out.append((slug, units, before, after))
    return out


def flatten(units):
    lines = []
    for u in units:
        lines.append(u.get("title") or "")
        for s in u.get("subs") or []:
            lines.append("   " + (s.get("title") or ""))
    return lines


def write_spreadsheets(changes) -> int:
    BACKUP.mkdir(parents=True, exist_ok=True)
    for slug, path, rows in changes:
        keep = BACKUP / path.name
        if not keep.exists():
            shutil.copy2(path, keep)
        wb, ws, col = sheet_of(path)
        for r, _before, after in rows:
            ws.cell(row=r, column=col, value=after)
        wb.save(path)
        print(f"  wrote {path.name}: {len(rows)} titles")
    return len(changes)


def main() -> int:
    write = "--write" in sys.argv
    print("== input spreadsheets")
    sp = spreadsheet_changes()
    for slug, path, rows in sp:
        print(f"  {slug} ({len(rows)})")
        for r, before, after in rows:
            print(f"     row {r:>3}  {before!r} -> {after!r}")
    print(f"  {len(sp)} spreadsheets, "
          f"{sum(len(r) for _, _, r in sp)} titles")
    if write and sp:
        write_spreadsheets(sp)

    print("== book-derived lists (normalised where the page renders them)")
    for slug, units, before, after in book_changes():
        print(f"  {slug}")
        for b, a in zip(before, after):
            if b != a:
                print(f"     - {b}\n     + {a}")
        for a in after[len(before):]:
            print(f"     + {a}")
    if write:
        print("\nthe page's JSON is rebuilt by:"
              "\n  .venv/bin/python tools/inputs_to_json.py"
              "\n  .venv/bin/python tools/make_book_sections_json.py"
              "\n  .venv/bin/python tools/make_syllabus_json.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())