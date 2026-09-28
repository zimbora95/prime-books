"""Harvest the real structure of every built unit: page count, folios, running heads, headings,
QR codes (decoded from the PDF) with their labels, glossary terms and cited sources.

Writes fm/build/harvest.json. Results are cached per PDF (mtime) in fm/build/cache/ so the
build is restartable and cheap to re-run while other units are still changing.

    /root/.hermes/cache/scratch/exp-venv/bin/python harvest.py
"""
import html as H
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(HERE, "build")
CACHE = os.path.join(BUILD, "cache")
sys.path.insert(0, HERE)
import qrscan  # noqa: E402
from plan import UNITS  # noqa: E402


def unit_dir(u):
    return ROOT if u["folder"] == "." else os.path.join(ROOT, u["folder"])


def clean(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def lines_of(pg):
    """text lines with bbox + max size + bold flag (spans in one line are glued without spaces)"""
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            t = "".join(s["text"] for s in l["spans"]).strip()
            out.append(dict(bbox=l["bbox"], size=max(s["size"] for s in sp), text=t,
                            bold=any((s["flags"] & 16) or re.search(r"Bold|Black|Heavy|ExtraBold|SemiBold|[6-9]00", s["font"]) for s in sp),
                            fonts=sorted({s["font"] for s in sp})))
    return out


def pdf_pages(pdf):
    d = pymupdf.open(pdf)
    pages = []
    for i, pg in enumerate(d):
        W, Hh = pg.rect.width, pg.rect.height
        L = lines_of(pg)
        run = [l for l in L if l["bbox"][3] < 36]
        runL = " ".join(l["text"] for l in run if l["bbox"][0] < W / 2)
        runR = " ".join(l["text"] for l in run if l["bbox"][0] >= W / 2)
        fol = [l["text"] for l in L if l["bbox"][1] > Hh - 45 and re.fullmatch(r"\d{1,3}", l["text"])]
        body = [l for l in L if 36 <= l["bbox"][3] < Hh - 45]
        mx = max([l["size"] for l in body], default=0)
        h1 = " ".join(l["text"] for l in body if l["size"] >= mx - 0.5) if mx >= 20 else ""
        pages.append(dict(pdf_page=i + 1, runL=runL, runR=runR, folio=fol, h1=h1, h1size=round(mx, 1),
                          text=pg.get_text(), bold=[l["text"] for l in L if l["bold"]]))
    return pages, d


def html_pages(path):
    """section.page blocks of a built unit.html -> running head right part, headings, classes"""
    if not os.path.exists(path):
        return []
    src = open(path, encoding="utf-8").read()
    src = re.sub(r"<script.*?</script>", "", src, flags=re.S)
    body = src[src.find("<body"):]
    secs = re.split(r"(?=<section\b[^>]*class=\"[^\"]*\bpage\b)", body)[1:]
    out = []
    for s in secs:
        cls = re.search(r'class="([^"]*)"', s).group(1)
        run = re.search(r'<header class="run[^"]*">(.*?)</header>', s, re.S)
        runL = runR = ""
        if run:
            spans = re.findall(r"<span[^>]*>(.*?)</span>(?=\s*(?:<span|$))", run.group(1) + "", re.S)
            parts = re.findall(r"<span>(.*?)</span>", run.group(1), re.S) or spans
            if parts:
                runL = clean(parts[0])
                runR = clean(parts[-1]) if len(parts) > 1 else ""
        h = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S) or re.search(r"<h2[^>]*>(.*?)</h2>", s, re.S)
        kick = re.search(r'<div class="kick"[^>]*>(.*?)</div>', s, re.S)
        gl = []
        for g in re.finditer(r'<div class="(?:glos2|gloss)[^"]*"[^>]*>(.*?)</div>\s*(?:</div>|\n)', s, re.S):
            for t, dfn in re.findall(r"<b>(.*?)</b>\s*[—–-]\s*(.*?)(?=</p>|<br|<b>|$)", g.group(1), re.S):
                gl.append((clean(t), clean(dfn)))
        srcs = [clean(m) for m in re.findall(r">([^<>]*?\b(?:Fontes?|Fonte consultada|Texto adaptado de|Extrato de|Excerto de|in)\s*:[^<]{4,400})<", s)]
        out.append(dict(cls=cls, runL=runL, runR=runR, h1=clean(h.group(1)) if h else "",
                        kick=clean(kick.group(1)) if kick else "", gloss=gl, sources=srcs))
    return out


def qr_labels(doc, qrs):
    res = []
    for pno, url, r in qrs:
        pg = doc[pno - 1]
        clip = pymupdf.Rect(r.x1 + 2, r.y0 - 8, min(r.x1 + 190, pg.rect.width - 10), r.y1 + 8)
        t = clean(pg.get_textbox(clip).replace("\n", " "))
        if len(t) < 6:  # label may sit on the left or below
            clip = pymupdf.Rect(r.x0 - 10, r.y1, r.x1 + 120, r.y1 + 30)
            t = clean(pg.get_textbox(clip).replace("\n", " "))
        res.append(dict(pdf_page=pno, url=url, label=t[:160], rect=[round(v, 1) for v in r]))
    return res


def harvest_unit(u):
    d = unit_dir(u)
    pdf = os.path.join(d, "build", "unit.pdf")
    info = dict(n=u["n"], folder=u["folder"], exists=os.path.exists(pdf))
    donef = os.path.join(ROOT, "jobs", "logs", f"u{u['n']}.done")
    info["done_flag"] = os.path.exists(donef) or u["n"] == 1
    if not info["exists"]:
        return info
    st = os.stat(pdf)
    ck = os.path.join(CACHE, f"u{u['n']}.json")
    if os.path.exists(ck):
        c = json.load(open(ck))
        if c.get("mtime") == st.st_mtime and c.get("size") == st.st_size:
            c["done_flag"] = info["done_flag"]
            return c
    pages, doc = pdf_pages(pdf)
    hp = html_pages(os.path.join(d, "build", "unit.html"))
    if len(hp) != len(pages):
        hp_src = html_pages(os.path.join(d, "src", "unit.html"))
        if len(hp_src) == len(pages):
            hp = hp_src
    for k, p in enumerate(pages):
        p["html"] = hp[k] if k < len(hp) else None
    qrs = qrscan.scan(pdf)
    info.update(mtime=st.st_mtime, size=st.st_size, page_count=len(pages), pages=pages,
                qrs=qr_labels(doc, qrs), html_ok=len(hp) == len(pages))
    os.makedirs(CACHE, exist_ok=True)
    json.dump(info, open(ck, "w"), ensure_ascii=False)
    return info


def main():
    os.makedirs(BUILD, exist_ok=True)
    res = {}
    for u in UNITS:
        r = harvest_unit(u)
        res[u["n"]] = r
        print(f"u{u['n']}: exists={r['exists']} done={r['done_flag']} pages={r.get('page_count')} qrs={len(r.get('qrs', []))}")
    json.dump(res, open(os.path.join(BUILD, "harvest.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
