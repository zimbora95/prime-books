#!/usr/bin/env python3
"""Organise the house: archive real reviews, then remove clutter from the corpus.

The user's instruction (2026-08-14) was to remove every FEEDBACK.docx and every
"superseded" folder from the book tree, so a contributor opening a book folder
sees only the book.

TWO THINGS THIS SCRIPT REFUSES TO DO BLINDLY
  1. Eleven of the 89 FEEDBACK files carry a REAL teacher review, and a teacher
     review is a build gate, not clutter. Those are extracted to markdown under
     ARTIFACTS/reviews/ BEFORE the docx is removed, so the gate survives.
  2. Nothing is unlinked. Everything removed is MOVED to a quarantine folder
     outside both trees, with a manifest, so a mistake is recoverable. Empty it
     yourself once you are happy.

Usage:
    python tools/house_clean.py            # dry run, prints what would happen
    python tools/house_clean.py --go       # do it
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

MEGA = Path(r"C:\Users\alexa\Documents\MEGA\Projects\Prime Books")
BOOKS = MEGA / "BOOKS"
REVIEWS = MEGA / "ARTIFACTS" / "reviews"
QUARANTINE = Path(r"C:\Users\alexa\Documents\MEGA\Projects\_Prime Books quarantine")
REAL_REVIEW_CHARS = 200  # below this a FEEDBACK.docx is an empty template


def docx_text(p: Path) -> str:
    """Plain text of a .docx, paragraph per line. Empty string if unreadable."""
    try:
        with zipfile.ZipFile(p) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
    except Exception:
        return ""
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def slug(rel: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="actually move files")
    args = ap.parse_args()

    if not BOOKS.is_dir():
        print(f"BOOKS not found: {BOOKS}", file=sys.stderr)
        return 2

    feedback: list[Path] = []
    superseded: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(BOOKS):
        d = Path(dirpath)
        for dn in list(dirnames):
            if "supersed" in dn.lower():
                superseded.append(d / dn)
                dirnames.remove(dn)  # do not descend: the whole folder goes
        for fn in filenames:
            if fn.lower().startswith("feedback") and fn.lower().endswith((".docx", ".doc")):
                feedback.append(d / fn)

    reviews_kept: list[dict] = []
    for p in feedback:
        text = docx_text(p)
        if len(text) >= REAL_REVIEW_CHARS:
            rel = p.parent.relative_to(BOOKS).as_posix()
            reviews_kept.append({"src": str(p), "book": rel, "chars": len(text), "text": text})

    total_bytes = 0
    for p in superseded:
        for dp, _, fns in os.walk(p):
            for fn in fns:
                try:
                    total_bytes += (Path(dp) / fn).stat().st_size
                except OSError:
                    pass

    print(f"FEEDBACK files found      : {len(feedback)}")
    print(f"  carrying a real review  : {len(reviews_kept)}  -> archived to {REVIEWS}")
    print(f"  empty templates         : {len(feedback) - len(reviews_kept)}")
    print(f"superseded folders found  : {len(superseded)}  ({total_bytes / 1e9:.2f} GB)")
    print(f"quarantine                : {QUARANTINE}")
    if not args.go:
        print("\nDRY RUN. Re-run with --go to move them.")
        for r in reviews_kept:
            print(f"  review kept: {r['chars']:5d} chars  {r['book']}")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    qdir = QUARANTINE / stamp
    (qdir / "feedback").mkdir(parents=True, exist_ok=True)
    (qdir / "superseded").mkdir(parents=True, exist_ok=True)
    REVIEWS.mkdir(parents=True, exist_ok=True)

    # 1. Archive the real reviews as markdown, so the gate survives the cleanup.
    for r in reviews_kept:
        out = REVIEWS / (slug(r["book"]) + ".md")
        out.write_text(
            f"# Teacher review: {r['book']}\n\n"
            f"Extracted from `{Path(r['src']).name}` on {stamp} during the corpus\n"
            "cleanup that removed FEEDBACK.docx from the book folders. A review is a\n"
            "BUILD GATE: it is scoped to this book's audience and year, and the page\n"
            "references below belong to the edition that was reviewed.\n\n"
            "---\n\n" + r["text"] + "\n",
            encoding="utf-8",
        )
        r["archived_to"] = str(out)

    # 2. Move every FEEDBACK file into quarantine, keeping the book path readable.
    moved_fb = []
    for p in feedback:
        rel = p.relative_to(BOOKS)
        dest = qdir / "feedback" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
        moved_fb.append(str(rel))

    # 3. Move every superseded folder into quarantine.
    moved_sup = []
    for p in superseded:
        if not p.exists():
            continue
        rel = p.relative_to(BOOKS)
        dest = qdir / "superseded" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
        moved_sup.append(str(rel))

    (qdir / "MANIFEST.json").write_text(
        json.dumps(
            {
                "when": stamp,
                "why": "corpus cleanup: FEEDBACK.docx and superseded folders removed from BOOKS",
                "reviews_archived": [
                    {k: v for k, v in r.items() if k != "text"} for r in reviews_kept
                ],
                "feedback_moved": moved_fb,
                "superseded_moved": moved_sup,
            },
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"\nmoved {len(moved_fb)} FEEDBACK files and {len(moved_sup)} superseded folders")
    print(f"archived {len(reviews_kept)} real reviews to {REVIEWS}")
    print(f"quarantine manifest: {qdir / 'MANIFEST.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
