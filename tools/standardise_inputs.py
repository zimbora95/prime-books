"""Standardise every Prime Books input spreadsheet onto the site's Contents format.

Target format (the y01-art-and-design reference):
    sheet 'Contents', headers exactly:  Section type | Title | Page
    rows: Unit "Unit N · Name" / Subunit "N.M Name" / Section "Title"
    units in NUMERIC order, each immediately followed by its own subunits in order.

Source dialects seen in the repo (2026-09-14):
  * Contents            headers 'Section type','Title','Page'          (already standard)
  * Template export     'section_ids/name' + 'section_ids/chapter_ids/name' (+ hours)
  * Sheet1 export       'Chapter' + 'Topic Name'
  * deep export         section / chapter / chapter-bullet columns      (y08/y09 PE)
  * flat                'Unit N.M: Topic' repeated across columns       (y07/y09 spanish)

Raw originals are preserved under public/inputs-raw/.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import openpyxl

REPO = Path("/root/prime-books")
INPUTS = REPO / "public" / "inputs"
RAW = REPO / "public" / "inputs-raw"

UNIT_ONLY = re.compile(r"^unit\s*(\d+)\s*(.*)$", re.I)          # "Unit 1 Moving Well" / "Unit 1: Sports"
UNIT_SUB = re.compile(r"^unit\s*(\d+)\.(\d+)\s*[.:·-]?\s*(.*)$", re.I)  # "Unit 1.1: Self, Family…"
SUB_ONLY = re.compile(r"^(\d+)\.(\d+)\s*[.:·-]?\s*(.*)$")        # "1.1 Practise…"
NUM_UNIT = re.compile(r"^(\d+)\s*[.:·]\s*(\S.*)$")               # "2. Cross Country"


def classify(name):
    """-> ('unit', n, name) | ('subunit', (n, m), title) | ('section', title) | None"""
    n = (name or "").strip()
    if not n:
        return None
    m = UNIT_SUB.match(n)
    if m:
        a, b, rest = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        return ("subunit", (a, b), f"{a}.{b} {rest}".strip())
    m = SUB_ONLY.match(n)
    if m:
        a, b, rest = int(m.group(1)), int(m.group(2)), m.group(3).strip()
        if 1 <= b <= 60 and a <= 40:
            return ("subunit", (a, b), f"{a}.{b} {rest}".strip())
    m = UNIT_ONLY.match(n)
    if m:
        a, rest = int(m.group(1)), m.group(2).lstrip(" .:·-–")
        return ("unit", a, f"Unit {a} · {rest}".strip() if rest else f"Unit {a}")
    m = NUM_UNIT.match(n)
    if m:
        return ("unit", int(m.group(1)), f"Unit {int(m.group(1))} · {m.group(2).strip()}")
    return ("section", n)


def rows_of(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    rows = [[("" if c is None else str(c).strip()) for c in r] for r in ws.iter_rows(values_only=True)]
    return ws.title, [r for r in rows if any(r)]


def convert(path):
    sheet, rows = rows_of(path)
    hdr = [h.lower() for h in rows[0]]
    body = rows[1:]
    out = []

    if "section type" in hdr:                                    # already Contents
        ti, si = hdr.index("title"), hdr.index("section type")
        pi = hdr.index("page") if "page" in hdr else None
        for r in body:
            typ = (r[si] if si < len(r) else "").strip().lower()
            title = r[ti] if ti < len(r) else ""
            page = (r[pi] if pi is not None and pi < len(r) else "")
            if typ == "unit":
                c = classify(title)
                out.append(("unit", c[1] if c and c[0] == "unit" else 9999, title, page))
            elif typ == "subunit":
                c = classify(title)
                key = c[1] if c and c[0] == "subunit" else (9999, 9999)
                out.append(("subunit", key, title, page))
            else:
                out.append(("section", None, title, page))
        return out, True

    prev_unit = None
    for r in body:
        cells = [c for c in r if c]
        if not cells:
            continue
        # first cell that is genuinely a unit/subunit (export id columns sit to its left)
        ci = next((i for i, v in enumerate(cells) if (classify(v) or ("X",))[0] in ("unit", "subunit")), 0)
        u = cells[ci]
        cu = classify(u)
        if cu is None:
            continue
        if cu[0] == "unit":
            if cu[1] != prev_unit:
                out.append(("unit", cu[1], cu[2], ""))
                prev_unit = cu[1]
            for v in cells[ci + 1:]:                             # subunit lives later in the row
                cs = classify(v)
                if cs and cs[0] == "subunit":
                    out.append(("subunit", cs[1], cs[2], ""))
                    break
        elif cu[0] == "subunit":
            n = cu[1][0]
            if n != prev_unit:
                out.append(("unit", n, f"Unit {n}", ""))
                prev_unit = n
            out.append(("subunit", cu[1], cu[2], ""))
        else:
            out.append(("section", None, cu[1], ""))
    return out, False


def rebuild(out):
    """Units in numeric order; each unit followed by its subunits then any sections."""
    units, subs, secs = {}, {}, {}
    for typ, key, title, page in out:
        if typ == "unit":
            units.setdefault(key, title)
        elif typ == "subunit":
            subs.setdefault(key[0], []).append((key, title, page))
        else:
            secs.setdefault(None, []).append((title, page))
    rows = []
    for k in sorted(units):
        rows.append(("Unit", units[k], ""))
        for key, title, page in sorted(subs.get(k, []), key=lambda t: (t[0], t[1])):
            rows.append(("Subunit", title, page))
    for title, page in secs.get(None, []):
        rows.append(("Section", title, page))
    seen, ded = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            ded.append(r)
    return ded


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    report = []
    for path in sorted(INPUTS.glob("* - input.xlsx")):
        slug = path.name.replace(" - input.xlsx", "")
        out, already = convert(path)
        rows = rebuild(out)
        if not rows:
            report.append((slug, "SKIP - nothing parsed", 0, 0, 0))
            continue
        nums = [classify(r[1])[1] for r in rows if r[0] == "Unit" and classify(r[1])]
        ordered = nums == sorted(nums)
        shutil.copy2(path, RAW / path.name)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Contents"
        ws.append(["Section type", "Title", "Page"])
        for r in rows:
            ws.append(list(r))
        wb.save(path)
        report.append((slug, ("ok" if ordered else "ORDER FIX") + ("" if already else " (converted)"),
                       sum(1 for r in rows if r[0] == "Unit"),
                       sum(1 for r in rows if r[0] == "Subunit"),
                       sum(1 for r in rows if r[0] == "Section")))
    print(f"{'slug':34} {'status':30} unit sub sec")
    for r in report:
        print(f"{r[0]:34} {r[1]:30} {r[2]:4} {r[3]:3} {r[4]:3}")
    print("\nraw originals kept in public/inputs-raw/")


if __name__ == "__main__":
    main()