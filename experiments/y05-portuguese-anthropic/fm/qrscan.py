"""Decode every QR code in a PDF (the brief's tiled cv2 method, one 200-dpi render per page).

Returns [(page_no, url, rect_in_pt), ...] sorted by page then position.
Usage: python qrscan.py file.pdf
"""
import sys
import cv2
import numpy as np
import pymupdf

DPI = 200


def scan(pdf, pages=None, grid=(4, 8), multi=True):
    d = pymupdf.open(pdf)
    det = cv2.QRCodeDetector()
    found = {}
    for i, pg in enumerate(d):
        if pages and (i + 1) not in pages:
            continue
        W, H = pg.rect.width, pg.rect.height
        pix = pg.get_pixmap(dpi=DPI)
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
        k = DPI / 72
        gx, gy = grid
        for ty in range(gy):
            for tx in range(gx):
                clip = pymupdf.Rect(tx * W / gx - 40, ty * H / gy - 40, (tx + 1) * W / gx + 40, (ty + 1) * H / gy + 40) & pg.rect
                x0, y0, x1, y1 = [int(round(v * k)) for v in clip]
                tile = a[y0:y1, x0:x1]
                hits = []
                v, pts, _ = det.detectAndDecode(tile)
                if v:
                    hits.append((v, pts))
                if multi:  # dense pages (p. 147) hold several codes per tile
                    ok, vs, ptss, _ = det.detectAndDecodeMulti(tile)
                    if ok:
                        hits += [(vv, pp) for vv, pp in zip(vs, ptss) if vv]
                for v, pts in hits:
                    p = pts.reshape(-1, 2)
                    r = pymupdf.Rect((p[:, 0].min() + x0) / k, (p[:, 1].min() + y0) / k,
                                     (p[:, 0].max() + x0) / k, (p[:, 1].max() + y0) / k)
                    key = (i + 1, v)
                    # the same code can be decoded from overlapping tiles: keep one rect per code position
                    lst = found.setdefault(key, [])
                    if not any(abs(r.x0 - q.x0) < 20 and abs(r.y0 - q.y0) < 20 for q in lst):
                        lst.append(r)
    out = []
    for (pno, url), rects in found.items():
        for r in rects:
            out.append((pno, url, r))
    out.sort(key=lambda t: (t[0], round(t[2].y0 / 30), t[2].x0))
    return out


if __name__ == "__main__":
    for pno, url, r in scan(sys.argv[1]):
        print(pno, url, [round(v) for v in r])
