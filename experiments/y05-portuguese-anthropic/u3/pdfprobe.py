"""PDF-side probe (what actually prints): per page, lowest text line above the folio band and the
text of that line, plus lines that fall past 272 mm (other than folio/brand).
    python pdfprobe.py
"""
import pymupdf, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = pymupdf.open(os.path.join(HERE, "build", "unit.pdf"))
MM = 72 / 25.4
for i, p in enumerate(d):
    lines = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if not t:
                continue
            x0, y0, x1, y1 = l["bbox"]
            lines.append((y1 / MM, x0 / MM, t))
    body = [l for l in lines if l[0] < 280.5 and not (l[1] < 12 or l[1] > 198)]   # skip side tab text
    low = max(body) if body else (0, 0, "")
    past = [f"{l[0]:.0f}:{l[2][:30]}" for l in lines if 272 < l[0] < 283 and l[2] not in (str(65 + i),)]
    print(65 + i, f"lowest {low[0]:.1f}mm «{low[2][:40]}»", "| past272:", past[:4])
