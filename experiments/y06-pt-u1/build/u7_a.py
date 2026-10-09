import parts
from parts import *
parts.UNIT.update(n=7, total=7)

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea)"
LN = "#AEB7C4"

def U(h=6.5):
    """one ruled answer line"""
    return f'<span style="display:block;border-bottom:.6pt solid {LN};height:{h}mm"></span>'

def star(size=7, stroke="#17315A", fill="none"):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}mm;height:{size}mm;display:inline-block;vertical-align:middle">'
            f'<path d="M12 2.4l2.85 6.05 6.6.8-4.87 4.55 1.27 6.55L12 17.1l-5.85 3.25 1.27-6.55L2.55 9.25l6.6-.8z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/></svg>')

def stars(n=5, size=7, stroke="#17315A"):
    return '<span style="display:inline-flex;gap:1.2mm">' + ''.join(star(size, stroke) for _ in range(n)) + '</span>'

TICK = ('<svg viewBox="0 0 20 20" style="width:4.2mm;height:4.2mm;vertical-align:-.9mm"><path d="M3.5 10.5l4.2 4.2L16.5 5.5" '
        'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')

SCISSORS = ('<svg viewBox="0 0 24 24" style="width:6mm;height:6mm"><circle cx="6" cy="6" r="3" fill="none" stroke="#E4502F" stroke-width="1.8"/>'
            '<circle cx="6" cy="18" r="3" fill="none" stroke="#E4502F" stroke-width="1.8"/><path d="M8.4 7.8L20 17M8.4 16.2L20 7" '
            'stroke="#E4502F" stroke-width="1.8" stroke-linecap="round"/></svg>')

def field(label, h=6.5, span=1):
    return (f'<div style="grid-column:span {span}"><div style="font-family:Grotesk;font-size:6.4pt;font-weight:700;letter-spacing:.14em;'
            f'text-transform:uppercase;color:var(--muted)">{label}</div>{U(h)}</div>')

# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, f'''
<div class="abs" style="left:0;right:0;top:0;height:150mm"><img class="cover" src="img/leitora.jpg" style="object-position:50% 55%"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:159mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">7</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 7 · Atividades extra · Projeto de leitura autónoma</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">Três livros<br>escolhidos <em>por ti</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:5mm;font-size:12.2pt">Até aqui, foi o manual a escolher os textos. Agora, a escolha é tua. Ao longo do ano, vais ler <b>três obras</b> — uma em cada etapa — e registar cada uma num <b class="coral">caderno de leitura</b>: o tema, uma personagem, a frase de que mais gostaste e a tua opinião, sempre com razões e provas. No fim, vais recomendar um livro à turma.</p>
  <div class="panel" style="margin-top:5mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">3 min</div>
    <div style="font-size:10pt"><b class="blue">Que leitor és tu?</b> Conversa com o colega do lado: qual foi o último livro que leste <b>até ao fim</b> sem ninguém to pedir? Onde gostas de ler? Preferes aventuras, poemas, teatro ou banda desenhada? Escrevam uma palavra cada um no quadro: <b>«Para mim, ler é…»</b></div>
  </div>
  <div style="margin-top:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">p. 2</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.2pt;margin-top:.8mm">Como funciona</div></div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:2mm"><div class="kicker coral">p. 3–5</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.2pt;margin-top:.8mm">Caderno de leitura</div></div>
    <div style="border-top:1.2mm solid var(--sea);padding-top:2mm"><div class="kicker sea">p. 6</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.2pt;margin-top:.8mm">A apreciação fundamentada</div></div>
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">p. 7</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.2pt;margin-top:.8mm">Clube de leitura</div></div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 HOW IT WORKS + SUGGESTIONS
MONTHS = ["set.", "out.", "nov.", "dez.", "jan.", "fev.", "mar.", "abr.", "mai.", "jun."]
ETAPAS = [("1.ª etapa", "Obra 1", "set. – dez.", INK, "p. 3", 4), ("2.ª etapa", "Obra 2", "jan. – mar.", COR, "p. 4", 3),
          ("3.ª etapa", "Obra 3", "abr. – jun.", SEA, "p. 5", 3)]
STEPS = ["escolho e registo a ficha", "leio e anoto no diário de bordo", "completo o caderno", "partilho no Clube de leitura"]
tl_months = "".join(f'<div style="font-family:Grotesk;font-size:6.6pt;font-weight:700;letter-spacing:.1em;color:var(--muted);text-align:center;border-left:.6pt solid var(--rule)">{m}</div>' for m in MONTHS)
tl_bands = "".join(f'''<div style="grid-column:span {w};background:{c};color:#fff;border-radius:1.6mm;padding:2mm 3mm;margin:0 .8mm;display:flex;justify-content:space-between;align-items:baseline">
  <span style="font-family:Grotesk;font-size:7pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase">{e}</span>
  <span style="font-family:Fraunces;font-weight:600;font-size:12pt">{o} <span style="font-family:Grotesk;font-size:7pt;font-weight:700;color:#fff">{p}</span></span></div>''' for e, o, d, c, p, w in ETAPAS)
tl_steps = "".join(f'<div style="display:grid;grid-template-columns:5mm 1fr;gap:1.4mm;font-size:8.6pt;line-height:1.3;margin-top:1.2mm"><b style="color:var(--coral);font-family:Fraunces">{i}</b><span>{s}</span></div>' for i, s in enumerate(STEPS, 1))

BOOKS = [
    ("Aventura e vida real", INK, [
        ("Rosa, Minha Irmã Rosa", "Alice Vieira"),
        ("Pedro Alecrim", "António Mota"),
        ("Uma Aventura na Cidade", "Ana Maria Magalhães e Isabel Alçada"),
        ("Robinson Crusoé", "Daniel Defoe (adapt. John Lang)")]),
    ("Mitos e heróis", SEA, [
        ("Contos Gregos", "António Sérgio")]),
    ("Teatro", COR, [
        ("Os Piratas – Teatro", "Manuel António Pina"),
        ("O Bojador", "Sophia de Mello Breyner Andresen")]),
    ("Poesia", COR, [
        ("O Pássaro da Cabeça", "Manuel António Pina"),
        ("Primeiro Livro de Poesia", "seleção de Sophia de Mello Breyner Andresen")]),
    ("De outros países de língua portuguesa", SEA, [
        ("O Gato Malhado e a Andorinha Sinhá", "Jorge Amado · Brasil"),
        ("Ynari, a Menina das Cinco Tranças", "Ondjaki · Angola"),
        ("O Gato e o Escuro", "Mia Couto · Moçambique")]),
]
bl = ""
for grp, c, items in BOOKS:
    bl += f'<div class="kicker" style="color:{c};margin-top:2.6mm;font-size:6.8pt">{grp}</div>'
    for t, a in items:
        bl += (f'<div style="display:grid;grid-template-columns:5mm 1fr;gap:1.4mm;align-items:start;margin-top:1.2mm;line-height:1.25">'
               f'<span class="chk" style="margin:0;width:3.2mm;height:3.2mm;margin-top:.5mm"></span>'
               f'<div><span style="font-family:Fraunces;font-weight:600;font-style:italic;color:var(--ink);font-size:9.6pt">{t}</span>'
               f'<span style="font-size:8.2pt;color:var(--muted)"> — {a}</span></div></div>')

TEST = [("0–1", "fácil", "boa para ler depressa, por prazer", SEA), ("2–3", "à tua medida", "a escolha ideal", INK), ("4 ou +", "desafio", "lê com alguém ou deixa para mais tarde", COR)]
test = "".join(f'<div style="display:grid;grid-template-columns:13mm 1fr;gap:2mm;align-items:baseline;border-top:.6pt solid var(--rule);padding:1.4mm 0"><b class="display" style="font-size:12pt;color:{c};line-height:1">{n}</b><span style="font-size:8.6pt;line-height:1.3"><b style="color:{c}">{a}</b> · {b}</span></div>' for n, a, b, c in TEST)
CHOOSE = [("Capa e título", "O que me prometem?"), ("Contracapa", "Lê o resumo: queres saber mais?"), ("Primeira página", "Faz o teste ao lado."),
          ("Pergunta a alguém", "professor, bibliotecário, colega, família.")]
ch = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:1.6mm;margin-top:1.8mm"><b class="display blue" style="font-size:13pt;line-height:1">{i}</b><div style="font-size:9pt;line-height:1.3"><b class="blue">{a}.</b> {b}</div></div>' for i, (a, b) in enumerate(CHOOSE, 1))

plan = "".join(f'''<div style="display:grid;grid-template-columns:18mm 1fr 30mm;gap:3mm;align-items:end;margin-top:2mm">
  <b style="font-family:Grotesk;font-size:7.2pt;letter-spacing:.12em;text-transform:uppercase;color:{c}">{o}</b>
  <div>{U(6)}</div><div style="font-size:7.6pt;color:var(--muted)">até <span style="display:inline-block;width:20mm;border-bottom:.6pt solid {LN};height:4mm"></span></div></div>''' for e, o, d, c, p, w in ETAPAS)

P[2] = page(2, f'''
<div class="kicker">Como funciona o projeto</div>
<h2 style="margin-top:2mm">Um ano, <em>três</em> livros</h2>
<p style="margin-top:2mm;font-size:10pt;line-height:1.45">Lês uma obra em cada etapa do ano letivo, ao teu ritmo, em casa e na escola. Para cada obra, preenches uma página do caderno de leitura (p. 3 a 5). No fim de cada etapa, apresentas o livro à turma.</p>
<div style="margin-top:4mm">
  <div style="display:grid;grid-template-columns:repeat(10,1fr)">{tl_months}</div>
  <div style="display:grid;grid-template-columns:repeat(10,1fr);margin-top:1.4mm">{tl_bands}</div>
  <div style="display:grid;grid-template-columns:4fr 3fr 3fr;margin-top:1.6mm">
    <div style="padding:0 3mm">{tl_steps}</div><div style="padding:0 3mm;border-left:.6pt solid var(--rule)">{tl_steps}</div><div style="padding:0 3mm;border-left:.6pt solid var(--rule)">{tl_steps}</div>
  </div>
</div>
<div style="display:grid;grid-template-columns:1fr 1.18fr;gap:7mm;margin-top:5mm;align-items:start">
  <div>
    <h3>Como escolher um livro</h3>
    {ch}
    <div class="panel blue" style="margin-top:3.4mm;padding:3.4mm 4mm">
      <div class="kicker blue">O teste da página</div>
      <p style="font-size:8.8pt;line-height:1.35;margin-top:1.2mm">Lê uma página ao acaso. Conta as palavras que <b>não conheces</b>.</p>
      <div style="margin-top:1.4mm">{test}</div>
    </div>
  </div>
  <div class="panel" style="padding:3.6mm 4.4mm">
    <div class="kicker blue">Sugestões para o 6.º ano</div>
    <p class="small muted" style="margin-top:.8mm;line-height:1.3">Assinala as que te apetece ler. Quase todas estão na lista oficial de obras para o 6.º ano.</p>
    {bl}
  </div>
</div>
<div style="margin-top:auto;display:grid;grid-template-columns:1fr 60mm;gap:7mm;align-items:end">
  <div><div class="kicker">O meu plano de leitura</div>{plan}</div>
  {qr("q-pnl", "Mais sugestões", "O Plano Nacional de Leitura recomenda livros para cada idade.")}
</div>
<p class="src" style="margin-top:2.4mm">Sugestões verificadas nas <i>Aprendizagens Essenciais</i> de Português, 6.º ano (DGE, Anexo 1 — lista de obras e textos), e nos catálogos das editoras. Os livros <i>Uma Aventura na Cidade</i>, <i>Ynari</i> e <i>O Gato e o Escuro</i> são sugestões deste manual.</p>
''', station="Projeto")

# ---------------------------------------------------------------- 3-5 READING NOTEBOOK
THEMES = ["amizade", "família", "coragem", "medo", "liberdade", "crescer", "natureza", "justiça", "viagem", "perda", "sonhos"]
OBRAS = {
    3: dict(no="1", c=INK, cls="blue", soft="var(--ink-soft)", etapa="1.ª etapa", title="O meu primeiro livro",
            tq="De que fala o livro, <b>para além da história</b>? Completa: «Este livro fala de… e mostra que…»",
            pq="Que <b>problema</b> tem a personagem? Como o resolve?"),
    4: dict(no="2", c=COR, cls="coral", soft="var(--coral-soft)", etapa="2.ª etapa", title="O meu segundo livro",
            tq="O tema deste livro é parecido com o da Obra 1, ou é diferente? Explica.",
            pq="O que <b>mudou</b> na personagem entre o início e o fim?"),
    5: dict(no="3", c=SEA, cls="sea", soft="var(--sea-soft)", etapa="3.ª etapa", title="O meu terceiro livro",
            tq="Que <b>mensagem</b> levas deste livro para a tua vida? Porquê?",
            pq="Se pudesses fazer uma pergunta à personagem, qual seria? O que te responderia?"),
}

def trait(label, c):
    return (f'<div style="border:1px solid var(--rule);border-top:1mm solid {c};border-radius:0 0 2mm 2mm;padding:1.6mm 2.6mm 1.4mm;background:#fff">'
            f'<div style="font-family:Grotesk;font-size:6.4pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{c}">{label}</div>{U(5)}{U(5)}</div>')

def obra(n):
    o = OBRAS[n]; c = o["c"]
    chips = "".join(f'<span class="chip" style="font-size:7.4pt;padding:.4mm 2.2mm">{t}</span>' for t in THEMES)
    genres = "".join(f'<span style="font-size:8.4pt;white-space:nowrap"><span class="chk" style="width:3.2mm;height:3.2mm;border-color:{c}"></span>{g}</span>' for g in ["narrativa", "poesia", "teatro", "banda desenhada", "outro"])
    weeks = "".join(f'<div style="border:1px solid var(--rule);border-radius:1.6mm;padding:1mm 1.6mm;background:#fff"><div style="font-family:Grotesk;font-size:6.2pt;font-weight:700;letter-spacing:.1em;color:{c}">DIA</div><span style="display:block;border-bottom:.6pt solid {LN};height:4.2mm"></span><div style="font-family:Grotesk;font-size:6.2pt;font-weight:700;letter-spacing:.1em;color:var(--muted);margin-top:.8mm">ATÉ À P.</div><span style="display:block;border-bottom:.6pt solid {LN};height:4.2mm"></span></div>' for _ in range(8))
    ap = [("Na minha opinião,", "este livro é…"), ("Razão 1", ""), ("Prova", "(p. ___)"), ("Razão 2", ""), ("Prova", "(p. ___)"), ("Por isso,", "recomendo-o a…")]
    aph = "".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:2mm;align-items:end;margin-top:.4mm"><div style="font-size:8.8pt;padding-bottom:1mm;line-height:1.15"><b style="color:{c}">{a}</b> <span class="muted" style="font-size:7.8pt">{b}</span></div>{U(5.8)}</div>' for a, b in ap)
    return page(n, f'''
<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:5mm">
  <div style="display:flex;align-items:baseline;gap:4mm">
    <div class="display" style="font-size:40pt;line-height:.85;color:{c}">{o["no"]}</div>
    <div><div class="kicker" style="color:{c}">Caderno de leitura · Obra {o["no"]} · {o["etapa"]}</div><h2 style="margin-top:1mm">{o["title"]}</h2></div>
  </div>
  <div style="text-align:right"><div style="font-family:Grotesk;font-size:6.4pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:1mm">A minha classificação · pinta</div>{stars(5, 7.4, "#17315A")}</div>
</div>
<div class="panel" style="margin-top:3.6mm;padding:3.2mm 4.4mm 3.6mm;background:{o["soft"]}">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.4mm 5mm">
    {field("Título", 6.5, 2)}{field("Autor", 6.5, 2)}
    {field("Ilustrador ou tradutor")}{field("Editora")}{field("Ano de edição")}{field("N.º de páginas")}
  </div>
  <div style="display:flex;gap:4mm;flex-wrap:wrap;margin-top:2.6mm;align-items:center"><b style="font-family:Grotesk;font-size:6.4pt;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Género</b>{genres}</div>
</div>
<div style="margin-top:3.4mm"><div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker" style="color:{c}">Diário de bordo</div><span class="small muted">Sempre que leres, regista o dia e a página onde paraste.</span></div>
  <div style="display:grid;grid-template-columns:repeat(8,1fr);gap:2mm;margin-top:1.6mm">{weeks}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:3.6mm">
  <div>
    <div class="kicker" style="color:{c}">Tema</div>
    <p style="font-size:9pt;line-height:1.35;margin-top:1mm">{o["tq"]}</p>
    <div class="opts" style="gap:1.2mm;margin-top:1.4mm">{chips}</div>
    <p class="small muted" style="margin-top:1mm">Rodeia um ou dois temas.</p>
    {lines(3)}
  </div>
  <div style="position:relative">
    <div class="kicker" style="color:{c}">A minha citação preferida</div>
    <div style="display:grid;grid-template-columns:9mm 1fr;gap:1mm;margin-top:.6mm">
      <div class="display" style="font-size:40pt;line-height:.8;color:{c}">“</div>
      <div>{lines(3)}</div>
    </div>
    <div style="display:grid;grid-template-columns:auto 16mm;justify-content:end;gap:2mm;align-items:end;margin-top:1mm"><span style="font-size:8.6pt;color:var(--muted)">página</span>{U(5)}</div>
    <div style="font-size:9pt;margin-top:1mm"><b style="color:{c}">Escolhi-a porque…</b></div>{lines(2)}
  </div>
</div>
<div style="margin-top:2.5mm"><div class="kicker" style="color:{c}">Uma personagem</div>
  <div style="display:grid;grid-template-columns:40mm 1fr 34mm 1fr;gap:3mm;margin-top:1.6mm;align-items:stretch">
    <div style="grid-row:span 2;border:1.2px dashed {c};border-radius:2mm;display:flex;flex-direction:column;justify-content:flex-end;padding:2mm;background:repeating-linear-gradient(135deg,transparent 0 3mm,rgba(201,207,217,.18) 3mm 3.4mm)">
      <div style="font-family:Grotesk;font-size:6.2pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{c};text-align:center">Retrato</div>
    </div>
    {trait("Como é por fora", c)}
    <div style="grid-row:span 2;display:flex;align-items:center;justify-content:center">
      <div style="width:32mm;height:32mm;border-radius:50%;border:1.4mm solid {c};background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:3mm">
        <div style="font-family:Grotesk;font-size:6pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Nome</div>
        <span style="display:block;width:22mm;border-bottom:.6pt solid {LN};height:6mm"></span>
      </div>
    </div>
    {trait("Como é por dentro", c)}
    {trait("O que deseja", c)}
    {trait("Um gesto que o prova (p. ___)", c)}
  </div>
  <p style="font-size:9pt;margin-top:2mm"><b style="color:{c}">Pensa:</b> {o["pq"]}</p>{lines(1)}
</div>
<div style="margin-top:3mm;border-top:.6pt solid var(--rule);padding-top:2mm"><div class="kicker" style="color:{c}">Apreciação fundamentada <span class="muted" style="letter-spacing:.06em;text-transform:none;font-family:Body;font-weight:400;font-size:7.8pt">· modelo na p. 6</span></div>
  {aph}
</div>
''', station=f"Obra {o['no']}")

for n in (3, 4, 5):
    P[n] = obra(n)

# ---------------------------------------------------------------- 6 HOW TO WRITE AN APRECIAÇÃO FUNDAMENTADA
MODEL = [
    ("1", "Apresento a obra", "título, origem ou autor e o assunto numa frase.",
     'Na Unidade 4 deste manual, li <b>«Dédalo e Ícaro»</b>, um mito grego recontado a partir das <i>Metamorfoses</i>, do poeta latino Ovídio. Conta a história de um inventor que fabrica asas para fugir, com o filho, da ilha de Creta.'),
    ("2", "Dou a minha opinião", "clara, logo no início: é a minha tese.",
     '<span class="mk-o">Na minha opinião, é um dos melhores textos do ano</span>, porque é uma história curta que nos faz pensar durante muito tempo.'),
    ("3", "Razão 1 + prova", "a prova é uma citação, entre aspas.",
     '<b class="coral">Em primeiro lugar,</b> o mito prende-nos do princípio ao fim. Logo no início, Dédalo avisa que, se o filho subir muito, <span class="mk-f">«o calor do sol derreteria a cera»</span>. Por isso, quando lemos que Ícaro <span class="mk-f">«subiu, subiu, em direção ao céu»</span>, já estamos a temer o que vai acontecer.'),
    ("4", "Razão 2 + prova", "outra razão, com outro exemplo.",
     '<b class="coral">Além disso,</b> a história fala de coisas que ainda hoje nos acontecem. Ícaro desobedece porque está entusiasmado, como nós às vezes. Na versão em teatro, Dédalo diz: <span class="mk-f">«Dei-lhe asas e não lhe dei juízo.»</span> Esta frase mostra que a liberdade precisa de prudência.'),
    ("5", "Admito outra opinião", "e respondo-lhe.",
     '<b class="coral">É verdade que</b> o final é triste. <b class="coral">Porém,</b> é esse final que torna a lição inesquecível.'),
    ("6", "Concluo e recomendo", "a quem? porquê?",
     '<b class="coral">Por isso,</b> recomendo este mito a quem gosta de aventuras e a quem já teve vontade de voar mais alto do que devia.'),
]
mh = "".join(f'''<div style="display:grid;grid-template-columns:1fr 50mm;gap:6mm;margin-top:{'0' if i == 0 else '1.4mm'}">
  <p style="font-family:FrauncesText;font-size:10pt;line-height:1.5;position:relative;padding-left:7mm"><span style="position:absolute;left:0;top:.6mm;width:4.8mm;height:4.8mm;border-radius:50%;background:var(--sea);color:#fff;font-family:Grotesk;font-weight:700;font-size:6.8pt;line-height:4.8mm;text-align:center">{k}</span>{t}</p>
  <div style="border-left:1mm solid var(--sea);padding:.4mm 0 .4mm 2.6mm;font-size:8.4pt;line-height:1.3"><b class="sea">{a}</b><br><span class="muted">{b}</span></div></div>''' for i, (k, a, b, t) in enumerate(MODEL))
CHECK = ["Indiquei o título e o autor (ou a origem) da obra.", "A minha opinião está clara no início.", "Dei pelo menos duas razões.",
         "Cada razão tem uma prova do livro, com a página.", "Pus as citações entre aspas «…».", "Usei conectores para ligar as ideias.",
         "Não contei o fim a quem ainda não leu.", "Terminei com uma recomendação."]
chk = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:1mm;margin-top:1mm;font-size:8.8pt;line-height:1.28"><span class="chk" style="border-color:var(--sea)"></span><span>{t}</span></div>' for t in CHECK)
CONN = ["Na minha opinião,", "Considero que", "Em primeiro lugar,", "Além disso,", "Por exemplo,", "Como se lê na página…", "É verdade que… porém,", "Por isso,", "Em suma,"]
conn = "".join(f'<span class="chip" style="font-size:7.6pt">{t}</span>' for t in CONN)
WEAK = ["Gostei porque sim.", "O livro é fixe.", "Não gostei porque é chato."]
weak = "".join(f'<div style="display:grid;grid-template-columns:44mm 6mm 1fr;gap:2mm;align-items:end;margin-top:1.6mm"><span style="font-family:FrauncesText;font-style:italic;font-size:9.2pt;color:var(--coral);text-decoration:line-through;text-decoration-thickness:.5pt">{w}</span><span style="text-align:center">→</span>{U(6)}</div>' for w in WEAK)

P[6] = page(6, f'''
<div class="kicker sea">Oficina de escrita</div>
<h2 style="margin-top:2mm">Como escrever uma <em>apreciação fundamentada</em></h2>
<p class="lead" style="margin-top:1.6mm;font-size:10.2pt">Dizer «gostei» não chega. Numa <b>apreciação fundamentada</b>, dás a tua opinião sobre uma obra e <b class="sea">provas</b> que tens razão, com exemplos tirados do próprio texto.</p>
<div style="display:grid;grid-template-columns:1fr 50mm;gap:6mm;margin-top:2.4mm;align-items:end">
  <div class="kicker">Texto-modelo · sobre um texto deste manual</div>
  <div class="kicker sea">O que faz cada parte</div>
</div>
<div style="border-top:.6pt solid var(--rule);padding-top:2.6mm;margin-top:1.4mm">{mh}</div>
<p class="src" style="margin-top:1.6mm">Texto escrito para este manual. As citações vêm de «Dédalo e Ícaro» e de «Ícaro em cena» (Unidade 4). <span class="mk-o">Laranja</span>: opinião · <span class="mk-f">azul</span>: provas · <b class="coral">conectores</b> a cor.</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:2.2mm;align-items:start">
  <div class="panel sea" style="padding:3.4mm 4.2mm">
    <div class="kicker sea">Verifica a tua apreciação</div>{chk}
  </div>
  <div>
    <div class="kicker">Conectores úteis</div>
    <div class="opts" style="gap:1.4mm">{conn}</div>
    {act(1, "Melhorar", 'Estas frases não provam nada. Reescreve cada uma como uma <b>razão</b> sobre um livro que leste.' + weak, "sea")}
  </div>
</div>
{act(2, "Escrever", 'Escreve uma apreciação fundamentada da <b>Bela Infanta</b> (Unidade 3), com a tua opinião, <b>duas razões</b> e uma citação como prova. Revê-a com a lista acima (continua no caderno).' + lines(3), "sea")}
''', station="Oficina")

# ---------------------------------------------------------------- 7 SHARING + YEAR SELF-ASSESSMENT
TALK = [("0:00", "Gancho", "Começa com uma pergunta, um som ou uma frase do livro.", 2, INK),
        ("0:20", "Apresento", "Título, autor e o início da história — sem contar o fim!", 3, COR),
        ("0:50", "Um momento", "Lê em voz alta a tua citação preferida e diz porque a escolheste.", 4, SEA),
        ("1:30", "Opinião", "A tua apreciação: duas razões e a quem o recomendas.", 3, INK)]
talk = "".join(f'''<div style="grid-column:span {w};padding:0 1mm">
  <div style="background:{c};color:#fff;border-radius:1.4mm;padding:1.4mm 2.4mm;display:flex;justify-content:space-between;align-items:baseline"><b style="font-family:Grotesk;font-size:7pt;letter-spacing:.12em;text-transform:uppercase">{a}</b><span style="font-family:Grotesk;font-size:7pt;font-weight:700">{t}</span></div>
  <div style="font-size:8.6pt;line-height:1.3;margin-top:1.4mm">{b}</div></div>''' for t, a, b, w, c in TALK)
SELF = ["Escolhi livros à minha medida e li-os até ao fim.", "Identifiquei o tema de cada obra.", "Caracterizei uma personagem com provas do texto.",
        "Escrevi apreciações com opinião, razões e provas.", "Apresentei um livro à turma com clareza e boa voz.", "Ouvi os colegas e fiquei com vontade de ler outros livros.", "Usei a biblioteca para encontrar livros novos.", "Hoje leio mais, ou melhor, do que no início do ano."]
selfh = "".join(f'<tr><td style="font-weight:400;color:#1d2433;width:auto;font-size:8.8pt">{s}</td>' + ''.join(f'<td style="text-align:center;width:15mm"><span class="chk{o}" style="margin:0"></span></td>' for o in ("", "", " o")) + '</tr>' for s in SELF)

P[7] = page(7, f'''
<div class="kicker">Partilhar</div>
<h2 style="margin-top:2mm">Clube de <em>leitura</em></h2>
<p style="margin-top:2mm;font-size:10pt;line-height:1.45">No fim de cada etapa, a turma reúne-se em Clube de leitura. Cada leitor faz uma <b>apresentação de dois minutos</b> do livro que leu: o objetivo é deixar os colegas com vontade de o ler.</p>
<div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:3.6mm"><div class="kicker blue">A apresentação em 2 minutos</div><span style="font-family:Grotesk;font-size:7pt;font-weight:700;color:var(--muted)">2:00 · FIM</span></div>
<div style="display:grid;grid-template-columns:repeat(12,minmax(0,1fr));margin-top:1.6mm">{talk}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:3.4mm">
  <div class="rule-card" style="font-size:8.8pt;line-height:1.4"><b class="blue">Na voz e no corpo.</b> Fala devagar e alto, para o fundo da sala. Olha para os colegas, não para o papel. Mostra o livro. Leva só um cartão com <b>três palavras-chave</b>.</div>
  <div class="rule-card o" style="font-size:8.8pt;line-height:1.4"><b class="coral">Enquanto ouves.</b> Anota o título que mais te interessou e faz uma pergunta ao apresentador no fim.<div style="display:grid;grid-template-columns:auto 1fr;gap:2mm;align-items:end;margin-top:1mm"><span class="muted">Quero ler:</span>{U(5.4)}</div></div>
</div>
<div style="margin-top:4.4mm;border:1.2px dashed var(--coral);border-radius:3mm;padding:3.6mm 4.4mm;position:relative;background:#fff">
  <div style="position:absolute;top:-3.4mm;left:6mm;background:var(--paper);padding:0 1.4mm">{SCISSORS}</div>
  <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker">Mural da turma · Recomendo!</div><span class="small muted">Recorta e afixa no mural da sala ou da biblioteca.</span></div>
  <div style="display:grid;grid-template-columns:1.3fr 1fr;gap:2mm 6mm;margin-top:1.4mm">
    {field("Recomendo o livro")}{field("de (autor)")}
    {field("a quem gosta de…")}<div><div style="font-family:Grotesk;font-size:6.4pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Classificação · pinta</div><div style="margin-top:1mm">{stars(5, 6, "#E4502F")}</div></div>
    {field("Não te conto o fim, mas…", 6.5, 2)}
    {field("Uma razão para o leres", 6.5, 2)}
    {field("Assinado")}{field("Turma e data")}
  </div>
</div>
<div style="margin-top:4.4mm;display:grid;grid-template-columns:1fr 50mm;gap:6mm;align-items:start">
  <div>
    <div class="kicker blue">Autoavaliação · o meu ano de leitor</div>
    <table class="cmp ruled" style="margin-top:1.6mm;font-size:8.6pt">
      <tr><th style="background:var(--ink)">Neste projeto…</th><th style="background:var(--ink);text-align:center;padding:2mm 1mm">Consigo</th><th style="background:var(--ink);text-align:center;padding:2mm 1mm">Quase</th><th style="background:var(--coral);text-align:center;padding:2mm 1mm">Ainda não</th></tr>
      {selfh}
    </table>
  </div>
  <div class="panel" style="padding:3.4mm 4mm">
    <div class="kicker blue">O meu livro do ano</div>{U(6.4)}
    <div style="font-size:8.6pt;margin-top:2.2mm"><b class="blue">Para as férias, quero ler…</b></div>{U(6.4)}{U(6.4)}
    <div style="margin-top:3mm">{qr("q-rbe", "A tua biblioteca", "A Rede de Bibliotecas Escolares: livros, leituras e concursos.")}</div>
  </div>
</div>
<div class="hand" style="margin-top:auto;text-align:center;font-size:17pt">Boas leituras — que o farol continue aceso!</div>
''', station="Chegada")
