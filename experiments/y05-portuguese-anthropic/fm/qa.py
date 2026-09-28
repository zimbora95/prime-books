#!/usr/bin/env python3
"""QA of the assembled book (fm/build/book.pdf) — run after assemble.py.

1. page count and even; 2. contents (Índice) spot-check: 10+ entries, each checked against the real page text;
3. p. 147 «Recursos digitais»: every QR decoded one crop per code at 200 dpi and compared with the codes decoded in
the units themselves (brief's tiled method); 4. whole-book QR decode (brief's tiled method); 5. fonts.
Writes build/qa.json and prints a summary.
"""
import json
import os
import random
import re
import sys

import cv2
import numpy as np
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
sys.path.insert(0, HERE)
import qrscan  # noqa: E402

FRONT = 8


def norm(s):
    s = s.lower()
    s = re.sub(r"[^\wáàâãéêíóôõúç]", "", s)
    return s


def per_code_decode(pg):
    det = cv2.QRCodeDetector()
    rs = []
    for x in pg.get_drawings():
        r = x["rect"]
        if 35 < r.width < 60 and abs(r.width - r.height) < 1 and not any(abs(r.x0 - q.x0) < 3 and abs(r.y0 - q.y0) < 3 for q in rs):
            rs.append(r)
    rs.sort(key=lambda r: (round(r.y0), r.x0))
    out = []
    for r in rs:
        v = ""
        for m in (8, 2, 12, 0, 4):  # 200 dpi, crop margins in pt; cv2 is sensitive to the crop, not to the code
            pix = pg.get_pixmap(dpi=200, clip=r + (-m, -m, m, m))
            a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3].copy()
            v, _, _ = det.detectAndDecode(a)
            if v:
                break
        out.append(dict(rect=[round(c) for c in r], url=v))
    return out


def main():
    book = pymupdf.open(os.path.join(BUILD, "book.pdf"))
    M = json.load(open(os.path.join(BUILD, "model.json")))
    H = json.load(open(os.path.join(BUILD, "harvest.json")))
    qa = dict(pages=book.page_count, even=book.page_count % 2 == 0)
    # --- 2. contents spot-check: two entries per unit (first real section and a random later one)
    random.seed(7)
    checks = []
    for u in M["units"]:
        es = [e for e in u["entries"] if not e.get("provisional")]
        if not es:
            continue
        pick = [es[0]] + random.sample(es[1:], min(1, len(es) - 1))
        for e in pick:
            txt = norm(book[e["page"] + FRONT - 1].get_text())
            probe = e["subs"][0] if e["subs"] else e["label"].split("·")[-1]
            ok = norm(probe) in txt
            checks.append(dict(unit=u["n"], entry=e["label"], probe=probe, page=e["page"], ok=ok))
    qa["contents_checks"] = checks
    # --- 3. p. 147
    p147 = book[147 + FRONT - 1]
    codes = per_code_decode(p147)
    unit_urls = [q["url"] for k in map(str, range(1, 8)) for q in (H.get(k) or {}).get("qrs", [])]
    dec = [c["url"] for c in codes]
    qa["p147"] = dict(codes=len(codes), decoded=sum(1 for c in codes if c["url"]),
                      matches_units=set(dec) == set(unit_urls),
                      missing_from_p147=sorted(set(unit_urls) - set(dec)), extra_on_p147=sorted(set(dec) - set(unit_urls) - {""}))
    # --- 4. whole book, brief's tiled method
    allq = qrscan.scan(os.path.join(BUILD, "book.pdf"), multi=False)
    qa["book_qr_tiled"] = [(p, u) for p, u, _ in allq]
    # --- 5. fonts
    fonts = sorted({(f[2], re.sub(r"^[A-Z]{6}\+", "", f[3])) for pg in book for f in pg.get_fonts()})
    qa["fonts"] = fonts
    json.dump(qa, open(os.path.join(BUILD, "qa.json"), "w"), ensure_ascii=False, indent=1)
    print(f"pages {qa['pages']} even={qa['even']}")
    print(f"contents spot-checks: {sum(c['ok'] for c in checks)}/{len(checks)} ok")
    for c in checks:
        print("   ", "ok " if c["ok"] else "BAD", f"p.{c['page']}", c["entry"], "|", c["probe"])
    print("p.147:", qa["p147"]["decoded"], "/", qa["p147"]["codes"], "decoded; same set as the units:", qa["p147"]["matches_units"],
          "| missing:", qa["p147"]["missing_from_p147"], "| extra:", qa["p147"]["extra_on_p147"])
    print("whole-book tiled decode:", len(allq), "codes on", len({p for p, _, _ in allq}), "pages")
    print("fonts:", fonts)


if __name__ == "__main__":
    main()
