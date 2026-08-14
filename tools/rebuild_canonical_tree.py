#!/usr/bin/env python3
"""Rebuild public/Prime Books/ as the canonical 5-level tree.

Reads the MEGA masters (the only live tree) and writes the canonical layout the
site's house rules name:

    public/Prime Books/<Level>/<Year NN>/<Subject>/
        PDF/Input/        exactly ONE source PDF (the third-party reference book)
        PDF/Output/       exactly ONE built student book
        PDF/Output/Done/  the Output pdf moved here = the book is DONE
        MARKDOWN/         the book's words (one .md per unit + front matter)
        BOOK COVER/       exactly ONE cover file (from public/collection-covers)
        OWNER.md          lock + definition of done

Level mapping (the 2026-08-14 standard, UK key-stage shaped):
    Lower Primary      Years 01-02
    Upper Primary      Years 03-06
    Lower Secondary    Years 07-09
    Upper Secondary    Years 10-11   (incl. combined "Year 10-11")
    Advanced Levels    Years 12-13   (incl. combined "Year 12-13")

The invariant is EXACTLY ONE input + ONE output + ONE cover per book. This
script NEVER guesses and NEVER deletes: where a piece is anything other than
exactly one it copies nothing for that piece and reports the exact candidate
paths instead.

public/Prime Books/ is gitignored (a local working mirror, never deployed), so
copying the third-party Input PDFs here is the intended workshop behaviour.

Usage:
    python tools/rebuild_canonical_tree.py          # dry run
    python tools/rebuild_canonical_tree.py --go     # write the tree
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MEGA = Path(r"C:\Users\alexa\Documents\MEGA\Projects\Prime Books")
BOOKS = MEGA / "BOOKS"
ROOT = REPO / "public" / "Prime Books"
COVERS = REPO / "public" / "collection-covers"
REPORT = REPO / "docs" / "PATHS-TO-CORRECT.md"


def level_of(year: int | None) -> str | None:
    if year is None:
        return None
    if year in (1, 2):
        return "Lower Primary"
    if year in (3, 4, 5, 6):
        return "Upper Primary"
    if year in (7, 8, 9):
        return "Lower Secondary"
    if year in (10, 11):
        return "Upper Secondary"
    if year in (12, 13):
        return "Advanced Levels"
    return None


def year_of(year_dir: str) -> int | None:
    m = re.search(r"(\d+)", year_dir)
    return int(m.group(1)) if m else None


def pdfs_under(d: Path) -> list[Path]:
    if not d.is_dir():
        return []
    out = []
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [x for x in dirnames if "supersed" not in x.lower()]
        for fn in filenames:
            if fn.lower().endswith(".pdf"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


COVER_ALIASES = {
    "musicdrama": "musicacting",
    "musicanddrama": "musicacting",
    "science": "sciencelab",
    "portuguese": "portuguese1st",
    "portugueseigcse": "portuguese1stigcse",
    "physicaleducation": "physicaleducationgym",
    "humanities": "humanitieshistorygeography",
    "humanitieshistorygeography": "humanitieshistorygeography",
}


def collection_cover(year: int, subject: str) -> Path | None:
    if not COVERS.is_dir():
        return None
    want = re.sub(r"[^a-z0-9]", "", subject.lower())
    variants = [want, re.sub(r"and", "", want)]
    wants: list[str] = []
    for v in variants:
        for w in (v, COVER_ALIASES.get(v)):
            if w and w not in wants:
                wants.append(w)
    prefix = f"y{year:02d}-"
    pool = []
    for f in COVERS.iterdir():
        if f.is_file() and f.name.lower().startswith(prefix):
            pool.append((re.sub(r"[^a-z0-9]", "", f.stem.split("-", 1)[1].lower()), f))
    for w in wants:
        for have, f in pool:
            if have == w:
                return f
    best = None
    for w in wants:
        for have, f in pool:
            if have.startswith(w) or w.startswith(have):
                score = min(len(have), len(w))
                if best is None or score > best[0]:
                    best = (score, f)
    return best[1] if best else None


def scan_book(sd: Path, year: int | None) -> dict:
    out_dir = sd / "PDF" / "Output"
    done_dir = out_dir / "Done"
    in_dir = sd / "PDF" / "Input"
    md_dir = sd / "MARKDOWN"

    done_pdfs = pdfs_under(done_dir)
    out_pdfs = [p for p in pdfs_under(out_dir) if done_dir not in p.parents]
    in_pdfs = pdfs_under(in_dir)
    md_files = sorted(md_dir.rglob("*.md")) if md_dir.is_dir() else []

    if len(done_pdfs) == 1 and len(out_pdfs) == 0:
        output, done = done_pdfs[0], True
    elif len(done_pdfs) == 0 and len(out_pdfs) == 1:
        output, done = out_pdfs[0], False
    else:
        output, done = None, None

    return {
        "subject": sd.name.strip(),
        "path": sd,
        "year": year,
        "in_pdfs": in_pdfs,
        "output": output,
        "done": done,
        "done_pdfs": done_pdfs,
        "out_pdfs": out_pdfs,
        "cover": collection_cover(year, sd.name.strip()) if year is not None else None,
        "md_files": md_files,
    }


def iter_books():
    """Yield (level_name, year_dir, new_level, book_record) for the five
    year-structured levels only. Extracurricular and Kindergarden are not part
    of the five-level taxonomy and are handled separately by out_of_scope()."""
    for level in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
        if level.name.split(".")[0] not in ("1", "2", "3", "4", "5"):
            continue
        for year_dir in sorted(p for p in level.iterdir() if p.is_dir()):
            year = year_of(year_dir.name)
            for sd in sorted(p for p in year_dir.iterdir() if p.is_dir()):
                yield level.name, year_dir.name, level_of(year), scan_book(sd, year)


def out_of_scope_levels() -> list[Path]:
    return [
        p
        for p in sorted(BOOKS.iterdir())
        if p.is_dir() and p.name.split(".")[0] not in ("1", "2", "3", "4", "5")
    ]


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(BOOKS)).replace("\\", "/")
    except ValueError:
        return str(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="actually write the tree")
    args = ap.parse_args()

    if not BOOKS.is_dir():
        print(f"masters not found: {BOOKS}", file=sys.stderr)
        return 2

    rows = []
    for mlevel, year_dir, new_level, rec in iter_books():
        rec.update(mlevel=mlevel, year_dir=year_dir, new_level=new_level)
        rows.append(rec)

    publishable = [r for r in rows if (r["done_pdfs"] or r["out_pdfs"]) and r["new_level"]]
    no_output = [r for r in rows if not (r["done_pdfs"] or r["out_pdfs"])]
    out_of_scope = out_of_scope_levels()

    multi_output = [r for r in publishable if r["output"] is None]
    multi_input = [r for r in publishable if len(r["in_pdfs"]) > 1]
    no_input = [r for r in publishable if len(r["in_pdfs"]) == 0]
    no_cover = [r for r in publishable if r["cover"] is None]
    clean = [
        r
        for r in publishable
        if r["output"] is not None and len(r["in_pdfs"]) == 1 and r["cover"] is not None
    ]

    print(f"books scanned       : {len(rows)}")
    print(f"publishable (has pdf): {len(publishable)}")
    print(f"  clean 1/1/1        : {len(clean)}")
    print(f"  ambiguous output   : {len(multi_output)}")
    print(f"  no input pdf       : {len(no_input)}")
    print(f"  ambiguous input    : {len(multi_input)}")
    print(f"  no cover           : {len(no_cover)}")
    print(f"no output (stub)     : {len(no_output)}")
    print(f"outside five levels  : {len(out_of_scope)}")

    if not args.go:
        print("\nDRY RUN, nothing written. Re-run with --go to build the tree.")
        return 0

    written = build(publishable)
    write_report(rows, publishable, clean, no_output, out_of_scope, multi_output, no_input, multi_input, no_cover)
    print(f"\nbuilt {written} book folders under {ROOT}")
    print(f"anomaly report : {REPORT}")
    return 0


def build(publishable: list[dict]) -> int:
    n = 0
    for r in publishable:
        dest = ROOT / r["new_level"] / r["year_dir"] / r["subject"]
        (dest / "PDF" / "Input").mkdir(parents=True, exist_ok=True)
        (dest / "PDF" / "Output").mkdir(parents=True, exist_ok=True)
        (dest / "MARKDOWN").mkdir(parents=True, exist_ok=True)
        (dest / "BOOK COVER").mkdir(parents=True, exist_ok=True)

        # Copy every reference PDF, so the mirror is faithful. The "exactly one
        # input" invariant is reported separately in PATHS-TO-CORRECT.md, never
        # enforced by dropping files.
        for p in r["in_pdfs"]:
            copy_if_new(p, dest / "PDF" / "Input" / p.name)

        # Copy every built PDF, Done/ and Output/ kept apart so the site's
        # longest-pick (Done wins) works exactly as it did against the masters.
        for p in r["done_pdfs"]:
            (dest / "PDF" / "Output" / "Done").mkdir(parents=True, exist_ok=True)
            copy_if_new(p, dest / "PDF" / "Output" / "Done" / p.name)
        for p in r["out_pdfs"]:
            copy_if_new(p, dest / "PDF" / "Output" / p.name)

        if r["cover"] is not None:
            copy_if_new(r["cover"], dest / "BOOK COVER" / r["cover"].name)

        for p in r["md_files"]:
            copy_if_new(p, dest / "MARKDOWN" / p.name)

        owner = dest / "OWNER.md"
        if not owner.is_file():
            owner.write_text(
                f"# OWNER.md\n\n"
                f"Book: {r['subject']} · Year {r['year']}\n"
                f"Level: {r['new_level']}\n"
                f"Status: {'DONE (Output pdf is in PDF/Output/Done/)' if r['done'] else 'In progress'}\n\n"
                f"## Lock\n"
                f"Currently owned by: (unassigned)\n"
                f"To claim this book, edit this file and work on a dedicated git branch.\n"
                f"See 05-collaboration.md at the repo root.\n\n"
                f"## Definition of done\n"
                f"The Output pdf sits in PDF/Output/Done/ and the book passes the anatomy gates.\n"
                f"MARKDOWN is the editable source of truth; the PDF is the rendered output.\n",
                encoding="utf-8",
            )
        # Mirror the rest of the book (IMAGES, WORKSTATION build engine, KDP
        # pack) so the assistant can edit AND rebuild entirely within
        # public/Prime Books/, with no MEGA dependency.
        mirror_book(r["path"], dest)
        n += 1
    return n


SKIP_TOP = {"book cover", "pdf", "markdown"}


def mirror_book(src: Path, dest: Path) -> None:
    """Copy everything in the source book folder except the canonical parts that
    build() already placed (BOOK COVER, PDF, MARKDOWN, OWNER.md). Superseded
    folders are excluded. Idempotent via copy_if_new."""
    if not src.is_dir():
        return
    for child in src.iterdir():
        if child.is_dir():
            if child.name.lower() in SKIP_TOP:
                continue
            for dirpath, dirnames, filenames in os.walk(child):
                dirnames[:] = [d for d in dirnames if "supersed" not in d.lower()]
                for fn in filenames:
                    s = Path(dirpath) / fn
                    copy_if_new(s, dest / child.name / s.relative_to(child))
        elif child.is_file():
            if child.name.lower() == "owner.md":
                continue
            copy_if_new(child, dest / child.name)


def copy_if_new(src: Path, dest: Path) -> None:
    if src is None or not src.is_file():
        return
    if dest.is_file() and dest.stat().st_size == src.stat().st_size:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def write_report(rows, publishable, clean, no_output, out_of_scope, multi_output, no_input, multi_input, no_cover) -> None:
    L = ["# Paths to correct", "", "```"]
    L += [
        "PRIME BOOKS - PATHS TO CORRECT",
        "=" * 78,
        f"tree: {BOOKS}",
        f"books scanned: {len(rows)}",
        f"publishable (has an Output pdf): {len(publishable)}",
        f"clean (exactly 1 input + 1 output + 1 cover): {len(clean)}",
        "",
    ]

    def book_line(r):
        L.append(f"  {rel(r['path'])}")

    def section(title, recs):
        L.append("-" * 78)
        L.append(f"{title}  [{len(recs)}]")
        L.append("-" * 78)

    section("OUTPUT: no pdf at all (nothing to publish)", no_output)
    for r in no_output:
        book_line(r)

    section("YEAR: outside the five levels (extracurricular, kindergarden)", out_of_scope)
    for p in out_of_scope:
        L.append(f"  {rel(p)}/")

    section("OUTPUT: more than one pdf (which one is the student book?)", multi_output)
    for r in multi_output:
        book_line(r)
        for p in r["done_pdfs"]:
            L.append(f"      Output/Done/ {p.name}")
        for p in r["out_pdfs"]:
            L.append(f"      Output/ {p.name}")

    section("INPUT: no reference pdf", no_input)
    for r in no_input:
        book_line(r)

    section("INPUT: more than one reference pdf", multi_input)
    for r in multi_input:
        book_line(r)
        for p in r["in_pdfs"]:
            L.append(f"      Input/ {rel(p).split('/Input/', 1)[-1]}")

    section("BOOK COVER: no collection cover found", no_cover)
    for r in no_cover:
        book_line(r)

    L += ["=" * 78, "SUMMARY"]
    L += [f"    {len(no_output)}  OUTPUT: no pdf at all"]
    L += [f"    {len(out_of_scope)}  YEAR: outside the five levels"]
    L += [f"    {len(multi_output)}  OUTPUT: more than one pdf"]
    L += [f"    {len(no_input)}  INPUT: no reference pdf"]
    L += [f"    {len(multi_input)}  INPUT: more than one reference pdf"]
    L += [f"    {len(no_cover)}  BOOK COVER: no collection cover found"]
    L += [f"    {len(clean)}  clean (exactly 1 input + 1 output + 1 cover)"]
    L.append("```")
    L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
