"""Assemble the unit, print it with Chromium, and audit every page.

python build.py            -> build/farol-u1.pdf + renders/pNN.png
Fails loudly if any element spills out of its page's live area.
"""
import importlib, sys, json, pathlib, asyncio
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from parts import TOTAL

import os
U = os.environ.get("UNIT", "1")
MODS = {"0": ("u0_a",), "1": ("pages_a", "pages_b", "pages_c"), "2": ("u2_a", "u2_b"), "3": ("u3_a", "u3_b"),
        "4": ("u4_a", "u4_b"), "5": ("u5_a",), "6": ("u6_a",), "7": ("u7_a",), "fm": ("fm",)}[U]
if os.environ.get("MODS"):            # e.g. MODS=u2_a to build one part in isolation
    MODS = tuple(os.environ["MODS"].split(","))
TAG = os.environ.get("TAG") or ("u1" if U == "1" else "u" + U)
import importlib.util
MODS = tuple(m for m in MODS if importlib.util.find_spec(m) is not None)
pages = {}
for mod in MODS:
    try:
        m = importlib.import_module(mod)
        pages.update(m.P)
    except ModuleNotFoundError as e:
        if e.name != mod:
            raise
html = ('<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Farol · Português 6</title>'
        '<link rel="stylesheet" href="farol.css"></head><body>'
        + "".join(pages[k] for k in sorted(pages)) + '</body></html>')
(HERE / f"farol-{TAG}.html").write_text(html, encoding="utf-8")
print("pages:", sorted(pages))

AUDIT = r"""
() => {
  const out = [];
  for (const pg of document.querySelectorAll('.page')) {
    const n = pg.dataset.n, P = pg.getBoundingClientRect();
    const live = pg.querySelector(':scope > .live');
    const L = live ? live.getBoundingClientRect() : P;
    for (const el of pg.querySelectorAll('*')) {
      if (el.closest('.tide') || el.closest('.rh')) continue;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      const box = live && live.contains(el) ? L : P;
      if (r.bottom > box.bottom + 1 || r.right > box.right + 1 || r.left < box.left - 1)
        out.push({n, tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '', txt: (el.textContent||'').trim().slice(0,50), over: Math.round(Math.max(r.bottom-box.bottom, r.right-box.right, box.left-r.left))});
    }
  }
  return out;
}"""

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 900, "height": 1200})
        await pg.goto((HERE / f"farol-{TAG}.html").as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(400)
        issues = await pg.evaluate(AUDIT)
        # keep only the outermost offender per page
        seen = {}
        for i in issues:
            seen.setdefault(i["n"], []).append(i)
        for n, lst in seen.items():
            print(f"OVERFLOW p{n}:", [(x['tag'], x['txt'][:30], x['over']) for x in lst[:4]])
        await pg.pdf(path=str(HERE / f"farol-{TAG}.pdf"), prefer_css_page_size=True, print_background=True)
        await b.close()

asyncio.run(main())

import fitz
doc = fitz.open(HERE / f"farol-{TAG}.pdf")
print("pdf pages:", doc.page_count, "size(mm):", round(doc[0].rect.width/72*25.4), round(doc[0].rect.height/72*25.4))
rd = HERE.parent / ("renders" if U == "1" else f"renders-{TAG}"); rd.mkdir(exist_ok=True)
only = [int(a) for a in sys.argv[1:]]
for i, page in enumerate(doc, 1):
    if only and i not in only: continue
    page.get_pixmap(dpi=110).save(rd / f"p{i:02d}.png")
fonts = set()
for page in doc:
    for f in page.get_fonts(): fonts.add((f[3], f[1]))
print("fonts:", sorted(fonts))
bad = [f for f in fonts if any(x in f[0] for x in ("DejaVu", "Liberation", "Type3")) or f[1] != "ttf"]
if bad:
    print("!! FALLBACK/NON-TRUETYPE FONTS:", bad)
# spreads as a reader sees them: 1 | 2-3 | 4-5 | ... | last
from PIL import Image
imgs = {i: rd / f"p{i:02d}.png" for i in range(1, doc.page_count + 1)}
def sp(a, b=None):
    A = Image.open(imgs[a]); W, H = A.size
    S = Image.new("RGB", (W * 2, H), (70, 70, 70))
    if b is None:
        S.paste(A, (W if a == 1 else 0, 0))
    else:
        S.paste(A, (0, 0)); S.paste(Image.open(imgs[b]), (W, 0))
    return S
if not only:
    n = doc.page_count
    groups = [(1, None)] + [(i, i + 1 if i + 1 < n else None) for i in range(2, n, 2)] + ([(n, None)] if n % 2 == 0 else [])
    for a, b in groups:
        sp(a, b).save(rd / f"spread-{a:02d}.png")
