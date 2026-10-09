"""Unidade 2 · parte B (pp. 15–28): Sophia (Cavaleiro), Mia Couto (Palavrinha), lendas, Saci, Consegues?"""
import math
import parts
from parts import *
parts.UNIT.update(n=2, total=28)
from u2_b_maps import EU, EU_W, EU_H, EU_PT, PT_LAND, PT, PT_W, PT_H, PT_PT

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea)"
U = lambda h=6.5: f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'
TICK = '<svg viewBox="0 0 20 20" style="width:{s};height:{s};vertical-align:-.4mm"><path d="M3 10.5l4.5 4.5L17 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def para(n, html, c=INK):
    return (f'<p style="position:relative"><span style="position:absolute;left:-7.5mm;top:.3mm;width:5mm;height:5mm;border-radius:50%;'
            f'background:{c};color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>')


def gloss(items):
    return '<dl class="gloss" style="margin-top:2mm">' + "".join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in items) + '</dl>'


def pic(src, h, pos="50% 50%"):
    return f'<div style="height:{h}mm;border-radius:3mm;overflow:hidden"><img class="cover" src="img/{src}" style="object-position:{pos}"></div>'


def th(cols, col=INK):
    return "<tr>" + "".join(f'<th style="background:{col}">{c}</th>' for c in cols) + "</tr>"


def trow(cells, h=10, w0="30mm"):
    first, rest = cells[0], cells[1:]
    return (f'<tr><td style="width:{w0};font-size:9pt">{first}</td>' +
            "".join(f'<td style="height:{h}mm;font-size:8.8pt;color:var(--muted)">{c}</td>' for c in rest) + "</tr>")


def ico(svg, s=8):
    return svg.replace('class="ico"', f'class="ico" style="width:{s}mm;height:{s}mm"')


def fillrow(label, w="52mm", gap="3mm"):
    return (f'<div style="display:flex;gap:{gap};align-items:baseline;margin-top:3.2mm;font-size:9.4pt"><span style="width:{w};flex:none">{label}</span>'
            f'<span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div>')


def chk_row(items, size="8.6pt"):
    return (f'<div style="display:flex;gap:4.5mm;flex-wrap:wrap;font-size:{size}">' +
            "".join(f'<span><span class="chk"></span>{i}</span>' for i in items) + '</div>')


# ================================================================ EUROPE MAP (the knight's journey)
L0, B1, K, C = -10.5, 58.8, 10, math.cos(math.radians(45))
def pe(lon, lat):
    return ((lon - L0) * K * C, (B1 - lat) * K)

def poly(pts):
    return " ".join(f"{pe(*p)[0]:.1f},{pe(*p)[1]:.1f}" for p in pts)

IDA = [(9.9, 57.1), (8.0, 57.7), (4.0, 55.0), (1.6, 51.0), (-5.0, 49.4), (-9.8, 43.6), (-10.0, 38.6), (-7.6, 36.4),
       (-5.6, 35.95), (0.0, 37.0), (9.4, 37.9), (11.6, 37.25), (15.0, 35.6), (25.0, 34.1), (32.0, 33.0), (34.75, 32.05)]
MAR = [(34.75, 32.05), (28.0, 34.3), (22.5, 35.9), (19.2, 39.9), (16.0, 42.6), (13.4, 44.1), (12.2, 44.42)]
TERRA = [(12.2, 44.42), (12.33, 45.44), (11.62, 44.84), (11.34, 44.49), (11.25, 43.77), (9.6, 44.3), (8.93, 44.41),
         (7.6, 45.9), (5.2, 47.4), (3.6, 49.6), (4.40, 51.22), (6.8, 52.6), (9.2, 54.6), (9.6, 56.1), (9.9, 57.1)]
STOPS = [  # n, lon, lat, label, anchor, dx, dy
    ("1", 35.22, 31.78, "Jerusalém · Belém", "end", -7, 13),
    ("2", 34.75, 32.05, "Jafa", "end", -8, -5),
    ("3", 12.2, 44.42, "Ravena", "start", 8, 6),
    ("4", 12.33, 45.44, "Veneza", "start", 8, -2),
    ("5", 11.25, 43.77, "Florença", "start", 7, 9),
    ("6", 8.93, 44.41, "Génova", "end", -7, 9),
    ("7", 4.40, 51.22, "Antuérpia", "end", -8, 3),
    ("8", 9.9, 57.1, "a floresta · casa", "start", 8, 3),
]
# Label placement is COMPUTED, not eyeballed: every label is tried at candidate
# positions around its point and takes the first whose box touches no route line,
# no stop badge, no other label and stays inside the map.
def _segs(pts):
    q = [pe(*p) for p in pts]
    return list(zip(q, q[1:]))
SEGS = _segs(IDA) + _segs(MAR) + _segs(TERRA)
BADGES = [(pe(lon, lat)[0] + {"1": (9, 10)}.get(k, (0, 0))[0], pe(lon, lat)[1] + {"1": (9, 10)}.get(k, (0, 0))[1]) for k, lon, lat, *_ in STOPS]
PLACED = []

def _seg_hits(r, p, q, pad=1.4):
    x0, y0, x1, y1 = r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad
    (ax, ay), (bx, by) = p, q
    for i in range(33):                       # sample the segment densely
        t = i / 32; x = ax + (bx - ax) * t; y = ay + (by - ay) * t
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False

def _box(x, y, t, size, anchor, bold):
    w = len(t) * size * (0.60 if bold else 0.54); h = size * 0.78
    x0 = x if anchor == "start" else x - w if anchor == "end" else x - w / 2
    return (x0, y - h, x0 + w, y + size * 0.18)

def _free(r):
    if r[0] < 2 or r[1] < 2 or r[2] > EU_W - 2 or r[3] > EU_H - 2:
        return False
    if any(_seg_hits(r, p, q) for p, q in SEGS):
        return False
    if any(r[0] - 7 < bx < r[2] + 7 and r[1] - 7 < by < r[3] + 7 for bx, by in BADGES):
        return False
    return not any(r[0] < o[2] + 1 and o[0] < r[2] + 1 and r[1] < o[3] + 1 and o[1] < r[3] + 1 for o in PLACED)

def _place(x, y, t, size, bold, cands):
    for dx, dy, anc in cands:
        r = _box(x + dx, y + dy, t, size, anc, bold)
        if _free(r):
            PLACED.append(r); return x + dx, y + dy, anc
    dx, dy, anc = cands[0]; PLACED.append(_box(x + dx, y + dy, t, size, anc, bold))
    print(f"u2_b map: no clear spot for {t!r}")
    return x + dx, y + dy, anc

AROUND = [(8, 3, "start"), (-8, 3, "end"), (0, -9, "middle"), (0, 15, "middle"), (8, -6, "start"), (8, 12, "start"),
          (-8, -6, "end"), (-8, 12, "end"), (11, 3, "start"), (-11, 3, "end"), (0, -14, "middle"), (0, 20, "middle")]
AREA = [(0, 0, "middle")] + [(dx, dy, "middle") for dy in (-7, 7, -13, 13, -19, 19) for dx in (0, -12, 12, -22, 22)]

LEADER = {"1": (9, 10)}   # badges too close to a neighbour sit off their point, with a leader line

def stop(n, lon, lat, t, a, dx, dy):
    x0, y0 = pe(lon, lat)
    ox, oy = LEADER.get(n, (0, 0))
    x, y = x0 + ox, y0 + oy
    lead = (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#E4502F" stroke-width=".9"/>'
            f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="1.7" fill="#E4502F"/>') if (ox or oy) else ""
    lx, ly, la = _place(x, y, t, 8.4, True, [(dx, dy, a)] + AROUND)
    return lead + (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.6" fill="#E4502F" stroke="#fff" stroke-width="1.2"/>'
            f'<text x="{x:.1f}" y="{y+2.6:.1f}" text-anchor="middle" font-family="Grotesk" font-weight="700" font-size="7.2" fill="#fff">{n}</text>'
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{la}" font-family="Grotesk" font-weight="700" font-size="8.4" fill="#17315A">{t}</text>')

def small(lon, lat, t, a="start", dx=4, dy=3, dot=True, it=False, size=6.8, col="#5B6475"):
    x, y = pe(lon, lat)
    d = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{col}"/>' if dot else ""
    cands = ([(dx, dy, a)] + [(c[0] * .6, c[1] * .6, c[2]) for c in AROUND]) if dot else [(dx + ex, dy + ey, an) for ex, ey, an in AREA]
    lx, ly, la = _place(x, y, t, size, False, cands)
    s = ' font-style="italic"' if it else ""
    return d + f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{la}" font-family="Grotesk" font-size="{size}" fill="{col}"{s}>{t}</text>'

_stops = "".join(stop(*s_) for s_ in STOPS)        # stops first: they have priority
_labels = "".join([
    small(-9.14, 38.72, "Lisboa", "start", 4, 3),
    small(7.6, 45.9, "Alpes", "middle", 0, -5, dot=False, it=True, size=7.4),
    small(2.8, 47.0, "FRANÇA", "middle", 0, 0, dot=False, size=7.4),
    small(10.4, 51.0, "ALEMANHA", "middle", 0, 0, dot=False, size=6.6),
    small(-4.0, 40.0, "PENÍNSULA IBÉRICA", "middle", 0, 0, dot=False, size=6.6),
    small(3.0, 56.6, "mar do Norte", "middle", 0, 0, dot=False, it=True, size=7, col="#2B4C7E"),
    small(18.0, 33.3, "mar Mediterrâneo", "middle", 0, 0, dot=False, it=True, size=7.6, col="#2B4C7E"),
    small(15.2, 43.2, "mar Adriático", "middle", 0, 0, dot=False, it=True, size=6.2, col="#2B4C7E"),
    small(30.5, 36.8, "tempestade", "middle", 0, 0, dot=False, it=True, size=7.4, col="#E4502F"),
])
EU_SVG = f'''<svg viewBox="0 0 {EU_W} {EU_H}" style="width:100%;display:block;border-radius:2.4mm;background:#DCE5F0">
<path d="{EU}" fill="#F4EDE1" stroke="#9FB0C6" stroke-width=".6" stroke-linejoin="round"/>
<polyline points="{poly(IDA)}" fill="none" stroke="#17315A" stroke-width="1.5" stroke-dasharray="1.5 3.2" stroke-linecap="round"/>
<polyline points="{poly(MAR)}" fill="none" stroke="#E4502F" stroke-width="2" stroke-dasharray="6 3.5" stroke-linecap="round"/>
<polyline points="{poly(TERRA)}" fill="none" stroke="#E4502F" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
{_labels}{_stops}
</svg>'''

# ================================================================ PORTUGAL MAP (origin legends)
def pp(k):
    return PT_PT[k]
PINS = [("lisboa", "A", "Lisboa", "end", -7, 3), ("nazare", "B", "Nazaré", "end", -7, 3),
        ("estrela", "C", "Serra da Estrela", "start", 7, 3), ("silves", "D", "Silves", "start", 7, -4)]
def pin(k, n, t, a, dx, dy):
    x, y = PT_PT[k]
    return (f'<circle cx="{x}" cy="{y}" r="7" fill="#2E8C7B" stroke="#fff" stroke-width="1.4"/>'
            f'<text x="{x}" y="{y+3.2}" text-anchor="middle" font-family="Grotesk" font-weight="700" font-size="8.6" fill="#fff">{n}</text>'
            f'<text x="{x+dx}" y="{y+dy}" text-anchor="{a}" font-family="Grotesk" font-weight="700" font-size="10.5" fill="#17315A">{t}</text>')
PT_SVG = f'''<svg viewBox="-34 0 {PT_W+34} {PT_H}" style="width:100%;display:block;border-radius:2.4mm;background:#DCE5F0">
<path d="{PT_LAND}" fill="#EFE9DE" stroke="#B7C3D3" stroke-width=".6"/>
<path d="{PT}" fill="#F7F1E6" stroke="#2E8C7B" stroke-width="1.3" stroke-linejoin="round"/>
<text x="-20" y="140" font-family="Grotesk" font-size="9.5" font-style="italic" fill="#2B4C7E" transform="rotate(-90 -20 140)">oceano Atlântico</text>
<text x="150" y="190" font-family="Grotesk" font-size="9" fill="#8A93A3" text-anchor="middle">ESPANHA</text>
{"".join(pin(*p) for p in PINS)}
</svg>'''


# ================================================================ 15  STATION 2.5 OPENER — Cavaleiro
parts6 = [("1", "A floresta e a promessa", "Natal na Dinamarca: o anúncio"),
          ("2", "A Terra Santa", "Jerusalém e Belém"),
          ("3", "O mar, Ravena e Veneza", "a tempestade · Vanina"),
          ("4", "Florença", "Giotto, Dante e Beatriz"),
          ("5", "De Génova à Flandres", "a febre · Antuérpia · Pêro Dias"),
          ("6", "A última noite", "o regresso pela neve")]
ph = "".join(f'<tr><td style="width:7mm;text-align:center;font-family:Fraunces;font-size:12pt;color:var(--coral)">{n}</td>'
             f'<td style="font-weight:400;color:var(--text);width:auto"><b class="blue" style="font-family:FrauncesText">{t}</b><div class="small muted" style="line-height:1.2">{s}</div></td>'
             f'<td style="width:21mm"></td><td style="width:9mm;text-align:center;vertical-align:middle"><span class="chk o"></span></td></tr>' for n, t, s in parts6)
P[15] = page(15, f'''
<div class="kicker">Estação 2.5 · Narrativa longa · leitura integral</div>
<h2 style="margin-top:2mm">O Cavaleiro da <em>Dinamarca</em></h2>
<div style="margin-top:3.4mm">{pic("cavaleiro.jpg", 76, "50% 42%")}</div>
<div class="grid2" style="margin-top:4.6mm;grid-template-columns:1fr 1.06fr;gap:7mm;align-items:start">
  <div>
    <p class="lead" style="font-size:11.4pt">Numa noite de Natal, um cavaleiro que vive numa floresta do Norte anuncia à família que vai partir em peregrinação à Terra Santa — e promete estar de volta, à mesma mesa, dois Natais depois. Entre a partida e o regresso há mar, cidades, histórias… e muitas razões para não voltar.</p>
    <div class="rule-card o" style="margin-top:4mm;font-size:9pt;line-height:1.4"><b class="coral">Sophia de Mello Breyner Andresen</b> (Porto, 1919 – Lisboa, 2004) já a conheces de <i>A Fada Oriana</i> (p. 11). Publicou <i>O Cavaleiro da Dinamarca</i> em 1964. Recebeu o Prémio Camões em 1999.</div>
    {act(1, "Prever", 'Observa a imagem. Que duas cidades parecem flutuar no céu? Porque achas que o cavaleiro «as leva» consigo?' + lines(3))}
  </div>
  <div>
    <div class="kicker blue">O meu plano de leitura · 6 partes</div>
    <table class="cmp" style="margin-top:1.6mm;font-size:9pt"><tr><th style="background:var(--ink)" colspan="2">Parte</th><th style="background:var(--ink)">Li no dia</th><th style="background:var(--coral);text-align:center">{TICK.format(s="3mm")}</th></tr>{ph}</table>
    <p class="small muted" style="margin-top:1.6mm">Lê uma parte por semana, na edição da turma. Depois de cada parte, preenche o diário de bordo (p. 16).</p>
  </div>
</div>
<div class="kicker coral" style="margin-top:3mm">Palavras para levar</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:1.6mm"><div style="border-top:1.2mm solid var(--coral);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">peregrinação</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">viagem a um lugar sagrado, por fé</div></div><div style="border-top:1.2mm solid var(--coral);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">Terra Santa</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">a Palestina, onde se passa a vida de Jesus</div></div><div style="border-top:1.2mm solid var(--coral);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">promessa</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">compromisso de fazer alguma coisa</div></div><div style="border-top:1.2mm solid var(--coral);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">regresso</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">volta ao lugar de onde se partiu</div></div></div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center;padding:3.6mm 4.5mm">
  <div><div class="kicker">Enquanto lês</div><p style="font-size:9.3pt;margin-top:1mm">Cola três marcadores no livro: <b class="coral">P</b> onde o cavaleiro faz a <b>promessa</b>, <b class="coral">C</b> sempre que alguém o <b>convida a ficar</b>, <b class="coral">H</b> quando alguém lhe conta uma <b>história</b>. Vais precisar deles na p. 17.</p></div>
  {qr("q-cavaleiro", "Saber mais", "A obra e a autora,<br>na Wikipédia.")}
</div>
''', station="2.5 · Cavaleiro")

# ================================================================ 16  JOURNEY MAP + LOG
log = [("1 · Jerusalém e Belém", "Onde passa o primeiro Natal?"), ("2 · Jafa e o mar", "O que acontece no navio?"),
       ("3 · Ravena", "O que mais admira?"), ("4 · Veneza", "Quem o recebe? Que história ouve?"),
       ("5 · Florença", "Em casa de quem fica? O que aprende?"), ("6 · perto de Génova", "Que problema o atrasa?"),
       ("7 · Antuérpia", "Que história ouve? De quem?"), ("8 · a floresta", "Que perigos enfrenta na última noite?")]
lgr = lambda rows: "".join(f'<tr><td style="width:33mm;font-size:8.8pt">{a}<div class="small muted" style="font-weight:400;line-height:1.2;margin-top:.3mm">{b}</div></td><td style="height:14mm"></td></tr>' for a, b in rows)
facts = [("2 anos", "de viagem, de uma primavera ao segundo Natal"), ("3", "convites para ficar longe de casa"),
         ("3", "histórias ouvidas pelo caminho"), ("1", "promessa")]
fh = "".join(f'<div style="border-top:.6pt solid var(--rule);padding:1.5mm 0"><div class="display" style="font-size:15pt;line-height:1;color:var(--coral)">{a}</div><div class="small muted" style="line-height:1.25">{b}</div></div>' for a, b in facts)
P[16] = page(16, f'''
<div class="kicker">Estação 2.5 · Diário de bordo</div>
<h2 style="margin-top:2mm">A rota do <em>peregrino</em></h2>
<div style="display:grid;grid-template-columns:1fr 54mm;gap:6mm;margin-top:3mm;align-items:start">
  <div>{EU_SVG}</div>
  <div>
    <div class="kicker blue">Legenda</div>
    <div style="font-size:8.6pt;line-height:1.35;margin-top:1.4mm">
      <div style="display:flex;gap:2mm;align-items:center"><svg width="11mm" height="3mm" viewBox="0 0 40 10"><path d="M2 5h36" stroke="#17315A" stroke-width="2.4" stroke-dasharray="2 4" stroke-linecap="round"/></svg>ida, por mar</div>
      <div style="display:flex;gap:2mm;align-items:center;margin-top:1mm"><svg width="11mm" height="3mm" viewBox="0 0 40 10"><path d="M2 5h36" stroke="#E4502F" stroke-width="3" stroke-dasharray="8 5"/></svg>regresso, por mar</div>
      <div style="display:flex;gap:2mm;align-items:center;margin-top:1mm"><svg width="11mm" height="3mm" viewBox="0 0 40 10"><path d="M2 5h36" stroke="#E4502F" stroke-width="3.2"/></svg>regresso, por terra</div>
    </div>
    <div class="kicker blue" style="margin-top:4mm">A viagem em números</div>
    <div style="margin-top:1mm">{fh}</div>
    <p class="src" style="margin-top:2mm">Mapa: Natural Earth (domínio público). A rota de ida é aproximada: o livro diz só que o cavaleiro foi por mar, com vento do norte, até às costas da Palestina.</p>
  </div>
</div>
{act(1, "Registar", 'Depois de cada parte, completa uma linha com palavras-chave. Não te esqueças do mês ou da estação do ano.')}
<div class="grid2" style="gap:5mm;margin-top:2mm;align-items:start"><table class="cmp ruled">{th(["Paragem", "O que acontece · quem · quando"])}{lgr(log[:4])}</table><table class="cmp ruled">{th(["Paragem", "O que acontece · quem · quando"])}{lgr(log[4:])}</table></div>
''', station="2.5 · Cavaleiro")

# ================================================================ 17  THE JOURNEY AS A TRIAL
obst = ["a tempestade no mar", "o navio desfeito em Ravena", "a febre", "os navios que já partiram de Génova",
        "o inverno sem barcos para o Norte", "a neve e a noite na floresta", "os lobos e o urso"]
ob = "".join(f'<span class="chip" style="font-weight:500">{o}</span>' for o in obst)
conv = [("Veneza", "o Mercador"), ("Florença", "o banqueiro Averardo"), ("Antuérpia", "o negociante flamengo")]
cv = "".join(f'<tr><td style="width:44mm;font-size:9pt">{a}<div class="small muted" style="font-weight:400">{b}</div></td><td style="height:9.5mm"></td><td></td></tr>' for a, b in conv)
hist = [("Vanina e Guidobaldo", "Veneza"), ("Giotto, Dante e Beatriz", "Florença"), ("Pêro Dias", "Antuérpia")]
hs = "".join(f'<tr><td style="width:40mm;font-size:9pt">{a}<div class="small muted" style="font-weight:400">{b}</div></td><td style="width:34mm;height:9mm"></td><td></td></tr>' for a, b in hist)
P[17] = page(17, f'''
<div class="kicker">Estação 2.5 · Educação literária</div>
<h2 style="margin-top:2mm">A viagem como <em>prova</em></h2>
<div class="rule-card o" style="margin-top:3mm;font-size:9.5pt;line-height:1.42">Numa narrativa de viagem, o caminho <b>põe à prova</b> quem viaja. Há obstáculos que vêm <b>de fora</b> (o mar, a doença, o frio) e tentações que vêm <b>de dentro</b> (ficar, enriquecer, desistir). Aquilo que faz a personagem continuar mostra os seus <b class="coral">valores</b>.</div>
{act(1, "Classificar", f'Estes obstáculos atrasam o cavaleiro. Rodeia a <b class="blue">azul</b> os que vêm da natureza e a <b class="coral">vermelho</b> os que vêm do acaso. Qual foi, para ti, a prova mais dura? Porquê?<div class="opts" style="margin-top:2mm">{ob}</div>' + lines(1))}
{act(2, "Caçar frases", 'Três pessoas convidam o cavaleiro a ficar. Usa os marcadores <b class="coral">C</b>: o que lhe oferecem? Copia do livro <b>uma frase curta</b> da resposta dele.')}
<table class="cmp ruled" style="margin-top:2mm">{th(["Onde · quem", "O que lhe oferece", "A resposta do cavaleiro (copia) · p."], COR)}{cv}</table>
{act(3, "Relacionar", 'Pelo caminho, o cavaleiro <b>ouve histórias</b> (marcadores <b class="coral">H</b>). São narrativas dentro da narrativa. Quem as conta? Que ideia leva ele de cada uma?')}
<table class="cmp ruled" style="margin-top:2mm">{th(["História · onde", "Quem a conta", "O que aprende o cavaleiro"], COR)}{hs}</table>
<div class="grid2" style="margin-top:3mm;gap:7mm;grid-template-columns:1fr 1fr">
  <div>{act(4, "Concluir", 'Escolhe dois valores e prova-os com um episódio: <span class="small muted">lealdade · fé · coragem · curiosidade · persistência · respeito pela palavra dada</span>' + lines(2))}</div>
  <div class="panel coral" style="margin-top:4.2mm;padding:3.4mm 4mm">
    <div style="display:flex;gap:2.4mm;align-items:center">{ico(MICRO, 7)}<div class="kicker">Oralidade · Apresenta um episódio</div></div>
    <p class="small" style="margin-top:1.2mm;line-height:1.38">Escolhe um episódio e apresenta-o à turma em <b>2 minutos</b>, com um cartão de notas: <b>onde e quando</b> · <b>quem</b> · <b>o que acontece</b> · <b>porque conta para a viagem</b> · <b>uma frase do livro</b> para ler em voz alta.</p>
    <div style="margin-top:1.6mm">{chk_row(["olho a turma", "sigo as notas, não leio tudo", "digo porque é importante"], "8pt")}</div>
  </div>
</div>
''', station="2.5 · Cavaleiro")

# ================================================================ 18  GRAMMAR (CI + formas de tratamento) + WRITING
ci_s = ["O cavaleiro prometeu um regresso à família.", "Filippo contou a história de Giotto aos convidados.",
        "O capitão mostrou três cofres ao negociante.", "O Mercador ofereceu um belo cavalo ao amigo dinamarquês."]
cis = "".join(f'<div style="font-family:FrauncesText;font-size:10pt;line-height:1.55">{chr(97+i)}) {s}</div>' for i, s in enumerate(ci_s))
trat = [("a um amigo", "tu", "Fica comigo!"), ("a um banqueiro que respeitas", "o senhor", ""), ("a um rei", "Vossa Majestade", ""), ("à tua professora", "a senhora professora", "")]
tt = "".join(f'<tr><td style="width:40mm;font-size:8.8pt;font-weight:400;color:var(--text)">{a}</td><td style="width:34mm;font-size:8.8pt;color:var(--sea)">{b}</td><td style="height:8.4mm;font-family:FrauncesText;font-size:9.4pt;color:var(--text)"><i>{c}</i></td></tr>' for a, b, c in trat)
P[18] = page(18, f'''
<div class="kicker sea">Estação 2.5 · Gramática e escrita</div>
<h2 style="margin-top:2mm">A quem? E <em>como</em> se trata alguém?</h2>
<div class="grid2" style="margin-top:3.4mm;gap:6mm">
  <div class="panel sea" style="padding:3.6mm 4.2mm">
    <div class="kicker sea">Complemento indireto</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.4">Indica <b>a quem</b> ou <b>para quem</b> se dirige a ação. Começa pela preposição <b>a</b> (ou <b>para</b>) e pode ser substituído por <b>lhe</b> / <b>lhes</b>. Aparece com verbos como <i>dar, oferecer, contar, dizer, prometer, pedir, mostrar</i>.</p>
    <p style="font-family:FrauncesText;font-size:9.8pt;margin-top:2mm;line-height:1.5">Averardo deu <span class="mk-f">uma carta</span> <span class="mk-c">ao cavaleiro</span>.<br>Averardo deu-<span class="mk-c">lhe</span> uma carta.</p>
    <p class="small muted" style="margin-top:1mm"><span class="mk-f">CD</span> o quê? · <span class="mk-c">CI</span> a quem?</p>
  </div>
  <div class="panel" style="padding:3.6mm 4.2mm">
    <div class="kicker">Formas de tratamento</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.4">Escolhemos a forma de tratar alguém conforme a <b>proximidade</b> e o <b>respeito</b>: <b>tu</b> (família, amigos) · <b>você</b> (colegas, conhecidos) · <b>o senhor / a senhora</b> · <b>Vossa Excelência</b>, <b>Vossa Majestade</b> (cerimónia). Com todas, exceto <i>tu</i>, o verbo vai para a <b>3.ª pessoa</b>.</p>
    <p style="font-family:FrauncesText;font-size:9.8pt;margin-top:2mm">Tu <b>ficas</b>? · O senhor <b>fica</b>? · Vossa Majestade <b>fica</b>?</p>
  </div>
</div>
<div class="grid2" style="gap:6mm">
  <div>{act(1, "Identificar", f'Sublinha o <b class="blue">CD</b> e rodeia o <b class="sea">CI</b>.<div style="margin-top:1.4mm">{cis}</div>', "sea")}
  {act(2, "Substituir", 'Reescreve as frases b) e c), trocando o CI por <b>lhe</b> ou <b>lhes</b>.' + lines(2), "sea")}</div>
  <div>{act(3, "Adequar", 'O Mercador de Veneza pede ao cavaleiro: «Fica comigo!» Como diria o mesmo pedido a outras pessoas?', "sea")}
  <table class="cmp ruled" style="margin-top:2mm">{th(["Falar…", "Tratamento", "O pedido"], SEA)}{tt}</table></div>
</div>
<div class="panel coral" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{ico(LAPIS, 8)}<div><div class="kicker">Escrita · Uma cidade e uma decisão</div><div class="small muted">Escolhe <b>Veneza</b> ou <b>Florença</b>. Escreve dois parágrafos (90–120 palavras).</div></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:2.2mm;font-size:8.8pt;line-height:1.32">
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">§ 1 · Descreve a cidade</b><br>o que se vê, o que se ouve, o que espanta; adjetivos e uma comparação («como…»).</div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">§ 2 · Conta a decisão</b><br>quem o convida a ficar, o que lhe oferece, o que ele responde e <b>porquê</b>.</div>
  </div>
  {lines(7)}
  <div style="margin-top:2mm">{chk_row(["dois parágrafos", "três adjetivos", "uma comparação", "um complemento indireto", "a razão da decisão"])}</div>
</div>
''', station="2.5 · Cavaleiro")

# ================================================================ 19  STATION 2.6 OPENER — Palavrinha
clues = [("vizinhas", "Lê a frase inteira e a seguinte."), ("família", "Conheces uma palavra parecida?"),
         ("imagem", "A ilustração ajuda?"), ("troca", "Põe outra palavra no lugar. Faz sentido?")]
cl = "".join(f'<div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral" style="font-family:Grotesk;font-size:7pt;letter-spacing:.12em;text-transform:uppercase">{a}</b><div class="small" style="line-height:1.3;margin-top:.4mm">{b}</div></div>' for a, b in clues)
wcard = lambda n: (f'<div class="panel" style="padding:2.8mm 3.2mm"><div class="display" style="font-size:16pt;line-height:1;color:var(--coral)">{n}</div>'
                   f'<div class="small muted" style="margin-top:1.4mm">A palavra</div>{U(6)}<div class="small muted" style="margin-top:1.6mm">Pista do contexto · p.</div>{U(6)}{U(6)}'
                   f'<div class="small muted" style="margin-top:1.6mm">Acho que quer dizer…</div>{U(6)}{U(6)}'
                   f'<div class="small" style="margin-top:2mm"><span class="chk"></span>confirmei no dicionário</div></div>')
P[19] = page(19, f'''
<div class="kicker">Estação 2.6 · Conto · leitura integral</div>
<h2 style="margin-top:2mm">O Beijo da <em>Palavrinha</em></h2>
<div style="margin-top:3.4mm">{pic("palavrinha.jpg", 64, "50% 55%")}</div>
<div class="grid2" style="margin-top:4.4mm;grid-template-columns:1.05fr 1fr;gap:7mm;align-items:start">
  <div>
    <p class="lead" style="font-size:11.2pt">Numa aldeia do interior de Moçambique, tão longe da costa que o rio parecia não ter fim, vivia uma menina que nunca tinha visto o mar. Quando ela adoece, o irmão tem uma ideia: levar-lhe o mar… numa palavra.</p>
    <div class="rule-card o" style="margin-top:3.4mm;font-size:9pt;line-height:1.4"><b class="coral">Mia Couto</b> nasceu na Beira, em Moçambique, em 1955. É biólogo e um dos escritores mais lidos da língua portuguesa. Recebeu o Prémio Camões em 2013. <i>O Beijo da Palavrinha</i> tem ilustrações do pintor moçambicano Malangatana.</div>
  </div>
  <div>
    {act(1, "Prever", 'O título tem um <b>diminutivo</b>. Como pode uma palavra dar um beijo? Escreve a tua hipótese.' + lines(2))}
    {act(2, "Ler", 'Lê o conto inteiro, na edição da turma. Depois, conta-o a alguém em casa em <b>cinco frases</b>. Quem ouviu?' + '<div style="margin-top:1mm">' + U(6) + '</div>')}
  </div>
</div>
<div class="panel" style="margin-top:auto;padding:3.6mm 4.5mm">
  <div style="display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center">
    <div style="display:flex;gap:3mm;align-items:center">{ico(MICRO, 8)}<div><div class="kicker">Oralidade · Detetive de palavras</div><div class="small muted">Escolhe <b>três palavras novas</b> do conto. Descobre o sentido pelo contexto e explica-o ao teu grupo, em 30 segundos cada.</div></div></div>
    {qr("q-palavrinha", "Ouvir o conto", "RTP Ensina: narrado em português<br>e em Língua Gestual Portuguesa.")}
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:2.4mm">{cl}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:2.6mm">{wcard(1)}{wcard(2)}{wcard(3)}</div>
</div>
''', station="2.6 · Palavrinha")

# ================================================================ 20  THE VALUE OF WORDS
names = [("Maria Poeirinha", "poeira"), ("Zeca Zonzo", "zonzo"), ("Tio Jaime Litorânio", "litoral")]
nm = "".join(f'<tr><td style="width:36mm;font-size:9pt">{a}<div class="small muted" style="font-weight:400">faz lembrar: <i>{b}</i></td><td style="height:12.5mm"></td><td></td></tr>' for a, b in names)
letter = lambda L, hint: (f'<div style="border:1px solid var(--rule);border-radius:2.5mm;padding:2.6mm 3mm;background:#fff">'
                          f'<div style="font-family:FrauncesText;font-size:34pt;line-height:.9;color:var(--ink);text-align:center">{L}</div>'
                          f'<div class="small muted" style="text-align:center;margin-top:1mm">{hint}</div>{U(6)}{U(6)}</div>')
P[20] = page(20, f'''
<div class="kicker">Estação 2.6 · Compreender e interpretar</div>
<h2 style="margin-top:2mm">Uma palavra onde cabe o <em>mar</em></h2>
{act(1, "Interpretar", 'Em Mia Couto, os <b>nomes</b> dizem muito das personagens. O que sugere cada nome? O que faz cada uma na história?')}
<table class="cmp ruled" style="margin-top:2mm">{th(["Personagem", "O que o nome sugere", "O que faz na história"], COR)}{nm}</table>
<div class="grid2" style="gap:7mm;grid-template-columns:1fr 1fr">
  <div>{act(2, "Explicar", 'Porque é que ver o mar era, para esta família, um sonho quase impossível? Dá duas razões do texto.' + lines(4))}</div>
  <div>{act(3, "Comparar", 'Toda a gente esperava que o Zeca <b>desenhasse</b> o mar. O que fez ele, em vez disso? Porque é que a ideia dele é melhor?' + lines(4))}</div>
</div>
{act(4, "Visualizar", 'O Zeca leva o dedo da irmã pelas letras. Em que se transforma cada letra, para Poeirinha? Escreve e desenha.')}
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:2.2mm;padding-left:12mm">{letter("m", "pista: a forma")}{letter("a", "pista: a forma")}{letter("r", "pista: o som")}</div>
<div class="grid2" style="margin-top:auto;gap:6mm;grid-template-columns:1.25fr 1fr;align-items:stretch">
  <div>{act(5, "Refletir", 'No fim, o autor não usa a palavra «morrer». Que imagem escolhe para contar o que acontece a Poeirinha? Porque achas que o faz assim?' + lines(3))}</div>
  <div class="panel coral" style="margin-top:4.2mm;padding:3.4mm 4mm">
    <div class="kicker">O valor da história contada</div>
    <p class="small" style="margin-top:1.2mm;line-height:1.42">Este conto fala de uma perda, mas conta-a com ternura: a menina que nunca viu o mar recebe-o inteiro numa palavra. As histórias ajudam-nos a guardar quem amamos. Se quiseres, conversa sobre isto com o teu professor ou com a tua família.</p>
  </div>
</div>
''', station="2.6 · Palavrinha")

# ================================================================ 21  GRAMMAR (radical, afixos, composição) + EXPOSITORY WRITING
dw = ["marinheiro", "empoeirado", "palavrinha", "desconhecido", "reler", "impossível"]
dws = "".join(f'<tr><td style="width:30mm;font-family:FrauncesText;font-size:10pt;font-weight:400;color:var(--text)">{w}</td><td></td><td></td><td></td></tr>' for w in dw)
comp_a = ["beija-", "guarda-", "arco-", "passa-", "girassol"]
P[21] = page(21, f'''
<div class="kicker sea">Estação 2.6 · Gramática e escrita</div>
<h2 style="margin-top:2mm">Palavras que <em>crescem</em></h2>
<div class="grid2" style="margin-top:3.4mm;gap:6mm;grid-template-columns:1.1fr 1fr">
  <div class="panel sea" style="padding:3.6mm 4.2mm">
    <div class="kicker sea">Radical e afixos · derivação</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.4">O <b>radical</b> é a parte que guarda o sentido da palavra. Juntando-lhe <b>afixos</b>, formam-se palavras novas: o <b>prefixo</b> vem antes, o <b>sufixo</b> vem depois.</p>
    <p style="font-family:FrauncesText;font-size:10.4pt;margin-top:2mm;line-height:1.6"><span class="mk-c">des</span>·<b>conhec</b>·<span class="mk-o">ido</span> &nbsp; <b>poeir</b>·<span class="mk-o">inha</span> &nbsp; <b>mar</b>·<span class="mk-o">inheiro</span></p>
    <p class="small muted" style="margin-top:.6mm"><span class="mk-c">prefixo</span> · <b>radical</b> · <span class="mk-o">sufixo</span></p>
  </div>
  <div class="panel" style="padding:3.6mm 4.2mm">
    <div class="kicker">Composição</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.4">Juntam-se <b>duas ou mais palavras</b> para formar uma nova.</p>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.45"><b>Justaposição</b> — as palavras ficam inteiras: <i>beija-flor, guarda-chuva, passatempo</i>.<br><b>Aglutinação</b> — uma delas perde sons: <i>planalto</i> (plano + alto), <i>aguardente</i> (água + ardente).</p>
  </div>
</div>
<div class="grid2" style="gap:6mm;grid-template-columns:1.1fr 1fr">
  <div>{act(1, "Decompor", 'Separa as partes de cada palavra.', "sea")}
  <table class="cmp ruled" style="margin-top:1.8mm;font-size:8.8pt">{th(["Palavra", "Prefixo", "Radical", "Sufixo"], SEA)}{dws}</table></div>
  <div>{act(2, "Formar", 'Escreve quatro palavras da família de <b>mar</b> e sublinha o sufixo.' + lines(2), "sea")}
  {act(3, "Compor", 'Completa as palavras compostas. No quadrado, escreve <b>J</b> (justaposição) ou <b>A</b> (aglutinação).<div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm 5mm;margin-top:2mm;font-size:9.4pt"><div style="display:flex;align-items:flex-end;gap:1.6mm;white-space:nowrap">beija-<span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span class="chk"></span></div><div style="display:flex;align-items:flex-end;gap:1.6mm;white-space:nowrap">guarda-<span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span class="chk"></span></div><div style="display:flex;align-items:flex-end;gap:1.6mm;white-space:nowrap">arco-<span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span class="chk"></span></div><div style="display:flex;align-items:flex-end;gap:1.6mm;white-space:nowrap">plan<span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span class="chk"></span></div></div>', "sea")}</div>
</div>
<div class="panel coral" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{ico(LAPIS, 8)}<div><div class="kicker">Escrita · Texto expositivo</div><div class="small muted"><b>O que aprende o Zeca Zonzo?</b> Explica, em três parágrafos (100–130 palavras), o que a personagem descobre sobre as palavras.</div></div></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:2.2mm;font-size:8.7pt;line-height:1.3">
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">Introdução</b><br>Quem é o Zeca e qual é o problema da irmã.</div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">Desenvolvimento</b><br>O que ele faz e o que aprende. Dá <b>dois exemplos</b> do conto.</div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">Conclusão</b><br>O que esta história nos ensina sobre o valor das palavras.</div>
  </div>
  {lines(8)}
  <div style="margin-top:2mm">{chk_row(["três parágrafos", "dois exemplos do conto", "conectores: primeiro, depois, por isso, assim", "sem opiniões na introdução"])}</div>
</div>
''', station="2.6 · Palavrinha")

# ================================================================ 22  STATION 2.7 — ORIGIN LEGENDS + MAP + ORAL
legs = [("A", "Lisboa", "Ulisses, o herói que conheceste na p. 7, teria parado na foz do Tejo e fundado ali uma cidade, a que chamou <i>Ulisseia</i>. Desde a Idade Média, há quem ligue o antigo nome da cidade, <i>Olisipo</i>, ao herói grego."),
        ("B", "Nazaré", "Numa manhã de nevoeiro de 1182, D. Fuas Roupinho perseguia um veado que se atirou da falésia. O cavaleiro pediu ajuda a Nossa Senhora e o cavalo parou mesmo à beira do abismo. No local ergueu-se a Ermida da Memória."),
        ("C", "Serra da Estrela", "Um pastor guiava-se todas as noites por uma estrela. Um rei quis comprar-lha e ofereceu-lhe riquezas, mas o pastor recusou. A montanha ficou a chamar-se Serra da Estrela."),
        ("D", "Silves · Algarve", "Um rei mouro plantou milhares de amendoeiras para que a princesa do Norte com quem casara voltasse a ver «neve». Vais lê-la na p. 23.")]
lgh = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2.4mm;padding:2mm 0;border-top:.6pt solid var(--rule)"><div style="width:6.4mm;height:6.4mm;border-radius:50%;background:var(--sea);color:#fff;font-family:Grotesk;font-weight:700;font-size:8pt;line-height:6.4mm;text-align:center">{n}</div><div><b class="blue" style="font-family:FrauncesText;font-size:10pt">{t}</b><div style="font-size:8.8pt;line-height:1.36;margin-top:.3mm">{d}</div></div></div>' for n, t, d in legs)
expl = "".join(f'<tr><td style="width:12mm;text-align:center;font-family:Grotesk;color:var(--sea)">{n}</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td></tr>' for n, *_ in legs)
notes = [("Onde?", 2), ("Quem?", 2), ("O que acontece? (3 palavras-chave)", 3), ("O que explica?", 2)]
nh = "".join(f'<div><div class="small" style="font-weight:700;color:var(--sea)">{a}</div>{lines(k)}</div>' for a, k in notes)
P[22] = page(22, f'''
<div class="kicker sea">Estação 2.7 · Lendas</div>
<h2 style="margin-top:2mm">Lendas de <em>origens</em></h2>
<div class="grid2" style="margin-top:3.4mm;grid-template-columns:62mm 1fr;gap:7mm;align-items:start">
  <div>{PT_SVG}<p class="src" style="margin-top:1.4mm">Mapa: Natural Earth (domínio público).</p></div>
  <div>
    <div class="panel sea" style="padding:3.4mm 4mm">
      <div class="kicker sea">O que é uma lenda?</div>
      <p style="font-size:9.2pt;margin-top:1.2mm;line-height:1.4">É uma narrativa <b>tradicional</b>, passada de boca em boca, que mistura o <b>real</b> (lugares que existem, por vezes pessoas que viveram) com o <b>maravilhoso</b>. Muitas lendas explicam a <b>origem</b> de um nome, de um monumento ou de uma paisagem. No mito, os protagonistas são deuses e heróis de um tempo muito antigo; na lenda, a história prende-se a <b>um lugar</b> que podemos visitar.</p>
    </div>
    <div style="margin-top:2.4mm">{lgh}</div>
  </div>
</div>
<div class="grid2" style="gap:7mm;grid-template-columns:1fr 1.25fr">
  <div>{act(1, "Classificar", 'O que explica cada lenda? Assinala.', "sea")}
    <table class="cmp" style="margin-top:2mm;font-size:8.6pt">{th(["", "nome", "monumento", "paisagem"], SEA)}{expl}</table>
    {act(2, "Pesquisar", 'Há uma lenda de origem na tua terra? Pergunta em casa e escreve o nome.' + lines(1), "sea")}
  </div>
  <div class="panel" style="margin-top:4.2mm;padding:3.4mm 4mm">
    <div style="display:flex;gap:2.4mm;align-items:center">{ico(MICRO, 7)}<div class="kicker sea">Oralidade · Narrar a partir de notas</div></div>
    <p class="small" style="margin-top:1mm;line-height:1.36">Escolhe a lenda B ou C. Na biblioteca ou em casa, procura uma versão mais longa. Toma notas <b>só com palavras-chave</b> e conta-a à turma, sem ler, em 2 minutos.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1mm 4mm;margin-top:1mm">{nh}</div>
  </div>
</div>
<p class="src" style="margin-top:auto">Resumos escritos para este manual. Nazaré: Junta de Freguesia da Nazaré e pt.wikipedia.org/wiki/Lenda_da_Nazaré; Lisboa: Damião de Góis, <i>Urbis Olisiponis Descriptio</i> (1554).</p>
''', station="2.7 · Lendas")

# ================================================================ 23  LEGEND TEXT — amendoeiras
LA = [
 'Há muitos, muitos séculos, quando o Algarve se chamava <i>al-Gharb</i> e era governado por reis mouros, reinava em Chelb — a cidade a que hoje chamamos Silves — o jovem Ibn-Almundim. Era valente e justo, e dizia-se que nunca perdera uma batalha.',
 'Certo dia, entre os prisioneiros trazidos de uma batalha, os guardas levaram à sua presença uma rapariga de olhos claros e cabelos cor de trigo. Chamava-se Gilda e era uma princesa das terras do Norte. O rei deu-lhe a liberdade e, pouco depois, pediu-a em casamento. Gilda aceitou, e houve festa em todo o reino.',
 'Mas, com o passar dos meses, a princesa foi ficando triste. Deixou de sorrir, quase não comia e passava as tardes na torre mais alta do castelo, a olhar para norte. Os médicos e os sábios do reino não descobriam que doença era aquela.',
 'Até que um velho cativo, também vindo das terras do Norte, pediu para falar com o rei.<br>— Senhor, a princesa não tem nenhuma doença do corpo. Tem saudades da neve. Na terra dela, no inverno, os campos ficam todos brancos.',
 'Ibn-Almundim ficou calado. Podia dar-lhe ouro, sedas, jardins inteiros — mas como dar neve a quem vive no Algarve? Nessa noite, não dormiu. De manhã, mandou chamar os jardineiros:<br>— Plantem amendoeiras. Muitas amendoeiras, por todo o reino, a perder de vista!',
 'Assim foi feito. E, no fim do inverno seguinte, o rei e a princesa subiram juntos à torre.<br>— Abre os olhos, Gilda — pediu ele.<br>A princesa olhou. Os montes e os vales estavam brancos, cobertos por milhares de pequenas flores. Parecia que tinha nevado sobre o al-Gharb.',
 'Gilda sorriu pela primeira vez em muitos meses e, pouco a pouco, recuperou a alegria. E dizem que é por isso que, no fim de cada inverno, as amendoeiras do Algarve se cobrem de branco: para lembrar a neve que um rei plantou por amor.',
]
def para2(n, html, c=SEA):
    return (f'<p style="position:relative;padding-left:7.5mm"><span style="position:absolute;left:0;top:.6mm;width:5mm;height:5mm;border-radius:50%;'
            f'background:{c};color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>')
lat2 = "".join(para2(i, t) for i, t in enumerate(LA, 1))
P[23] = page(23, f'''
<div class="kicker sea">Estação 2.8 · Lenda · texto integral</div>
<h2 style="margin-top:2mm;font-size:27pt">A Lenda das <em>amendoeiras</em></h2>
<div style="margin-top:3mm">{pic("amendoeiras.jpg", 52, "50% 58%")}</div>
<div class="reading" style="margin-top:4mm;column-count:2;column-gap:9mm;column-rule:.6pt solid var(--rule)">{lat2}</div>
<div style="margin-top:auto;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:end;border-top:.6pt solid var(--rule);padding-top:2mm">
  <dl class="gloss" style="display:grid;grid-template-columns:repeat(4,auto);gap:0 5mm">{"".join(f'<div><dt>{a}</dt><dd style="margin:0">{b}</dd></div>' for a, b in [("mouros", "muçulmanos que governaram parte da Península Ibérica."), ("cativo", "prisioneiro."), ("a perder de vista", "até onde os olhos alcançam."), ("saudades", "tristeza pela falta de alguém ou de algo.")])}</dl>
</div>
<p class="src" style="margin-top:1.4mm">Texto escrito para este manual, a partir da lenda tradicional do Algarve.</p>
''', station="2.8 · Amendoeiras")

# ================================================================ 24  UNDERSTAND + COMPARE + GRAMMAR + REWRITE
rf = ["Silves é uma cidade do Algarve.", "Os mouros governaram o Algarve durante séculos.", "Um rei plantou todas as amendoeiras por amor.",
      "As amendoeiras florescem no fim do inverno.", "As flores curaram a tristeza da princesa."]
rfh = "".join(f'<div style="display:grid;grid-template-columns:1fr 7mm 7mm;gap:2mm;align-items:center;font-size:9pt;padding:1mm 0;border-bottom:.6pt solid var(--rule)"><span>{s}</span><span class="chk" style="margin:0 auto"></span><span class="chk o" style="margin:0 auto"></span></div>' for s in rf)
cmp_rows = [("Lugar", ""), ("Personagens", ""), ("Elemento maravilhoso", ""), ("O que explica", "")]
cmh = "".join(f'<tr><td style="width:30mm;font-size:8.8pt">{a}</td><td style="height:9mm"></td><td></td></tr>' for a, _ in cmp_rows)
sj = ["Ibn-Almundim e Gilda subiram à torre.", "A princesa olhou para norte.", "Os médicos e os sábios não sabiam a cura.", "— Senhor, a princesa tem saudades da neve."]
sjh = "".join(f'<div style="display:grid;grid-template-columns:1fr 20mm;gap:2mm;align-items:end;font-family:FrauncesText;font-size:9.6pt;margin-top:1.5mm"><span>{chr(97+i)}) {s}</span>{U(5)}</div>' for i, s in enumerate(sj))
P[24] = page(24, f'''
<div class="kicker sea">Estação 2.8 · Compreender, comparar, escrever</div>
<h2 style="margin-top:2mm">Uma paisagem com <em>história</em></h2>
<div class="grid2" style="gap:6mm;grid-template-columns:1fr 1fr">
  <div>{act(1, "Distinguir", 'Real (<b class="blue">R</b>) ou lendário (<b class="coral">L</b>)? Assinala.<div style="display:grid;grid-template-columns:1fr 7mm 7mm;gap:2mm;margin-top:1.4mm;font-family:Grotesk;font-size:7pt;font-weight:700"><span></span><span class="blue" style="text-align:center">R</span><span class="coral" style="text-align:center">L</span></div>' + rfh, "sea")}
  {act(2, "Explicar", 'O que explica esta lenda na paisagem do Algarve?' + lines(2), "sea")}</div>
  <div>{act(3, "Comparar", 'Compara-a com a lenda B ou C da p. 22.', "sea")}
  <table class="cmp ruled" style="margin-top:2mm;font-size:8.6pt">{th(["", "Amendoeiras", "Lenda ___"], SEA)}{cmh}</table></div>
</div>
<div class="panel sea" style="margin-top:3mm;display:grid;grid-template-columns:1fr 1fr;gap:6mm;padding:3.2mm 4.2mm">
  <div><div class="kicker sea">Sujeito simples e composto</div><p style="font-size:9pt;margin-top:1.2mm;line-height:1.4">O sujeito <b>simples</b> tem um só núcleo: <i><u>A princesa</u> sorriu.</i> O <b>composto</b> tem dois ou mais: <i><u>O rei</u> e <u>a princesa</u> subiram.</i> Com sujeito composto, o verbo vai para o <b>plural</b>.</p></div>
  <div><div class="kicker sea">Vocativo</div><p style="font-size:9pt;margin-top:1.2mm;line-height:1.4">Palavra ou expressão com que <b>chamamos</b> alguém. <b>Não</b> é o sujeito e separa-se <b>sempre por vírgula</b>: <i>— Abre os olhos<b class="coral">,</b> Gilda.</i> · <i>— Senhor<b class="coral">,</b> escute.</i></p></div>
</div>
<div class="grid2" style="gap:6mm;grid-template-columns:1fr 1fr">
  <div>{act(4, "Classificar", 'Escreve <b>S</b> (sujeito simples), <b>C</b> (composto) ou <b>V</b> (há vocativo).' + sjh, "sea")}</div>
  <div>{act(5, "Pontuar", 'Coloca as vírgulas e sublinha o vocativo.<div style="font-family:FrauncesText;font-size:9.8pt;line-height:1.75;margin-top:1.4mm">Jardineiros plantem amendoeiras!<br>Não fiques triste minha princesa.<br>Diz-me velho o que tem a Gilda.</div>', "sea")}</div>
</div>
<div class="panel coral" style="margin-top:auto;padding:3.8mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{ico(LAPIS, 8)}<div><div class="kicker">Escrita · Outro narrador</div><div class="small muted">Reescreve os §§ 3 a 6 com <b>Gilda como narradora</b>: «Com o passar dos meses, eu…». Usa a 1.ª pessoa e diz o que ela sente.</div></div></div>
  {lines(5)}
  <div style="margin-top:1.8mm">{chk_row(["1.ª pessoa do princípio ao fim", "sentimentos da Gilda", "um vocativo com vírgula", "um sujeito composto"])}</div>
</div>
''', station="2.8 · Amendoeiras")

# ================================================================ 25  STATION 2.9 OPENER — Saci (text part 1)
S1 = [
 'Nas fazendas do interior do Brasil, quando um redemoinho de vento levanta a poeira do terreiro, os mais velhos avisam logo as crianças:<br>— Cuidado! Lá dentro pode ir o Saci.',
 'O Saci-Pererê é um rapazinho negro, esperto como ninguém, que só tem <b>uma perna</b>. Não precisa de mais: anda aos saltos, tão depressa que ninguém o apanha. Na cabeça traz um <b>gorro vermelho</b> — e é esse gorro que lhe dá poderes. Com ele, aparece e desaparece quando quer e viaja dentro dos <b>redemoinhos</b>. Muitas vezes leva um cachimbo ao canto da boca. E assobia: um assobio fino, que parece vir de todo o lado e de lado nenhum.',
]
S2 = [
 'O Saci não é mau, mas adora pregar partidas. Na cozinha, troca o sal pelo açúcar e deixa queimar o feijão. Em casa, <b>esconde</b> a agulha da costureira, o dedal, a chave da porta. Nos caminhos, confunde os viajantes, que andam horas às voltas sem dar com a estrada. E, à noite, entra no curral, monta os cavalos, corre com eles até os deixar cansados e <b>faz-lhes tranças nas crinas</b>, tão apertadas que ninguém as consegue desfazer.',
 '— Foi o Saci! — dizem as pessoas quando, de manhã, encontram os cavalos suados e de crina entrançada, ou quando alguma coisa desaparece lá de casa.',
 'Mas há quem saiba como apanhá-lo. Quando se vê um redemoinho a rodar no terreiro, atira-se para o meio dele uma <b>peneira</b>, e o Saci fica preso. Então, tira-se-lhe o gorro vermelho: sem gorro, o Saci perde os poderes. Há quem conte que, para o reaver, ele promete fazer tudo o que lhe mandarem.',
 'Há mais de cem anos que os escritores brasileiros contam histórias do Saci. Em 1918, Monteiro Lobato publicou um livro com tudo o que os leitores de um jornal lhe tinham contado sobre ele. E, no estado de São Paulo e em várias cidades do Brasil, o dia <b>31 de outubro</b> é, por lei, o Dia do Saci: uma festa das lendas brasileiras.',
]
s1 = "".join(para(i, t, SEA) for i, t in enumerate(S1, 1))
s2 = "".join(para(i, t, SEA) for i, t in enumerate(S2, 3))
P[25] = page(25, f'''
<div class="kicker sea">Estação 2.9 · Lenda do Brasil</div>
<h2 style="margin-top:2mm">O Saci-<em>Pererê</em></h2>
<div style="margin-top:3.4mm">{pic("saci.jpg", 74, "40% 50%")}</div>
<div class="grid2" style="margin-top:4.2mm;grid-template-columns:1fr 1fr;gap:7mm;align-items:start">
  <div>
    <p class="lead" style="font-size:11pt">Há figuras que vivem na imaginação de um povo inteiro. No Brasil, uma das mais conhecidas é um rapazinho de uma perna só, que salta, assobia e faz partidas.</p>
    <div class="panel sea" style="margin-top:3.4mm;padding:3.2mm 3.8mm">
      <div class="kicker sea">De onde vem?</div>
      <p class="small" style="margin-top:1mm;line-height:1.42"><i>Saci</i> vem da língua <b>tupi</b>, e <i>pererê</i> quer dizer «ir aos saltos». A figura juntou crenças <b>indígenas</b>, <b>africanas</b> e <b>portuguesas</b>: o gorro vermelho lembra o do <b>trasgo</b>, um ser pequeno e traquinas das lendas de Trás-os-Montes.</p>
    </div>
    {act(1, "Ativar", 'Conheces outra figura do imaginário (de Portugal ou de outro país) que faz partidas? Qual?' + lines(2), "sea")}
  </div>
  <div>
    <div class="kicker sea">Texto 2 · O menino do redemoinho</div>
    <div class="reading" style="margin-top:2mm;padding-left:7.5mm">{s1}</div>
  </div>
</div>
<div class="kicker sea" style="margin-top:4mm">Palavras para levar</div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:1.6mm"><div style="border-top:1.2mm solid var(--sea);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">redemoinho</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">vento que gira depressa em espiral e levanta poeira e folhas</div></div><div style="border-top:1.2mm solid var(--sea);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">gorro</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">barrete de pano que cobre a cabeça</div></div><div style="border-top:1.2mm solid var(--sea);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">partida</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">brincadeira para enganar alguém, sem maldade</div></div><div style="border-top:1.2mm solid var(--sea);padding-top:1.4mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">fazenda</b><div class="small muted" style="line-height:1.3;margin-top:.3mm">grande propriedade agrícola, no Brasil</div></div></div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center;padding:3.4mm 4.5mm">
  <div><div class="kicker sea">Enquanto lês</div><p style="font-size:9.2pt;margin-top:1mm">Sublinha a <b class="sea">verde</b> as partes do corpo e os objetos do Saci; a <b class="coral">vermelho</b>, as partidas que ele faz.</p></div>
  {qr("q-saci", "Saber mais", "O Saci na Wikipédia:<br>nomes, origens, Dia do Saci.")}
</div>
''', station="2.9 · Saci")

# ================================================================ 26  SACI text part 2 + comprehension + oral
ev = [("A crina do cavalo aparece entrançada.", ""), ("Uma agulha ou uma chave desaparece.", ""), ("O feijão queima-se no lume.", ""),
      ("Um viajante perde-se no caminho.", ""), ("Um redemoinho levanta a poeira.", "")]
evh = "".join(f'<tr><td style="width:72mm;font-weight:400;color:var(--text);font-size:9pt">{a}</td><td style="height:7mm"></td></tr>' for a, _ in ev)
P[26] = page(26, f'''
<div style="display:grid;grid-template-columns:1fr 44mm;gap:6mm">
  <div class="reading" style="padding-left:7.5mm">{s2}
    <p class="src" style="margin-top:.8mm">Texto escrito para este manual, a partir das versões tradicionais. Fontes: L. da Câmara Cascudo, <i>Dicionário do Folclore Brasileiro</i> (verbete «Saci», citado em pt.wikipedia.org/wiki/Saci); Brasil Escola.</p></div>
  <aside style="border-left:.6pt solid var(--rule);padding-left:4.5mm">
    <div class="kicker sea">Glossário</div>
    {gloss([("terreiro", "espaço de terra batida em frente da casa."), ("curral", "lugar fechado onde se guarda o gado."), ("crina", "pelos compridos do pescoço do cavalo."), ("peneira", "utensílio com rede fina, para separar a farinha."), ("reaver", "voltar a ter.")])}
  </aside>
</div>
<div class="kicker sea" style="margin-top:1.4mm">Depois de ler</div>
<div class="grid2" style="gap:6mm;grid-template-columns:1.2fr 1fr">
  <div>{act(1, "Relacionar", 'Uma lenda explica o que acontece no dia a dia. Que explicação dá esta lenda para cada acontecimento?', "sea")}
  <table class="cmp ruled" style="margin-top:2mm">{th(["Acontecimento", "Explicação da lenda"], SEA)}{evh}</table></div>
  <div>{act(2, "Retratar", 'Completa: sem o <span class="fill"></span> o Saci perde os poderes; para o apanhar é preciso uma <span class="fill"></span>; viaja dentro dos <span class="fill"></span>.', "sea")}
  {act(3, "Interpretar", 'O Saci é uma <b>figura do imaginário</b>: ninguém o viu, mas toda a gente o conhece. Porque achas que as pessoas continuam a contar esta lenda?' + lines(2), "sea")}</div>
</div>
<div class="panel" style="margin-top:auto;padding:3.6mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{ico(MICRO, 8)}<div><div class="kicker sea">Oralidade · Conta a lenda e explica</div><div class="small muted">Conta a lenda do Saci em 1 minuto e meio, sem ler. No fim, diz que acontecimento ela explica: «Quando…, as pessoas dizem que…»</div></div></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:1.4mm;font-size:8.7pt;line-height:1.28">
    <div style="border-top:1.2mm solid var(--sea);padding-top:1.3mm"><b class="sea">1 · Quem é</b><br>aspeto e gorro</div>
    <div style="border-top:1.2mm solid var(--sea);padding-top:1.3mm"><b class="sea">2 · O que faz</b><br>duas partidas</div>
    <div style="border-top:1.2mm solid var(--sea);padding-top:1.3mm"><b class="sea">3 · Como se apanha</b><br>a peneira</div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.3mm"><b class="coral">4 · O que explica</b><br>«Quando…, dizem que…»</div>
  </div>
  <div style="margin-top:1.6mm;border-top:.6pt solid var(--rule);padding-top:1.4mm">{chk_row(["<b class=\"sea\">O colega avalia:</b> ordem certa", "voz expressiva", "não leu", "explicou o acontecimento"])}</div>
</div>
''', station="2.9 · Saci")

# ================================================================ 27  GRAMMAR (feminino, número, gerúndio) + INFORMATIVE TEXT
fem = [("-o → -a", "menino → menina"), ("-or → -ora", "contador → contadora"), ("-ão → -ã, -oa, -ona", "irmão → irmã · leão → leoa · comilão → comilona"),
       ("-ês → -esa", "português → portuguesa"), ("outra palavra", "cavalo → égua · rei → rainha"), ("só muda o determinante", "o / a artista · o / a estudante")]
num = [("+ s", "gorro → gorros"), ("-r, -z, -s → + es", "mar → mares · rapaz → rapazes"), ("-m → -ns", "homem → homens"),
       ("-ão → -ões, -ães, -ãos", "balão → balões · pão → pães · irmão → irmãos"), ("-al, -el, -ol, -ul → -is", "animal → animais · azul → azuis")]
AR = lambda t: t.replace("→", '<span style="font-family:Body">→</span>')
tb = lambda rows: "".join(f'<tr><td style="width:36mm;font-size:8.4pt;color:var(--sea);font-family:Body">{a}</td><td style="font-family:FrauncesText;font-size:9pt;color:var(--text);font-weight:400">{AR(b)}</td></tr>' for a, b in rows)
plan = [("§ 1", "Quem é e de onde vem"), ("§ 2", "Como é"), ("§ 3", "Poderes e partidas"), ("§ 4", "Como se apanha"), ("§ 5", "Uma curiosidade")]
plh = "".join(f'<div style="border-top:1.2mm solid var(--coral);padding-top:1.2mm"><b class="coral">{a}</b> <span style="font-size:8.4pt">{b}</span>{U(5.5)}{U(5.5)}</div>' for a, b in plan)
P[27] = page(27, f'''
<div class="kicker sea">Estação 2.9 · Gramática e escrita</div>
<h2 style="margin-top:2mm">Um Saci, duas <em>sacis</em>?</h2>
<div class="grid2" style="margin-top:3.2mm;gap:6mm">
  <div class="panel sea" style="padding:3.4mm 4mm"><div class="kicker sea">Feminino dos nomes</div>
    <table class="cmp" style="margin-top:1.4mm">{tb(fem)}</table>
    <p class="small" style="margin-top:1.4mm;line-height:1.35">Os <b>adjetivos</b> seguem regras parecidas (<i>esperto → esperta</i>), mas alguns têm uma só forma: <i>feliz, alegre, veloz</i>.</p></div>
  <div class="panel" style="padding:3.4mm 4mm"><div class="kicker">Número dos nomes e adjetivos</div>
    <table class="cmp" style="margin-top:1.4mm">{tb(num)}</table>
    <div class="rule-card c" style="margin-top:2mm;font-size:8.6pt;line-height:1.35"><b class="sea">Gerúndio</b> (-ndo): ação a decorrer. No Brasil diz-se <i>está <b>saltando</b></i>; em Portugal, mais vezes, <i>está <b>a saltar</b></i>.</div></div>
</div>
<div class="grid2" style="gap:6mm">
  <div>{act(1, "Transformar", 'Passa para o <b>feminino</b>: <div style="font-family:FrauncesText;font-size:9.8pt;margin-top:1.2mm">O rapaz esperto e brincalhão.</div>' + lines(1) + 'Agora passa esta frase para o <b>plural</b>: <div style="font-family:FrauncesText;font-size:9.8pt;margin-top:1.2mm">O cavalo cansado tem a crina azul.</div>' + lines(1), "sea")}</div>
  <div>{act(2, "Adaptar", 'Reescreve em português de Portugal.<div style="font-family:FrauncesText;font-size:9.8pt;margin-top:1.2mm">O Saci está assobiando no terreiro.</div>' + lines(1) + '<div style="font-family:FrauncesText;font-size:9.8pt;margin-top:1.2mm">Os meninos estão correndo atrás do redemoinho.</div>' + lines(1), "sea")}</div>
</div>
<div class="panel coral" style="margin-top:auto;padding:3.8mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{ico(LAPIS, 8)}<div><div class="kicker">Escrita · Texto informativo em parágrafos</div><div class="small muted"><b>Quem é o Saci-Pererê?</b> Escreve para um colega que nunca ouviu falar dele. Um parágrafo para cada ideia.</div></div></div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-top:2.2mm">{plh}</div>
  <div class="small muted" style="margin-top:2mm">O meu texto:</div>
  {lines(6)}
  <div style="margin-top:1.8mm">{chk_row(["um parágrafo por ideia", "informação do texto, não opinião", "um título", "um gerúndio ou «a + infinitivo»"])}</div>
</div>
''', station="2.9 · Saci")

# ================================================================ 28  CONSEGUES? — whole unit
TXT = ('— Avô, porque é que aquela pedra tem a forma de um barco? — perguntou a Rita.<br>'
       'O avô e a neta tinham subido ao monte ao fim da tarde. O velho sentou-se e contou: há muitos anos, um pescador e a mulher '
       'tinham perdido o barco numa tempestade. Nessa noite, o pescador pediu ao mar um abrigo para a família. De manhã, no alto do monte, '
       'estava uma pedra enorme, com a forma de um barco virado, onde nenhuma onda chegava.<br>'
       '— E eles foram morar lá? — Foram. E ainda hoje, quando o vento sopra, parece que se ouvem remos a bater.')
gen = [("mito", "Dédalo e Ícaro"), ("adaptação de um clássico", "Ulisses"), ("conto maravilhoso", "A Fada Oriana"), ("narrativa longa", "O Cavaleiro da Dinamarca"), ("lenda", "O Saci-Pererê")]
genh = "".join(f'<div style="display:grid;grid-template-columns:1fr 7mm 1fr;align-items:center;font-size:8.6pt;margin-top:1.1mm"><span>{chr(97+i)}) <i>{b}</i></span><span class="chk" style="margin:0 auto"></span><span class="muted">{i+1}. {a}</span></div>' for i, (a, b) in enumerate(gen))
cando = ["Distingo mito, lenda, conto e narrativa longa.", "Explico o que uma lenda diz sobre um lugar.", "Apresento um episódio com notas, sem ler.",
         "Uso o mais-que-perfeito e o particípio.", "Encontro o CD, o CI, o sujeito e o vocativo.", "Formo palavras por derivação e composição."]
cah = "".join(f'<div style="display:grid;grid-template-columns:1fr 7mm 7mm 7mm;align-items:center;gap:1mm;font-size:8.5pt;padding:1.2mm 0;border-top:.6pt solid var(--rule)"><span>{c}</span><span class="chk" style="margin:0 auto"></span><span class="chk" style="margin:0 auto"></span><span class="chk o" style="margin:0 auto"></span></div>' for c in cando)
cahd = '<div style="display:grid;grid-template-columns:1fr 7mm 7mm 7mm;gap:1mm;font-family:Grotesk;font-size:6.4pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:center"><span></span><span>sim</span><span>quase</span><span class="coral">ainda<br>não</span></div>'

q = lambda n, v, h: act(n, v, h)
P[28] = page(28, f'''
<div class="kicker">Chegada · Unidade 2</div>
<h2 style="margin-top:1.6mm">Consegues?</h2>
<div class="panel" style="margin-top:2mm;padding:2.8mm 4.2mm"><div class="reading">{TXT} <span class="src">Texto escrito para esta revisão.</span></div></div><style>.page[data-n="28"] .act{{margin-top:3mm}}</style>
<div class="grid2" style="gap:6mm;grid-template-columns:1fr 1fr">
<div>
{q(1, "Classificar", 'Este texto é uma <span class="fill"></span>, porque explica <span class="fill l"></span>. Liga cada texto da unidade ao seu género (escreve o número).' + genh)}
{q(2, "Mais-que-perfeito", 'Copia duas formas do <b>mais-que-perfeito composto</b>. Passa uma delas para a forma simples.' + lines(2))}
{q(3, "Verbo e complementos", 'Em «o pescador pediu ao mar um abrigo», o verbo é <span class="fill s"></span>, o CD é <span class="fill"></span> e o CI é <span class="fill"></span>. «O velho sentou-se»: o verbo <i>sentar-se</i> é transitivo ou intransitivo? <span class="fill"></span>')}
{q(4, "Auxiliar e particípio", 'Em «tinham perdido», qual é o verbo auxiliar e qual é o particípio passado?' + lines(1))}
</div>
<div>
{q(5, "Sujeito e vocativo", 'Sublinha o sujeito composto e rodeia o vocativo. Porque é que o vocativo tem vírgula?' + lines(1))}
{q(6, "Tratamento", 'Reescreve a pergunta da Rita, dirigida a um senhor que ela não conhece.' + lines(1))}
{q(7, "Palavras", 'Separa radical e sufixo: <i>pescador</i> <span class="fill"></span> · Escreve uma palavra composta com <i>guarda-</i> <span class="fill"></span>')}
{q(8, "Flexão e gerúndio", 'Passa para o plural: <i>uma pedra enorme</i> <span class="fill l"></span>. Escreve o gerúndio de <i>soprar</i> <span class="fill"></span>')}
</div>
</div>
<div class="panel blue" style="margin-top:auto;padding:3mm 4.2mm"><div style="display:flex;justify-content:space-between;align-items:end"><div class="kicker blue">Autoavaliação · Consigo…</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 6mm;margin-top:1mm">{cahd}{cahd}{cah}</div></div>
''', station="Chegada")
