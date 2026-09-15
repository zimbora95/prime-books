"""Quality gate for every input spreadsheet: ordering, contiguity, empties.

    .venv/bin/python /tmp/qa_inputs.py            # all inputs
    .venv/bin/python /tmp/qa_inputs.py --units    # list every unit label per book
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import openpyxl

INPUTS = Path("/root/prime-books/public/inputs")
UNUM = re.compile(r"^(unit|unidade|unidad|module|modulo|theme|topic|part|stop|section|chapter|term|termo)\s*(\d+)\b", re.I)
SUBN = re.compile(r"^(\d+)\.(\d+)\b")


def audit(path: Path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = [[("" if c is None else str(c).strip()) for c in r] for r in ws.iter_rows(values_only=True)]
    rows = [r for r in rows if any(r)]
    if not rows:
        return None
    hdr, body = rows[0], rows[1:]
    problems = []
    if hdr[:3] != ["Section type", "Title", "Page"]:
        problems.append(f"headers are {hdr[:4]}")
    units, subs, seen = [], {}, set()
    cur = None
    for r in body:
        typ, title = (r + ["", ""])[0], (r + ["", ""])[1]
        if typ not in ("Unit", "Subunit", "Section"):
            problems.append(f"unknown type {typ!r} ({title[:24]})")
        if not title:
            problems.append(f"empty title under {typ}")
        if typ == "Unit":
            m = UNUM.match(title)
            units.append(int(m.group(2)) if m else None)
            cur = units[-1]
            subs.setdefault(cur, [])
        elif typ == "Subunit":
            if cur is None:
                problems.append(f"subunit before any unit: {title[:30]}")
            m = SUBN.match(title)
            if m:
                subs.setdefault(cur, []).append(int(m.group(2)))
        if (typ, title) in seen:
            problems.append(f"duplicate row {typ} {title[:30]}")
        seen.add((typ, title))

    nums = [u for u in units if u is not None]
    if len(nums) != len(units):
        problems.append(f"{len(units) - len(nums)} unit heading(s) with no number")
    if nums and nums != sorted(nums):
        problems.append(f"units out of order: {nums}")
    if nums and nums != list(range(min(nums), max(nums) + 1)):
        problems.append(f"unit numbers not contiguous: {nums}")
    suborder = {u: v for u, v in subs.items() if v and v != sorted(v)}
    if suborder:
        problems.append(f"subunits out of order in unit(s) {list(suborder)[:4]}")
    return {"units": units, "nsub": sum(len(v) for v in subs.values()),
            "nsections": sum(1 for r in body if r and r[0] == "Section"),
            "problems": problems}


def main():
    show = "--units" in sys.argv
    bad = 0
    for path in sorted(INPUTS.glob("* - input.xlsx")):
        slug = path.name.replace(" - input.xlsx", "")
        try:
            a = audit(path)
        except Exception as e:                                        # noqa: BLE001
            print(f"{slug:34} ERROR {e}")
            bad += 1
            continue
        if a is None:
            print(f"{slug:34} EMPTY")
            bad += 1
            continue
        verdict = "ok" if not a["problems"] else "CHECK"
        if a["problems"]:
            bad += 1
        print(f"{slug:34} {verdict:5} units={len(a['units']):3} subs={a['nsub']:3} secs={a['nsections']:3}"
              + ("   " + "; ".join(a["problems"][:3]) if a["problems"] else ""))
        if show:
            for u in a["units"]:
                print(f"        Unit {u}")
    print(f"\n{len(list(INPUTS.glob('* - input.xlsx')))} inputs, {bad} needing a look")


if __name__ == "__main__":
    main()