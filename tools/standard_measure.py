#!/usr/bin/env python3
"""Measure the Prime Books house standard from the y01 Physical Education master.

Nothing here is remembered: every number is read off the PDF that the site serves.
"""
import json, os, sys
import pymupdf

REPO = "/root/prime-books"
BOOK = os.path.join(REPO, "public", "library", "y01-physical-education", "book.pdf")
OUT = os.path.join(REPO, "work", "standard")
os.makedirs(OUT, exist_ok=True)

doc = pymupdf.open(BOOK)
n = doc.page_count
report = {"source": BOOK, "pages": n, "page_size": {}, "pages_detail": {}}

W, H = doc[0].rect.width, doc[0].rect.height
report["page_size"] = {"w": round(W, 2), "h": round(H, 2)}

# ---- text spans, with font/size/colour, for the pages that carry the standard
def spans(p, minlen=1):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if len(s["text"].strip()) >= minlen:
                    out.append({
                        "text": s["text"],
                        "font": s["font"],
                        "size": round(s["size"], 2),
                        "colour": "#%06x" % s["color"],
                        "bbox": [round(v, 1) for v in s["bbox"]],
                    })
    return out

# ---- running-header band: the wide filled rect at the top of an interior page
def band(p):
    best = None
    for d in p.get_drawings():
        f = d.get("fill")
        r = d["rect"]
        if f and r.width > 400 and r.y0 < 60 and 20 < r.height < 60:
            if best is None or r.width > best[0].width:
                best = (r, tuple(round(c, 3) for c in f))
    if not best:
        return None
    r, f = best
    return {"rect": [round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1)],
            "height": round(r.height, 1),
            "fill_rgb": f,
            "fill_hex": "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in f)}

def folio(p):
    """The page-number badge: a filled circle bottom-right."""
    best = None
    for d in p.get_drawings():
        f = d.get("fill")
        r = d["rect"]
        if f and r.y0 > H - 90 and 8 < r.width < 40 and abs(r.width - r.height) < 3:
            best = (r, tuple(round(c, 3) for c in f))
    if not best:
        return None
    r, f = best
    return {"centre": [round((r.x0 + r.x1) / 2, 1), round((r.y0 + r.y1) / 2, 1)],
            "diameter": round(r.width, 1),
            "fill_rgb": f,
            "fill_hex": "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in f)}

for label, idx in [("cover", 0), ("p2_imprint", 1), ("p3_welcome", 2), ("p4_contents", 3),
                   ("p5_first_body", 4), ("p10_last_front", 9),
                   ("p11_unit1_opener", 10), ("p70", n - 3), ("p71", n - 2), ("p72_back", n - 1)]:
    p = doc[idx]
    report["pages_detail"][label] = {
        "folio_no": idx + 1,
        "band": band(p),
        "badge": folio(p),
        "images": len(p.get_images(full=True)),
        "drawings": len(p.get_drawings()),
        "spans": spans(p)[:40],
    }

# ---- fonts in use across the whole book
fonts = {}
for pg in doc:
    for f in pg.get_fonts(full=True):
        fonts[f[3]] = fonts.get(f[3], 0) + 1
report["fonts"] = dict(sorted(fonts.items(), key=lambda kv: -kv[1]))

# ---- the unit colour table: sample the running-header band of each unit's pages
units = {}
for i in range(10, n - 2):
    b = band(doc[i])
    if not b:
        continue
    units.setdefault(b["fill_hex"], []).append(i + 1)
report["header_band_runs"] = {k: [min(v), max(v), len(v)] for k, v in
                              sorted(units.items(), key=lambda kv: min(kv[1]))}

with open(os.path.join(OUT, "y01pe_measured.json"), "w") as fh:
    json.dump(report, fh, indent=1)

print("page", report["page_size"])
print("fonts:", list(report["fonts"])[:8])
print()
print("running-header band runs (hex -> [first, last, count]):")
for k, v in report["header_band_runs"].items():
    print(f"   {k}  pages {v[0]}-{v[1]}  ({v[2]} pages)")
print()
for label, d in report["pages_detail"].items():
    b = d["band"] or {}
    bd = d["badge"] or {}
    print(f"{label:18s} p{d['folio_no']:<3d} band={b.get('fill_hex','-'):>8s} h={b.get('height','-')} "
          f"badge={bd.get('fill_hex','-'):>8s} d={bd.get('diameter','-')} imgs={d['images']}")
print()
print("written:", os.path.join(OUT, "y01pe_measured.json"))
