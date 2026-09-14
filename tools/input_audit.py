#!/usr/bin/env python3
"""Input audit: for every catalogue book, is there an input file (scheme of work
xlsx/csv or publisher source PDF), and what is the state of the book itself.

Definitions (per prime-books-book-builder doctrine):
  RAW   public/inputs/<slug> - input.<ext>      the real source (xlsx/csv/pdf)
  CORR  spreadsheet copy for the site — now simply the .xlsx/.csv raw input;
        the legacy public/input-corrections/ folder was retired 2026-09-14
  JSON  public/inputs/<slug>.json               rendered panel payload (derived)
  PDF   public/library/<slug>/book.pdf          the output master
"""
import json, os, csv, sys
from pathlib import Path

ROOT = Path("/root/prime-books")
PUB = ROOT / "public"

lib = json.load(open(PUB / "library.json"))
coll = json.load(open(PUB / "collection-books.json"))
if isinstance(coll, dict):
    coll_rows = coll.get("books", coll.get("items", []))
else:
    coll_rows = coll
coll_slugs = set()
for r in coll_rows:
    if isinstance(r, dict):
        s = r.get("slug") or r.get("id") or r.get("key")
        if s:
            coll_slugs.add(s)

def raw_kind(slug):
    d = PUB / "inputs"
    hits = []
    for f in sorted(d.glob(f"{slug} - input.*")):
        hits.append(f.name)
    # tolerate unstandardised names
    for f in sorted(d.iterdir()):
        if f.name.startswith(slug) and f.suffix.lower() in (".pdf", ".xlsx", ".xls", ".csv", ".docx") and f.name not in hits:
            hits.append(f.name)
    return hits

def ext_of(hits):
    exts = sorted({Path(h).suffix.lower().lstrip(".") for h in hits})
    return "+".join(exts)

rows = []
orphan_inputs = []
for r in lib:
    slug = r["slug"]
    hits = raw_kind(slug)
    # the site's spreadsheet payload comes straight from the raw .xlsx/.csv input now
    corr = any(h.lower().endswith((".xlsx", ".xls", ".csv")) for h in hits)
    js = (PUB / "inputs" / f"{slug}.json").exists()
    pdf = PUB / "library" / slug / "book.pdf"
    has_pdf = pdf.exists()
    mb = round(pdf.stat().st_size / 1e6, 2) if has_pdf else 0.0
    rows.append(dict(
        slug=slug, year=r.get("year"), subject=r.get("subject"),
        pages=r.get("pages"), done=bool(r.get("done")),
        input_files=";".join(hits), input_ext=ext_of(hits),
        has_raw=bool(hits), corr=corr, json=js, pdf=has_pdf, mb=mb,
        in_collection=slug in coll_slugs,
    ))

known = {r["slug"] for r in lib}
for f in sorted((PUB / "inputs").iterdir()):
    name = f.name
    if name.endswith(".json"):
        slug = name[:-5]
    elif " - input." in name:
        slug = name.split(" - input.")[0]
    else:
        slug = name.split(".")[0]
    if slug not in known:
        orphan_inputs.append(name)

rows.sort(key=lambda x: (x["year"] or 0, x["slug"]))

out = ROOT / "tools" / "out" 
os.makedirs(out, exist_ok=True)
with open(out / "input_audit.json", "w") as f:
    json.dump(dict(rows=rows, orphan_inputs=orphan_inputs), f, indent=1)

w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()), delimiter="\t")
w.writeheader()
for r in rows:
    w.writerow(r)

print("\n=== TOTALS ===")
print("catalogue rows:", len(rows))
print("with RAW input:", sum(r["has_raw"] for r in rows))
print("with corrections xlsx:", sum(r["corr"] for r in rows))
print("with inputs json:", sum(r["json"] for r in rows))
print("with book.pdf:", sum(r["pdf"] for r in rows))
print("MISSING RAW INPUT:", sum(not r["has_raw"] for r in rows))
print("orphan input files (no catalogue row):", orphan_inputs)
