"""The brief's QR decode snippet, verbatim, run on u5/build/unit.pdf (pages reported as book folios)."""
import os
import pymupdf, cv2, numpy as np
here = os.path.dirname(os.path.abspath(__file__))
d = pymupdf.open(os.path.join(here, "build", "unit.pdf")); det = cv2.QRCodeDetector(); found = set()
for i, pg in enumerate(d):
    W, H = pg.rect.width, pg.rect.height
    for ty in range(8):
        for tx in range(4):
            clip = pymupdf.Rect(tx*W/4-40, ty*H/8-40, (tx+1)*W/4+40, (ty+1)*H/8+40) & pg.rect
            pix = pg.get_pixmap(dpi=200, clip=clip); a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
            v, _, _ = det.detectAndDecode(a)
            if v: found.add((i+97, v))
for f in sorted(found): print(f)
print(len(found), "QR codes decoded")
