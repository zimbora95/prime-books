#!/usr/bin/env python3
"""Build Unit 2 — Lugar, Tempo e Memória (Português · Year 5), pp. 25–64.

src/head.html + src/pages-*.html (with {{…}} tokens) -> build/unit.html -> build/unit.pdf -> build/png/NN.png
Run with the experiment venv:
    /root/.hermes/cache/scratch/exp-venv/bin/python build.py [--check] [--nopng]
Everything lives inside u2/; shared fonts and the Mourinha art are read from ../fonts and ../art.
"""
import glob, json, os, re, subprocess, sys
import numpy as np
from PIL import Image
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "y05-portuguese-anthropic"
SITE = f"https://prime-books-pi.vercel.app/library/{SLUG}/"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell")  # light & fast under load
ART, BUILD = os.path.join(HERE, "art"), os.path.join(HERE, "build")
PROFILE = os.path.join(BUILD, "chrome-profile")  # private profile: no collisions with u3/u4 builds
FIRST_FOLIO = 25

QRS = {
    "galo": SITE + "audio/u2-01-lenda-galo-barcelos.mp3",
    "sintra": SITE + "audio/u2-02-relato-viagem-sintra.mp3",
    "aristides": SITE + "audio/u2-03-biografia-aristides.mp3",
    "pardais": SITE + "audio/u2-04-os-pardais-da-horta.mp3",
    "misterio": SITE + "audio/u2-05-o-misterio-das-coisas-de-la.mp3",
    "eletrico": SITE + "audio/u2-06-no-eletrico-28.mp3",
    "solucoes": SITE + "solucoes-u2.html",
    "panteao": "https://www.dge.mec.pt/noticias/honras-de-panteao-nacional-aristides-de-sousa-mendes",
    "cplp": "https://www.cplp.org/estados-membros",
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


# ---------------------------------------------------------------- art
def gutters(a, axis):
    """Return the index ranges of near-white gutter bands along an axis (0 = rows, 1 = cols)."""
    g = a.mean(axis=2)
    prof_mean = g.mean(axis=1 - axis)
    prof_min = g.min(axis=1 - axis)
    white = (prof_mean > 246) & (prof_min > 200)
    bands, start = [], None
    for i, w in enumerate(white):
        if w and start is None:
            start = i
        if not w and start is not None:
            bands.append((start, i)); start = None
    if start is not None:
        bands.append((start, len(white)))
    return bands


def split_grid(src, n=2):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(float)
    H, W = a.shape[:2]
    def cuts(axis, size):
        bands = [b for b in gutters(a, axis) if 0.25 * size < (b[0] + b[1]) / 2 < 0.75 * size]
        if bands:
            b = max(bands, key=lambda b: b[1] - b[0])
            return [(0, b[0]), (b[1], size)]
        return [(0, size // 2), (size // 2, size)]
    rows, cols = cuts(0, H), cuts(1, W)
    out = []
    for r0, r1 in rows:
        for c0, c1 in cols:
            p = im.crop((c0, r0, c1, r1))
            # trim outer white margin
            pa = np.asarray(p).astype(float).mean(axis=2)
            ys = np.where(pa.min(axis=1) < 235)[0]; xs = np.where(pa.min(axis=0) < 235)[0]
            if len(ys) and len(xs):
                p = p.crop((xs[0], ys[0], xs[-1] + 1, ys[-1] + 1))
            out.append(p)
    return out


def prep_art():
    grids = {"galo-grid": "galo", "sintra-grid": "sintra"}
    for g, stem in grids.items():
        src = os.path.join(ART, g + ".png")
        first = os.path.join(ART, f"{stem}-1.jpg")
        if os.path.exists(first) and os.path.getmtime(first) > os.path.getmtime(src):
            continue
        for i, p in enumerate(split_grid(src), 1):
            p.save(os.path.join(ART, f"{stem}-{i}.jpg"), quality=88, optimize=True, progressive=True)
    for src in glob.glob(os.path.join(ART, "*.png")):
        n = os.path.basename(src)[:-4]
        if n.endswith("-grid"):
            continue
        dst = os.path.join(ART, n + ".jpg")
        if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src):
            continue
        im = Image.open(src).convert("RGB")
        w = 1700 if n == "opener" else 1400
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, quality=86, optimize=True, progressive=True)


# ---------------------------------------------------------------- vector art
def line_svg():
    """'A Linha da Memória': the unit plan drawn as a railway line with nine stations."""
    C = {"verm": "#DC4A2E", "turq": "#1C7C89", "ameixa": "#7B3F6E", "ultra": "#2D4BA8", "verde": "#2F6E5C",
         "ocre": "#D9922A", "tinta": "#1C2536"}
    st = [  # colour, number, name (| = line break), pages, what
        ("verm", "2.1", "A Lenda|do Galo", "pp. 28–31", "perfeito e imperfeito"),
        ("turq", "2.2", "Relato de|uma Viagem", "pp. 32–35", "conectores de tempo"),
        ("ameixa", "2.3", "Uma|Biografia", "pp. 36–39", "biografia e autobiografia"),
        ("ultra", "2.4", "Literaturas de|Língua Portuguesa", "pp. 40–43", "sinónimos e antónimos"),
        ("verde", "2.5", "O Rapaz|de Bronze", "pp. 44–47", "personificação"),
        ("ocre", "2.6", "Ynari, a Menina|das Cinco Tranças", "pp. 48–51", "família de palavras"),
        ("verm", "2.7", "Um Problema|para Resolver", "pp. 52–55", "nome · adjetivo · verbo"),
        ("tinta", "2.8", "Conto de|Mistério", "pp. 56–59", "tempos verbais e pistas"),
        ("turq", "2.9", "História Contada|com Falas", "pp. 60–63", "discurso direto"),
    ]
    W, H = 640, 330
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Figtree">',
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7" fill="#FBF7EF" stroke="#1C2536" stroke-width="1.6"/>']
    xs = [102, 316, 506]
    ys = [80, 184, 288]
    pts = []
    for r in range(3):
        cols = xs if r % 2 == 0 else xs[::-1]
        pts += [(c, ys[r]) for c in cols]
    bx = 614  # right bend
    lx = 28   # left bend
    d = (f"M{lx} {ys[0]} L{xs[2]} {ys[0]} C{bx} {ys[0]} {bx} {ys[1]} {xs[2]} {ys[1]} "
         f"L{xs[0]} {ys[1]} C{lx} {ys[1]} {lx} {ys[2]} {xs[0]} {ys[2]} L{bx} {ys[2]}")
    out.append(f'<path d="{d}" fill="none" stroke="#1C2536" stroke-width="7" stroke-linecap="round"/>')
    out.append(f'<path d="{d}" fill="none" stroke="#FBF7EF" stroke-width="3" stroke-dasharray="7 7"/>')
    for (x, y), (c, n, name, pages, what) in zip(pts, st):
        col = C[c]
        l1, l2 = name.split("|")
        out.append(f'<text x="{x}" y="{y-48}" text-anchor="middle" font-family="Fraunces" font-weight="650" font-size="13" fill="#1C2536">{l1}</text>')
        out.append(f'<text x="{x}" y="{y-34}" text-anchor="middle" font-family="Fraunces" font-weight="650" font-size="13" fill="#1C2536">{l2}</text>')
        out.append(f'<text x="{x}" y="{y-21}" text-anchor="middle" font-size="8.8" fill="#4B5467">{what}</text>')
        out.append(f'<circle cx="{x}" cy="{y}" r="13" fill="#fff" stroke="{col}" stroke-width="4.5"/>')
        out.append(f'<text x="{x}" y="{y+3.6}" text-anchor="middle" font-family="DM Mono" font-weight="500" font-size="9.5" fill="{col}">{n}</text>')
        out.append(f'<text x="{x}" y="{y+27}" text-anchor="middle" font-family="DM Mono" font-weight="500" font-size="8" fill="{col}" letter-spacing=".6">{pages}</text>')
    out.append(f'<rect x="{lx-9}" y="{ys[0]-10}" width="18" height="20" rx="3" fill="#2F6E5C"/>')
    out.append(f'<text x="{lx-9}" y="{ys[0]+27}" font-family="DM Mono" font-size="7.4" fill="#2F6E5C" letter-spacing=".8">PARTIDA</text>')
    out.append(f'<text x="{lx-9}" y="{ys[0]+37}" font-family="DM Mono" font-size="7.4" fill="#2F6E5C" letter-spacing=".8">p. 27</text>')
    out.append(f'<rect x="{bx-9}" y="{ys[2]-10}" width="18" height="20" rx="3" fill="#2F6E5C"/>')
    out.append(f'<text x="{bx+9}" y="{ys[2]+27}" text-anchor="end" font-family="DM Mono" font-size="7.4" fill="#2F6E5C" letter-spacing=".8">CHEGADA</text>')
    out.append(f'<text x="{bx+9}" y="{ys[2]+37}" text-anchor="end" font-family="DM Mono" font-size="7.4" fill="#2F6E5C" letter-spacing=".8">p. 64</text>')
    out.append("</svg>")
    return "".join(out)


def map_svg():
    """The nine CPLP member states on an equirectangular world map (Natural-Earth-derived outline)."""
    geo = json.load(open(os.path.join(HERE, "data", "countries.geo.json")))
    C = {"PRT": "#DC4A2E", "BRA": "#2F6E5C", "AGO": "#D9922A", "MOZ": "#7B3F6E", "GNB": "#1C7C89",
         "GNQ": "#2D4BA8", "TLS": "#B7723A", "CPV": "#1C7C89", "STP": "#2D4BA8"}
    lon0, lon1, lat0, lat1 = -95, 150, -42, 58
    W = 700; k = W / (lon1 - lon0); H = (lat1 - lat0) * k
    P = lambda lon, lat: ((lon - lon0) * k, (lat1 - lat) * k)
    out = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" font-family="Figtree">',
           f'<rect width="{W:.0f}" height="{H:.0f}" fill="#DCE6EC"/>']
    # graticule
    for lat in range(-40, 60, 20):
        y = P(0, lat)[1]; out.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="#C3D2DB" stroke-width=".6"/>')
    for lon in range(-80, 150, 20):
        x = P(lon, 0)[0]; out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H:.0f}" stroke="#C3D2DB" stroke-width=".6"/>')
    ey = P(0, 0)[1]
    out.append(f'<line x1="0" y1="{ey:.1f}" x2="{W}" y2="{ey:.1f}" stroke="#A9BCC8" stroke-width=".9" stroke-dasharray="4 3"/>')
    for f in geo["features"]:
        g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        fill = C.get(f["id"], "#EFE6D4")
        d = []
        for poly in polys:
            for ring in poly[:1]:
                pts = [P(x, y) for x, y in ring if lon0 - 20 < x < lon1 + 20]
                if len(pts) > 2:
                    d.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        if d:
            out.append(f'<path d="{" ".join(d)}" fill="{fill}" stroke="{"#FBF7EF" if f["id"] in C else "#D2C6AE"}" stroke-width="{.9 if f["id"] in C else .5}"/>')
    # island states and small countries: rings so they can be seen
    for code, lon, lat in [("CPV", -23.9, 15.6), ("STP", 6.9, 0.7), ("GNQ", 10.3, 1.6), ("GNB", -15.0, 12.0), ("TLS", 125.8, -8.8)]:
        x, y = P(lon, lat)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 if code in ("CPV","STP") else 8}" fill="{C[code] if code in ("CPV","STP") else "none"}" fill-opacity="{.9 if code in ("CPV","STP") else 0}" stroke="{C[code]}" stroke-width="1.6"/>')
    # numbered markers (legend in HTML)
    labels = [("1", "PRT", -8.0, 39.6, -30, -22), ("2", "BRA", -52, -10, 0, 0), ("3", "CPV", -23.9, 15.6, -26, -8),
              ("4", "GNB", -15.0, 12.0, -22, 20), ("5", "STP", 6.9, 0.7, -24, 16), ("6", "GNQ", 10.3, 1.6, 20, -16),
              ("7", "AGO", 17.5, -12.3, 0, 0), ("8", "MOZ", 35.5, -17.5, 22, 4), ("9", "TLS", 125.8, -8.8, 0, -22)]
    for n, code, lon, lat, dx, dy in labels:
        x, y = P(lon, lat)
        if dx or dy:
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" stroke="#1C2536" stroke-width=".9"/>')
        out.append(f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="8.6" fill="#1C2536" stroke="#fff" stroke-width="1.4"/>')
        out.append(f'<text x="{x+dx:.1f}" y="{y+dy+3.4:.1f}" text-anchor="middle" font-family="Fraunces" font-weight="700" font-size="10" fill="#fff">{n}</text>')
    # compass / ocean names in small italic
    for name, lon, lat in [("Oceano Atlântico", -38, 22), ("Oceano Índico", 72, -22), ("Oceano Pacífico", 127, 30)]:
        x, y = P(lon, lat)
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-family="Fraunces" font-style="italic" font-size="11" fill="#6F8796">{name}</text>')
    out.append(f'<rect x=".5" y=".5" width="{W-1:.0f}" height="{H-1:.0f}" fill="none" stroke="#1C2536" stroke-width="1.2"/>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- check script (same probe as Unit 1)
CHECK_JS = open(os.path.join(HERE, "check.js"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "check.js")) else ""


def assemble():
    rd = lambda n: open(os.path.join(HERE, "src", n), encoding="utf-8").read()
    head = rd("base.css.html") + rd("u2.css.html") + "\n</style>\n</head>\n<body>\n"
    parts = [open(p, encoding="utf-8").read() for p in sorted(glob.glob(os.path.join(HERE, "src", "pages-*.html")))]
    html = head + "\n".join(parts) + "\n</body>\n</html>\n"
    # folios: number pages in order, odd/even classes
    chunks = re.split(r'(?=<section class="page )', html)
    n = [FIRST_FOLIO - 1]
    for i, ch in enumerate(chunks):
        if not ch.startswith('<section class="page '):
            continue
        n[0] += 1
        side = "odd" if n[0] % 2 else "even"
        ch = ch.replace('<section class="page ', f'<section class="page {side} pg{n[0]} ', 1)
        chunks[i] = ch.replace("{{N}}", str(n[0]))
    html = "".join(chunks)
    # auto-number activities in reading order (the source numbers are placeholders)
    k = [0]
    def num(m):
        k[0] += 1
        return f'<span class="num">{k[0]}</span>'
    html = re.sub(r'<span class="num">\d+</span>', num, html)  # auto-number
    html = html.replace("{{LINE}}", line_svg()).replace("{{MAP}}", map_svg())
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    html = html.replace("{{QRICON}}", '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>')
    for k, u in QRS.items():
        html = html.replace("{{QR:%s}}" % k, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {sorted(set(left))}")
    return html, n[0] - FIRST_FOLIO + 1


def build(check=False, png=True):
    os.makedirs(BUILD, exist_ok=True)
    prep_art()
    html, pages = assemble()
    out = os.path.join(BUILD, "unit.html")
    open(out, "w", encoding="utf-8").write(html)
    base = [CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--run-all-compositor-stages-before-draw"]
    pdf = os.path.join(BUILD, "unit.pdf")
    subprocess.run(base + ["--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={pdf}", "file://" + out],
                   check=True, capture_output=True, timeout=300)
    import fitz
    doc = fitz.open(pdf)
    if png:
        pdir = os.path.join(BUILD, "png")
        os.makedirs(pdir, exist_ok=True)
        for f in glob.glob(os.path.join(pdir, "*.png")):
            os.remove(f)
        for i, pg in enumerate(doc):
            pg.get_pixmap(dpi=110).save(os.path.join(pdir, f"{i + FIRST_FOLIO:02d}.png"))
    fonts = sorted({(f[3], f[1]) for pg in doc for f in pg.get_fonts()})
    print("sections", pages, "pdf pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)


if __name__ == "__main__":
    build(check="--check" in sys.argv, png="--nopng" not in sys.argv)
