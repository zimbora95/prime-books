#!/usr/bin/env python3
"""Build Unit 5 — O Comboio das Quatro Estações (Revisões Anuais) · Português · Year 5 · pp. 97–112.

u5/src/unit.html ({{…}} tokens) -> u5/build/unit.html -> u5/build/unit.pdf -> u5/build/png/NN.png
The Unit 1 stylesheet (../src/unit.html) is read — never modified — and inlined so the type system is identical.
Run:  /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--check]
"""
import os, re, subprocess, sys
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLUG = "y05-portuguese-anthropic"
SITE = f"https://prime-books-pi.vercel.app/library/{SLUG}/"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
ART, BUILD = os.path.join(HERE, "art"), os.path.join(HERE, "build")
PROFILE = os.path.join(BUILD, "chrome-profile-u5")
FIRST_FOLIO = 97

QRS = {
    "relato": SITE + "audio/u5-01-relato-linha-do-douro.mp3",
    "ditado": SITE + "audio/u5-02-ditado.mp3",
    "conto": SITE + "audio/u5-03-conto-a-mala-azul.mp3",
    "poema": SITE + "audio/u5-04-poema-comboio-da-noite.mp3",
    "cena": SITE + "audio/u5-05-cena-carruagem-5.mp3",
    "solucoes": SITE + "solucoes-u5.html",
    "pinhao": "https://www.ippatrimonio.pt/pt-pt/estacoes/estacao-do-pinhao",
    "barcelos": "https://www.cm-barcelos.pt/visitar/caminho-portugues-de-santiago/a-lenda-do-galo",
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


def map_svg():
    """The year's route: a railway line through the four stations and the last stops."""
    C = {"verde": "#2F6E5C", "ultra": "#2D4BA8", "ameixa": "#7B3F6E", "turq": "#1C7C89",
         "ocre": "#D9922A", "verm": "#DC4A2E", "tinta": "#1C2536"}
    T = {"verde": "#D7E6DC", "ultra": "#DCE1F3", "ameixa": "#EBDCE5", "turq": "#D3E9EA",
         "ocre": "#F6E3BF", "verm": "#F7D9CE", "tinta": "#E3DED2"}
    W, H = 612, 262
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Figtree">',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="6" fill="#FBF7EF" stroke="#1C2536" stroke-width="2"/>']
    # track: serpentine, left→right on top row, down, right→left bottom row
    top, bot = 78, 196
    xs = [60, 190, 320, 450]
    track = f"M28 {top} H{W-70} C{W-18} {top} {W-18} {bot} {W-70} {bot} H28"
    o.append(f'<path d="{track}" fill="none" stroke="#1C2536" stroke-width="7" stroke-linecap="round"/>')
    o.append(f'<path d="{track}" fill="none" stroke="#FBF7EF" stroke-width="3" stroke-dasharray="7 7"/>')
    stops_top = [
        (xs[0], "verde", "ESTAÇÃO 1", "O Gabinete", "pp. 99–101", "informar e descrever"),
        (xs[1], "ultra", "ESTAÇÃO 2", "A Memória", "pp. 102–104", "texto narrativo"),
        (xs[2], "ameixa", "ESTAÇÃO 3", "A Poesia", "pp. 105–106", "texto poético"),
        (xs[3], "turq", "ESTAÇÃO 4", "O Palco", "pp. 107–108", "texto dramático"),
    ]
    for x, c, lab, name, pp, what in stops_top:
        o.append(f'<circle cx="{x}" cy="{top}" r="13" fill="{C[c]}" stroke="#1C2536" stroke-width="2.4"/>')
        o.append(f'<circle cx="{x}" cy="{top}" r="5" fill="#fff"/>')
        o.append(f'<rect x="{x-52}" y="{top-66}" width="116" height="44" rx="4" fill="{T[c]}" stroke="{C[c]}" stroke-width="1.6"/>')
        o.append(f'<text x="{x-44}" y="{top-51}" font-family="DM Mono" font-weight="500" font-size="8.4" letter-spacing="1.2" fill="{C[c]}">{lab}</text>')
        o.append(f'<text x="{x-44}" y="{top-31}" font-family="Fraunces" font-weight="650" font-size="15" fill="#1C2536">{name}</text>')
        o.append(f'<text x="{x-44}" y="{top+30}" font-size="9.6" fill="#4B5467">{what}</text>')
        o.append(f'<text x="{x-44}" y="{top+43}" font-family="DM Mono" font-size="7.8" letter-spacing=".6" fill="{C[c]}">{pp}</text>')
    stops_bot = [
        (xs[3], "ocre", "OFICINA", "Reparações", "p. 109", "clínica da gramática"),
        (xs[2], "verm", "CARRUAGEM", "A Escuta", "p. 110", "ouvir · ditado"),
        (xs[1], "verm", "DESAFIO", "Bilhete Dourado", "p. 111", "todas as estações"),
        (xs[0], "tinta", "TERMINAL", "Balanço", "p. 112", "o que levo do ano"),
    ]
    for x, c, lab, name, pp, what in stops_bot:
        o.append(f'<rect x="{x-11}" y="{bot-11}" width="22" height="22" rx="3" fill="{C[c]}" stroke="#1C2536" stroke-width="2.4"/>')
        o.append(f'<rect x="{x-52}" y="{bot+22}" width="116" height="30" rx="4" fill="{T[c]}" stroke="{C[c]}" stroke-width="1.4"/>')
        o.append(f'<text x="{x-44}" y="{bot+34}" font-family="DM Mono" font-weight="500" font-size="7.8" letter-spacing="1.1" fill="{C[c]}">{lab} · {pp}</text>')
        o.append(f'<text x="{x-44}" y="{bot+47}" font-family="Fraunces" font-weight="650" font-size="12" fill="#1C2536">{name}</text>')
        o.append(f'<text x="{x-44}" y="{bot-20}" font-size="9.4" fill="#4B5467">{what}</text>')
    # departure
    o.append(f'<path d="M22 {top-16}v32" stroke="#DC4A2E" stroke-width="6"/>')
    o.append(f'<text x="16" y="{top+64}" font-family="DM Mono" font-weight="500" font-size="7.6" letter-spacing="1.1" fill="#DC4A2E">PARTIDA · P. 98</text>')
    # direction arrows on the line
    o.append('<defs><marker id="ar5" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="#DC4A2E"/></marker></defs>')
    for x in (125, 255, 385):
        o.append(f'<line x1="{x-8}" y1="{top}" x2="{x+8}" y2="{top}" stroke="#DC4A2E" stroke-width="2.2" marker-end="url(#ar5)"/>')
    for x in (125, 255, 385):
        o.append(f'<line x1="{x+8}" y1="{bot}" x2="{x-8}" y2="{bot}" stroke="#DC4A2E" stroke-width="2.2" marker-end="url(#ar5)"/>')
    # centre caption
    o.append(f'<text x="{W/2-10}" y="{(top+bot)/2+4}" text-anchor="middle" font-family="Fraunces" font-style="italic" font-size="14" fill="#4B5467">a linha do ano — segue o carril, estação a estação</text>')
    o.append("</svg>")
    return "".join(o)


def u1_css():
    src = open(os.path.join(ROOT, "src", "unit.html"), encoding="utf-8").read()
    css = src.split("<style>", 1)[1].split("/* ---------- per-page vertical tuning", 1)[0]
    return css.replace("url(../fonts/", "url(../../fonts/").replace("url(../art/", "url(../../art/")


def prep_art():
    jpg = {"opener": 1500, "misterio": 1500, "cegonha": 800, "ninho": 800, "revisor": 800, "mala": 700,
           "st-1": 700, "st-2": 700, "st-3": 800, "st-4": 800, "galo": 600}
    for n, w in jpg.items():
        src, dst = os.path.join(ART, n + ".png"), os.path.join(ART, n + ".jpg")
        if not os.path.exists(src):
            continue
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        im = Image.open(src)
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
        im = im.convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=86, optimize=True, progressive=True)
    face = os.path.join(ART, "revisor-face.jpg")
    if not os.path.exists(face) and os.path.exists(os.path.join(ART, "revisor.png")):
        im = Image.open(os.path.join(ART, "revisor.png")).convert("RGB")
        # pad white headroom above the cap so the circular mask does not crowd it
        c = im.crop(FACE_BOX); pad = 36
        sq = Image.new("RGB", (c.width + 2 * pad, c.height + 2 * pad), "white")
        sq.paste(c, (pad, 2 * pad))
        sq = sq.crop((0, 0, c.width + 2 * pad, c.width + 2 * pad))
        sq.resize((600, 600), Image.LANCZOS).save(face, quality=88)


FACE_BOX = (60, 0, 480, 440)

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
  p.querySelectorAll('.tip,[style*="bottom:21mm"]').forEach(t=>{
    const tb=t.getBoundingClientRect();
    p.querySelectorAll('.act,.grid2,.box,.gloss,.txt,.tint').forEach(a=>{ if(t.contains(a)||a.contains(t))return;
      const ab=a.getBoundingClientRect(); if(ab.bottom>tb.top+1 && ab.top<tb.bottom) issues.push('TIP-OVERLAP '+a.className+' by '+Math.round((ab.bottom-tb.top)/96*25.4*10)/10+'mm');});
  });
  out.push({page:i+97,issues:[...new Set(issues)].slice(0,8)});
 });
 const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);
},600)});
</script>"""


def render_html():
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    html = html.replace("{{U1CSS}}", u1_css())
    html = html.replace("{{MAP}}", map_svg())
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    html = html.replace("{{QRICON}}", '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>')
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    return html


def chrome(args, **kw):
    import shutil, tempfile
    os.makedirs(PROFILE, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="run-", dir=PROFILE)  # fresh profile per run, inside u5/
    base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw", "--no-first-run", "--no-default-browser-check",
            ]  # NB: an explicit --user-data-dir makes this Chromium hang with --virtual-time-budget; headless already uses a private temp profile
    try:
        return subprocess.run(base + args, **kw)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def build(check=False):
    import json
    os.makedirs(BUILD, exist_ok=True)
    prep_art()
    html = render_html()
    out = os.path.join(BUILD, "unit.html")
    if check:
        open(out, "w", encoding="utf-8").write(html.replace("</body>", CHECK_JS + "</body>"))
        r = chrome(["--virtual-time-budget=9000", "--window-size=794,1123", "--dump-dom", "file://" + out],
                   capture_output=True, text=True, timeout=480)
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
    chrome(["--no-pdf-header-footer", "--virtual-time-budget=9000", f"--print-to-pdf={pdf}", "file://" + out],
           check=True, capture_output=True, timeout=600)
    import fitz
    doc = fitz.open(pdf)
    pngdir = os.path.join(BUILD, "png")
    os.makedirs(pngdir, exist_ok=True)
    for f in os.listdir(pngdir):
        os.remove(os.path.join(pngdir, f))
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=110).save(os.path.join(pngdir, f"{FIRST_FOLIO + i:03d}.png"))
    fonts = sorted({(f[3], f[1]) for pg in doc for f in pg.get_fonts()})
    print("pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)


if __name__ == "__main__":
    build(check="--check" in sys.argv)
