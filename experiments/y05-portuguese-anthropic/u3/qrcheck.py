"""Decode every QR in build/unit.pdf (brief's snippet: 200 dpi, tiled crops, cv2.QRCodeDetector) + font check."""
import pymupdf, cv2, numpy as np, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = pymupdf.open("build/unit.pdf"); det = cv2.QRCodeDetector(); found = set()
for i, pg in enumerate(d):
    W, H = pg.rect.width, pg.rect.height
    for ty in range(8):
        for tx in range(4):
            clip = pymupdf.Rect(tx*W/4-40, ty*H/8-40, (tx+1)*W/4+40, (ty+1)*H/8+40) & pg.rect
            pix = pg.get_pixmap(dpi=200, clip=clip); a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
            v, _, _ = det.detectAndDecode(a)
            if v: found.add((i + 65, v))
for f in sorted(found): print("p.%d  %s" % f)
print("pages", d.page_count, "size mm", round(d[0].rect.width/72*25.4, 1), "x", round(d[0].rect.height/72*25.4, 1))
fonts = {}
for p in d:
    for x in p.get_fonts(full=True):
        fonts[x[3] or "(Type3, unnamed)"] = (x[2], x[1])
for k, v in sorted(fonts.items()): print("font", k, v)
blank = [i + 65 for i, p in enumerate(d) if not p.get_text().strip() and not p.get_images()]
print("blank pages", blank)
