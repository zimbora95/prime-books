#!/usr/bin/env python
"""Sync the real Student Books from H: into public/books/ for the flipbook.

Reads every  H:/Shared drives/Prime Books/Year NN/<Subject>/PDF/Output/
folder, picks the one Student Book PDF in it (COVER TEMPLATE files are not
books), web-optimises it via tools/webopt_pdf.py and writes it to

    public/books/Year NN/<Subject>/<Subject> - Year N - Student Book.pdf

plus a manifest at public/books-manifest.json that index.html loads to
decide which Preview buttons can open a flipbook.

Serving folder/file names use "and" instead of "&": Vite's dev server
SPA-falls-back on public paths containing "&", and pdf.js then chokes on
the returned HTML with InvalidPDFException.

    python tools/sync_books.py            # incremental (skips up-to-date)
    python tools/sync_books.py --force    # re-optimise everything
    python tools/sync_books.py --dry-run  # just report the plan
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from webopt_pdf import optimise  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
H_ROOT = Path("H:/Shared drives/Prime Books")
PUBLIC = REPO / "public"
BOOKS_DIR = PUBLIC / "books"
MANIFEST = PUBLIC / "books-manifest.json"
CATALOGUE = PUBLIC / "collection-books.json"

# A few subject folders on H: are named differently from the catalogue.
# key: (year, normalised on-disk folder name) -> catalogue subject
DISK_OVERRIDES = {
    (1, "science"): "Science & Lab",
}


def norm(name: str) -> str:
    """Collapse the '&' / 'and' / ' - ' connector noise between two words."""
    s = name.lower().strip()
    s = s.replace("&", " ")
    s = re.sub(r"\band\b", " ", s)
    s = s.replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def safe(name: str) -> str:
    """Serving-safe form of a subject name: no '&', collapsed whitespace."""
    s = name.replace("&", "and")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def load_catalogue() -> dict[tuple[int, str], str]:
    """(year, normalised subject) -> exact catalogue subject string."""
    rows = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    return {(int(r["year"]), norm(r["subject"])): r["subject"] for r in rows}


def is_student_book(p: Path) -> bool:
    n = p.name.lower()
    if not n.endswith(".pdf"):
        return False
    if "cover template" in n:
        return False
    return "student book" in n or "prime book" in n


def discover() -> tuple[list[dict], list[str]]:
    """Find every Student Book on H: and pair it with a catalogue subject."""
    cat = load_catalogue()
    found: list[dict] = []
    problems: list[str] = []

    for ydir in sorted(H_ROOT.glob("Year *")):
        if not ydir.is_dir():
            continue
        m = re.match(r"Year (\d+)$", ydir.name)
        if not m:
            continue
        year = int(m.group(1))

        for sdir in sorted(ydir.iterdir()):
            if not sdir.is_dir():
                continue

            # Normal layout: <Subject>/PDF/Output/*.pdf
            out = sdir / "PDF" / "Output"
            pdfs = [p for p in out.glob("*.pdf") if is_student_book(p)] if out.is_dir() else []
            # Two Gym books sit loose in the subject folder instead.
            if not pdfs:
                pdfs = [p for p in sdir.glob("*.pdf") if is_student_book(p)]
            if not pdfs:
                continue
            if len(pdfs) > 1:
                problems.append(
                    "Year %02d / %s: %d candidate books, using newest: %s"
                    % (year, sdir.name, len(pdfs), ", ".join(p.name for p in pdfs))
                )
                pdfs.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            key = DISK_OVERRIDES.get((year, norm(sdir.name)))
            subject = key or cat.get((year, norm(sdir.name)))
            if not subject:
                problems.append(
                    "Year %02d / %s: no catalogue entry (book %s NOT published)"
                    % (year, sdir.name, pdfs[0].name)
                )
                continue

            found.append(
                {
                    "year": year,
                    "subject": subject,
                    "src": pdfs[0],
                    "rel": "Year %02d/%s/%s - Year %d - Student Book.pdf"
                    % (year, safe(subject), safe(subject), year),
                }
            )

    return found, problems


def main() -> int:
    force = "--force" in sys.argv
    dry = "--dry-run" in sys.argv

    books, problems = discover()
    print("found %d Student Books on H:" % len(books))
    for p in problems:
        print("  !! " + p)

    if dry:
        for b in books:
            print("  Year %-2d %-38s <- %s" % (b["year"], b["subject"], b["src"].name))
        return 0

    manifest: list[dict] = []
    t_all = time.time()

    for i, b in enumerate(books, 1):
        dst = BOOKS_DIR / b["rel"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        src_mtime = b["src"].stat().st_mtime

        if not force and dst.exists() and dst.stat().st_mtime >= src_mtime:
            import fitz

            d = fitz.open(dst)
            pages = d.page_count
            d.close()
            print("[%2d/%2d] skip (up to date)  %s" % (i, len(books), b["rel"]))
        else:
            t0 = time.time()
            print("[%2d/%2d] optimising %s ..." % (i, len(books), b["rel"]), flush=True)
            st = optimise(str(b["src"]), str(dst))
            pages = st["pages"]
            os.utime(dst, (src_mtime, src_mtime))
            print(
                "         %.1f MB -> %.1f MB  (%d pages, %d imgs recoded, %.0fs)"
                % (st["src_mb"], st["dst_mb"], st["pages"], st["recoded"], time.time() - t0)
            )

        manifest.append(
            {
                "year": b["year"],
                "subject": b["subject"],
                "pages": pages,
                "mb": round(dst.stat().st_size / 1048576, 2),
                "pdf": "/books/"
                + "/".join(quote(part) for part in b["rel"].split("/")),
            }
        )

    manifest.sort(key=lambda r: (r["year"], r["subject"]))
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    total = sum(r["mb"] for r in manifest)
    print(
        "\nwrote %s  (%d books, %.0f MB total, %.0fs)"
        % (MANIFEST.relative_to(REPO), len(manifest), total, time.time() - t_all)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
