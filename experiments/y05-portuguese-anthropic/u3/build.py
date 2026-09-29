#!/usr/bin/env python3
"""Build Unit 3 — O Coreto das Palavras (Português · 5.º Ano, pp. 65–80).

src/base.css (Unit 1 type/colour system) + src/unit.html ({{…}} tokens)
  -> build/unit.html -> build/unit.pdf -> build/png/NN.png (NN = book folio 65..80)
Run with the experiment venv:
    /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--check] [--sheets]
"""
import json, os, re, subprocess, sys
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "y05-portuguese-anthropic"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
ART, BUILD = os.path.join(HERE, "art"), os.path.join(HERE, "build")
PROFILE = os.path.join(BUILD, "chrome-profile-u3")   # own profile dir: concurrent unit builds never collide
FIRST_FOLIO = 65

# Only stable public resources (no self-recorded audio, no temporary site). Verified HTTP 200, 2026-09-28.
QRS = {
    "fonico": "https://ensina.rtp.pt/explicador/recursos-expressivos-a-nivel-fonico/",       # p. 70 · rima (Pessoa, AABB)
    "aula58": "https://www.rtp.pt/play/estudoemcasa/p7800/e549488/portugues-5-e-6-anos",     # p. 71 · a sílaba métrica
    "semantico": "https://ensina.rtp.pt/explicador/recursos-expressivos-a-nivel-semantico-11/",  # p. 72 · personificação
}

# "say it aloud" icon: a speech bubble with sound arcs on the page accent (replaces the old audio QRs)
SAYICON = ('<svg class="si" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" style="fill:var(--c)"/>'
           '<path d="M6 8.5h8.5a1.5 1.5 0 0 1 1.5 1.5v4a1.5 1.5 0 0 1-1.5 1.5H10l-3 2.4V15.5H6a1.5 1.5 0 0 1-1.5-1.5v-4A1.5 1.5 0 0 1 6 8.5z" fill="#fff"/>'
           '<path d="M18.2 9.6q1.5 2.4 0 4.8M20.3 8.2q2.4 3.8 0 7.6" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/></svg>')

KEYC = {"bronze": "#B7723A", "prata": "#8E99A6", "ouro": "#D6A21E"}

# art: name -> max width in px for the web-weight JPEG used by the page
JPG = {"opener": 1500, "telhado": 1700, "desk": 900, "vento": 900, "chuva": 900, "livro": 900,
       "duo": 800, "recital": 900, "livrinhos": 900, "micro": 800}


def key_svg(k):
    c = KEYC[k]
    return (f'<svg class="key" viewBox="0 0 34 16" aria-label="chave {k}"><circle cx="7.5" cy="8" r="5.6" fill="none" stroke="{c}" stroke-width="3"/>'
            f'<path d="M13 8h19M26 8v5M30.5 8v4" stroke="{c}" stroke-width="3" stroke-linecap="round" fill="none"/></svg>')


def qr_svg(url):
    q = segno.make(url, error="m")
    svg = q.svg_inline(scale=1, border=4, dark="#1C2536", light="#ffffff")
    m = re.search(r'width="(\d+)" height="(\d+)"', svg)
    return svg.replace(m.group(0), f'viewBox="0 0 {m.group(1)} {m.group(2)}" shape-rendering="crispEdges"', 1)


def prep_art():
    for n, w in JPG.items():
        src, dst = os.path.join(ART, n + ".png"), os.path.join(ART, n + ".jpg")
        if not os.path.exists(src):
            continue
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=86, optimize=True, progressive=True)


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
    if(el.scrollWidth>el.clientWidth+2&&s.overflow!=='visible'&&el.clientWidth>0&&!el.closest('svg'))issues.push('CLIP '+(el.className||el.tagName));
  });
  p.querySelectorAll('.tip,[style*="bottom:21mm"]').forEach(t=>{
    const tb=t.getBoundingClientRect();
    p.querySelectorAll('.act,.grid2,.box,.gloss,.poem-card,.duas').forEach(a=>{ if(t.contains(a)||a.contains(t))return;
      const ab=a.getBoundingClientRect(); if(ab.bottom>tb.top+1 && ab.top<tb.bottom) issues.push('TIP-OVERLAP '+a.className+' by '+Math.round((ab.bottom-tb.top)/96*25.4*10)/10+'mm');});
  });
  out.push({page:i+%d,issues:[...new Set(issues)].slice(0,8)});
 });
 const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);
},400)});
</script>""" % FIRST_FOLIO


def chrome(args, **kw):
    # a fresh throw-away profile per call (inside u3/build): a killed run can never leave a lock behind
    import shutil, tempfile
    os.makedirs(BUILD, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="chrome-u3-", dir=BUILD)
    base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw", f"--user-data-dir={prof}"]
    try:
        for attempt in range(4):          # the shared host is heavily loaded; headless Chrome sometimes stalls
            try:
                return subprocess.run(base + args, **{**kw, "timeout": 240})
            except subprocess.TimeoutExpired:
                print("chrome stalled, retry", attempt + 1, file=sys.stderr)
        raise RuntimeError("chrome stalled 4 times")
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def render_html():
    css = open(os.path.join(HERE, "src", "base.css"), encoding="utf-8").read()
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    html = html.replace("{{BASECSS}}", css)
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    html = html.replace("{{QRICON}}", '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>')
    html = html.replace("{{SAYICON}}", SAYICON)
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    return html


def sheets(png_dir, out_dir, per=6):
    files = sorted(f for f in os.listdir(png_dir) if f.endswith(".png"))
    for s in range(0, len(files), per):
        ims = [Image.open(os.path.join(png_dir, f)).convert("RGB") for f in files[s:s + per]]
        w, h = ims[0].size
        sheet = Image.new("RGB", (w * 3 + 40, h * 2 + 30), (120, 116, 106))
        for i, im in enumerate(ims):
            sheet.paste(im, (10 + (i % 3) * (w + 10), 10 + (i // 3) * (h + 10)))
        sheet.save(os.path.join(out_dir, f"sheet{s // per + 1}.jpg"), quality=82)


def build(check=False, make_sheets=False):
    os.makedirs(BUILD, exist_ok=True)
    prep_art()
    html = render_html()
    out = os.path.join(BUILD, "unit.html")
    if check:
        open(out, "w", encoding="utf-8").write(html.replace("</body>", CHECK_JS + "</body>"))
        r = chrome(["--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + out],
                   capture_output=True, text=True, timeout=1500)
        m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
        rep = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")) if m else r.stderr[-2000:]
        for p in rep if isinstance(rep, list) else []:
            if p["issues"]:
                print(p["page"], p["issues"])
        if not isinstance(rep, list):
            print(rep)
        print("check done")
    open(out, "w", encoding="utf-8").write(html)
    pdf = os.path.join(BUILD, "unit.pdf")
    chrome(["--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", "file://" + out],
           check=True, capture_output=True, timeout=1500)
    import fitz
    doc = fitz.open(pdf)
    png = os.path.join(BUILD, "png")
    os.makedirs(png, exist_ok=True)
    for f in os.listdir(png):
        os.remove(os.path.join(png, f))
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=110).save(os.path.join(png, f"{i + FIRST_FOLIO:02d}.png"))
    fonts = sorted({(f[3], f[1]) for pg in doc for f in pg.get_fonts()})
    print("pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)
    if make_sheets:
        sheets(png, BUILD)


if __name__ == "__main__":
    build(check="--check" in sys.argv, make_sheets="--sheets" in sys.argv)
