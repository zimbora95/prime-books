"""Front matter (pp. 1-6) and back matter (last 3 pages) of Farol · Português 6.

Everything a reader can check against the book is COMPUTED from the unit modules,
never retyped: the contents (stations, headings, page numbers), the glossary page
references, the list of sources and the QR targets (decoded from the QR images).
Build:  MODS=fm TAG=fm UNIT=fm ../.venv/bin/python build.py
"""
import importlib, os, re, html as H
import parts
from parts import *

# ------------------------------------------------------------------ the volume
UNITS = [  # (n, modules)
    (0, ("u0_a",)), (1, ("pages_a", "pages_b", "pages_c")), (2, ("u2_a", "u2_b")),
    (3, ("u3_a", "u3_b")), (4, ("u4_a", "u4_b")), (5, ("u5_a",)), (6, ("u6_a",)), (7, ("u7_a",)),
]
FRONT = 6          # pp. 1-6
BACK = 3           # glossary, sources, back cover
UC = {0: "#2E8C7B", 1: "#17315A", 2: "#E4502F", 3: "#6B4E9B", 4: "#B7791F", 5: "#3F7FB5", 6: "#9A3B3B", 7: "#5E8C3A"}
UCS = {0: "#D5EEE7", 1: "#DCE5F0", 2: "#FBE1D8", 3: "#E8E0F2", 4: "#F5E7CC", 5: "#DDEAF5", 6: "#F2DCDC", 7: "#E2ECD8"}

strip = lambda s: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def load():
    data, start = [], FRONT + 1
    for n, mods in UNITS:
        pages = {}
        for m in mods:
            if importlib.util.find_spec(m) is None:
                continue
            try:                      # a unit still being written must not break the front matter
                mod = importlib.import_module(m)
                pages.update(mod.P)
            except Exception as e:
                print(f"fm: skipped {m}: {e.__class__.__name__}: {e}")
        if not pages:
            data.append(dict(n=n, pages={}, start=start, total=0)); continue
        total = max(pages)
        data.append(dict(n=n, pages=pages, start=start, total=total))
        start += total
    parts.UNIT.update(n="fm", total=10)
    return data, start - 1


DATA, LAST_UNIT_PAGE = load()
TOTAL = LAST_UNIT_PAGE + BACK


def info(u):
    """Title, genre kicker and the station list of a unit, read from its pages."""
    ps = u["pages"]
    if not ps:
        return dict(title="(em preparação)", kicker="", stations=[])
    p1 = ps[min(ps)]
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", p1, re.S)
    title = strip(h1.group(1).replace("<br>", " ")) if h1 else f"Unidade {u['n']}"
    kick = re.search(r'class="kicker[^"]*">(Unidade[^<]*)<', p1) or next(
        (re.search(r'class="kicker[^"]*">(Unidade[^<]*)<', ps[k]) for k in sorted(ps) if re.search(r'class="kicker[^"]*">(Unidade[^<]*)<', ps[k])), None)
    kicker = strip(kick.group(1)) if kick else f"Unidade {u['n']}"
    st, seen = [], set()
    for k in sorted(ps):
        m = re.search(r'class="station[^"]*">([^<]*)<', ps[k])
        s = strip(m.group(1)) if m else ""
        if not s or s in ("A rota", "Partida") or s in seen:
            continue
        seen.add(s)
        h = re.search(r"<h[12][^>]*>(.*?)</h[12]>", ps[k], re.S)
        st.append((s, strip(h.group(1).replace("<br>", " ")) if h else "", k + u["start"] - 1))
    return dict(title=title, kicker=kicker, stations=st)


INFO = {u["n"]: info(u) for u in DATA}


def fol(n, side=None):
    side = side or ("odd" if n % 2 else "even")
    pos = "right:14mm" if side == "odd" else "left:14mm"
    return (f'<div style="position:absolute;bottom:9mm;{pos};width:9mm;height:9mm;border-radius:50%;background:var(--ink);'
            f'color:#fff;font-family:Fraunces;font-weight:700;font-size:10.5pt;display:flex;align-items:center;justify-content:center">{n}</div>')


def fmpage(n, body, cls=""):
    side = "odd" if n % 2 else "even"
    lr = "left:23.5mm;right:20mm" if side == "odd" else "left:20mm;right:23.5mm"   # gutter side wider (BookVault 20 mm)
    return (f'<section class="page {side} fm {cls}" data-n="{n}"><div class="live" style="{lr};top:16mm;bottom:22mm;display:flex;flex-direction:column">'
            f'{body}</div>{fol(n)}</section>')


def head(kicker, title, color="var(--ink)"):
    return (f'<div style="display:flex;align-items:flex-end;justify-content:space-between;border-bottom:1.2pt solid {color};padding-bottom:3mm">'
            f'<div><div class="kicker" style="color:{color}">{kicker}</div><h1 style="font-size:30pt;margin-top:1mm">{title}</h1></div>'
            f'<img src="img/logo.png" style="width:13mm;height:13mm"></div>')


P = {}

# =============================================================== 1 COVER
P[1] = f'''<section class="page odd fm" data-n="1">
<div class="full" style="background:#F2E4D0"><img class="cover" src="img/capa.jpg" style="object-position:30% 50%"></div>
<div style="position:absolute;right:16mm;top:16mm;width:104mm;text-align:right">
  <div style="font-family:Grotesk;font-weight:700;letter-spacing:.34em;font-size:9pt;color:var(--ink)">PRIME SCHOOL PRESS</div>
  <div style="font-family:Fraunces;font-weight:700;font-size:92pt;line-height:.86;color:var(--ink);margin-top:6mm;letter-spacing:-.01em">Farol</div>
  <div style="height:1.4mm;width:30mm;background:var(--coral);margin:5mm 0 0 auto"></div>
  <div style="font-family:FrauncesText;font-weight:700;font-size:22pt;color:var(--ink);margin-top:4mm">Português · 6.º ano</div>
</div>
<div style="position:absolute;left:16mm;bottom:13mm;display:flex;align-items:center;gap:3mm;background:rgba(255,253,249,.92);padding:2.4mm 4mm 2.4mm 2.6mm;border-radius:2mm">
  <img src="img/logo.png" style="width:10mm;height:10mm">
  <div style="font-family:Grotesk;font-size:7.6pt;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);line-height:1.45"><b>Manual do aluno</b><br>Prime School · Portugal</div>
</div>
</section>'''

# =============================================================== 2 IMPRINT
rows = [
    ("Título", "<i>Farol · Português 6</i> — manual do aluno do 6.º ano de escolaridade."),
    ("Edição", f"1.ª edição, 2026. Formato 216 × 279 mm, impressão a cores, {TOTAL} páginas."),
    ("Editora", "A Prime School Press é a chancela editorial da Prime School, Portugal."),
    ("Direitos", "© Prime School 2026. Todos os direitos reservados. Nenhuma parte desta publicação pode ser reproduzida, armazenada ou transmitida, por qualquer forma ou meio, sem autorização prévia e escrita do editor."),
    ("Textos", "Os textos originais desta edição — entrevistas, peças, poemas, notícias e textos de revisão — foram escritos para este manual e estão assinalados como tal. "
               "As obras protegidas de Eugénio de Andrade, Maria Alberta Menéres, Sophia de Mello Breyner Andresen e Mia Couto aparecem apenas em citações breves, com o nome do autor e da obra, "
               "ao abrigo do direito de citação para fins de ensino (Código do Direito de Autor e dos Direitos Conexos, art. 75.º); as obras completas leem-se na edição da turma. "
               "O romance <i>Bela Infanta</i> segue a recolha de Almeida Garrett (domínio público); os mitos e as lendas são recontados por nós."),
    ("Imagens", "Ilustrações criadas para esta edição com ferramentas digitais e revistas pela equipa editorial; não retratam pessoas reais. Esquemas e mapas desenhados para o manual."),
    ("Códigos QR", "Todos os códigos QR levam a páginas de instituições e enciclopédias públicas (Diário da República, Wikipédia, organismos oficiais), verificadas à data da edição. Nenhum depende do sítio de desenvolvimento deste manual."),
    ("Tipografia", "Fraunces, Instrument Sans, Space Grotesk e Caveat (SIL Open Font License), incorporadas no ficheiro."),
    ("Língua", "Português europeu, segundo o Acordo Ortográfico de 1990."),
    ("Créditos", "Conselho Editorial: Grupo Académico Pedagógico · Equipa Pedagógica · Departamento Pedagógico · Equipa de Criação de Conteúdos. Escrito, ilustrado e paginado no estúdio da Prime School Press."),
    ("ISBN", "A atribuir na primeira impressão."),
]
rowhtml = "".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:4mm;padding:2.6mm 0;border-top:.5pt dotted #B9C3D1">'
                  f'<div style="font-family:Grotesk;font-weight:700;font-size:7.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:.6mm">{k}</div>'
                  f'<div style="font-size:9.2pt;line-height:1.45">{v}</div></div>' for k, v in rows)
P[2] = fmpage(2, f'''
{head("Prime School Press", "Farol <em>·</em> Português 6")}
<p class="lead" style="margin-top:5mm;font-size:11.4pt">Um farol não faz a viagem por ti: mostra a costa, avisa dos rochedos e deixa-te escolher o rumo. Este manual quer ser isso — uma luz para leres, escreveres e falares com confiança.</p>
<div style="margin-top:5mm;border:1pt solid var(--ink);border-radius:2mm;padding:1mm 5mm 2mm;position:relative">
  <div style="position:absolute;top:-3.4mm;left:5mm;background:var(--ink);color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.2em;padding:1mm 3mm;border-radius:1mm">FICHA TÉCNICA</div>
  <div style="margin-top:3mm">{rowhtml}</div>
</div>
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;border-top:.6pt solid #D8D2C6;padding-top:3mm;font-size:8pt;color:var(--muted)">
  <div style="max-width:120mm;line-height:1.45">A Prime School é uma escola independente. Este manual foi concebido para o percurso da escola e não é um manual certificado pelo Ministério da Educação.</div>
  <div style="text-align:right;font-family:Grotesk;font-weight:700;letter-spacing:.1em;color:var(--ink)">PRIME SCHOOL PRESS<br><span style="font-weight:500;color:var(--coral)">primeschool.pt</span></div>
</div>''')

# =============================================================== 3 HOW TO USE
def key(icon, title, text, color):
    return (f'<div style="display:grid;grid-template-columns:13mm 1fr;gap:3mm;align-items:start">'
            f'<div style="width:13mm;height:13mm">{icon}</div><div><b style="color:{color};font-family:FrauncesText;font-size:11pt">{title}</b>'
            f'<p style="font-size:9.2pt;line-height:1.42;margin-top:.6mm">{text}</p></div></div>')

tide_demo = ('<svg viewBox="0 0 40 120" style="width:13mm;height:38mm;display:block"><rect width="40" height="120" fill="#F4EDE1"/>'
             '<rect y="70" width="40" height="50" fill="#17315A"/><path d="M0 70 q5 -4 10 0 t10 0 t10 0 t10 0" fill="#17315A"/>'
             '<text x="20" y="112" font-family="Fraunces" font-weight="700" font-size="12" fill="#fff" text-anchor="middle">42</text></svg>')
P[3] = fmpage(3, f'''
{head("Antes de zarpar", "Como usar o <em>Farol</em>")}
<p class="lead" style="margin-top:5mm;font-size:11pt">Cada unidade é uma viagem por estações. Estes sinais repetem-se em todo o livro: aprende-os agora e vais orientar-te sempre.</p>
<div class="grid2" style="margin-top:6mm;gap:6mm 9mm">
  {key(LUPA, "Informar", "Textos que explicam e dão a conhecer: o expositivo, a divulgação, a entrevista.", "var(--ink)")}
  {key(MEGA, "Convencer", "Textos que defendem uma opinião com argumentos: o artigo de opinião, o debate.", "var(--coral)")}
  {key(PONTE, "Ligar", "Conectores e ferramentas de gramática que ligam as ideias e as frases.", "var(--sea)")}
  {key(MICRO, "Ouvir e falar", "Atividades de oralidade: ouvir, ler em voz alta, apresentar, debater.", "var(--ink)")}
  {key(LAPIS, "Escrever", "Planear, escrever, rever e passar a limpo, sempre com uma lista de verificação.", "var(--coral)")}
  <div style="display:grid;grid-template-columns:13mm 1fr;gap:3mm;align-items:start"><div style="width:13mm;height:13mm;border-radius:50%;background:var(--ink);color:#fff;font-family:Fraunces;font-weight:700;font-size:13pt;display:flex;align-items:center;justify-content:center">1</div>
  <div><b style="color:var(--ink);font-family:FrauncesText;font-size:11pt">Atividades numeradas</b><p style="font-size:9.2pt;line-height:1.42;margin-top:.6mm">Cada atividade começa por um verbo — <i>Ler</i>, <i>Explicar</i>, <i>Opinar</i> — que te diz o que fazer. Responde sempre nas linhas.</p></div></div>
</div>
<div class="grid2" style="margin-top:7mm;gap:9mm;grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="panel" style="display:grid;grid-template-columns:15mm 1fr;gap:4mm;align-items:center">{tide_demo}
    <div><div class="kicker">A maré</div><p style="font-size:9.2pt;line-height:1.45;margin-top:1mm">A barra na margem da página sobe à medida que avanças na unidade. Nela lês o nome da estação e o número da página. Quando a maré está cheia, chegaste ao <b>Consegues?</b>.</p></div></div>
  <div class="panel sea" style="display:grid;grid-template-columns:17mm 1fr;gap:4mm;align-items:center">
    <img src="img/q-canhao.svg" style="width:17mm;height:17mm">
    <div><div class="kicker sea">Os códigos QR</div><p style="font-size:9.2pt;line-height:1.45;margin-top:1mm">Aponta a câmara de um telemóvel ou tablet para veres a fonte de um facto, um documento oficial ou mais informação. Pede sempre autorização a um adulto.</p></div></div>
</div>
<div style="margin-top:auto" class="panel coral">
  <div class="kicker">Cada unidade tem</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:2mm;font-size:9pt;line-height:1.4">
    <div><b class="coral">Partida</b><br>uma imagem de abertura e as perguntas da viagem.</div>
    <div><b class="coral">A rota</b><br>o mapa da unidade: textos, estações e páginas.</div>
    <div><b class="coral">Estações</b><br>ler, compreender, gramática, escrever e falar.</div>
    <div><b class="coral">Consegues?</b><br>mostras o que aprendeste e avalias-te.</div>
  </div>
</div>''')

# =============================================================== 4-5 CONTENTS
bar = "".join(f'<div style="flex:{max(u["total"],1)};background:{UC[u["n"]]};height:100%" title="U{u["n"]}"></div>' for u in DATA)
def card(u):
    i = INFO[u["n"]]; c, cs = UC[u["n"]], UCS[u["n"]]
    end = u["start"] + max(u["total"], 1) - 1
    rows = "".join(f'<div style="display:grid;grid-template-columns:1fr 9mm;gap:2mm;padding:.6mm 0;border-top:.4pt dotted rgba(23,49,90,.28)">'
                   f'<div style="font-size:8.6pt;line-height:1.3"><b style="color:{c}">{H.escape(s)}</b>{(" — " + H.escape(t)) if t and t != s else ""}</div>'
                   f'<div style="text-align:right;font-family:Grotesk;font-weight:700;font-size:8.4pt;color:{c}">{p}</div></div>' for s, t, p in i["stations"])
    return (f'<div style="background:{cs};border-radius:2.4mm;padding:2.8mm 4.4mm 2.6mm;display:grid;grid-template-columns:17mm 1fr;gap:4mm">'
            f'<div><div style="font-family:Fraunces;font-weight:700;font-size:34pt;line-height:.9;color:{c}">{u["n"]}</div>'
            f'<div style="height:1.2mm;background:{c};margin-top:2mm;width:12mm"></div>'
            f'<div style="font-family:Grotesk;font-weight:700;font-size:8pt;color:{c};margin-top:2mm">pp. {u["start"]}–{end}</div></div>'
            f'<div><div class="kicker" style="color:{c}">{H.escape(i["kicker"])}</div>'
            f'<div style="font-family:FrauncesText;font-weight:700;font-size:13.4pt;color:var(--ink);margin:.6mm 0 1.4mm">{H.escape(i["title"])}</div>{rows}</div></div>')

split = 3   # U0-U2 on p. 4 (U1 and U2 carry the most stations), U3-U7 on p. 5
left, right = DATA[:split], DATA[split:]
P[4] = fmpage(4, f'''
{head("Índice", "O que vais <em>encontrar</em>")}
<div style="display:flex;height:3mm;border-radius:1.5mm;overflow:hidden;margin-top:4mm">{bar}</div>
<div style="display:flex;flex-direction:column;gap:3.6mm;margin-top:5mm">{"".join(card(u) for u in left)}</div>''')
P[5] = fmpage(5, f'''
<div style="display:flex;height:3mm;border-radius:1.5mm;overflow:hidden">{bar}</div>
<div style="display:flex;flex-direction:column;gap:2.6mm;margin-top:4mm">{"".join(card(u) for u in right)}</div>
<div style="margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm">
  <div class="panel" style="padding:3mm 4mm"><div class="kicker">No fim do livro</div><div style="display:flex;justify-content:space-between;font-size:9pt;margin-top:1mm"><span>Glossário</span><b>{LAST_UNIT_PAGE + 1}</b></div><div style="display:flex;justify-content:space-between;font-size:9pt"><span>Fontes e créditos</span><b>{LAST_UNIT_PAGE + 2}</b></div></div>
  <div class="panel" style="padding:3mm 4mm;grid-column:span 2"><div class="kicker">Antes de começar</div><div style="display:flex;justify-content:space-between;font-size:9pt;margin-top:1mm"><span>Como usar o <i>Farol</i></span><b>3</b></div><div style="display:flex;justify-content:space-between;font-size:9pt"><span>A escada de leitura do ano</span><b>6</b></div></div>
</div>''')

# =============================================================== 6 READING LADDER
def dots(c):
    one = f'<span style="width:4.4mm;height:4.4mm;border:.8pt solid {c};border-radius:50%;display:inline-block"></span>'
    return one * 5


LADDER = [  # (unit, what, genre) — the texts a pupil actually reads this year, in book order
    (0, "A noite do faroleiro", "narrativa"), (1, "O Canhão da Nazaré", "texto expositivo"), (1, "Os vizinhos do canhão", "divulgação"),
    (1, "«O mar da Nazaré guarda um segredo no fundo»", "entrevista"), (1, "Duas opiniões, o mesmo mar", "opinião"),
    (2, "Dédalo e Ícaro · Ulisses · A Fada Oriana", "mito e clássicos"), (2, "O Cavaleiro da Dinamarca · O Beijo da Palavrinha", "narrativas de autor"),
    (2, "Lenda das amendoeiras · Saci-Pererê", "lendas"), (3, "Bela Infanta", "romance tradicional"), (3, "Eugénio de Andrade · Canção do calceteiro", "poesia"),
    (4, "O julgamento da escolha · Ícaro em cena", "texto dramático"), (7, "Três obras à tua escolha", "leitura autónoma"),
]
rungs = "".join(
    f'<div style="display:grid;grid-template-columns:9mm 1fr 34mm 30mm;gap:3mm;align-items:center;padding:2.1mm 0;border-top:.5pt solid #E3DCCD">'
    f'<div style="width:7mm;height:7mm;border-radius:50%;background:{UC[u]};color:#fff;font-family:Fraunces;font-weight:700;font-size:9pt;display:flex;align-items:center;justify-content:center">{u}</div>'
    f'<div style="font-family:FrauncesText;font-weight:700;font-size:10pt;color:var(--ink)">{t}</div>'
    f'<div class="small muted">{g}</div>'
    f'<div style="display:flex;gap:1.6mm">{dots(UC[u])}</div></div>'
    for u, t, g in LADDER)
P[6] = fmpage(6, f'''
{head("O meu ano", "A escada de <em>leitura</em>")}
<div class="grid2" style="margin-top:5mm;gap:8mm;grid-template-columns:1fr 62mm;align-items:start">
  <p class="lead" style="font-size:11pt">Estes são os textos que vais ler este ano, degrau a degrau. Quando acabares cada um, pinta os círculos: <b>um</b> se não gostaste, <b>cinco</b> se o recomendas a toda a gente.</p>
  <div class="panel" style="padding:3mm 4mm"><div class="kicker">Este livro pertence a</div><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:8mm"></span><div class="small muted" style="margin-top:2mm">Turma · Ano letivo</div><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:7mm"></span></div>
</div>
<div style="margin-top:5mm">{rungs}</div>
<div class="grid2" style="margin-top:auto;gap:6mm">
  <div class="panel coral"><div class="kicker">O texto de que mais gostei</div><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:7mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:7mm"></span></div>
  <div class="panel blue"><div class="kicker blue">Um livro que quero ler a seguir</div><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:7mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:7mm"></span></div>
</div>''')

# =============================================================== GLOSSARY
GLOSS = [  # term, definition, search key (first page that teaches it)
    ("Texto expositivo", "Texto que explica um assunto de forma clara e objetiva, organizado em introdução, desenvolvimento e conclusão.", "Raio-X de um texto que explica"),
    ("Texto de divulgação", "Texto que dá a conhecer ciência ou cultura a um público alargado, de forma rigorosa mas acessível.", "Informar a explicar, informar a encantar"),
    ("Entrevista", "Texto construído com perguntas de um entrevistador e respostas de um entrevistado, precedido de uma apresentação.", "Por dentro de uma entrevista"),
    ("Texto de opinião", "Texto em que o autor defende um ponto de vista com argumentos e exemplos, e termina com uma conclusão.", "O esqueleto de um texto de opinião"),
    ("Argumento", "Razão apresentada para defender uma opinião; é mais forte quando é apoiado por um facto ou um exemplo.", "Argumento forte ou argumento fraco?"),
    ("Conector", "Palavra ou expressão que liga frases e ideias e mostra a relação entre elas (causa, oposição, conclusão…).", "Palavras que ligam ideias"),
    ("Mito", "Narrativa tradicional que explica a origem do mundo, dos fenómenos ou dos comportamentos, com deuses e heróis.", "mito"),
    ("Lenda", "Narrativa tradicional que mistura factos e elementos fantásticos para explicar a origem de um lugar ou de um costume.", "lenda"),
    ("Pretérito mais-que-perfeito", "Tempo verbal que indica uma ação anterior a outra, já passada: <i>fizera</i> (simples), <i>tinha feito</i> (composto).", "mais-que-perfeito"),
    ("Romance tradicional", "Poema narrativo de origem popular, transmitido oralmente, que conta uma história em verso.", "A espera, a prova"),
    ("Verso · estrofe · rima", "O verso é cada linha do poema; a estrofe é um conjunto de versos; a rima é a igualdade de sons no fim dos versos.", "O que o poeta vê a mais"),
    ("Metáfora", "Relação de semelhança entre duas realidades, sem palavra de comparação: <i>o mar é um espelho</i>.", "A oficina das metáforas"),
    ("Comparação", "Relação de semelhança expressa com <i>como</i>, <i>tal como</i>, <i>parece</i>: <i>o mar brilha como um espelho</i>.", "A oficina das metáforas"),
    ("Refrão", "Verso ou conjunto de versos que se repete ao longo do poema ou da canção.", "Ritmo, repetição e voz"),
    ("Gerúndio", "Forma do verbo terminada em <i>-ndo</i> que exprime uma ação em curso: <i>cantando</i>, <i>batendo</i>.", "O gerúndio e as vírgulas da lista"),
    ("Texto dramático", "Texto escrito para ser representado, com falas das personagens e indicações cénicas.", "Anatomia do texto dramático"),
    ("Indicação cénica (didascália)", "Informação, em itálico e entre parênteses, sobre gestos, tom, espaço, luz ou som.", "Anatomia do texto dramático"),
    ("Aparte", "Fala que uma personagem diz para o público, sem que as outras personagens a oiçam.", "Anatomia do texto dramático"),
    ("Frase simples · frase complexa", "A frase simples tem uma só forma verbal; a complexa tem mais do que uma.", "Frase simples, frase complexa"),
    ("Vocativo", "Palavra ou expressão usada para chamar ou interpelar alguém; separa-se por vírgula: <i>Inês, espera!</i>", "Frase simples, frase complexa"),
    ("Verbo transitivo · intransitivo", "O transitivo precisa de um complemento (<i>Ulisses cegou o Ciclope</i>); o intransitivo tem sentido completo (<i>O barco partiu</i>).", "transitivo"),
    ("Verbo auxiliar", "Verbo que se junta a outro para formar tempos compostos ou a voz passiva: <i>ter</i>, <i>haver</i>, <i>ser</i>, <i>estar</i>.", "auxiliar"),
    ("Particípio passado", "Forma do verbo que termina geralmente em <i>-ado</i> ou <i>-ido</i> e se usa com os auxiliares: <i>tinha partido</i>.", "particípio"),
    ("Formas de tratamento", "Modos de nos dirigirmos a alguém, conforme a relação e a situação: <i>tu</i>, <i>você</i>, <i>o senhor</i>, <i>Vossa Excelência</i>.", "formas de tratamento"),
    ("Radical · afixos", "O radical é a parte da palavra que tem o sentido principal; os afixos (prefixos e sufixos) juntam-se-lhe: <i>in-feliz-mente</i>.", "radical"),
    ("Composição", "Formação de uma palavra nova pela junção de duas ou mais palavras ou radicais: <i>guarda-chuva</i>, <i>girassol</i>.", "composição"),
    ("Sujeito simples · composto", "O sujeito simples tem um só núcleo; o composto tem dois ou mais: <i>O rei e a princesa</i> olhavam o campo.", "sujeito composto"),
    ("Complemento direto", "Constituinte que completa o verbo sem preposição e pode ser substituído por <i>o, a, os, as</i>.", "Quem dá o quê a quem?"),
    ("Complemento indireto", "Constituinte que completa o verbo com a preposição <i>a</i> e pode ser substituído por <i>lhe, lhes</i>.", "Quem dá o quê a quem?"),
]


def where(keytext):
    k = keytext.lower()
    best = None
    for u in DATA:
        for n in sorted(u["pages"]):
            b = u["pages"][n]
            heads = " ".join(strip(x) for x in re.findall(r"<h[123][^>]*>(.*?)</h[123]>", b, re.S)).lower()
            if k in heads:
                return n + u["start"] - 1
            if best is None and k in strip(b).lower():
                best = n + u["start"] - 1
    return best


gl = []
for t, d, k in sorted(GLOSS, key=lambda g: where(g[2]) or 10**6):
    p = where(k)
    if p is None:
        continue
    gl.append(f'<div style="break-inside:avoid;padding:1.1mm 0;border-top:.4pt dotted #B9C3D1"><div style="display:flex;justify-content:space-between;gap:3mm">'
              f'<b style="font-family:FrauncesText;font-size:9.6pt;color:var(--ink)">{t}</b><span style="font-family:Grotesk;font-weight:700;font-size:8pt;color:var(--coral)">p. {p}</span></div>'
              f'<div style="font-size:8.4pt;line-height:1.32;margin-top:.2mm">{d}</div></div>')
G = LAST_UNIT_PAGE + 1
P[G] = fmpage(G, f'''
{head("No fim da viagem", "Glossário")}
<p class="small muted" style="margin-top:3mm">Os termos que aprendeste este ano, por ordem de chegada, com a página onde os estudaste.</p>
<div style="column-count:2;column-gap:9mm;margin-top:3mm">{"".join(gl)}</div>''')

# =============================================================== SOURCES & CREDITS
def qr_url(key):
    try:
        import pymupdf, numpy as np, cv2
        s = pymupdf.open(f"img/{key}.svg"); pdf = pymupdf.open("pdf", s.convert_to_pdf())
        out = pymupdf.open(); p = out.new_page(width=300, height=300); p.show_pdf_page(pymupdf.Rect(40, 40, 260, 260), pdf, 0)
        px = p.get_pixmap(dpi=200); a = np.frombuffer(px.samples, np.uint8).reshape(px.height, px.width, px.n)[:, :, :3].copy()
        return cv2.QRCodeDetector().detectAndDecode(a)[0] or "?"
    except Exception as e:  # pragma: no cover
        return f"? ({e})"


blocks, qrs = [], []
for u in DATA:
    srcs = []
    for n in sorted(u["pages"]):
        b = u["pages"][n]; gp = n + u["start"] - 1
        for m in re.finditer(r'<p class="src"[^>]*>(.*?)</p>', b, re.S):
            t = strip(m.group(1))
            if t and t not in [x[1] for x in srcs]:
                srcs.append((gp, t))
        for m in re.finditer(r'<img src="img/(q-[\w-]+)\.svg"', b):
            if m.group(1) != "q-canhao" or u["n"] == 1:
                qrs.append((gp, m.group(1)))
    if srcs:
        blocks.append(f'<div style="break-inside:avoid;margin-bottom:2.6mm"><div class="kicker" style="color:{UC[u["n"]]}">Unidade {u["n"]}</div>'
                      + "".join(f'<div style="font-size:7.6pt;line-height:1.3;margin-top:.6mm"><b style="font-family:Grotesk;color:{UC[u["n"]]}">p. {p}</b> {H.escape(t)}</div>' for p, t in srcs) + "</div>")
seen, qrrows = set(), []
for p, k in qrs:
    if k in seen:
        continue
    seen.add(k)
    url = qr_url(k)
    qrrows.append(f'<div style="display:grid;grid-template-columns:9mm 1fr;gap:2mm;font-size:7.6pt;line-height:1.3;padding:.7mm 0;border-top:.4pt dotted #B9C3D1"><b style="font-family:Grotesk;color:var(--coral)">p. {p}</b><span style="word-break:break-all">{H.escape(url)}</span></div>')
S = LAST_UNIT_PAGE + 2
P[S] = fmpage(S, f'''
{head("Para verificar", "Fontes <em>e</em> créditos")}
<div style="column-count:2;column-gap:8mm;margin-top:4mm">{"".join(blocks)}</div>
<div class="panel sea" style="margin-top:auto;padding:3mm 4mm"><div class="kicker sea">Os códigos QR deste livro</div>
<div style="column-count:2;column-gap:8mm;margin-top:1.4mm">{"".join(qrrows)}</div></div>''')

# =============================================================== BACK COVER
B = TOTAL
bul = ["Oito unidades: do texto expositivo e da opinião ao mito, à poesia e ao teatro.",
       "Textos originais, clássicos portugueses e literaturas de língua portuguesa.",
       "Gramática em contexto, com fichas claras e atividades graduadas.",
       "Oralidade e escrita com planificação, revisão e grelhas de avaliação.",
       "Códigos QR para fontes verificadas; um projeto de leitura autónoma para o ano inteiro."]
P[B] = f'''<section class="page even fm" data-n="{B}">
<div class="full" style="background:var(--sand)"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:11mm;background:var(--ink)"></div>
<div style="position:absolute;left:28mm;right:24mm;top:24mm">
  <div style="font-family:Grotesk;font-weight:700;font-size:9pt;letter-spacing:.34em;color:#6B6B5E">P R I M E&nbsp;&nbsp;S C H O O L&nbsp;&nbsp;P R E S S</div>
  <div style="font-family:Fraunces;font-weight:700;font-size:44pt;line-height:1;color:var(--ink);margin-top:5mm">Farol <span style="color:var(--coral)">·</span> Português 6</div>
  <div style="width:9mm;height:1.2mm;background:var(--coral);margin-top:5mm"></div>
  <div style="font-family:Body;font-size:11pt;color:#5B6475;margin-top:3mm">6.º Ano · Prime School Press · Manual do aluno</div>
  <p style="font-family:FrauncesText;font-size:12.6pt;line-height:1.5;color:#2E2A24;margin-top:7mm;max-width:150mm">Um farol não faz a viagem por ti: mostra a costa e deixa-te escolher o rumo. Neste manual, lês para saber e para sentir, escreves para explicar e para convencer, e aprendes a dar voz a romances, poemas e peças de teatro.</p>
  <div style="margin-top:9mm;background:#fff;border-radius:3mm;padding:5mm 6mm;max-width:150mm">
    <div style="font-family:Grotesk;font-weight:700;font-size:8.6pt;letter-spacing:.18em;color:#5A2409">NESTE LIVRO</div>
    {"".join(f'<div style="display:grid;grid-template-columns:5mm 1fr;margin-top:2.4mm;font-size:10pt;line-height:1.4"><span style="width:2mm;height:2mm;background:var(--coral);border-radius:50%;margin-top:1.6mm"></span><span>{b}</span></div>' for b in bul)}
  </div>
</div>
<div style="position:absolute;left:28mm;right:24mm;bottom:52mm;display:grid;grid-template-columns:repeat(5,1fr);gap:3mm">
  {"".join(f'<div><div style="height:30mm;border-radius:2mm;overflow:hidden"><img class="cover" src="img/{im}.jpg" style="object-position:{pos}"></div><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;text-transform:uppercase;color:{UC[u]};margin-top:1.6mm">Unidade {u}</div><div style="font-size:8pt;color:#2E2A24;line-height:1.3">{t}</div></div>' for im, pos, u, t in [("onda","50% 40%",1,"Informar ou convencer?"),("labirinto","50% 50%",2,"Mitos, clássicos e lendas"),("infanta","50% 30%",3,"Vozes que o tempo guardou"),("palco","50% 40%",4,"O palco das escolhas"),("leitora","50% 40%",7,"Três livros escolhidos por ti")])}
</div>
<div style="position:absolute;left:28mm;right:80mm;bottom:17mm;display:flex;align-items:center;gap:4mm">
  <img src="img/logo.png" style="width:13mm;height:13mm">
  <div style="font-size:9pt;line-height:1.5;color:#2E2A24"><b style="font-family:Grotesk;letter-spacing:.06em">Prime School Press · Português</b><br>11–12 anos · 6.º Ano<br><span style="color:var(--coral);font-family:Grotesk;font-weight:700">primeschool.pt</span></div>
</div>
</section>'''
