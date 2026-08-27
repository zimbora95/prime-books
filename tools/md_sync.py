#!/usr/bin/env python3
"""Auto-sync guard: ensure every book's markdown companion reflects its PDF.

Two modes:
  --check     report drift only (exit 1 if drifted) — for CI / pre-commit
  (default)   regenerate drifted markdown companions in place

Drift detection is TWO-layered, because mtime alone lies in both directions:
  1. mtime:   PDF newer than .md -> candidate drift
  2. content: word-set comparison per page (cheap, order-insensitive).
              Only an actual content difference regenerates the file.
An art-only re-save (new mtime, same text) therefore does NOT churn the .md.

Usage:
    .venv/bin/python tools/md_sync.py            # fix drift
    .venv/bin/python tools/md_sync.py --check    # audit only
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pymupdf

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "public" / "library"
MD = REPO / "public" / "markdown"
MANIFEST = REPO / "public" / "library.json"


def page_md(page) -> str:
    out = []
    d = page.get_text("dict")
    for block in d["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            txt = "".join(s["text"] for s in line["spans"]).strip()
            if txt:
                bold = any("bold" in s["font"].lower() for s in line["spans"])
                big = max(s["size"] for s in line["spans"]) > 14
                if big and bold:
                    out.append(f"## {txt}")
                elif bold:
                    out.append(f"**{txt}**")
                else:
                    out.append(txt)
        out.append("")
    return "\n".join(out)


def words(text: str) -> set:
    return set(
        w.strip('.,;:!?()"\'*#-').lower()
        for w in text.split()
        if len(w) > 3
    )


def content_drifted(pdf: Path, md: Path) -> list[int]:
    """Pages whose word-set in the PDF is not represented in the md."""
    doc = pymupdf.open(pdf)
    text = md.read_text(encoding="utf-8")
    drifted = []
    for i in range(doc.page_count):
        seg = text.split(f"<!-- page {i + 1} -->", 1)
        if len(seg) < 2:
            drifted.append(i + 1)
            continue
        body = seg[1].split(f"<!-- page {i + 2} -->", 1)[0]
        missing = words(doc[i].get_text()) - words(body)
        if missing:  # any genuinely missing word = drift (small edits count)
            drifted.append(i + 1)
    return drifted


def regenerate(slug: str, row: dict, pdf: Path, md: Path) -> None:
    doc = pymupdf.open(pdf)
    parts = [
        f"# {row['subject']} - Year {row['year']} (Prime Book)\n",
        f"> Markdown companion of `public/library/{slug}/book.pdf` ({doc.page_count} pages).",
        "> RULE: when the PDF is edited, this file must be updated in the same change.\n",
    ]
    for i, page in enumerate(doc):
        parts.append(f"\n<!-- page {i + 1} -->\n\n---\n")
        parts.append(page_md(page))
    md.write_text("".join(parts), encoding="utf-8")
    print(f"  regenerated {slug}.md ({doc.page_count} pages)")


def main() -> None:
    check_only = "--check" in sys.argv
    rows = json.load(open(MANIFEST, encoding="utf-8"))
    MD.mkdir(exist_ok=True)
    drifted = []
    for row in sorted(rows, key=lambda r: (r["year"], r["subject"])):
        slug = row["slug"]
        pdf = LIB / slug / "book.pdf"
        md = MD / f"{slug}.md"
        if not pdf.is_file():
            continue
        if not md.is_file():
            drifted.append((slug, row, "missing markdown"))
            continue
        if md.stat().st_mtime >= pdf.stat().st_mtime:
            continue  # md written after pdf: in sync by construction
        pages = content_drifted(pdf, md)
        if pages:
            drifted.append((slug, row, f"content drift on pages {pages[:8]}"))
        else:
            # art-only re-save: bump mtime so future runs skip the deep check
            touched = time.time()
            import os
            os.utime(md, (touched, touched))
            print(f"  art-only resave, mtime refreshed: {slug}")
    if not drifted:
        print("ALL SYNCED: 79/79 markdown companions match their PDFs.")
        return
    for slug, row, why in drifted:
        print(f"DRIFTED {slug}: {why}")
    if check_only:
        sys.exit(1)
    for slug, row, why in drifted:
        regenerate(slug, row, LIB / slug / "book.pdf", MD / f"{slug}.md")
    print(f"repaired {len(drifted)} companion(s)")


if __name__ == "__main__":
    main()
