#!/usr/bin/env python3
"""Prime Books INPUT point-of-situation report.

Classifies every catalogue book by its INPUT state:
  A  input + built       - raw source file present (xlsx/csv/pdf)
  B  panel-only          - `<slug>.json` + corrections xlsx exist but the RAW input file is absent
  C  built, no source    - real book (>=20pp) with no input file at all
  D  stub, no source     - placeholder book (<=6pp) with no input file at all
Also lists un-rendered spreadsheets (xlsx present, .json missing).
"""
import json, os
from pathlib import Path

ROOT = Path("/root/prime-books")
PUB = ROOT / "public"
lib = json.load(open(PUB / "library.json"))
EXTS = (".xlsx", ".xls", ".csv", ".pdf", ".docx", ".doc")

def raw(slug):
    d = PUB / "inputs"
    hits = []
    for f in sorted(d.iterdir()):
        if f.name.startswith(slug) and f.suffix.lower() in EXTS:
            hits.append(f.name)
    return hits

rows = []
for r in lib:
    slug = r["slug"]
    hits = raw(slug)
    exts = sorted({Path(h).suffix.lower().lstrip(".") for h in hits})
    corr = any(h.lower().endswith((".xlsx", ".xls", ".csv")) for h in hits)
    js = (PUB / "inputs" / f"{slug}.json").exists()
    rows.append(dict(slug=slug, year=r.get("year"), subject=r.get("subject"),
                     pages=r.get("pages") or 0, done=bool(r.get("done")),
                     files=hits, exts="+".join(exts), corr=corr, js=js))

def group(r):
    if r["files"]:
        return "A"
    if r["js"] or r["corr"]:
        return "B"
    return "C" if r["pages"] >= 20 else "D"

for r in rows:
    r["grp"] = group(r)

A = [r for r in rows if r["grp"] == "A"]
B = [r for r in rows if r["grp"] == "B"]
C = [r for r in rows if r["grp"] == "C"]
D = [r for r in rows if r["grp"] == "D"]
norender = [r for r in A if r["exts"] in ("xlsx", "csv") and not r["js"]]

def line(r):
    return (f"  Y{r['year']:<2} {r['slug']:<34} {r['pages']:>4}pp  "
            f"{r['subject']}")

out = []
p = out.append
p("=" * 78)
p("PRIME BOOKS - INPUT POINT OF SITUATION")
p(f"catalogue rows: {len(rows)}   with a raw input file: {len(A)}   "
  f"MISSING AN INPUT FILE: {len(B)+len(C)+len(D)}")
p("=" * 78)

p(f"\n### A. HAS AN INPUT FILE ({len(A)})  -- source scheme-of-work / Student Book present")
for r in sorted(A, key=lambda x: (x["year"], x["slug"])):
    p(line(r) + f"   [{r['exts']}]")

p(f"\n### B. INPUT PANEL DATA ONLY - corrections xlsx / json exist but the RAW INPUT FILE IS MISSING ({len(B)})")
for r in sorted(B, key=lambda x: (x["year"], x["slug"])):
    p(line(r) + f"   corr={r['corr']} json={r['js']}")

p(f"\n### C. BUILT BOOK, NO INPUT AT ALL  (>=20pp - someone built these without an input on this host) ({len(C)})")
for r in sorted(C, key=lambda x: (x["year"], x["slug"])):
    p(line(r))

p(f"\n### D. NOT BUILT, NO INPUT  (<20pp - placeholder / cover-only shell) ({len(D)})")
for r in sorted(D, key=lambda x: (x["year"], x["slug"])):
    p(line(r) + f"   {r['pages']}pp")

if norender:
    p(f"\n### E. SPREADSHEET INPUT NOT RENDERED TO THE INPUT PANEL ({len(norender)})")
    for r in norender:
        p(line(r) + f"   [{r['exts']}] - run tools/inputs_to_json.py")

p("\n" + "=" * 78)
p("BY YEAR - missing an input file")
p("=" * 78)
for y in sorted({r["year"] for r in rows}):
    yr = [r for r in rows if r["year"] == y]
    miss = [r for r in yr if r["grp"] != "A"]
    p(f"  Year {y:<3} {len(miss):>2}/{len(yr):<3} missing input")

p("\n" + "=" * 78)
p("CROSS-TAB: input present x book actually built")
p("=" * 78)
def built(r):
    return r["pages"] >= 20
quads = {
    "input YES / book BUILT      ": [r for r in rows if r["grp"] == "A" and built(r)],
    "input YES / book NOT BUILT  ": [r for r in rows if r["grp"] == "A" and not built(r)],
    "input NO  / book BUILT      ": [r for r in rows if r["grp"] != "A" and built(r)],
    "input NO  / book NOT BUILT  ": [r for r in rows if r["grp"] != "A" and not built(r)],
}
for k, v in quads.items():
    p(f"\n  {k} ({len(v)})")
    if k.strip().startswith("input YES / book NOT BUILT"):
        for r in sorted(v, key=lambda x: (x["year"], x["slug"])):
            p(line(r) + f"   [{r['exts']}]")

p("\n" + "=" * 78)
p("ACTION LISTS")
p("=" * 78)
p(f"  1. Get/generate the input file for {len(B)+len(C)} built books -> group B + C")
p(f"  2. Chase the raw source for the 5 panel-only books (group B)")
p(f"  3. Build the {len(D)} stub books once their input arrives (group D)")
p(f"  4. Build the {len([r for r in A if not built(r)])} books whose input is already in the repo but the book is still a stub")


txt = "\n".join(out)
Path(PUB / "inputs-missing-report.txt").write_text(txt + "\n")
print(txt)
