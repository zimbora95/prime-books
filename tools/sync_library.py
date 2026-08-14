#!/usr/bin/env python3
"""Build the Prime Books library the site serves, straight from the canonical
tree at public/Prime Books/.

REPLACES tools/sync_books.py, public/books/, public/covers/ and public/subjects/.

THE SHAPE THIS ENFORCES (the user's house rules, 2026-08-14)
  <Subject>/PDF/Input/         exactly ONE pdf, the third-party reference book.
                               SCOPE AND SEQUENCE ONLY. Never published, never
                               copied here, never fed to marker.
  <Subject>/PDF/Output/        exactly ONE pdf, the Prime student book.
  <Subject>/PDF/Output/Done/   move that pdf in here and the book shows as DONE
                               on the site. Move it back out and it is in
                               progress again. The folder IS the switch.
  <Subject>/BOOK COVER/        exactly ONE file, the cover artwork.
  <Subject>/MARKDOWN/          the book's words, so a reader can edit and rebuild.

WHAT IT WRITES
  public/library/<slug>/book.pdf      web-optimised copy the flipbook fetches
  public/library/<slug>/cover.webp    cover art for the catalogue and 3D book
  public/library.json                 PUBLIC manifest: only what a browser needs
  public/library.local.json           gitignored: absolute MEGA paths for the
                                      authoring agent. Never deployed.

The site NEVER reads MEGA at runtime, so a stale run ships stale books. Judge a
book by PAGE COUNT, never by mtime: a newer file can be a stub or a per-unit
extract.

Usage:
    python tools/sync_library.py --dry-run
    python tools/sync_library.py                     # everything
    python tools/sync_library.py --only "Year 01/Art & Design"
    python tools/sync_library.py --manifest-only     # re-index, copy nothing
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# The canonical tree is the repo's own public/Prime Books/. Everything the site
# and the AI assistant touch lives here; the MEGA archive is no longer a working
# dependency.
BOOKS = REPO / "public" / "Prime Books"
LIBRARY = REPO / "public" / "library"
COLLECTION_COVERS = REPO / "public" / "collection-covers"
PUBLIC_MANIFEST = REPO / "public" / "library.json"
LOCAL_MANIFEST = REPO / "public" / "library.local.json"

# Year band names as they are printed on the covers.
BANDS = {
    1: "Cambridge Early Years", 2: "Cambridge Early Years", 3: "Cambridge Early Years",
    4: "Cambridge Primary", 5: "Cambridge Primary", 6: "Cambridge Primary",
    7: "Cambridge Lower Secondary", 8: "Cambridge Lower Secondary",
    9: "Cambridge Lower Secondary",
    10: "Cambridge IGCSE", 11: "Cambridge IGCSE",
    12: "Cambridge International AS & A Level", 13: "Cambridge International AS & A Level",
}
# Which cover-art family a year belongs to. Y1-Y6 are the watercolour
# animal-character books; Y7+ are the grown-up geometric still lifes. Both
# families share the identical title block, so only the ART below it changes.
def family(year: int) -> str:
    return "storybook" if 1 <= year <= 6 else "geometric"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.replace("&", " and ")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)


def year_of(year_dir: str) -> int | None:
    m = re.search(r"(\d+)", year_dir)
    return int(m.group(1)) if m else None


def pdfs_under(d: Path) -> list[Path]:
    """Every pdf below d, superseded folders excluded."""
    if not d.is_dir():
        return []
    out = []
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [x for x in dirnames if "supersed" not in x.lower()]
        for fn in filenames:
            if fn.lower().endswith(".pdf"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def page_count(pdf: Path) -> int:
    try:
        import fitz  # PyMuPDF

        with fitz.open(pdf) as doc:
            return doc.page_count
    except Exception:
        return 0


def web_optimise(src: Path, dest: Path) -> bool:
    """Shrink a print PDF for the browser. Falls back to a plain copy."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    helper = REPO / "tools" / "webopt_pdf.py"
    if helper.is_file():
        r = subprocess.run(
            [sys.executable, str(helper), str(src), str(dest)],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and dest.is_file() and dest.stat().st_size > 0:
            return True
    shutil.copy2(src, dest)
    return dest.is_file()


# Cover filenames were minted from an older subject vocabulary, so a few do not
# match the folder name letter for letter. These are the real aliases, verified
# against public/collection-covers on 2026-08-14; anything not listed here and
# not matching directly genuinely has NO cover art yet.
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
    """Find this book's cover in public/collection-covers.

    Names there are Y07-HumanitiesHistoryGeography.webp style: year padded to
    two digits, subject stripped of everything but letters. Matching is done on
    that stripped form, then through COVER_ALIASES, so "Music & Drama" resolves
    to the MusicActing artwork it has always used.
    """
    if not COLLECTION_COVERS.is_dir():
        return None
    want = re.sub(r"[^a-z0-9]", "", subject.lower())
    # "Music and Drama" and "Music & Drama" must both reach MusicDrama /
    # MusicActing, so try the form with the joining word dropped too.
    variants = [want, re.sub(r"and", "", want)]
    wants: list[str] = []
    for v in variants:
        for w in (v, COVER_ALIASES.get(v)):
            if w and w not in wants:
                wants.append(w)
    prefix = f"y{year:02d}-"
    pool = []
    for f in COLLECTION_COVERS.iterdir():
        if f.is_file() and f.name.lower().startswith(prefix):
            pool.append((re.sub(r"[^a-z0-9]", "", f.stem.split("-", 1)[1].lower()), f))
    for w in wants:
        for have, f in pool:
            if have == w:
                return f
    # Last resort: a clean prefix relationship, longest common wins. Guards
    # against "Science" grabbing "ScienceLab" when a plain Science cover exists.
    best = None
    for w in wants:
        for have, f in pool:
            if have.startswith(w) or w.startswith(have):
                score = min(len(have), len(w))
                if best is None or score > best[0]:
                    best = (score, f)
    return best[1] if best else None


def scan() -> list[dict]:
    rows = []
    for level in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
        for year_dir in sorted(p for p in level.iterdir() if p.is_dir()):
            year = year_of(year_dir.name)
            for subject_dir in sorted(p for p in year_dir.iterdir() if p.is_dir()):
                rows.append(scan_book(level.name, year_dir.name, year, subject_dir))
    return rows


def scan_book(level: str, year_dir: str, year: int | None, sd: Path) -> dict:
    out_dir = sd / "PDF" / "Output"
    done_dir = out_dir / "Done"
    in_dir = sd / "PDF" / "Input"
    cover_dir = sd / "BOOK COVER"
    md_dir = sd / "MARKDOWN"

    done_pdfs = pdfs_under(done_dir)
    out_pdfs = [p for p in pdfs_under(out_dir) if done_dir not in p.parents]
    in_pdfs = pdfs_under(in_dir)

    # The book to publish: whatever sits in Done wins, because Done is the
    # user's explicit "this one is finished" switch. Otherwise the single
    # Output pdf. With several candidates take the LONGEST, never the newest:
    # a newer file is often a stub or a single-unit extract.
    pool = done_pdfs or out_pdfs
    chosen, pages = None, 0
    for p in pool:
        n = page_count(p)
        if n > pages:
            chosen, pages = p, n
    if chosen is None and pool:
        chosen = pool[0]

    md_files = sorted(f.name for f in md_dir.iterdir() if f.is_file()) if md_dir.is_dir() else []
    cover_files = sorted(f.name for f in cover_dir.iterdir() if f.is_file()) if cover_dir.is_dir() else []

    subject = sd.name.strip()
    return {
        "level": level,
        "year_dir": year_dir,
        "year": year,
        "subject": subject,
        "slug": f"y{year:02d}-{slugify(subject)}" if year else slugify(subject),
        "band": BANDS.get(year or 0, ""),
        "family": family(year or 0),
        "book_dir": str(sd),
        "source_pdf": str(chosen) if chosen else None,
        "pages": pages,
        "done": bool(done_pdfs) and chosen is not None and done_dir in chosen.parents,
        "output_pdfs": [p.name for p in out_pdfs],
        "done_pdfs": [p.name for p in done_pdfs],
        "input_pdfs": [str(p.relative_to(in_dir)).replace("\\", "/") for p in in_pdfs],
        "cover_files": cover_files,
        "markdown_dir": str(md_dir) if md_dir.is_dir() else None,
        "markdown_count": len(md_files),
        "buildable": (sd / "WORKSTATION" / "_build" / "build.py").is_file(),
    }


def merge_rows(manifest: Path, fresh: list[dict]) -> list[dict]:
    """Merge freshly scanned rows into an existing manifest, keyed on slug.

    Used by --only. A book that has DISAPPEARED from the masters is not removed
    here, because --only never looked at it; a full run rewrites the file.
    """
    existing: list[dict] = []
    if manifest.is_file():
        try:
            loaded = json.loads(manifest.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                existing = loaded
        except (OSError, json.JSONDecodeError):
            existing = []
    by_slug = {r.get("slug"): r for r in existing if isinstance(r, dict)}
    for r in fresh:
        by_slug[r["slug"]] = r
    rows = list(by_slug.values())
    rows.sort(key=lambda r: (r.get("year") or 99, r.get("subject") or ""))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help='substring filter, e.g. "Year 01/Art & Design"')
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--manifest-only", action="store_true", help="re-index, copy nothing")
    ap.add_argument("--force", action="store_true", help="recopy even when up to date")
    args = ap.parse_args()

    if not BOOKS.is_dir():
        print(f"masters not found: {BOOKS}", file=sys.stderr)
        return 2

    rows = scan()
    if args.only:
        needle = args.only.replace("\\", "/").lower()
        rows = [r for r in rows if needle in f"{r['year_dir']}/{r['subject']}".lower()]

    publishable = [r for r in rows if r["source_pdf"] and r["pages"] > 0]
    print(f"books found      : {len(rows)}")
    print(f"with a real pdf  : {len(publishable)}")
    print(f"marked done      : {sum(1 for r in publishable if r['done'])}")

    if args.dry_run:
        for r in publishable[:20]:
            flag = "DONE" if r["done"] else "wip "
            print(f"  {flag} {r['slug']:34s} {r['pages']:4d}pp  {r['subject']}")
        print("\nDRY RUN, nothing written.")
        return 0

    public_rows, local_rows = [], []
    for r in publishable:
        slug = r["slug"]
        dest_dir = LIBRARY / slug
        pdf_dest = dest_dir / "book.pdf"
        if not args.manifest_only:
            src = Path(r["source_pdf"])
            fresh = (
                pdf_dest.is_file()
                and not args.force
                and pdf_dest.stat().st_mtime >= src.stat().st_mtime
            )
            if not fresh:
                web_optimise(src, pdf_dest)
                print(f"  pdf   {slug}  {pdf_dest.stat().st_size / 1e6:.1f} MB")

            cov = collection_cover(r["year"], r["subject"])
            if cov:
                cdest = dest_dir / ("cover" + cov.suffix.lower())
                for old in dest_dir.glob("cover.*"):
                    if old.name != cdest.name:
                        old.unlink()
                if args.force or not cdest.is_file() or cdest.stat().st_mtime < cov.stat().st_mtime:
                    shutil.copy2(cov, cdest)

        cover_rel = None
        for c in sorted(dest_dir.glob("cover.*")) if dest_dir.is_dir() else []:
            cover_rel = f"/library/{slug}/{c.name}"
            break

        pub = {
            "slug": slug,
            "year": r["year"],
            "subject": r["subject"],
            "band": r["band"],
            "family": r["family"],
            "level": r["level"],
            "pages": r["pages"],
            "done": r["done"],
            "pdf": f"/library/{slug}/book.pdf",
            "cover": cover_rel,
            "mb": round(pdf_dest.stat().st_size / 1e6, 2) if pdf_dest.is_file() else 0,
            "buildable": r["buildable"],
            "editable": r["markdown_count"] > 0,
        }
        public_rows.append(pub)
        local_rows.append(
            {
                **pub,
                "book_dir": r["book_dir"],
                "source_pdf": r["source_pdf"],
                "markdown_dir": r["markdown_dir"],
                "markdown_count": r["markdown_count"],
                "output_pdfs": r["output_pdfs"],
                "done_pdfs": r["done_pdfs"],
                "input_pdfs": r["input_pdfs"],
                "cover_files": r["cover_files"],
            }
        )

    public_rows.sort(key=lambda r: (r["year"] or 99, r["subject"]))
    local_rows.sort(key=lambda r: (r["year"] or 99, r["subject"]))

    # With --only we scanned a SUBSET, so the rows we just built must be MERGED
    # into the existing manifests, never written over them. Writing the subset
    # straight out truncated a 76-book library to one book, which looks exactly
    # like a corpus that lost 75 books.
    if args.only:
        public_rows = merge_rows(PUBLIC_MANIFEST, public_rows)
        local_rows = merge_rows(LOCAL_MANIFEST, local_rows)

    PUBLIC_MANIFEST.write_text(json.dumps(public_rows, indent=1, ensure_ascii=False), encoding="utf-8")
    LOCAL_MANIFEST.write_text(json.dumps(local_rows, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n{PUBLIC_MANIFEST.name}: {len(public_rows)} books")
    print(f"{LOCAL_MANIFEST.name}: authoring paths (gitignored)")
    if LIBRARY.is_dir():
        total = sum(f.stat().st_size for f in LIBRARY.rglob("*") if f.is_file())
        print(f"public/library: {total / 1e6:.0f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
