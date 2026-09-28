"""PDF-based layout probe for Unit 7 (no Chromium needed).
For each page: lowest content (mm from top, excluding folio badge and side tab), and text spans
that overlap other text spans or the folio badge.  Usage: python pdfmetrics.py
"""
import os
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 72 / 25.4
d = pymupdf.open(os.path.join(HERE, "build", "unit.pdf"))
print("folio  bottom_mm  issues   (content must end <= 277 mm; folio badge is 280-289 mm)")
for i, pg in enumerate(d):
    W, H = pg.rect.width, pg.rect.height
    odd = (129 + i) % 2 == 1
    folio = pymupdf.Rect((W - 21 * MM, 279 * MM, W - 11 * MM, 290 * MM) if odd else (11 * MM, 279 * MM, 21 * MM, 290 * MM))
    spans = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if len(s["text"].strip()) > 2:
                    spans.append((pymupdf.Rect(s["bbox"]), s["text"].strip()))
    items = [r for r, t in spans]
    items += [pymupdf.Rect(im["bbox"]) for im in pg.get_image_info()]
    items += [dr["rect"] for dr in pg.get_drawings() if dr["rect"].height < H * 0.9]
    def keep(r):
        if r.intersects(folio) and r.width < 12 * MM:
            return False
        if r.x1 < 9 * MM or r.x0 > W - 9 * MM:  # side tab
            return False
        return r.height < H * 0.9
    bottom = max((r.y1 for r in items if keep(r)), default=0) / MM if i else 0
    issues = []
    for r, t in spans:
        if r.intersects(folio) and t != str(129 + i):
            issues.append(f"FOLIO-HIT '{t[:25]}'")
    for a in range(len(spans)):
        for b in range(a + 1, len(spans)):
            ra, rb = spans[a][0], spans[b][0]
            inter = ra & rb
            if not inter.is_empty and inter.width > 2 and inter.height > 0.45 * min(ra.height, rb.height):
                issues.append(f"TEXT-OVERLAP '{spans[a][1][:18]}'/'{spans[b][1][:18]}'")
    flag = " TOO-LOW" if bottom > 277 else ""
    print(129 + i, round(bottom, 1), issues[:6], flag)
