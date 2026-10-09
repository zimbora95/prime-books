#!/usr/bin/env python3
"""Prove the illustrations survive the Standard A-2.3 rebuild intact.

The review of the first pilot pass found the engine re-cutting the art to fit
the band: master p43 -> the new p46 showed the master's picture with a band
trimmed off it (28% of the picture's height; the chimney, roof apex and skyline
were gone). The engine now lays every plate at the PICTURE's own aspect inside
the band, so this script checks, for every plate of the rebuilt book:

  * the band carries the whole source illustration: the picture region the
    engine intends (the contain-fit box for that source's aspect) matches the
    source at that size, and the rest of the band is uniform margin;
  * the rebuilt picture is NOT a crop of the master's picture. A crop leaves the
    same artwork shorter, so the master's picture slide-aligns inside the
    rebuilt picture at a non-zero offset with a low difference - the exact
    signature the review used to find the defect.

  ./.venv/bin/python tools/y01pe_std_art_check.py [rebuilt.pdf] [--json out.json]

exit 0 = every picture whole, no crop signature against the master.
"""
import io
import json
import os
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

IMG_DIR = os.path.join(REPO, "work", "y01pe", "img")
MASTER = os.path.join(REPO, "public", "library", "y01-physical-education",
                      "book.pdf")
DEFAULT = os.path.join(REPO, "work", "y01pe_std", "book_new.pdf")
NORM_W = 256
SAME = 8.0           # mean abs difference (0-255) that counts as the same picture
MARGIN = 8           # how flat the band's surround must be


def raster(doc, info):
    return Image.open(io.BytesIO(doc.extract_image(info["xref"])["image"])) \
        .convert("RGB")


def bands(doc):
    """[(page, band raster)] for every picture band of a book."""
    for i, page in enumerate(doc):
        for info in page.get_image_info(xrefs=True):
            x0, y0, x1, y1 = info["bbox"]
            if (x1 - x0) >= 450 and (y1 - y0) >= 100:
                yield i + 1, raster(doc, info)


def picture_region(band):
    """The picture inside a band, found from the pixels: every pixel that is not
    the band's own margin colour. None if the band is a single flat area."""
    a = np.asarray(band).astype(int)
    frame = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                            a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    margin = np.median(frame, axis=0)
    mask = (np.abs(a - margin).max(axis=2) > MARGIN)
    ys, xs = np.where(mask)
    if len(xs) < 20:
        return None
    return band.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1,
                      int(ys.max()) + 1))


def contain_box(band, aspect, w=980):
    """The region a source of this aspect occupies inside the band raster, as
    plate_png() lays it out: the whole picture, centred, nothing re-cut."""
    cw = min(w, band.width)
    ch = band.height
    want = cw / ch
    if aspect > want:
        nw, nh = cw, max(1, int(round(cw / aspect)))
    else:
        nh, nw = ch, max(1, int(round(ch * aspect)))
    x, y = (cw - nw) // 2, (ch - nh) // 2
    return (x, y, x + nw, y + nh)


def margin_std(band, box):
    """How flat the band is outside the picture (a contain-fit leaves margin)."""
    a = np.asarray(band).astype(float)
    m = np.ones(a.shape[:2], bool)
    m[box[1]:box[3], box[0]:box[2]] = False
    if m.sum() < 50:
        return 0.0
    return round(float(a[m].std(axis=0).mean()), 2)


def cover_crop(src, aspect):
    """The centre-crop the OLD engine made (how the master's rasters were cut),
    used only to identify which source a master band was built from."""
    w0, h0 = src.size
    have = w0 / h0
    if have > aspect:
        nw = int(h0 * aspect)
        return src.crop(((w0 - nw) // 2, 0, (w0 - nw) // 2 + nw, h0))
    nh = int(w0 / aspect)
    return src.crop((0, (h0 - nh) // 2, w0, (h0 - nh) // 2 + nh))


def norm(im, w=NORM_W):
    return np.asarray(im.resize((w, max(1, int(round(im.height * w / im.width))))
                                )).astype(float)


def slide(a, b):
    """Best mean abs difference of the shorter array slid inside the longer."""
    if b.shape[0] > a.shape[0]:
        a, b = b, a
    best = (1e9, 0)
    for off in range(0, a.shape[0] - b.shape[0] + 1):
        d = float(np.abs(a[off:off + b.shape[0]] - b).mean())
        if d < best[0]:
            best = (round(d, 2), off)
    return best


def main():
    args, skip = [], False
    for a in sys.argv[1:]:
        if skip:
            skip = False
            continue
        if a == "--json":
            skip = True
            continue
        if not a.startswith("--"):
            args.append(a)
    path = args[0] if args else DEFAULT

    import y01pe_std_build as build
    build.apply_tokens()
    flat, _groups, _placed, _sig, _added = build.assemble(pad=1)
    if 3 + len(flat) != pymupdf.open(path).page_count:
        for _pad in (0, 1, 2, 3):
            flat, _groups, _placed, _sig, _added = build.assemble(pad=_pad)
            if 3 + len(flat) == pymupdf.open(path).page_count:
                break
    want, kinds = {}, {}
    for p in flat:
        kinds[p["num"]] = p["kind"]
        spec = p.get("spec") or {}
        if p["kind"] == "opener" and spec.get("img"):
            want[p["num"]] = spec["img"]
            continue
        for name, b in spec.get("blocks", []):
            if name == "plate":
                want[p["num"]] = b["img"]

    sources = {f[:-4]: Image.open(os.path.join(IMG_DIR, f)).convert("RGB")
               for f in os.listdir(IMG_DIR) if f.endswith(".png")}
    new, master = pymupdf.open(path), pymupdf.open(MASTER)

    checked, failures, regions = [], [], {}
    for page, band in bands(new):
        if page == 1 or page == new.page_count:
            continue      # cover and back cover are the master's own pages
        img = want.get(page)
        if img is None or img not in sources:
            checked.append(dict(page=page, img=img, diff=None))
            failures.append(dict(page=page, img=img, diff=None,
                                 why="no planned picture for this band"))
            continue
        src = sources[img]
        cut = 0
        if kinds.get(page) == "opener":
            # The unit opener is a designed full-bleed arch frame (the master
            # fills it the same way, corners cut to the arch), so the comparison
            # samples the picture's interior only.
            w0, h0 = band.size
            crop = (int(w0 * 0.25), int(h0 * 0.30), int(w0 * 0.75), h0)
            box = (0, 0, w0, h0)
            region = band.crop(crop)
            scaled = cover_crop(src, w0 / h0).resize(band.size).crop(crop)
        else:
            box = contain_box(band, src.width / src.height)
            region = band.crop(box)
            scaled = src.resize((box[2] - box[0], box[3] - box[1]))
        regions[page] = region
        d = float(np.abs(np.asarray(scaled).astype(float)
                         - np.asarray(region).astype(float)).mean())
        margin = margin_std(band, box)
        checked.append(dict(page=page, img=img, diff=round(d, 2),
                            kind=kinds.get(page),
                            picture_pct=round(100.0 * region.width / band.width),
                            margin_std=margin,
                            margin_pct=round(100.0 * (1 - region.width
                                                      * region.height
                                                      / (band.width * band.height)), 1),
                            src_aspect=round(src.width / src.height, 3),
                            region_aspect=round(region.width / region.height, 3)))
        if d > (SAME + 3 if kinds.get(page) == "opener" else SAME):
            failures.append(dict(page=page, img=img, diff=round(d, 2),
                                 why="picture is not the whole source"
                                     if kinds.get(page) != "opener"
                                     else "opener interior (arch frame) does not "
                                         "match its source"))
        if margin > 6:
            failures.append(dict(page=page, img=img, margin_std=margin,
                                 why="band margin is not flat"))

    crops = []
    by_img = {}
    for c in checked:
        by_img.setdefault(c["img"], []).append(c["page"])
    for mpage, band in bands(master):
        asp = band.width / band.height
        best = (1e9, None)
        for nm, src in sources.items():
            c = cover_crop(src, asp)
            d = float(np.abs(np.asarray(c.resize((96, 64))).astype(float)
                             - np.asarray(band.resize((96, 64))).astype(float)
                             ).mean())
            if d < best[0]:
                best = (round(d, 2), nm)
        if best[1] is None or best[0] > SAME or best[1] not in by_img:
            continue
        nreg = regions.get(by_img[best[1]][0])
        if nreg is None:
            continue
        mreg = band
        a, b = norm(mreg), norm(nreg)
        # The defect's signature: the rebuilt picture holds LESS of the artwork
        # than the master's did, and the master's raster still aligns inside it
        # at a non-zero offset (the same picture with a band taken off). More
        # artwork than the master is the fix, not the defect.
        if b.shape[0] >= a.shape[0] - 2:
            continue
        d, off = slide(a, b)
        if d < SAME and off > 0:
            crops.append(dict(master_page=mpage, new_page=by_img[best[1]][0],
                              img=best[1], mean_abs_diff=d, offset=off,
                              master_h=int(a.shape[0]), new_h=int(b.shape[0])))

    plates = [c for c in checked if c.get("picture_pct")
              and c.get("kind") != "opener"]
    smallest = min((c["picture_pct"] for c in plates), default=None)
    report = dict(pdf=os.path.relpath(path, REPO), plates=len(checked),
                  failures=failures, crop_signatures=crops,
                  smallest_picture_pct_of_band=smallest, checked=checked)
    print("bands checked            :", len(checked))
    print("pictures NOT whole        :", len(failures),
          [(f["page"], f["img"], f["diff"]) for f in failures])
    print("crop signatures vs master :", len(crops), crops)
    print("narrowest picture         :", smallest, "% of the band")
    print("widest margin             :",
          max((c.get("margin_pct") or 0) for c in plates), "% of a picture band")
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        with open(out, "w") as fh:
            json.dump(report, fh, indent=1)
        print("json ->", out)
    return 1 if (failures or crops) else 0


if __name__ == "__main__":
    sys.exit(main())