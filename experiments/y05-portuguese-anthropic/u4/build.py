#!/usr/bin/env python3
"""Build Unit 4 — Texto Dramático (Português · Year 5), pp. 81–96.

u4/src/unit.html (with {{…}} tokens) -> u4/build/unit.html -> u4/build/unit.pdf -> u4/build/png/NN.png
Run with the experiment venv:
    /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--check]
Paths in src/unit.html are relative to build/unit.html: own art = ../art/, shared fonts = ../../fonts/,
shared mascot = ../../art/mou-*.png (read-only).
"""
import json, os, re, subprocess, sys
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "y05-portuguese-anthropic"
SITE = f"https://prime-books-pi.vercel.app/library/{SLUG}/"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")  # light & fast under load
ART, BUILD = os.path.join(HERE, "art"), os.path.join(HERE, "build")
PROFILE = os.path.join(BUILD, "chrome-profile")  # own profile dir: concurrent builds must not collide

QRS = {
    "aviso": SITE + "audio/u4-01-o-aviso.mp3",
    "chave": SITE + "audio/u4-02-a-chave-desaparecida.mp3",
    "frases": SITE + "audio/u4-03-ouve-e-decide.mp3",
    "solucoes": SITE + "solucoes-u4.html",
    "tndm": "https://www.tndm.pt/historia",
}

KEYC = {"bronze": "#B7723A", "prata": "#8E99A6", "ouro": "#D6A21E"}


def key_svg(k):
    c = KEYC[k]
    return (f'<svg class="key" viewBox="0 0 34 16" aria-label="chave {k}"><circle cx="7.5" cy="8" r="5.6" fill="none" stroke="{c}" stroke-width="3"/>'
            f'<path d="M13 8h19M26 8v5M30.5 8v4" stroke="{c}" stroke-width="3" stroke-linecap="round" fill="none"/></svg>')


def qr_svg(url):
    q = segno.make(url, error="m")
    svg = q.svg_inline(scale=1, border=4, dark="#1C2536", light="#ffffff")
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    return svg.replace(m.group(0), f'viewBox="0 0 {m.group(1)} {m.group(2)}" shape-rendering="crispEdges"', 1)


def flat(im):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


# name -> (source png, crop box or None, max width)
JOBS = {
    "opener": ("opener-raw.png", None, 1400),
    "aviso-c1": ("aviso-raw3.png", (0, 0, 1536, 498), 1500),
    "aviso-c2": ("aviso-raw3.png", (0, 512, 1536, 1024), 1500),
    "chave": ("chave-raw.png", None, 1500),
    "stage": ("stage-raw.png", None, 1500),
    "ensaio": ("ensaio-raw.png", None, 1100),
}
SPOTS = ["cast-beatriz", "cast-lucas", "cast-guilhermina", "cast-anselmo", "cast-rosa", "cast-mou-aviso",
         "prop-lupa", "prop-caderno", "prop-tabuleiro", "prop-escadote", "prop-espanador", "prop-cabide",
         "prop-placard", "prop-chavena", "prop-relogio"]


def prep_art():
    for n, (src, box, w) in JOBS.items():
        s, d = os.path.join(ART, src), os.path.join(ART, n + ".jpg")
        if os.path.exists(d) and os.path.getmtime(d) > os.path.getmtime(s) and os.path.getmtime(d) > os.path.getmtime(__file__):
            continue
        im = flat(Image.open(s))
        if box:
            im = im.crop(box)
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(d, quality=86, optimize=True, progressive=True)
    for n in SPOTS:
        s, d = os.path.join(ART, n + ".png"), os.path.join(ART, n + ".jpg")
        if os.path.exists(d) and os.path.getmtime(d) > os.path.getmtime(s):
            continue
        im = flat(Image.open(s))
        if im.width > 700:
            im = im.resize((700, round(im.height * 700 / im.width)), Image.LANCZOS)
        im.save(d, quality=86, optimize=True)


CHECK_JS = r"""
<script>
window.addEventListener('load',()=>{setTimeout(()=>{
 const out=[];const mm=v=>v*96/25.4;
 document.querySelectorAll('.page').forEach((p,i)=>{
  const r=p.getBoundingClientRect();const lim=r.bottom-mm(15);const issues=[];
  p.querySelectorAll('*').forEach(el=>{
    if(el.closest('.folio,.tab,.art,.veil,.foot,.p-open'))return;
    const s=getComputedStyle(el);if(s.position==='absolute'&&!el.classList.contains('tip'))return;
    const b=el.getBoundingClientRect();if(!b.height)return;
    if(b.bottom>lim+0.5&&el.children.length===0)issues.push((el.className||el.tagName)+':'+Math.round((b.bottom-lim)/96*25.4*10)/10+'mm');
    if(b.right>r.right-mm(12)&&el.children.length===0)issues.push('RIGHT '+(el.className||el.tagName));
  });
  p.querySelectorAll('.tip,.pin-bottom').forEach(t=>{
    const tb=t.getBoundingClientRect();
    p.querySelectorAll('.act,.grid2,.box,.gloss,.play,.tint').forEach(a=>{ if(t.contains(a)||a.contains(t))return;
      const ab=a.getBoundingClientRect(); if(ab.bottom>tb.top+1 && ab.top<tb.bottom) issues.push('TIP-OVERLAP '+a.className+' by '+Math.round((ab.bottom-tb.top)/96*25.4*10)/10+'mm');});
  });
  out.push({page:i+1,issues:[...new Set(issues)].slice(0,8)});
 });
 const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);
},400)});
</script>"""


def render_html():
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    html = html.replace("{{QRICON}}", '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>')
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    return html


def chrome_base():
    return [CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw", f"--user-data-dir={PROFILE}"]


def chrome(args, timeout=420, tries=3):
    last = None
    for _ in range(tries):
        try:
            return subprocess.run(chrome_base() + args, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            last = e
            subprocess.run(["pkill", "-f", PROFILE])
    raise last


def build(check=False, dpi=110):
    os.makedirs(BUILD, exist_ok=True)
    prep_art()
    html = render_html()
    out = os.path.join(BUILD, "unit.html")
    if check:
        open(out, "w", encoding="utf-8").write(html.replace("</body>", CHECK_JS + "</body>"))
        r = chrome(["--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + out])
        m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
        rep = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")) if m else r.stderr[-2000:]
        for p in rep if isinstance(rep, list) else [rep]:
            if not isinstance(p, dict) or p["issues"]:
                print(80 + p["page"] if isinstance(p, dict) else "", p["issues"] if isinstance(p, dict) else p)
        print("check done")
    open(out, "w", encoding="utf-8").write(html)
    pdf = os.path.join(BUILD, "unit.pdf")
    chrome(["--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", "file://" + out])
    import pymupdf
    doc = pymupdf.open(pdf)
    pngdir = os.path.join(BUILD, "png")
    os.makedirs(pngdir, exist_ok=True)
    for f in os.listdir(pngdir):
        os.remove(os.path.join(pngdir, f))
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=dpi).save(os.path.join(pngdir, f"{81 + i:02d}.png"))
    fonts = sorted({(f[3], f[1]) for pg in doc for f in pg.get_fonts()})
    print("pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)


if __name__ == "__main__":
    build(check="--check" in sys.argv)
