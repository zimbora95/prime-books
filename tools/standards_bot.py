#!/usr/bin/env python3
"""The standards bot: measure every book against the locked standard, publish the result.

What it does, in order:

  1. runs tools/standards_check.py over every book in public/library.json, in
     parallel, and writes public/standards-report.json (the machine record:
     per book, pass or fail, every failure, every warning, the measured facts)
  2. merges the teacher's manual sign-off from public/standardized.json, so a
     book can read "machine clean, awaiting sign-off" and never silently
     becomes "standardised"
  3. regenerates public/status.json (via tools/make_status_json.py) and adds the
     machine verdict to every row, so /status shows both columns
  4. optional --push: commits the two JSON files and pushes, which redeploys the
     status page

It NEVER touches standardized.json. Certification stays a human act: the machine
cannot see whether teacher content was preserved, whether an image is licensed,
whether a colour passes contrast in the printed book, or whether a QR code scans
off paper. A green machine result means "ready for sign-off", nothing more.

Usage
    .venv/bin/python tools/standards_bot.py                 # measure + write
    .venv/bin/python tools/standards_bot.py --push          # ... and publish
    .venv/bin/python tools/standards_bot.py --jobs 6
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUB = REPO / "public"
LOCK = PUB / "standards" / "years-1-4.json"
REPORT = PUB / "standards-report.json"
STATUS = PUB / "status.json"
FLAGS = PUB / "standardized.json"


def lock_id() -> str:
    try:
        return json.loads(LOCK.read_text(encoding="utf-8")).get("id", "A-2.2-Y1-4")
    except Exception:                                            # noqa: BLE001
        return "A-2.2-Y1-4"


def scope_years() -> set:
    """The years the locked standard actually governs. A-2.2 covers Years 1 to 4."""
    try:
        raw = json.loads(LOCK.read_text(encoding="utf-8"))
        ys = raw.get("scope_years") or raw.get("scope", {}).get("years")
        if isinstance(ys, list) and ys:
            return {int(y) for y in ys}
    except Exception:                                            # noqa: BLE001
        pass
    return {1, 2, 3, 4}


def year_of(slug: str) -> int:
    m = re.match(r"y(\d{1,2})", slug or "")
    return int(m.group(1)) if m else 0


def signoffs() -> dict:
    try:
        raw = json.loads(FLAGS.read_text(encoding="utf-8"))
        return {k: True for k, v in raw.items() if v is True or isinstance(v, dict)}
    except Exception:                                            # noqa: BLE001
        return {}


def check_one(item):
    slug, path = item
    sys.path.insert(0, str(REPO / "tools"))
    import standards_check as sc                                 # noqa: PLC0415
    if not path.exists():
        return {"slug": slug, "ok": False, "failures": ["no book.pdf"], "warnings": [], "facts": {}}
    try:
        return sc.check(str(path), slug, sc.lock())
    except Exception as e:                                       # noqa: BLE001
        return {"slug": slug, "ok": False, "failures": ["check error: %s" % e],
                "warnings": [], "facts": {}}


def state_of(rec, signed):
    if rec["ok"] and signed:
        return "signed-off"
    if rec["ok"]:
        return "machine-clean"
    if signed:
        return "signed-off with machine failures"
    return "not-standardised"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=min(6, (os.cpu_count() or 4)))
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="measure only the first N books")
    ap.add_argument("--all-years", action="store_true",
                    help="also measure books outside the standard's scope (noisy: they are not governed by it)")
    a = ap.parse_args()

    manifest = json.loads((PUB / "library.json").read_text(encoding="utf-8"))
    inscope = scope_years()
    jobs, skipped = [], []
    for r in manifest:
        item = (r["slug"], PUB / "library" / r["slug"] / "book.pdf")
        if a.all_years or year_of(r["slug"]) in inscope:
            jobs.append(item)
        else:
            skipped.append(r["slug"])
    if a.limit:
        jobs = jobs[:a.limit]
    signed = signoffs()
    started = datetime.now(timezone.utc)

    print("measuring %d book(s) against %s with %d workers (%d outside scope, not governed)"
          % (len(jobs), lock_id(), a.jobs, len(skipped)))
    results = []
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        for rec in ex.map(check_one, jobs):
            results.append(rec)
            print("  %-34s %5s %3d fail  %s"
                  % (rec["slug"], rec.get("pages", "-"), len(rec["failures"]),
                     "clean" if rec["ok"] else rec["failures"][0][:60]))

    for r in results:
        r["state"] = state_of(r, bool(signed.get(r["slug"])))
    results += [{"slug": s, "ok": None, "scope": False, "state": "out of scope",
                 "failures": [], "warnings": [], "facts": {"reason": "not a Years 1-4 title"}}
                for s in skipped]
    clean = [r for r in results if r["ok"]]
    report = {
        "generated": started.strftime("%Y-%m-%d %H:%M UTC"),
        "spec": lock_id(),
        "certified_by": "the teacher, click by click on /status",
        "machine_cannot_check": [
            "teacher content preserved on its page",
            "image rights and credits",
            "illustration quality",
            "colour contrast in the printed book",
            "QR codes scanned off paper",
            "the physical print proof",
        ],
        "scope": "Years 1 to 4 only; other years are measured only with --all-years",
        "totals": {
            "books": len(jobs),
            "out_of_scope": len(skipped),
            "machine_clean": len(clean),
            "signed_off": sum(1 for r in results if r["state"] == "signed-off"),
            "awaiting_sign_off": sum(1 for r in results if r["state"] == "machine-clean"),
            "failing": len(jobs) - len(clean),
        },
        "books": results,
    }
    REPORT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("\nmachine clean %d/%d in scope, signed off %d, failing %d, %d out of scope"
          % (report["totals"]["machine_clean"], len(jobs),
             report["totals"]["signed_off"], report["totals"]["failing"], len(skipped)))
    print("written:", REPORT.relative_to(REPO))

    # refresh status.json, then merge the machine verdict into every row
    subprocess.run([sys.executable, str(REPO / "tools" / "make_status_json.py")],
                   cwd=REPO, check=False, capture_output=True)
    try:
        status = json.loads(STATUS.read_text(encoding="utf-8"))
    except Exception as e:                                        # noqa: BLE001
        print("could not read status.json:", e)
        status = None
    if status:
        by = {r["slug"]: r for r in results}
        status["checked_at"] = report["generated"]
        status["spec"] = report["spec"]
        status["totals"]["machineClean"] = report["totals"]["machine_clean"]
        for y in status.get("years", []):
            for row in y.get("books", []):
                rec = by.get(row["slug"])
                if rec and rec.get("scope", True):
                    row["checked"] = {"ok": rec["ok"],
                                      "failures": len(rec["failures"]),
                                      "warnings": len(rec["warnings"]),
                                      "state": rec["state"]}
        STATUS.write_text(json.dumps(status, indent=1), encoding="utf-8")
        print("status.json updated with the machine verdict for %d rows" % len(by))

    if a.push:
        rel = [str(REPORT.relative_to(REPO)), str(STATUS.relative_to(REPO))]
        subprocess.run(["git", "add", *rel], cwd=REPO, check=False)
        msg = ("standards bot: %d/%d machine clean, %d signed off (%s)"
               % (report["totals"]["machine_clean"], len(jobs),
                  report["totals"]["signed_off"], report["spec"]))
        c = subprocess.run(["git", "commit", "-q", "-m", msg], cwd=REPO, capture_output=True, text=True)
        if c.returncode != 0:
            print("nothing to commit")
        p = subprocess.run(["git", "push", "-q", "origin", "HEAD:main"], cwd=REPO,
                           capture_output=True, text=True)
        print("push:", "ok" if p.returncode == 0 else p.stderr[-300:])
    return 0


if __name__ == "__main__":
    sys.exit(main())