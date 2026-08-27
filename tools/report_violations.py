#!/usr/bin/env python3
"""Turn audit_corpus.json into the human list of paths the user must correct.

The house rule being reported: every book folder should hold EXACTLY ONE pdf in
PDF/Input (the third-party reference kept for scope only) and EXACTLY ONE pdf in
PDF/Output (the student book, optionally inside PDF/Output/Done once finished).
Anything else is ambiguous and the site cannot pick a book for the reader.

Reads the MEGA half of the audit only: that is the tree of truth.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "audit_corpus.json").read_text(encoding="utf-8"))
BOOKS = DATA["mega"]["books"]
ROOT = DATA["mega"]["root"]

out: list[str] = []
w = out.append

w("PRIME BOOKS - PATHS TO CORRECT")
w("=" * 78)
w(f"tree: {ROOT}")
w(f"books: {len(BOOKS)}")
w("")

buckets = {
    "OUTPUT: no pdf at all (nothing to publish)": [b for b in BOOKS if b["out_count"] == 0],
    "OUTPUT: more than one pdf (which one is the student book?)": [b for b in BOOKS if b["out_count"] > 1],
    "INPUT: no reference pdf": [b for b in BOOKS if b["in_count"] == 0],
    "INPUT: more than one reference pdf": [b for b in BOOKS if b["in_count"] > 1],
    "BOOK COVER: not exactly one file": [b for b in BOOKS if len(b["cover_files"]) != 1],
    "MARKDOWN: empty or missing (reader cannot edit this book)": [b for b in BOOKS if b["markdown_count"] == 0],
}

for title, rows in buckets.items():
    w("")
    w("-" * 78)
    w(f"{title}  [{len(rows)}]")
    w("-" * 78)
    for b in rows:
        w(f"  {b['rel']}")
        if "OUTPUT" in title:
            for p in b["out_pdfs"]:
                w(f"      Output/ {p}")
            for p in b["done_pdfs"]:
                w(f"      Output/Done/ {p}")
        if "INPUT" in title:
            for p in b["in_pdfs"]:
                w(f"      Input/ {p}")
        if "COVER" in title:
            for p in b["cover_files"]:
                w(f"      BOOK COVER/ {p}")

w("")
w("=" * 78)
w("SUMMARY")
for title, rows in buckets.items():
    w(f"  {len(rows):4d}  {title}")
w("")
w(f"  {sum(1 for b in BOOKS if b['feedback']):4d}  books carrying a FEEDBACK file (to delete)")
w(f"  {sum(1 for b in BOOKS if b['superseded']):4d}  books carrying a superseded folder (to delete)")
w(f"  {sum(1 for b in BOOKS if b['has_build']):4d}  books with a build engine (rebuildable)")

text = "\n".join(out)
(HERE.parent / "docs" / "PATHS-TO-CORRECT.md").write_text(
    "# Paths to correct\n\n```\n" + text + "\n```\n", encoding="utf-8"
)
print(text)
