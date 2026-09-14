#!/usr/bin/env python3
"""Convert the per-book INPUT spreadsheets (schemes of work / contents) into
JSON the site's Input panel can render, and mirror them (plus the raw .xlsx)
into dist/ for the Vercel build.

Reads:   public/input-corrections/<slug> - contents.xlsx
Writes:  public/inputs/<slug>.json       (headers + rows, browser-friendly)
         dist/inputs/<slug>.json         (mirror)
         dist/input-corrections/*.xlsx   (mirror of the raw sources)

Run after adding or editing any input-corrections spreadsheet:
    .venv/bin/python tools/inputs_to_json.py
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
# ONE canonical input location. The 2026-09-14 standard: every book with a source
# keeps it at public/inputs/<slug> - input.<ext>; the legacy input-corrections
# folder is retired (its files were byte-identical duplicates of the raw inputs,
# and the five books that had only a "corrected" copy were moved in here).
SRC = REPO / "public" / "inputs"
OUT_PUBLIC = REPO / "public" / "inputs"
OUT_DIST = REPO / "dist" / "inputs"

# "y01-art-and-design - input.xlsx" -> "y01-art-and-design"
SLUG_RE = re.compile(r"^(?P<slug>[a-z0-9-]+?)\s*-\s*input\.(xlsx|pdf)$", re.IGNORECASE)


def convert(path: Path) -> dict | None:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = [[("" if c is None else str(c).strip()) for c in row]
            for row in ws.iter_rows(values_only=True)]
    rows = [r for r in rows if any(r)]
    if not rows:
        return None
    headers = rows[0]
    data = [dict(zip(headers, r + [""] * (len(headers) - len(r)))) for r in rows[1:]]
    return {
        "file": path.name,
        "sheet": ws.title,
        "headers": headers,
        "rows": data,
    }


def main() -> None:
    OUT_PUBLIC.mkdir(parents=True, exist_ok=True)
    OUT_DIST.mkdir(parents=True, exist_ok=True)
    n = 0
    for path in sorted(SRC.glob("*")):
        m = SLUG_RE.match(path.name)
        if not m:
            print(f"skip (name not <slug> - input.xlsx): {path.name}")
            continue
        if path.suffix.lower() != ".xlsx":
            print(f"skip (not a spreadsheet, panel renders xlsx only): {path.name}")
            continue
        slug = m.group("slug").lower()
        payload = convert(path)
        if not payload:
            print(f"skip (empty): {path.name}")
            continue
        out = OUT_PUBLIC / f"{slug}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        shutil.copy2(out, OUT_DIST / out.name)
        # keep the spreadsheet beside its rendered JSON so the deployed build
        # carries both; dist/ is a build artefact (gitignored), not a source tree.
        shutil.copy2(path, OUT_DIST / path.name)
        print(f"ok {slug}: {len(payload['rows'])} rows")
        n += 1
    print(f"{n} inputs converted")


if __name__ == "__main__":
    main()
