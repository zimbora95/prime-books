#!/usr/bin/env python3
"""Build Unit 7 — Atividades Extra (Português · 5.º Ano), pp. 129–144.

src/unit.html + src/base.css (Unit 1 type system) with {{…}} tokens
  -> build/unit.html -> build/unit.pdf -> build/png/NN.png   (NN = 01..16 = pp. 129..144)
Run with the experiment venv:
    /root/.hermes/cache/scratch/exp-venv/bin/python build.py
"""
import html as H, json, math, os, re, subprocess, sys
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_prep, puzzles  # noqa: E402

SLUG = "y05-portuguese-anthropic"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
BUILD = os.path.join(HERE, "build")
PROFILE = os.path.join(BUILD, "chrome-profile")  # own profile dir: no clash with the other units' builds
FIRST_FOLIO = 129

# Only stable public resources (no self-recorded tracks, no temporary-site links). Verified 28 Sep 2026.
QRS = {
    "trava": "https://ensina.rtp.pt/artigo/o-rato-roeu-a-rolha/",            # p. 138 · RTP Ensina video
    "adivinhas": "https://ensina.rtp.pt/artigo/adivinhas-que-animal-sou-eu/",  # p. 144 · RTP Ensina video
    "caligrama": "https://pt.wikipedia.org/wiki/Caligrama",                    # p. 144 · Wikipédia (pt)
    "priberam": "https://dicionario.priberam.org/",                            # p. 132
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


# ------------------------------------------------------------------ small SVG helpers
ICONS = {
    "ler": '<path d="M3 6c4-2 7-2 9 0v13c-2-2-5-2-9 0zM21 6c-4-2-7-2-9 0v13c2-2 5-2 9 0z"/>',
    "escrever": '<path d="M5 19l1-4L16 5l3 3L9 18zM14 7l3 3"/>',
    "falar": '<path d="M4 5h16v10H11l-5 4v-4H4z"/>',
    "gramatica": '<path d="M4 4h7v4a2 2 0 1 0 0 4v4H4zM13 4h7v7h-4a2 2 0 1 0-4 0z" />',
    "jogar": '<rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="9" cy="9" r="1.3" fill="currentColor"/><circle cx="15" cy="15" r="1.3" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/>',
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">{ICONS[name]}</svg>'


def pips(n):
    P = {1: [(12, 12)], 2: [(7, 7), (17, 17)], 3: [(6, 6), (12, 12), (18, 18)], 4: [(7, 7), (17, 7), (7, 17), (17, 17)],
         5: [(6, 6), (18, 6), (12, 12), (6, 18), (18, 18)], 6: [(7, 6), (17, 6), (7, 12), (17, 12), (7, 18), (17, 18)]}[n]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.3"/>' for x, y in P)
    return f'<svg class="pip" viewBox="0 0 24 24"><rect x="1" y="1" width="22" height="22" rx="5" fill="#fff" stroke="currentColor" stroke-width="1.6"/><g fill="currentColor">{dots}</g></svg>'


SCISSORS = ('<svg class="scis" viewBox="0 0 24 24" fill="none" stroke="#6D6A63" stroke-width="1.6"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>'
            '<path d="M8.5 7.8 20 17M8.5 16.2 20 7"/></svg>')


def balloon(kind):
    """Speech / thought balloons (empty, for the pupil). kind = say-bl | say-br | think-bl | think-br."""
    k, t = kind.split("-")
    st = 'fill="#fff" stroke="#1C2536" stroke-width="1.5" stroke-linejoin="round"'
    if k == "say":
        if t == "bl":
            d = "M50 3 C78 3 97 13 97 27 C97 41 80 50 50 51 L30 64 L37 49 C17 45 3 37 3 27 C3 13 22 3 50 3Z"
        else:
            d = "M50 3 C22 3 3 13 3 27 C3 41 20 50 50 51 L70 64 L63 49 C83 45 97 37 97 27 C97 13 78 3 50 3Z"
        return f'<svg viewBox="0 0 100 66" class="bal"><path d="{d}" {st}/></svg>'
    cx = 24 if t == "bl" else 76
    dots = f'<circle cx="{cx}" cy="55" r="4.2" {st}/><circle cx="{cx + (-8 if t == "bl" else 8)}" cy="62" r="2.6" {st}/>'
    d = ("M22 44 C8 44 4 32 12 26 C4 18 12 6 24 10 C28 2 44 0 50 7 C58 0 74 2 76 11 C88 7 97 18 90 26 "
         "C98 33 92 45 78 43 C74 51 58 52 50 46 C42 52 26 51 22 44Z")
    return f'<svg viewBox="0 0 100 66" class="bal"><path d="{d}" {st}/>{dots}</svg>'


# ------------------------------------------------------------------ puzzles -> HTML
def load_puzzles():
    cache = os.path.join(BUILD, "puzzles.json")
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(os.path.join(HERE, "puzzles.py")):
        return json.load(open(cache, encoding="utf-8"))
    P = {"cw": puzzles.crossword(), "ws": puzzles.wordsearch(), "dom": puzzles.domino()}
    json.dump(P, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return P


UNIT_OF = {"DIDASCALIA": "U4", "PERSONAGEM": "U2", "ONOMATOPEIA": "U3", "METAFORA": "U3", "NARRADOR": "U2", "ESTROFE": "U3",
           "VERBETE": "U1", "LENDA": "U2", "FACTO": "U1", "AVISO": "U1", "VERSO": "U3", "RIMA": "U3", "OSGA": "U1", "CENA": "U4"}


def cw_grid(cw, solved=False):
    num = cw["num"]
    rows = []
    for r, row in enumerate(cw["grid"]):
        tds = []
        for c, ch in enumerate(row):
            if ch is None:
                tds.append('<td class="x"></td>')
            else:
                n = num.get(f"{r},{c}")
                tds.append(f'<td>{f"<i>{n}</i>" if n else ""}{ch if solved else ""}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    return f'<table class="cw">{"".join(rows)}</table>'


def cw_clues(cw, d):
    out = []
    for n, dd, w, clue, r, c in cw["entries"]:
        if dd == d:
            out.append(f'<li><b>{n}</b><span>{H.escape(clue).replace("&#x27;", "’")} <em>({len(w)})</em></span><u>{UNIT_OF[w]}</u></li>')
    return "".join(out)


def ws_grid(ws, solved=False):
    used = {}
    for w, r, c, d in ws["sol"]:
        dr, dc = puzzles.WS_DIRS[d]
        for i in range(len(w)):
            used[(r + dr * i, c + dc * i)] = True
    rows = []
    for r, row in enumerate(ws["grid"]):
        rows.append("<tr>" + "".join(
            f'<td class="{"on" if solved and (r, c) in used else ("left" if solved else "")}">{ch}</td>' for c, ch in enumerate(row)) + "</tr>")
    return f'<table class="ws">{"".join(rows)}</table>'


def domino_html(dom):
    tiles = []
    for left, right, rel in dom["tiles"]:
        lab = "sinónimo" if rel == "sin" else "antónimo"
        tiles.append(f'<div class="dom"><div class="h l">{left}</div><div class="h r {rel}">{right}<small>{lab}</small></div></div>')
    for _ in range(3):
        tiles.append('<div class="dom blank"><div class="h l"><span class="fill"></span></div><div class="h r"><span class="fill"></span><small>sin. ou ant.?</small></div></div>')
    return "".join(tiles)


# ------------------------------------------------------------------ calligram (spiral snail)
CALI_TEXT = ("devagar, devagarinho, o caracol vai para a escola com a casa às costas; "
             "nunca se perde e nunca se atrasa, porque, onde quer que chegue, já está em casa")


def calligram():
    cx, cy, a, b = 150, 132, 7.0, 6.4  # archimedean spiral r = a + b*theta
    pts = []
    th = 13.2 * math.pi
    while th > 0.9 * math.pi:
        r = a + b * th / (2 * math.pi) * 2.05
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
        th -= 0.06
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return f'''<svg viewBox="0 0 300 250" class="cali">
  <path d="M36 232 C60 214 110 218 150 222 S250 228 286 214 L292 226 C250 246 70 248 30 240 Z" fill="#E7D9B8"/>
  <path d="M244 214 C262 192 268 172 262 150 L272 148 C282 176 274 200 258 220 Z" fill="#D9922A" opacity=".85"/>
  <path d="M262 150 L252 116 M270 149 L276 114" stroke="#1C2536" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="252" cy="113" r="4.6" fill="#1C2536"/><circle cx="276" cy="111" r="4.6" fill="#1C2536"/>
  <path id="spiral" d="{d}" fill="none"/>
  <text font-family="Fraunces" font-style="italic" font-size="10.4" fill="#1C2536" letter-spacing=".2"><textPath href="#spiral">{CALI_TEXT}</textPath></text>
</svg>'''


def kite():
    # a kite outline with dashed writing guides, for the pupil's own calligram
    guides = "".join(
        f'<path d="M150 {18+k*14} L{150+ (118-k*14)*0.74:.1f} {100} L150 {232-k*16} L{150-(118-k*14)*0.74:.1f} 100 Z" fill="none" stroke="#C9BFA9" stroke-width="1" stroke-dasharray="3 4"/>'
        for k in range(1, 6))
    return f'''<svg viewBox="0 0 300 270" class="kite">
  <path d="M150 18 L237 100 L150 232 L63 100 Z" fill="#fff" stroke="#1C2536" stroke-width="2"/>
  <path d="M150 18 V232 M63 100 H237" stroke="#E3DED2" stroke-width="1"/>
  {guides}
  <path d="M150 232 C140 246 164 252 150 266" stroke="#1C2536" stroke-width="1.6" fill="none"/>
  <path d="M143 244 l-9 -5 v10z M157 256 l9 -5 v10z" fill="#DC4A2E"/>
</svg>'''


# ------------------------------------------------------------------ checker (for metrics)
def render(html_path, pdf_path):
    """Chromium CLI print; fresh profile per attempt, whole process group killed on a hang, 3 attempts."""
    import shutil, signal, tempfile, time
    for attempt in range(3):
        prof = None
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
               "--run-all-compositor-stages-before-draw", "--no-first-run",  # NB: --user-data-dir makes this build hang (GCM)
               "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={pdf_path}", "file://" + html_path]
        pr = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        t0 = time.time()
        while pr.poll() is None and time.time() - t0 < 420:
            time.sleep(2)
        if pr.poll() is None:
            os.killpg(pr.pid, signal.SIGKILL)
            pr.wait()
        pass
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 10000:
            return
        print("render attempt", attempt + 1, "failed; retrying", flush=True)
    sys.exit("chromium render failed 3 times")


def build():
    os.makedirs(BUILD, exist_ok=True)
    art_prep.main()
    P = load_puzzles()
    html = open(os.path.join(HERE, "src", "unit.html"), encoding="utf-8").read()
    html = html.replace("{{BASECSS}}", open(os.path.join(HERE, "src", "base.css"), encoding="utf-8").read())
    rep = {
        "{{CW_GRID}}": cw_grid(P["cw"]), "{{CW_A}}": cw_clues(P["cw"], "A"), "{{CW_D}}": cw_clues(P["cw"], "D"),
        "{{WS_GRID}}": ws_grid(P["ws"]), "{{DOMINO}}": domino_html(P["dom"]),
        "{{CALIGRAMA}}": calligram(), "{{KITE}}": kite(), "{{SCIS}}": SCISSORS,
        "{{QRICON}}": '<svg viewBox="0 0 12 12" style="width:4mm;height:4mm;vertical-align:-1mm"><path d="M1 1h4v4H1zM7 1h4v4H7zM1 7h4v4H1zM7 7h2v2H7zM9 9h2v2H9z" fill="#1C2536"/></svg>',
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    for k in KEYC:
        html = html.replace("{{KEY:%s}}" % k, key_svg(k))
    for n in ICONS:
        html = html.replace("{{ICO:%s}}" % n, icon(n))
    for n in range(1, 7):
        html = html.replace("{{PIP:%d}}" % n, pips(n))
    for k in ("say-bl", "say-br", "think-bl", "think-br"):
        html = html.replace("{{BAL:%s}}" % k, balloon(k))
    for n, u in QRS.items():
        html = html.replace("{{QR:%s}}" % n, qr_svg(u))
    left = re.findall(r"\{\{[^}]+\}\}", html)
    if left:
        sys.exit(f"unresolved tokens: {left}")
    # folios and odd/even from the page order: first page = 129
    pages = html.count('<section class="page')
    out = os.path.join(BUILD, "unit.html")
    open(out, "w", encoding="utf-8").write(html)
    pdf = os.path.join(BUILD, "unit.pdf")
    render(out, pdf)
    import fitz
    doc = fitz.open(pdf)
    png = os.path.join(BUILD, "png")
    os.makedirs(png, exist_ok=True)
    for f in os.listdir(png):
        os.remove(os.path.join(png, f))
    for i, pg in enumerate(doc):
        pg.get_pixmap(dpi=110).save(os.path.join(png, f"{i+1:02d}.png"))
    fonts = sorted({f[3] for pg in doc for f in pg.get_fonts()})
    print("sections", pages, "pages", doc.page_count, "size", doc[0].rect, "MB", round(os.path.getsize(pdf) / 1e6, 2))
    print("fonts", fonts)


if __name__ == "__main__":
    build()
