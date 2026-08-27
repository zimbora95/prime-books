"""Standardise every book folder in public/Prime Books/.

Per-book rules (user, 2026-08-14):
  PDF/Input/    only "Student Book/" with EXACTLY ONE source file
  PDF/Output/   EXACTLY ONE built flipbook pdf; Done/ holds finished books
  BOOK COVER/   EXACTLY ONE file: the collection cover (Y<NN>-<Subject>.webp)

What this does (dry run by default):
  - PDF/Input: move "Work Book" folders and loose files to quarantine.
  - PDF/Input: report books whose Student Book/ has more than one file.
  - PDF/Output: DELETE _superseded* folders (user rule: no superseded anywhere).
  - PDF/Output: move KDP packages (FINAL-*MEGA*), teacher manuals, workbooks
                and cover wraps to KDP/.
  - PDF/Output: with several student-book candidates, keep the LONGEST page
                count and quarantine the rest.
  - BOOK COVER: keep the collection-cover webp, move FRONT/BACK/WRAP art to
                KDP/, and copy the collection-cover in where it is missing.

Usage:
    python tools/clean_tree.py            # dry run, report every action
    python tools/clean_tree.py --go       # execute
"""
import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(r"C:\Users\alexa\Documents\GitHub\prime-books")
BOOKS = REPO / "public" / "Prime Books"
COLLECTION_COVERS = REPO / "public" / "collection-covers"
QUARANTINE = Path(r"C:\Users\alexa\Documents\_Prime Books quarantine")

WORK_NAME = re.compile(r"work\s*book", re.IGNORECASE)
# Teacher editions only: "Teacher Manual", "Manual do Professor". NOT "Student
# Manual" (that is the student book under its older naming convention).
TEACHER_NAME = re.compile(r"teacher|professor", re.IGNORECASE)
KDP_DIR_NAME = re.compile(r"FINAL-.*MEGA", re.IGNORECASE)
COVER_WRAP = re.compile(r"cover\s*wrap", re.IGNORECASE)
# Canonical output name: Prime Book - {Subject} - Year {N} - Student Book.pdf
STRICT_STUDENT = re.compile(
    r"^Prime Book[s]? - .+ - Year \d+(?:-\d+)? - Student (?:Book|Manual)\.pdf$",
    re.IGNORECASE,
)


def page_count(pdf: Path) -> int:
    try:
        import fitz
        with fitz.open(pdf) as doc:
            return doc.page_count
    except Exception:
        return 0


def collection_cover_name(year_dir: str, subject: str) -> str:
    m = re.search(r"(\d+)", year_dir)
    yy = int(m.group(1)) if m else 0
    subj = re.sub(r"[^A-Za-z0-9]+", "", subject)
    return f"Y{yy:02d}-{subj}.webp"


def move_to_quarantine(src: Path, plan, why: str):
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    rel = src.relative_to(BOOKS)
    dest = QUARANTINE / stamp / rel
    plan.append(("QUARANTINE", str(src), str(dest), why))
    return dest


class Cleaner:
    def __init__(self):
        self.plan = []
        self.reports = []

    def add(self, action, src, dest, why):
        self.plan.append((action, str(src), str(dest), why))

    def report(self, msg):
        self.reports.append(msg)

    def process_book(self, year_dir: Path, sd: Path):
        rel = f"{year_dir.name}/{sd.name}"
        in_dir = sd / "PDF" / "Input"
        out_dir = sd / "PDF" / "Output"
        kdp_dir = sd / "KDP"
        cov_dir = sd / "BOOK COVER"

        # ---------- PDF/Input ----------
        if in_dir.is_dir():
            student = in_dir / "Student Book"
            for child in sorted(in_dir.iterdir()):
                if child.name.lower().startswith("_") and "supersed" in child.name.lower():
                    continue
                if child.is_dir() and WORK_NAME.search(child.name):
                    self.add("DELETE", child, "", f"{rel}: Input Work Book folder")
                    continue
                if child.is_dir() and child != student:
                    self.add("QUARANTINE", child, "", f"{rel}: Input extra folder {child.name}")
                    continue
                if child.is_file():
                    self.add("QUARANTINE", child, "", f"{rel}: Input loose file {child.name}")
            if student.is_dir():
                files = [f for f in student.iterdir() if f.is_file()]
                if len(files) > 1:
                    self.report(f"MULTI INPUT (Student Book has {len(files)} files): {rel} -> {[f.name for f in files]}")
                elif len(files) == 0:
                    self.report(f"EMPTY INPUT (no file in Student Book): {rel}")
            else:
                self.report(f"NO Student Book folder in Input: {rel}")

        # ---------- PDF/Output ----------
        if out_dir.is_dir():
            for child in sorted(out_dir.iterdir()):
                if child.is_dir():
                    if "supersed" in child.name.lower():
                        self.add("DELETE", child, "", f"{rel}: Output superseded folder")
                    elif child.name.lower() == "done":
                        pass  # the Done switch, keep
                    elif child.name.lower() == "_build":
                        # stray build folder: belongs in WORKSTATION
                        ws = sd / "WORKSTATION"
                        tgt = ws / "_build" if not (ws / "_build").exists() else ws / ("_build-output-" + datetime.now().strftime("%Y%m%d"))
                        self.add("MOVE", child, tgt, f"{rel}: Output _build -> WORKSTATION")
                    else:
                        self.add("MOVE", child, kdp_dir / child.name, f"{rel}: Output package -> KDP")
                    continue
                if child.is_file():
                    if child.suffix.lower() != ".pdf":
                        self.add("QUARANTINE", child, "", f"{rel}: Output non-pdf {child.name}")
                        continue
                    name = child.name
                    if TEACHER_NAME.search(name) or COVER_WRAP.search(name) or "workbook" in name.lower():
                        self.add("MOVE", child, kdp_dir / child.name, f"{rel}: Output {child.name} -> KDP")
                    # student-book candidates stay and are picked below

            # student-book candidates (excluding Done)
            done_dir = out_dir / "Done"
            candidates = [
                p for p in out_dir.rglob("*.pdf")
                if p.is_file()
                and done_dir not in p.parents
                and not TEACHER_NAME.search(p.stem)
                and not COVER_WRAP.search(p.stem)
                and "workbook" not in p.stem.lower()
                and "supersed" not in p.as_posix().lower()
            ]
            if len(candidates) > 1:
                # keep: strict canonical name first, then longest page count
                def rank(p):
                    return (1 if STRICT_STUDENT.match(p.name) else 0, page_count(p))
                best = max(candidates, key=rank)
                for p in candidates:
                    if p != best:
                        self.add("QUARANTINE", p, "", f"{rel}: Output duplicate candidate ({page_count(p)}pp vs {page_count(best)}pp)")
                self.report(f"MULTI OUTPUT (kept {best.name}, {page_count(best)}pp): {rel}")

        # ---------- BOOK COVER ----------
        if cov_dir.is_dir():
            files = [f for f in cov_dir.iterdir() if f.is_file()]
            keep = None
            for f in files:
                if f.suffix.lower() == ".webp" and re.match(r"^Y\d", f.stem, re.IGNORECASE):
                    keep = f
                    break
            if keep is None:
                want = collection_cover_name(year_dir.name, sd.name)
                src = COLLECTION_COVERS / want
                if src.is_file():
                    self.add("COPY", src, cov_dir / want, f"{rel}: missing collection cover -> copied in")
                    keep = cov_dir / want
                else:
                    self.report(f"NO COVER (no {want} in collection-covers): {rel}")
            for f in files:
                if keep and f == keep:
                    continue
                if f.name.upper().startswith(("FRONT", "BACK", "WRAP")) or f.suffix.lower() in (".jpg", ".jpeg", ".png"):
                    self.add("MOVE", f, kdp_dir / f.name, f"{rel}: print cover -> KDP")
                else:
                    self.add("QUARANTINE", f, "", f"{rel}: cover extra file {f.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="execute the plan")
    args = ap.parse_args()

    c = Cleaner()
    for year_dir in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
        if not re.match(r"^Year", year_dir.name, re.IGNORECASE):
            continue
        for sd in sorted(p for p in year_dir.iterdir() if p.is_dir()):
            c.process_book(year_dir, sd)

    # print plan
    n = {"DELETE": 0, "QUARANTINE": 0, "MOVE": 0, "COPY": 0}
    for action, src, dest, why in c.plan:
        n[action] = n.get(action, 0) + 1
        print(f"{action:11} {src}")
        print(f"{'':11} -> {dest if dest else '(removed)'}  [{why}]")
    print()
    for r in c.reports:
        print("REPORT:", r)
    print()
    print(f"PLAN: {len(c.plan)} actions "
          f"(delete {n['DELETE']}, quarantine {n['QUARANTINE']}, move {n['MOVE']}, copy {n['COPY']})")
    if not args.go:
        print("\nDRY RUN. Re-run with --go to execute.")
        return 0

    executed = 0
    for action, src, dest, why in c.plan:
        s, d = Path(src), Path(dest) if dest else None
        try:
            if action == "DELETE":
                if s.is_dir():
                    shutil.rmtree(s)
                elif s.is_file():
                    s.unlink()
            elif action == "QUARANTINE":
                rel = s.relative_to(BOOKS)
                stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                q = QUARANTINE / stamp / rel
                q.parent.mkdir(parents=True, exist_ok=True)
                if s.is_dir():
                    shutil.move(str(s), str(q))
                else:
                    shutil.move(str(s), str(q))
            elif action == "MOVE":
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(s), str(d))
            elif action == "COPY":
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(s), str(d))
            executed += 1
        except Exception as e:
            print(f"FAILED {action} {src}: {e}")
    print(f"\nExecuted {executed} actions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())