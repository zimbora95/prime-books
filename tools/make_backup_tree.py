#!/usr/bin/env python3
"""Stage a Year NN / Subject backup tree of the CURRENT book masters.

WHY: before a mass edit, you want a restorable copy of every book exactly as it
stands. This copies `public/library/<slug>/book.pdf` (the master) plus the book's
reference input file into:

    <dest>/Year 01/Art & Design/
        y01-art-and-design-output.pdf          the current built book
        y01-art-and-design-input.xlsx          the reference input, if there is one
        y01-art-and-design-input-corrected.xlsx the corrected input, if there is one

Two levels, exactly as the workshop asks: Year NN -> Subject Name -> files.

RULES
  * NEVER deletes anything, never overwrites a file whose bytes already match.
  * Idempotent: safe to re-run before every mass edit; unchanged files are skipped.
  * Windows-safe folder names: "/" in a subject ("German A1/A2") becomes "-".
  * Writes _MANIFEST.csv (sha256 per file -> the restore map) and _README.md.

Usage:
    .venv/bin/python tools/make_backup_tree.py                    # -> /root/pb-backup
    .venv/bin/python tools/make_backup_tree.py --dest /mnt/x/pb   # custom root
    .venv/bin/python tools/make_backup_tree.py --verify           # check, no writes
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = REPO / "public" / "library.json"
MASTERS = REPO / "public" / "library"
INPUTS = REPO / "public" / "inputs"
DEFAULT_DEST = Path("/root/pb-backup")
STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

INPUT_EXTS = (".pdf", ".xlsx", ".xls", ".csv", ".docx")


def safe_name(s: str) -> str:
    """Windows-legal folder name. '/' is a path separator on Windows, so a
    subject like 'German A1/A2' would silently create a nested folder."""
    for ch in '\\/:*?"<>|':
        s = s.replace(ch, "-")
    return " ".join(s.split()).strip(" .")


def sha256(p: Path, buf: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while chunk := f.read(buf):
            h.update(chunk)
    return h.hexdigest()


def find_input(slug: str) -> Path | None:
    if not INPUTS.is_dir():
        return None
    hits = [
        p
        for p in sorted(INPUTS.iterdir())
        if p.is_file()
        and p.name.startswith(f"{slug} - input.")
        and p.suffix.lower() in INPUT_EXTS
    ]
    return hits[0] if hits else None


LIVE_BASES = REPO / "index.html"


def live_base() -> str:
    """The public base the desktop can actually download from: the Cloudflare
    tunnel URL baked into index.html (__PB_LIVE_BASES). Not guessed — read."""
    import re

    if LIVE_BASES.is_file():
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", LIVE_BASES.read_text(encoding="utf-8"))
        if m:
            return m.group(0)
    return ""


def place(src: Path, dest: Path, rows: list[dict], verify: bool, url: str) -> str:
    """Copy src -> dest unless the bytes are already there. Never deletes."""
    rel = dest.as_posix()
    digest = sha256(src)
    if verify:
        if dest.is_file() and sha256(dest) == digest:
            rows.append({"status": "ok", "file": rel, "bytes": src.stat().st_size,
                         "sha256": digest, "source_url": url})
            return "ok"
        rows.append({"status": "MISSING" if not dest.is_file() else "DIFFERS", "file": rel,
                     "bytes": src.stat().st_size, "sha256": digest, "source_url": url})
        return "missing"
    if dest.is_file() and dest.stat().st_size == src.stat().st_size and sha256(dest) == digest:
        rows.append({"status": "unchanged", "file": rel, "bytes": src.stat().st_size,
                     "sha256": digest, "source_url": url})
        return "unchanged"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    rows.append({"status": "written", "file": rel, "bytes": dest.stat().st_size,
                 "sha256": digest, "source_url": url})
    return "written"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    ap.add_argument("--verify", action="store_true", help="report, write nothing")
    args = ap.parse_args()
    dest_root = Path(args.dest)

    books = json.loads(LIB.read_text(encoding="utf-8"))
    rows: list[dict] = []
    tally = {"written": 0, "unchanged": 0, "ok": 0}
    problems: list[str] = []
    total_bytes = 0

    for b in sorted(books, key=lambda r: (r["year"], r["subject"])):
        slug, year, subject = b["slug"], b["year"], b["subject"]
        book_dir = dest_root / f"Year {year:02d}" / safe_name(subject)
        master = MASTERS / slug / "book.pdf"
        if not master.is_file():
            problems.append(f"{slug}: no master pdf at {master}")
            continue
        st = place(master, book_dir / f"{slug}-output.pdf", rows, args.verify,
                   f"library/{slug}/book.pdf")
        tally[st if st in tally else "written"] += 1
        total_bytes += master.stat().st_size

        inp = find_input(slug)
        if inp:
            place(inp, book_dir / f"{slug}-input{inp.suffix.lower()}", rows, args.verify,
                  inp.relative_to(REPO / "public").as_posix())
            total_bytes += inp.stat().st_size

    if not args.verify:
        dest_root.mkdir(parents=True, exist_ok=True)
        fields = ["file", "bytes", "sha256", "source_url", "status"]
        with (dest_root / "_MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                w.writerow(r)

        # Machine-readable pull list for the Windows side: fetch <base>/<src> and
        # write it to <dest>. Served by the live file server at public/, so the
        # desktop can materialise this exact tree with no SSH.
        pull = [
            {
                "src": r["source_url"],
                # RELATIVE to the staging root: on Windows Join-Path with a rooted
                # second argument discards the destination and writes elsewhere.
                "dest": Path(r["file"]).relative_to(dest_root).as_posix(),
                "bytes": r["bytes"],
                "sha256": r["sha256"],
            }
            for r in rows
        ]
        (dest_root / "_DOWNLOAD.json").write_text(
            json.dumps({"generated": STAMP, "base": live_base(), "files": pull}, indent=1),
            encoding="utf-8",
        )

        n_books = len([r for r in rows if r["file"].endswith("-output.pdf")])
        n_inputs = len([r for r in rows if "-input" in Path(r["file"]).name])
        (dest_root / "_README.md").write_text(
            f"""# Prime Books backup tree

Staged {STAMP} from the masters in `/root/prime-books`.

    Year NN/<Subject>/<slug>-output.pdf            current built book (the master copy)
    Year NN/<Subject>/<slug>-input.<ext>           reference input, when one exists
    Year NN/<Subject>/<slug>-input-corrected.xlsx  corrected input, when one exists

* books: **{n_books}**  ·  extra input files: **{n_inputs}**  ·  total **{total_bytes / 2**30:.2f} GiB**
* `_MANIFEST.csv` carries the **sha256 of every file** — that is the restore map and
  the proof of what this backup contains. Verify with
  `.venv/bin/python tools/make_backup_tree.py --verify`.
* A copy of the master for book `X` is byte-identical to `public/library/X/book.pdf`.
  To restore one book: copy its `-output.pdf` back over that master path.
* Subject folders had "/" replaced with "-" (Windows cannot have "/" in a name).
* Nothing here is deleted or overwritten destructively; re-running is safe.
""",
            encoding="utf-8",
        )

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"dest        : {dest_root}")
    print(f"books       : {len([r for r in rows if r['file'].endswith('-output.pdf')])}")
    print(f"files       : {len(rows)}  {counts}")
    print(f"total bytes : {total_bytes / 2**30:.2f} GiB")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
