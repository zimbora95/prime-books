#!/usr/bin/env python3
"""Verify the built Year 1 Physical Education interior before publishing it.

Read-only: no page is written, nothing is published. It replays the builder's
own page plan (tools/y01pe_a2_build.py: assemble()) and then checks the file on
disk against it:

1. every contents entry points at a page that really carries that title;
2. every interior page carries its folio, in the folio position;
3. no page runs past the type area, outside the margins, or sits empty;
4. each unit has its own band and rule colour, and no two units share one;
5. every QR code decodes back to the address printed beside it;
6. reading text is at least Standard A 2.0's Year 1 size (16 pt).

  ./.venv/bin/python tools/y01pe_a2_verify.py [path-to-book.pdf]
"""
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pb_engine as E            # noqa: E402
import y01pe_book_content as C   # noqa: E402
import y01pe_a2_build as build   # noqa: E402

E.IMG_DIR = os.path.join(REPO, "work", "y01pe", "img")
DEFAULT = os.path.join(REPO, "work", "y01pe_a2", "book_new.pdf")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def bare(url):
    return re.sub(r"^https?://(www\.)?", "", (url or "").strip()).rstrip("/").lower()


def main(path):
    flat, entries, _placed = build.assemble()
    by_num = {p["num"]: p for p in flat}
    doc = pymupdf.open(path)
    problems = []

    # 1 ---- the contents page tells the truth -----------------------------
    checked = 0
    for label, num, lvl, _col in entries:
        if num is None or not (3 <= num <= doc.page_count):
            problems.append("contents: %r points at page %s" % (label, num))
            continue
        # a contents label may describe its page ("Look back: the whole year",
        # "Words we used (2)"): check the part that is the page's own title
        core = norm(re.sub(r"\(.*?\)", "", label.split("·")[-1].split(":")[0]))
        got = norm(" ".join(doc[num - 1].get_text().splitlines()[:8]))
        if core and core not in got:
            problems.append("contents: p%d should be %r, page reads %r"
                            % (num, label, got[:64]))
        checked += 1

    # 2/3 ---- folio, box, emptiness ---------------------------------------
    for p in flat:
        num, page = p["num"], doc[p["num"] - 1]
        opener = p["kind"] == "opener"
        marks = [w for w in page.get_text("words")
                 if w[4].strip() == str(num) and w[0] > 500 and w[3] > 745]
        if not marks:
            problems.append("folio: page %d has no folio" % num)
        ys = [b["bbox"][3] for b in page.get_text("dict")["blocks"]
              if b.get("type") == 0]
        if ys and max(ys) > 776:
            problems.append("box: page %d text reaches %.0f" % (num, max(ys)))
        if not opener:
            for b in page.get_text("dict")["blocks"]:
                if b.get("type") == 0 and (b["bbox"][0] < E.ML - 1.5
                                           or b["bbox"][2] > E.MR + 1.5):
                    problems.append("box: page %d text outside the margins" % num)
                    break
            if len(page.get_text().strip()) < 120 and not page.get_images(full=True):
                problems.append("empty: page %d has almost nothing on it" % num)

    # 4 ---- one colour per unit ------------------------------------------
    colours = {}
    for p in flat:
        u = build.unit_of(p.get("spec") or {}) or 0
        page = doc[p["num"] - 1]
        pix = page.get_pixmap(alpha=False)
        band = "#%02x%02x%02x" % pix.pixel(int(E.W / 2), int(E.BAND_H - 0.5))[:3]
        rule = "#%02x%02x%02x" % pix.pixel(int(E.W / 2), int(E.BAND_H))[:3]
        colours.setdefault(u, set()).add(band + "/" + rule)
    for u, c in sorted(colours.items(), key=lambda kv: kv[0]):
        if u and len(c) != 1:
            problems.append("colour: unit %d mixes %s" % (u, sorted(c)))
    bands = {u: sorted(c)[0].split("/")[1] for u, c in colours.items() if u}
    if len(set(bands.values())) != len(bands):
        problems.append("colour: units share a rule colour: %s" % bands)

    # 5 ---- QR codes decode back to the printed address -------------------
    import numpy as np
    import cv2
    det = cv2.QRCodeDetector()
    qr_pages, qr_count = 0, 0
    for p in flat:
        page = doc[p["num"] - 1]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n)[:, :, :3]
        _ok, texts, _pts, _ = det.detectAndDecodeMulti(img)
        got = {bare(t) for t in (texts or []) if t.strip()}
        if not got:
            continue
        qr_pages += 1
        qr_count += len(got)
        body = norm(page.get_text())
        # a page that carries the teacher's link grid prints the titles, not the
        # addresses; there the gate is that every code points somewhere known
        grid = any(n == "qrgrid" for n, _x in (p.get("spec") or {}).get("blocks", []))
        known = {bare(v[0]) for v in C.LINKS.values()}
        for u in got:
            if norm(u) not in body and not (grid and u in known):
                problems.append("qr: page %d decodes to %s but the page does not "
                                "print that address" % (p["num"], u))

    # 6 ---- type size ------------------------------------------------------
    import collections
    sizes = collections.Counter()
    for p in flat:
        if p["kind"] == "opener":
            continue
        for b in doc[p["num"] - 1].get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for span in line["spans"]:
                    sizes[round(span["size"], 1)] += len(span["text"].strip())
    body_size = max((s for s in sizes if sizes[s] > 3000), default=0)
    if body_size < 16.0:
        problems.append("type: the most-read size is only %.1f pt" % body_size)

    print("interior pages        :", len(flat))
    print("contents entries check:", checked)
    print("QR pages / codes      :", qr_pages, "/", qr_count)
    print("unit rule colours     :", bands)
    print("reading text size     :", body_size, "pt")
    print("type histogram (top 6):", sizes.most_common(6))
    if problems:
        print("PROBLEMS (%d):" % len(problems))
        for x in problems[:40]:
            print("  -", x)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
