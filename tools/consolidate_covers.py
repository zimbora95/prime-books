#!/usr/bin/env python3
"""Reduce every book's BOOK COVER to EXACTLY ONE file.

USER'S RULE: the cover folder must hold exactly one file, and that file is the
collection cover (Y01-ArtDesign.webp pattern). KDP print covers (FRONT_/BACK_)
go to KDP/ beside the existing print pack. Nothing is deleted; everything is
moved to KDP/ or quarantined.

DRY RUN FIRST.

Usage:
    python tools/consolidate_covers.py             # dry run
    python tools/consolidate_covers.py --go        # move them
"""
import argparse, json, os, shutil, sys
from datetime import datetime
from pathlib import Path

MEGA = Path(r"C:\Users\alexa\Documents\MEGA\Projects\Prime Books")
BOOKS = MEGA / "BOOKS"
QUARANTINE = Path(r"C:\Users\alexa\Documents\MEGA\Projects\_Prime Books quarantine")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true")
    args = ap.parse_args()

    plan = []
    for level in sorted(p for p in BOOKS.iterdir() if p.is_dir()):
        for yd in sorted(p for p in level.iterdir() if p.is_dir()):
            for sd in sorted(p for p in yd.iterdir() if p.is_dir()):
                cd = sd / "BOOK COVER"
                if not cd.is_dir():
                    continue
                files = sorted(f for f in cd.iterdir() if f.is_file())
                if not files:
                    continue
                rel = sd.relative_to(BOOKS).as_posix()
                if len(files) == 1:
                    plan.append(dict(rel=rel, action="clean", keep=files[0].name,
                                     move=[], scrap=[]))
                    continue
                webps = [f for f in files if f.suffix.lower() == ".webp"]
                col = [f for f in webps if f.stem.upper().startswith(("Y0","Y1"))]
                keep = col[0] if col else (webps[0] if webps else files[0])
                move, scrap = [], []
                for f in files:
                    if f.name == keep.name:
                        continue
                    n = f.name.lower()
                    if "front" in n or "back" in n or n.startswith("primebooks"):
                        move.append(f.name)
                    else:
                        scrap.append(f.name)
                plan.append(dict(rel=rel, action="consolidate", keep=keep.name,
                                 move=move, scrap=scrap))

    clean = sum(1 for p in plan if p["action"] == "clean")
    multi = sum(1 for p in plan if p["action"] != "clean")
    print(f"BOOK COVER folders: {len(plan)}  ({clean} clean, {multi} >1 file)")

    moved_n, scrap_n = 0, 0
    for p in plan:
        if p["action"] == "clean":
            continue
        moved_n += len(p["move"])
        scrap_n += len(p["scrap"])
        print(f"\n  {p['rel']}")
        print(f"    keep: {p['keep']}")
        for f in p["move"]:
            print(f"    -> KDP/ {f}")
        for f in p["scrap"]:
            print(f"    X scrap: {f}")
    print(f"\nfiles moved to KDP/: {moved_n}")
    print(f"files scrapped     : {scrap_n}")

    if not args.go:
        print("\nDRY RUN. Re-run with --go to move them.")
        return 0

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    qdir = QUARANTINE / stamp / "covers"
    qdir.mkdir(parents=True, exist_ok=True)
    total = 0
    for p in plan:
        if p["action"] == "clean":
            continue
        sd = BOOKS / p["rel"].replace("/", os.sep)
        cd, kd = sd / "BOOK COVER", sd / "KDP"
        kd.mkdir(exist_ok=True)
        for fn in p["move"]:
            shutil.move(str(cd / fn), str(kd / fn))
            total += 1
        for fn in p["scrap"]:
            dest = qdir / p["rel"].replace("/", "_").replace(" ", "_") / fn
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(cd / fn), str(dest))
            total += 1
    print(f"\nmoved {total} files. quarantine: {qdir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())