#!/usr/bin/env python3
"""Build Unit 1 — O Gabinete das Coisas Verdadeiras (Português · Year 5).

src/unit.html (with {{…}} tokens) -> build/unit.html -> build/unit.pdf -> build/png/NN.png
Run with the experiment venv (segno, pillow, pymupdf):
    /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--check]
"""
import json, os, re, subprocess, sys
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "y05-portuguese-anthropic"
SITE = f"https://prime-books-pi.vercel.app/library/{SLUG}/"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
ART, BUILD = os.path.join(HERE, "art"), os.path.join(HERE, "build")

QRS = {
    "artigo": SITE + "audio/01-artigo-osga.mp3",
    "fo": SITE + "audio/02-facto-ou-opiniao.mp3",
    "retratos": SITE + "audio/03-retratos.mp3",
    "leonor": SITE + "audio/04-visita-guiada-leonor.mp3",
    "solucoes": SITE + "solucoes.html",
    "museu": "https://museubiodiversidade.uevora.pt/elenco-de-especies/biodiversidade-actual/animais/cordados/repteis/tarentola-mauritanica/",
    "priberam": "https://dicionario.priberam.org/lamela",
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


def plan_svg():
    # museum floor plan = the unit map; path order Átrio→S1→S2→S3→S4→S5→Oficina→Saída
    C = {"ocre": "#D9922A", "verde": "#2F6E5C", "ultra": "#2D4BA8", "ameixa": "#7B3F6E", "verm": "#DC4A2E", "turq": "#1C7C89", "tinta": "#1C2536"}
    T = {"ocre": "#F6E3BF", "verde": "#D7E6DC", "ultra": "#DCE1F3", "ameixa": "#EBDCE5", "verm": "#F7D9CE", "turq": "#D3E9EA", "tinta": "#E3DED2"}
    W, H, gx, gy = 196, 90, 8, 8
    x0, y0 = 6, 6
    rooms = [  # col,row,colour,label,name,pages,what
        (0, 1, "ocre", "ÁTRIO", "Ler antes de ler", "p. 3", "prever pelo título e pelas imagens"),
        (0, 0, "verde", "SALA 1", "A Enciclopédia", "pp. 4–7", "artigo · facto e opinião"),
        (1, 0, "ultra", "SALA 2", "O Dicionário", "pp. 8–11", "verbete · nome coletivo"),
        (2, 0, "ameixa", "SALA 3", "Os Retratos", "pp. 12–16", "retrato · graus do adjetivo"),
        (2, 1, "verm", "SALA 4", "Os Avisos", "pp. 17–19", "aviso · modo imperativo"),
        (2, 2, "turq", "SALA 5", "A Visita Guiada", "pp. 20–21", "exposição oral"),
        (1, 2, "tinta", "OFICINA", "A Minha Vitrine", "pp. 22–23", "o projeto final"),
        (0, 2, "tinta", "SAÍDA", "O que levo daqui", "p. 24", "balanço"),
    ]
    out = [f'<svg viewBox="0 0 {x0*2+3*W+2*gx} {y0*2+3*H+2*gy}" xmlns="http://www.w3.org/2000/svg" font-family="Figtree">']
    tw, th = x0 * 2 + 3 * W + 2 * gx, y0 * 2 + 3 * H + 2 * gy
    out.append(f'<rect x="1" y="1" width="{tw-2}" height="{th-2}" rx="6" fill="#FBF7EF" stroke="#1C2536" stroke-width="2"/>')
    centres = []
    for col, row, c, lab, name, pages, what in rooms:
        x, y = x0 + col * (W + gx), y0 + row * (H + gy)
        centres.append((x + W / 2, y + H / 2))
        out.append(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="4" fill="{T[c]}" stroke="{C[c]}" stroke-width="2.4"/>')
        out.append(f'<text x="{x+12}" y="{y+24}" font-family="DM Mono" font-weight="500" font-size="10" letter-spacing="1.6" fill="{C[c]}">{lab}</text>')
        out.append(f'<text x="{x+W-12}" y="{y+24}" text-anchor="end" font-family="DM Mono" font-size="10" fill="#4B5467">{pages}</text>')
        out.append(f'<text x="{x+12}" y="{y+54}" font-family="Fraunces" font-weight="650" font-size="19" fill="#1C2536">{name}</text>')
        out.append(f'<text x="{x+12}" y="{y+74}" font-size="11.5" fill="#4B5467">{what}</text>')
    # corridor (centre cell)
    cx, cy = x0 + (W + gx), y0 + (H + gy)
    out.append(f'<rect x="{cx}" y="{cy}" width="{W}" height="{H}" rx="4" fill="none" stroke="#B9AE98" stroke-width="1.2" stroke-dasharray="3 3"/>')
    out.append(f'<text x="{cx+W/2}" y="{cy+40}" text-anchor="middle" font-family="Fraunces" font-style="italic" font-size="15" fill="#4B5467">corredor da Mourinha</text>')
    out.append(f'<text x="{cx+W/2}" y="{cy+62}" text-anchor="middle" font-size="10.5" fill="#4B5467">segue as setas: é este o teu percurso</text>')
    # entrance door
    ex, ey = x0, y0 + (H + gy) + H / 2
    out.append(f'<path d="M{ex-5} {ey-14}v28" stroke="#DC4A2E" stroke-width="5"/>')
    # path arrows between consecutive rooms, drawn along the gutters
    pts = centres
    d = "M" + " L".join(f"{px:.1f} {py+22:.1f}" if i == 0 else f"{px:.1f} {py+22:.1f}" for i, (px, py) in enumerate(pts))
    out.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 10 5 0 10z" fill="#DC4A2E"/></marker></defs>')
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        # connectors live on the room edges
        if ax == bx:  # vertical
            y1 = ay + (H / 2 if by > ay else -H / 2) - (0 if by > ay else 0)
            y2 = by - (H / 2 if by > ay else -H / 2)
            out.append(f'<line x1="{ax+W/2-26}" y1="{y1-6 if by>ay else y1+6}" x2="{ax+W/2-26}" y2="{y2+6 if by>ay else y2-6}" stroke="#DC4A2E" stroke-width="2.4" marker-end="url(#ar)"/>')
        else:
            x1 = ax + (W / 2 if bx > ax else -W / 2)
            x2 = bx - (W / 2 if bx > ax else -W / 2)
            yy = ay + H / 2 - 12
            out.append(f'<line x1="{x1-6 if bx>ax else x1+6}" y1="{yy}" x2="{x2+6 if bx>ax else x2-6}" y2="{yy}" stroke="#DC4A2E" stroke-width="2.4" marker-end="url(#ar)"/>')
    out.append("</svg>")
    return "".join(out)


def prep_art():
    jpg = {"opener": 1600, "osga-plate": 1600, "guilhermina": 1100, "sotao": 1700, "animais": 1700,
           "visita": 1700, "vitrine": 900, "dicionario": 900}
    for n, w in jpg.items():
        src, dst = os.path.join(ART, n + ".png"), os.path.join(ART, n + ".jpg")
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=86, optimize=True, progressive=True)
    face = os.path.join(ART, "guilhermina-face.jpg")
    if not os.path.exists(face):
        im = Image.open(os.path.join(ART, "guilhermina.png")).convert("RGB")
        im.crop(FACE_BOX).resize((600, 600), Image.LANCZOS).save(face, quality=88)


FACE_BOX = (232, 90, 792, 650)

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
  // collisions: absolute tips vs flow content
  p.querySelectorAll('.tip,[style*="bottom:21mm"]').forEach(t=>{
    const tb=t.getBoundingClientRect();
    p.querySelectorAll('.act,.grid2,.box,.gloss').forEach(a=>{ if(t.contains(a)||a.contains(t))return;
      const ab=a.getBoundingClientRect(); if(ab.bottom>tb.top+1 && ab.top<tb.bottom) issues.push('TIP-OVERLAP '+a.className+' by '+Math.round((ab.bottom-tb.top)/96*25.4*10)/10+'mm');});
  });
  out.push({page:i+1,issues:[...new Set(issues)].slice(0,8)});
 });
 const pre=document.createElement('pre');pre.id='report';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);
},400)});
</script>"""


def build(check=False):
    os.makedirs(BUILD, exist_ok=True)
    prep_art()
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    html = html.replace("{{PLAN}}", plan_svg())
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    html = html.replace("{{QRICON}}", '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>')
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    out = os.path.join(BUILD, "unit.html")
    open(out, "w", encoding="utf-8").write(html.replace("</body>", CHECK_JS + "</body>") if check else html)
    base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--run-all-compositor-stages-before-draw"]
    if check:
        r = subprocess.run(base + ["--virtual-time-budget=8000", "--window-size=794,1123", "--dump-dom", "file://" + out], capture_output=True, text=True, timeout=180)
        m = re.search(r'<pre id="report">(.*?)</pre>', r.stdout, re.S)
        rep = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")) if m else r.stderr[-2000:]
        for p in rep if isinstance(rep, list) else []:
            if p["issues"]:
                print(p["page"], p["issues"])
        print("check done")
        open(out, "w", encoding="utf-8").write(html)
    pdf = os.path.join(BUILD, "unit.pdf")
    subprocess.run(base + ["--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", "file://" + out], check=True, capture_output=True, timeout=240)
    import fitz
    doc = fitz.open(pdf)
    os.makedirs(os.path.join(BUILD, "png"), exist_ok=True)
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=110).save(os.path.join(BUILD, "png", f"{i+1:02d}.png"))
    fonts = sorted({f[3] for pg in doc for f in pg.get_fonts()})
    print("pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)


if __name__ == "__main__":
    build(check="--check" in sys.argv)
