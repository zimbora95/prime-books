#!/usr/bin/env python3
"""Build Unit 6 — «Avaliação» (Português · 5.º Ano), pp. 113–128.

src/unit.html ({{…}} tokens) -> build/unit.html -> build/unit.pdf -> build/png/NN.png (NN = 113..128)
Run with the experiment venv:
    /root/.venvs/y05exp/bin/python build.py
Tokens:
    {{QR:name}}          QR code (segno, viewBox + 4-module quiet zone)
    {{M:sec:n}}          margin mark box «[ __ /n ]»; build checks that every section adds up to its data-pts
"""
import os, re, subprocess, sys
from collections import defaultdict
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "y05-portuguese-anthropic"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
BUILD = os.path.join(HERE, "build")
FIRST_FOLIO = 113
N_PAGES = 16

QRS = {}  # no QR codes in this unit: part D is read aloud by the teacher; solutions are in the back matter


def qr_svg(url):
    q = segno.make(url, error="l", boost_error=False)  # version 5: larger modules, decodes more reliably at 200 dpi
    svg = q.svg_inline(scale=1, border=4, dark="#1C2536", light="#ffffff")
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    return svg.replace(m.group(0), f'viewBox="0 0 {m.group(1)} {m.group(2)}" shape-rendering="crispEdges"', 1)


def marks(html):
    """Replace {{M:sec:n}} and verify section totals against data-pts of <… data-sec="sec" data-pts="N">."""
    got = defaultdict(int)

    def rep(m):
        sec, n = m.group(1), int(m.group(2))
        got[sec] += n
        return f'<span class="mk" data-m="{sec}"><i></i><b>/{n}</b></span>'

    html = re.sub(r"\{\{M:([0-9A-D]+):(\d+)\}\}", rep, html)
    want = {s: int(p) for s, p in re.findall(r'data-sec="([0-9A-D]+)" data-pts="(\d+)"', html)}
    bad = {s: (got.get(s, 0), want[s]) for s in want if got.get(s, 0) != want[s]}
    extra = set(got) - set(want)
    for t in sorted({s[0] for s in want}):
        tot = sum(v for s, v in got.items() if s[0] == t)
        print(f"  Teste {t}: " + " · ".join(f"{s[1]} {got[s]}" for s in sorted(got) if s[0] == t) + f"  = {tot}")
        if tot != 100:
            bad[f"T{t}"] = (tot, 100)
    if bad or extra:
        sys.exit(f"marks mismatch: {bad} {extra}")
    return html


def build():
    os.makedirs(BUILD, exist_ok=True)
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    html = marks(html)
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    out = os.path.join(BUILD, "unit.html")
    open(out, "w", encoding="utf-8").write(html)
    if "--html" in sys.argv:
        return
    base = [CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw"]
    pdf = os.path.join(BUILD, "unit.pdf")
    subprocess.run(base + ["--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}",
                           "file://" + out], check=True, capture_output=True, timeout=600)
    import pymupdf as fitz
    doc = fitz.open(pdf)
    png = os.path.join(BUILD, "png")
    os.makedirs(png, exist_ok=True)
    for f in os.listdir(png):
        os.remove(os.path.join(png, f))
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=110).save(os.path.join(png, f"{FIRST_FOLIO + i}.png"))
    fonts = sorted({(f[3], f[1]) for pg in doc for f in pg.get_fonts()})
    print("pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)
    if doc.page_count != N_PAGES:
        print(f"!! page count {doc.page_count} != {N_PAGES}")


if __name__ == "__main__":
    build()
