"""Crop the generated art sheets into single spot images (idempotent)."""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "art")
CUT = os.path.join(ART, "cut")


def trim_white(im, thr=236, pad=0.06):
    a = np.asarray(im.convert("L"))
    ys, xs = np.where(a < thr)
    if not len(xs):
        return im
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w, h = x1 - x0, y1 - y0
    s = int(max(w, h) * (1 + 2 * pad))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    out = Image.new("RGB", (s, s), "white")
    out.paste(im.crop((x0, y0, x1 + 1, y1 + 1)), ((s - w) // 2, (s - h) // 2))
    return out


def whiten(im, lo=232):
    """Push near-white paper to pure white so multiply-blend shows no box."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    m = a.min(axis=2) >= lo
    a[m] = 255
    return Image.fromarray(a.astype(np.uint8))


def main_object(im, thr=236, dil=15):
    """Keep only the connected blob(s) around the centre of the crop (drops neighbour slivers)."""
    import cv2
    a = np.asarray(im.convert("L"))
    m = (a < thr).astype(np.uint8)
    m = cv2.dilate(m, np.ones((dil, dil), np.uint8))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(m)
    H, W = a.shape
    best, keep = None, np.zeros_like(m, bool)
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        d = np.hypot(cent[i][0] - W / 2, cent[i][1] - H / 2) / max(W, H)
        score = area * (1 - d) ** 2
        if best is None or score > best[0]:
            best = (score, i)
    keep = lab == best[1]
    out = np.asarray(im.convert("RGB")).copy()
    out[~keep] = 255
    return Image.fromarray(out)


def grid_cells(src, n, prefix, size=520, grow=0.10, dil=15):
    im = Image.open(os.path.join(ART, src)).convert("RGB")
    W, H = im.size
    for r in range(n):
        for c in range(n):
            box = (max(0, int(W * (c - grow) / n)), max(0, int(H * (r - grow) / n)), min(W, int(W * (c + 1 + grow) / n)), min(H, int(H * (r + 1 + grow) / n)))
            cell = whiten(trim_white(main_object(whiten(im.crop(box)), dil=dil)))
            cell.thumbnail((size, size), Image.LANCZOS)
            cell.save(os.path.join(CUT, f"{prefix}{r * n + c}.jpg"), quality=88)


def bd_panels(src="bd.png", size=900):
    im = Image.open(os.path.join(ART, src)).convert("RGB")
    W, H = im.size
    a = np.asarray(im.convert("L")).astype(np.int16)
    for r in range(2):
        for c in range(2):
            x0, x1, y0, y1 = c * W // 2, (c + 1) * W // 2, r * H // 2, (r + 1) * H // 2
            sub = a[y0:y1, x0:x1]
            # strip dark gutter lines / near-white margins at the edges
            def keep(v):
                return 40 < v < 247
            rows = [i for i in range(sub.shape[0]) if keep(sub[i].mean())]
            cols = [j for j in range(sub.shape[1]) if keep(sub[:, j].mean())]
            e = int(0.022 * W)
            ry0, ry1, cx0, cx1 = rows[0] + e, rows[-1] - e, cols[0] + e, cols[-1] - e
            p = im.crop((x0 + cx0, y0 + ry0, x0 + cx1, y0 + ry1))
            p.thumbnail((size, size), Image.LANCZOS)
            p.save(os.path.join(CUT, f"bd{r * 2 + c}.jpg"), quality=86)


def main(force=False):
    os.makedirs(CUT, exist_ok=True)
    stamp = os.path.join(CUT, ".done")
    srcs = [os.path.join(ART, f) for f in ("dice-a.png", "dice-b.png", "stamps.png", "spots.png", "bd.png", "opener.png", "ilha.png")]
    if not force and os.path.exists(stamp) and all(os.path.getmtime(stamp) > os.path.getmtime(s) for s in srcs if os.path.exists(s)):
        return
    grid_cells("dice-a.png", 3, "da", grow=0.04, dil=7)
    grid_cells("dice-b.png", 3, "db")
    # the tram (db1) is NOT used: its destination sign carries pseudo-digits
    grid_cells("stamps.png", 3, "st", size=420)
    grid_cells("spots.png", 2, "sp", size=700)
    bd_panels()
    isl = whiten(trim_white(main_object(whiten(Image.open(os.path.join(ART, "ilha.png")).convert("RGB")))))
    isl.thumbnail((520, 520), Image.LANCZOS)
    isl.save(os.path.join(CUT, "ilha.jpg"), quality=88)
    op = Image.open(os.path.join(ART, "opener.png")).convert("RGB")
    op.save(os.path.join(ART, "opener.jpg"), quality=87, optimize=True, progressive=True)
    open(stamp, "w").write("ok")


if __name__ == "__main__":
    main(force=True)
