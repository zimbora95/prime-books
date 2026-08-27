# ---------------------------------------------------------------------------
# SUPERSEDED 2026-08-14. The site no longer reads public/books/ nor
# books-manifest.json. The replacement is tools/sync_library.py, which builds
# public/library/<slug>/{book.pdf,cover.webp} + library.json / library.local.json
# straight from the MEGA masters, and folds the Done-folder status switch in.
# This file is kept only so the history of the web-optimisation contract is not
# lost; DO NOT RUN IT - it writes to folders the app has stopped reading.
# ---------------------------------------------------------------------------
#!/usr/bin/env python
"""Sync the real Student Books from the MEGA project into public/books/.

SOURCE OF TRUTH (DEC-040, 2026-08-06):

    C:/Users/alexa/Documents/MEGA/Projects/Prime Books/BOOKS
        <level>/Year NN/<Subject>/PDF/Output/*.pdf

The H: shared drive and 'Documents/The Prime Books' are RETIRED. H: may STILL
BE MOUNTED with a stale full copy, which is worse than a missing one because it
reads plausibly. This script therefore refuses to run against any drive letter
and takes its root from PRIME_BOOKS_ROOT or the constant below.

Note the layout differs from the old H: tree: MEGA interposes a <level> folder
('1. Lower Primary', ...) between BOOKS and 'Year NN'.

Each book is web-optimised via tools/webopt_pdf.py and written to

    public/books/Year NN/<Subject>/<Subject> - Year N - Student Book.pdf

plus a manifest at public/books-manifest.json that index.html loads to decide
which Preview buttons can open a flipbook.

Serving folder/file names use "and" instead of "&": Vite's dev server
SPA-falls-back on public paths containing "&", and pdf.js then chokes on the
returned HTML with InvalidPDFException.

    python tools/sync_books.py                 # incremental (skips up-to-date)
    python tools/sync_books.py --force          # re-optimise everything
    python tools/sync_books.py --dry-run        # just report the plan
    python tools/sync_books.py --only "Year 03" # substring filter on the plan
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

# The canonical masters root. Override with PRIME_BOOKS_ROOT for a machine that
# keeps MEGA somewhere else; never point this at a drive letter (see below).
DEFAULT_ROOT = Path(r"C:\Users\alexa\Documents\MEGA\Projects\Prime Books")
PROJECT_ROOT = Path(os.environ.get("PRIME_BOOKS_ROOT", DEFAULT_ROOT))
BOOKS_ROOT = PROJECT_ROOT / "BOOKS"

PUBLIC = REPO / "public"
BOOKS_DIR = PUBLIC / "books"
MANIFEST = PUBLIC / "books-manifest.json"
# Same rows plus the absolute MEGA paths, for the local authoring assistant only.
MANIFEST_LOCAL = PUBLIC / "books-manifest.local.json"
CATALOGUE = PUBLIC / "collection-books.json"

# Subject folders whose on-disk name does not normalise onto the catalogue name.
# The MEGA tree names folders by DISCIPLINE ('Humanities', 'Physical Education',
# 'Portuguese'), while the catalogue names the PRODUCT ('Humanities (History &
# Geography)', 'Physical Education & Gym', 'Portuguese 1st'). Without these the
# 628pp Year 12 PE book and every Humanities title silently stop publishing.
# key: (year, normalised on-disk folder name) -> catalogue subject
DISK_ALIASES = {
    "humanities": "Humanities (History & Geography)",
    "physical education": "Physical Education & Gym",
    "music drama": "Music & Drama",
}
DISK_OVERRIDES = {
    (1, "science"): "Science & Lab",
    (2, "science"): "Science & Lab",
    (4, "science"): "Science & Lab",
    # Lower/Upper Primary call the first-language course simply 'Portuguese';
    # Years 9-11 sit the IGCSE, where the catalogue adds the suffix.
    (1, "portuguese"): "Portuguese 1st",
    (2, "portuguese"): "Portuguese 1st",
    (3, "portuguese"): "Portuguese 1st",
    (4, "portuguese"): "Portuguese 1st",
    (5, "portuguese"): "Portuguese 1st",
    (6, "portuguese"): "Portuguese 1st",
    (7, "portuguese"): "Portuguese 1st",
    (8, "portuguese"): "Portuguese 1st",
    (9, "portuguese"): "Portuguese 1st (IGCSE)",
    (9, "portuguese 1st"): "Portuguese 1st (IGCSE)",
    (10, "portuguese 1st"): "Portuguese 1st (IGCSE)",
    (11, "portuguese 1st"): "Portuguese 1st (IGCSE)",
    # Years 1-2 brand the performing-arts book 'Music & Acting'.
    (1, "music drama"): "Music & Acting",
    (2, "music drama"): "Music & Acting",
}

# Anything that is NOT the pupil's book. A Teacher Manual or a Workbook sitting
# beside the Student Book must never win the pick: both used to match the old
# 'prime book' test and the newest-mtime tie-break then chose arbitrarily.
NOT_A_STUDENT_BOOK = (
    "cover template",
    "teacher manual",
    "teacher's manual",
    "workbook",
    "answer key",
    "scheme of work",
    # Per-unit extracts and worksheet packs are NOT the book. Year 1 Portuguese
    # was rebuilt on 2026-08-12 leaving only 'Unit 1 - Fichas.pdf' (8pp) in
    # Output, which the old test happily published as the Student Book.
    "fichas",
    "ficha ",
    "worksheet",
    "flashcard",
    "style prompt",
    "content style",
)

# A file whose name marks it as ONE unit or part is an extract, not the book.
EXTRACT_RE = re.compile(
    r"-\s*(unit|part|chapter|sem[aá]na|week)\s*\d+", re.IGNORECASE
)


def guard_root() -> None:
    """Fail loudly rather than silently reading a retired tree."""
    p = str(BOOKS_ROOT).replace("\\", "/")
    low = p.lower()
    if "shared drives" in low or "/the prime books" in low:
        sys.exit(
            "REFUSING TO RUN: %s looks like a retired tree.\n"
            "The masters live in MEGA/Projects/Prime Books (DEC-040)." % BOOKS_ROOT
        )
    drive = BOOKS_ROOT.drive.upper().rstrip(":")
    if drive and drive not in ("C",):
        sys.exit(
            "REFUSING TO RUN: %s is on drive %s:. The retired Google shared\n"
            "drive is still mountable and accepts reads; derive the root from\n"
            "the MEGA path instead." % (BOOKS_ROOT, drive)
        )
    if not BOOKS_ROOT.is_dir():
        sys.exit("masters root not found: %s" % BOOKS_ROOT)


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
    if any(bad in n for bad in NOT_A_STUDENT_BOOK):
        return False
    if EXTRACT_RE.search(n):
        return False
    return "student book" in n or "student manual" in n or "prime book" in n


def page_count(p: Path) -> int:
    """Page count without a full parse; used to pick between candidates."""
    try:
        import fitz

        d = fitz.open(p)
        n = d.page_count
        d.close()
        return n
    except Exception:
        try:
            data = p.read_bytes()
            return len(re.findall(rb"/Type\s*/Page[^s]", data))
        except Exception:
            return 0


def pick(cands: list[Path]) -> tuple[Path, list[str]]:
    """Choose the real Student Book from several candidates.

    PAGE COUNT WINS, NOT MTIME. A rebuild can leave a NEWER 14-page stub beside
    the real 66-page book (this is exactly why the site served a 14pp Year 3
    Mathematics while the master had 66pp, and the reading assistant correctly
    reported 'no text on page 1' - the stub's cover is a flat image).
    Ties break on the shorter, plainer filename, which is the canonical one
    ('... - Student Book.pdf' over '... - Student Book - horiz-fullart.pdf').
    """
    notes: list[str] = []
    scored = sorted(
        ((page_count(c), -len(c.name), c) for c in cands),
        key=lambda t: (-t[0], -t[1]),
    )
    best = scored[0][2]
    if len(cands) > 1:
        notes.append(
            "picked %s (%dpp) over %s"
            % (
                best.name,
                scored[0][0],
                ", ".join("%s (%dpp)" % (c.name, n) for n, _, c in scored[1:]),
            )
        )
    return best, notes


def discover() -> tuple[list[dict], list[str]]:
    """Find every Student Book in the MEGA tree, paired with its catalogue subject."""
    cat = load_catalogue()
    found: list[dict] = []
    problems: list[str] = []

    for level in sorted(BOOKS_ROOT.iterdir()):
        if not level.is_dir():
            continue
        for ydir in sorted(level.iterdir()):
            m = re.match(r"Year (\d+)$", ydir.name)
            if not m or not ydir.is_dir():
                continue
            year = int(m.group(1))

            for sdir in sorted(ydir.iterdir()):
                if not sdir.is_dir():
                    continue

                # Direct children of PDF/Output only. Output holds
                # _superseded_<date>/ subfolders with 21 old books in them, and
                # a recursive glob would resurrect those.
                out = sdir / "PDF" / "Output"
                pdfs = (
                    [p for p in out.iterdir() if p.is_file() and is_student_book(p)]
                    if out.is_dir()
                    else []
                )
                # Two Physical Education books sit loose in the subject folder.
                if not pdfs:
                    pdfs = [
                        p for p in sdir.iterdir() if p.is_file() and is_student_book(p)
                    ]
                if not pdfs:
                    continue

                src, notes = pick(pdfs)
                for n in notes:
                    problems.append("Year %02d / %s: %s" % (year, sdir.name, n))

                subject = (
                    DISK_OVERRIDES.get((year, norm(sdir.name)))
                    or cat.get((year, norm(sdir.name)))
                    or DISK_ALIASES.get(norm(sdir.name))
                )
                # An alias must still be a real product in that year group.
                if subject and (year, norm(subject)) not in cat:
                    subject = None
                if not subject:
                    problems.append(
                        "Year %02d / %s: no catalogue entry (book %s NOT published)"
                        % (year, sdir.name, src.name)
                    )
                    continue

                found.append(
                    {
                        "year": year,
                        "subject": subject,
                        "src": src,
                        "rel": "Year %02d/%s/%s - Year %d - Student Book.pdf"
                        % (year, safe(subject), safe(subject), year),
                    }
                )

    return found, problems


def manifest_row(b: dict, dst: Path, pages: int) -> dict:
    """One place builds a manifest row, so the skip and sync paths cannot drift.

    Carries absolute MEGA paths so the reading assistant can open the manuscript
    it is being asked about. Local-workstation paths only; they are inert unless
    a loopback Hermes with file tools acts on them.
    """
    book_dir = b["src"].parent.parent.parent
    return {
        "year": b["year"],
        "subject": b["subject"],
        "pages": pages,
        "mb": round(dst.stat().st_size / 1048576, 2),
        "pdf": "/books/" + "/".join(quote(part) for part in b["rel"].split("/")),
        "src": str(b["src"]),
        "book_dir": str(book_dir),
        "markdown": str(book_dir / "MARKDOWN"),
        "buildable": (book_dir / "WORKSTATION" / "_build" / "build.py").exists(),
    }


def main() -> int:
    guard_root()
    force = "--force" in sys.argv
    dry = "--dry-run" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]

    print("masters root: %s" % BOOKS_ROOT)
    books, problems = discover()
    if only:
        books = [b for b in books if only.lower() in b["rel"].lower()]
        print("--only %r -> %d book(s)" % (only, len(books)))
    print("found %d Student Books" % len(books))
    for p in problems:
        print("  !! " + p)

    if dry:
        for b in books:
            dst = BOOKS_DIR / b["rel"]
            have = page_count(dst) if dst.exists() else 0
            src_pp = page_count(b["src"])
            flag = ""
            if have and src_pp and src_pp != have:
                flag = "   <-- SERVED %dpp, MASTER %dpp" % (have, src_pp)
            print(
                "  Year %-2d %-38s %s%s"
                % (b["year"], b["subject"], b["src"].name, flag)
            )
        return 0

    manifest: list[dict] = []
    t_all = time.time()
    allow_shrink = "--allow-shrink" in sys.argv
    skipped_shrink: list[str] = []

    for i, b in enumerate(books, 1):
        dst = BOOKS_DIR / b["rel"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        src_mtime = b["src"].stat().st_mtime

        # Page count, not mtime, decides whether a served copy is stale: a
        # stub can carry a newer mtime than the real book.
        stale_pages = False
        served = page_count(dst) if dst.exists() else 0
        master = page_count(b["src"])
        if served and master and served != master:
            stale_pages = True

        # NEVER silently downgrade a live book. Some served copies came from the
        # retired H: tree and have MORE pages than the current MEGA master
        # (Year 1 Portuguese 84 -> 31, Year 1 Science 214 -> 183). That may be a
        # deliberate re-edition or a regression in the master, and only a human
        # can say which, so report it and leave the shipped file alone.
        if (
            not allow_shrink
            and served
            and master
            and master < served * 0.9
            and served - master > 5
        ):
            skipped_shrink.append(
                "Year %02d %s: master has %dpp, SERVED has %dpp - left alone"
                % (b["year"], b["subject"], master, served)
            )
            manifest.append(manifest_row(b, dst, served))
            print(
                "[%2d/%2d] SKIP (would shrink %dpp -> %dpp)  %s"
                % (i, len(books), served, master, b["rel"])
            )
            continue

        if not force and dst.exists() and dst.stat().st_mtime >= src_mtime and not stale_pages:
            pages = page_count(dst)
            print("[%2d/%2d] skip (up to date)  %s" % (i, len(books), b["rel"]))
        else:
            t0 = time.time()
            why = " [page count differs]" if stale_pages else ""
            print(
                "[%2d/%2d] optimising %s ...%s" % (i, len(books), b["rel"], why),
                flush=True,
            )
            st = optimise(str(b["src"]), str(dst))
            pages = st["pages"]
            os.utime(dst, (src_mtime, src_mtime))
            print(
                "         %.1f MB -> %.1f MB  (%d pages, %d imgs recoded, %.0fs)"
                % (st["src_mb"], st["dst_mb"], st["pages"], st["recoded"], time.time() - t0)
            )

        manifest.append(manifest_row(b, dst, pages))

    manifest.sort(key=lambda r: (r["year"], r["subject"]))
    # A partial run must not truncate the manifest: merge onto what is there.
    if only and MANIFEST.exists():
        old = {
            (r["year"], r["subject"]): r
            for r in json.loads(MANIFEST.read_text(encoding="utf-8"))
        }
        for r in manifest:
            old[(r["year"], r["subject"])] = r
        manifest = sorted(old.values(), key=lambda r: (r["year"], r["subject"]))
    # Two manifests. The PUBLIC one ships to the web and carries only what a
    # browser needs: leaking "C:\Users\alexa\..." to every visitor is needless,
    # and a remote Hermes cannot use those paths anyway. The LOCAL one keeps the
    # MEGA paths so the authoring assistant can open the manuscript; it is
    # gitignored and never deployed.
    public_fields = ("year", "subject", "pages", "mb", "pdf")
    MANIFEST.write_text(
        json.dumps(
            [{k: r[k] for k in public_fields if k in r} for r in manifest],
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    MANIFEST_LOCAL.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    total = sum(r["mb"] for r in manifest)
    if skipped_shrink:
        print("\n!! LEFT ALONE because the master is SHORTER than the shipped book:")
        for s in skipped_shrink:
            print("   " + s)
        print("   Re-run with --allow-shrink once you have confirmed the masters.")
    print(
        "\nwrote %s  (%d books, %.0f MB total, %.0fs)"
        % (MANIFEST.relative_to(REPO), len(manifest), total, time.time() - t_all)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
