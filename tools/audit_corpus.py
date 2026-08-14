#!/usr/bin/env python3
"""Audit the Prime Books corpus against the house rules.

House rules being checked (set by the user, 2026-08-14):
  * PDF/Output holds EXACTLY ONE pdf (the student book), optionally moved into
    PDF/Output/Done to flag it as finished.
  * PDF/Input holds EXACTLY ONE pdf (the third-party reference book, scope only).
  * BOOK COVER holds EXACTLY ONE file (the collection cover artwork).
  * MARKDOWN carries the book's words so a reader can edit and rebuild.
  * No FEEDBACK.docx, no *superseded* folders anywhere.

Writes a JSON + a human report next to itself so results survive a timeout.
Run FOREGROUND. Trailing-space folder names are reported with repr(), because
Win32 hides them from every normal os.listdir path (see prime-books skill).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TREES = {
    "mega": Path(r"C:\Users\alexa\Documents\MEGA\Projects\Prime Books\BOOKS"),
    "public": REPO / "public" / "Prime Books",
}


def bash_listdir(p: Path) -> list[str]:
    """List a directory through bash, which sees trailing-space names."""
    posix = "/" + str(p).replace(":", "", 1).replace("\\", "/")
    out = subprocess.run(
        ["bash", "-lc", f'ls -A -- "{posix}" 2>/dev/null'],
        capture_output=True, text=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def scan_tree(root: Path) -> dict:
    books = []
    if not root.exists():
        return {"root": str(root), "exists": False, "books": []}
    for level in sorted(p for p in root.iterdir() if p.is_dir()):
        for year in sorted(p for p in level.iterdir() if p.is_dir()):
            for subject in sorted(p for p in year.iterdir() if p.is_dir()):
                books.append(scan_book(root, level.name, year.name, subject))
    return {"root": str(root), "exists": True, "books": books}


def pdfs_in(d: Path) -> list[str]:
    if not d.is_dir():
        return []
    return sorted(f.name for f in d.iterdir() if f.is_file() and f.suffix.lower() == ".pdf")


def pdfs_under(d: Path, skip_superseded: bool = True) -> list[str]:
    """Every pdf at any depth below d, relative to d.

    Needed because the corpus does NOT keep reference books flat: 36 books put
    theirs in PDF/Input/Student Book, others in official-refs or Style-refs. A
    flat count reports 80 books as having no reference when they simply nest it.
    """
    if not d.is_dir():
        return []
    found = []
    for dirpath, dirnames, filenames in os.walk(d):
        if skip_superseded:
            dirnames[:] = [x for x in dirnames if "supersed" not in x.lower()]
        for fn in filenames:
            if fn.lower().endswith(".pdf"):
                found.append(str(Path(dirpath, fn).relative_to(d)).replace("\\", "/"))
    return sorted(found)


def scan_book(root: Path, level: str, year: str, subject_dir: Path) -> dict:
    rel = f"{level}/{year}/{subject_dir.name}"
    out_dir = subject_dir / "PDF" / "Output"
    in_dir = subject_dir / "PDF" / "Input"
    done_dir = out_dir / "Done"
    cover_dir = subject_dir / "BOOK COVER"
    md_dir = subject_dir / "MARKDOWN"

    out_pdfs = pdfs_under(out_dir)
    # Output/Done is the "finished" flag, so its pdfs are Output pdfs too and
    # must not be double counted by the recursive walk above.
    done_pdfs = pdfs_under(done_dir)
    out_pdfs = [p for p in out_pdfs if not p.replace("\\", "/").startswith("Done/")]
    in_pdfs = pdfs_under(in_dir)

    cover_files = sorted(f.name for f in cover_dir.iterdir() if f.is_file()) if cover_dir.is_dir() else []
    md_files = sorted(f.name for f in md_dir.iterdir() if f.is_file()) if md_dir.is_dir() else []

    # Anything superseded, anywhere under the book folder.
    superseded, feedback = [], []
    for dirpath, dirnames, filenames in os.walk(subject_dir):
        for dn in list(dirnames):
            if "supersed" in dn.lower():
                superseded.append(str(Path(dirpath, dn).relative_to(subject_dir)))
        for fn in filenames:
            if fn.lower().startswith("feedback"):
                feedback.append(str(Path(dirpath, fn).relative_to(subject_dir)))

    biggest = 0
    for p in out_pdfs:
        f = out_dir / p
        if f.is_file():
            biggest = max(biggest, f.stat().st_size)
    for p in done_pdfs:
        f = done_dir / p
        if f.is_file():
            biggest = max(biggest, f.stat().st_size)

    return {
        "rel": rel,
        "level": level,
        "year": year,
        "subject": subject_dir.name,
        "subject_repr": repr(subject_dir.name),
        "out_pdfs": out_pdfs,
        "done_pdfs": done_pdfs,
        "in_pdfs": in_pdfs,
        "out_count": len(out_pdfs) + len(done_pdfs),
        "in_count": len(in_pdfs),
        "done": bool(done_pdfs),
        "cover_files": cover_files,
        "markdown_files": md_files,
        "markdown_count": len(md_files),
        "has_workstation": (subject_dir / "WORKSTATION").is_dir(),
        "has_build": (subject_dir / "WORKSTATION" / "_build" / "build.py").is_file(),
        "superseded": superseded,
        "feedback": feedback,
        "biggest_pdf_bytes": biggest,
        "raw_children": bash_listdir(subject_dir),
    }


def main() -> int:
    result = {name: scan_tree(root) for name, root in TREES.items()}
    out_json = Path(__file__).with_name("audit_corpus.json")
    out_json.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = []
    for name, tree in result.items():
        books = tree["books"]
        lines.append(f"=== {name}: {tree['root']} ({len(books)} books) ===")
        if not books:
            continue
        bad_out = [b for b in books if b["out_count"] != 1]
        bad_in = [b for b in books if b["in_count"] != 1]
        bad_cov = [b for b in books if len(b["cover_files"]) != 1]
        no_md = [b for b in books if b["markdown_count"] == 0]
        sup = [b for b in books if b["superseded"]]
        fb = [b for b in books if b["feedback"]]
        done = [b for b in books if b["done"]]
        lines += [
            f"  output != 1 pdf : {len(bad_out)}",
            f"  input  != 1 pdf : {len(bad_in)}",
            f"  cover  != 1 file: {len(bad_cov)}",
            f"  no MARKDOWN     : {len(no_md)}",
            f"  superseded dirs : {len(sup)}",
            f"  FEEDBACK files  : {len(fb)}",
            f"  in Done folder  : {len(done)}",
            f"  buildable       : {sum(1 for b in books if b['has_build'])}",
        ]
    Path(__file__).with_name("audit_corpus.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nfull detail: {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
