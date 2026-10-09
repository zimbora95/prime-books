import parts
from parts import *
parts.UNIT.update(n=2, total=28)
from u2_a_maps import AEG, AEG_W, AEG_H, WORLD, LUSO, WW, WH

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea)"
U = lambda h=6.5: f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'
TICK = '<svg viewBox="0 0 20 20" style="width:{s};height:{s};vertical-align:-.4mm"><path d="M3 10.5l4.5 4.5L17 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def para(n, html, c=INK):
    return (f'<p style="position:relative"><span style="position:absolute;left:-7.5mm;top:.3mm;width:5mm;height:5mm;border-radius:50%;'
            f'background:{c};color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>')


def pg(n, body, station):
    return page(n, body, station=station)


def gloss(items):
    return '<dl class="gloss" style="margin-top:2.4mm">' + "".join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in items) + '</dl>'


def nums(title, rows, col=INK):
    h = "".join(f'<div style="border-top:.6pt solid var(--rule);padding:1.4mm 0"><div class="display" style="font-size:15pt;line-height:1;color:{col}">{a}</div><div class="small muted">{b}</div></div>' for a, b in rows)
    return f'<div class="panel" style="padding:3mm 3.4mm"><div class="kicker" style="color:{col}">{title}</div><div style="margin-top:1.4mm">{h}</div></div>'


def ulrow(label, w="24mm", h=6):
    return f'<div style="display:grid;grid-template-columns:{w} 1fr;gap:3mm;align-items:end;margin-top:1.2mm"><b class="blue" style="font-size:9pt">{label}</b>{U(h)}</div>'


def opener_strip():
    g = [("2.1 – 2.2", "Mitos e clássicos", "Dédalo e Ícaro · Ulisses", INK),
         ("2.3 – 2.6", "Autores de língua portuguesa", "Sophia · Mia Couto · o mundo que fala português", COR),
         ("2.7 – 2.9", "Lendas", "origens · amendoeiras · Saci-Pererê", SEA),
         ("p. 28", "Consegues?", "revisão e autoavaliação", INK)]
    return "".join(f'<div style="border-top:1.2mm solid {c};padding-top:2mm"><div class="kicker" style="color:{c}">{a}</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.2pt;margin-top:.8mm;line-height:1.15">{t}</div><div class="small muted" style="margin-top:.6mm;line-height:1.3">{s}</div></div>' for a, t, s, c in g)


# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, f'''
<div class="abs" style="left:0;right:0;top:0;height:140mm"><img class="cover" src="img/labirinto.jpg" style="object-position:50% 35%"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:150mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">2</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 2 · Texto narrativo</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">Mitos, clássicos<br>e <em>autores</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:6mm;font-size:12.4pt">Há histórias com mais de dois mil anos que ainda hoje se contam: um rapaz que voou alto demais, um herói que venceu um gigante com uma mentira. Nesta unidade, vais ler mitos e clássicos, conhecer autores de vários países onde se fala português e descobrir que <b class="coral">cada escolha de uma personagem</b> tem sempre uma consequência.</p>
  <div class="panel" style="margin-top:6mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4.5mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">3 min</div>
    <div style="font-size:10.2pt"><b class="blue">Lê a imagem.</b> Um homem e um rapaz no alto de uma torre, no meio de um labirinto. Penas a subir no ar. Com o teu colega: <b>quem são? porque estão ali? o que vão fazer com as penas?</b> Guardem as vossas respostas: na página 3 vão confirmá-las.</div>
  </div>
  <div style="margin-top:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">{opener_strip()}</div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 ROUTE + GOALS
st = [("2.1", "Mito de Dédalo e Ícaro", "reconto a partir de Ovídio", "3", INK),
      ("2.2", "Ulisses", "Maria Alberta Menéres", "7", INK),
      ("2.3", "A Fada Oriana", "Sophia de Mello Breyner Andresen", "11", COR),
      ("2.4", "Literaturas de língua portuguesa", "nove países, uma língua", "14", COR),
      ("2.5", "O Cavaleiro da Dinamarca", "Sophia de Mello Breyner Andresen", "15", COR),
      ("2.6", "O Beijo da Palavrinha", "Mia Couto · Moçambique", "19", COR),
      ("2.7–2.8", "Lendas de origens", "e a Lenda das amendoeiras", "22", SEA),
      ("2.9", "Lenda do Saci-Pererê", "uma lenda do Brasil", "25", SEA),
      (TICK.format(s="7mm"), "Consegues?", "revisão e autoavaliação", "28", INK)]
def strow(n, t, g, p, c):
    fs = "13pt" if "–" in n else "17pt"
    return f'''<div style="display:grid;grid-template-columns:17mm 1fr 10mm;gap:3mm;align-items:center;padding:2.3mm 0;border-top:.6pt solid var(--rule)">
  <div class="display" style="font-size:{fs};line-height:1;color:{c}">{n}</div>
  <div><div style="font-family:FrauncesText;font-weight:700;font-size:10.6pt;color:var(--ink);line-height:1.15">{t}</div><div class="small muted">{g}</div></div>
  <div style="font-family:Grotesk;font-weight:700;font-size:8pt;color:{c};text-align:right">p. {p}</div></div>'''
col1 = "".join(strow(*r) for r in st[:5])
col2 = "".join(strow(*r) for r in st[5:])
five = [("Narrador", "quem conta a história. Pode participar nela ou não."),
        ("Personagens", "quem vive a ação: principal(is) e secundárias."),
        ("Espaço", "onde se passa: lugares físicos e ambiente."),
        ("Tempo", "quando se passa e quanto tempo dura."),
        ("Ação", "o que acontece: situação inicial, peripécias, desenlace.")]
fh = "".join(f'<div style="display:grid;grid-template-columns:24mm 1fr;gap:2.5mm;padding:1.9mm 0;border-top:.6pt solid rgba(23,49,90,.18);font-size:9.1pt;line-height:1.32"><b class="blue" style="font-family:FrauncesText;font-size:10pt">{a}</b><span>{b}</span></div>' for a, b in five)
goals = ["identificar <b>narrador</b>, <b>personagens</b>, <b>espaço</b>, <b>tempo</b> e <b>ação</b> num mito e num conto;",
         "explicar a relação de <b>causa</b> e <b>consequência</b> entre acontecimentos;",
         "reconhecer num herói o <b>obstáculo</b> e a <b>artimanha</b>; numa personagem, a <b>promessa</b> e a <b>prova</b>;",
         "<b>contar</b> um mito, <b>expor</b> um plano e <b>ler em voz alta</b> uma passagem que escolheste;",
         "escrever um <b>resumo</b>, uma <b>narrativa com descrição e diálogo</b> e um <b>texto de opinião</b>;",
         "usar o <b>pretérito mais-que-perfeito</b>, o <b>verbo auxiliar</b> e o <b>particípio passado</b>;",
         "distinguir verbos <b>transitivos</b> e <b>intransitivos</b> e encontrar o <b>complemento direto</b>."]
gh = "".join(f'<li style="margin-top:1.7mm;display:grid;grid-template-columns:5.5mm 1fr"><span class="chk"></span><span>{g}</span></li>' for g in goals)
books = [("Maria Alberta Menéres", "Ulisses", "2.2"), ("Sophia de Mello Breyner Andresen", "A Fada Oriana", "2.3"),
         ("Sophia de Mello Breyner Andresen", "O Cavaleiro da Dinamarca", "2.5"), ("Mia Couto", "O Beijo da Palavrinha", "2.6")]
bh = "".join(f'<div style="border-left:1.2mm solid var(--coral);padding:.4mm 0 .4mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:6.8pt;letter-spacing:.12em;color:var(--coral)">{s}</div><div style="font-family:Fraunces;font-weight:600;font-style:italic;font-size:9.8pt;color:var(--ink);line-height:1.2">{t}</div><div class="small muted" style="line-height:1.25">{a}</div></div>' for a, t, s in books)
P[2] = pg(2, f'''
<div class="kicker">Antes de começar</div>
<h2 style="margin-top:2mm">A rota desta unidade</h2>
<div class="grid2" style="margin-top:3.4mm;gap:7mm;align-items:start"><div style="border-bottom:.6pt solid var(--rule)">{col1}</div><div style="border-bottom:.6pt solid var(--rule)">{col2}</div></div>
<div class="grid2" style="margin-top:6mm;grid-template-columns:1fr 1.08fr;gap:7mm;align-items:start">
  <div class="panel blue" style="padding:4mm 4.5mm">
    <div class="kicker blue">A caixa de ferramentas do leitor</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.4">Todas as narrativas desta unidade — mito, clássico, conto ou lenda — se constroem com as mesmas <b>cinco peças</b>. Vais usá-las em todas as estações.</p>
    <div style="margin-top:1.6mm">{fh}</div>
  </div>
  <div>
    <h3>No fim da unidade, vais conseguir…</h3>
    <ul style="list-style:none;margin-top:1.4mm;font-size:9.3pt;line-height:1.34">{gh}</ul>
  </div>
</div>
<div class="panel blue" style="margin-top:2mm;padding:2.6mm 4mm"><div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker blue">A caixa de ferramentas do leitor</div><div class="small muted">Usa-a em todas as narrativas desta unidade.</div></div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2.6mm;margin-top:1.8mm"><div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;border-top:1.2mm solid var(--ink)"><b class="blue" style="font-family:FrauncesText;font-size:9.6pt">Narrador</b><div style="font-size:8.2pt;line-height:1.3;margin-top:.5mm">Quem conta a história. Pode <b>participar</b> nela (1.ª pessoa: <i>eu</i>) ou <b>não participar</b> (3.ª pessoa: <i>ele, ela</i>).</div></div><div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;border-top:1.2mm solid var(--ink)"><b class="blue" style="font-family:FrauncesText;font-size:9.6pt">Personagens</b><div style="font-size:8.2pt;line-height:1.3;margin-top:.5mm">Quem vive a ação: a <b>principal</b> (o centro da história) e as <b>secundárias</b>.</div></div><div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;border-top:1.2mm solid var(--ink)"><b class="blue" style="font-family:FrauncesText;font-size:9.6pt">Espaço</b><div style="font-size:8.2pt;line-height:1.3;margin-top:.5mm"><b>Onde</b> a ação acontece: um país, uma ilha, uma casa, um barco…</div></div><div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;border-top:1.2mm solid var(--ink)"><b class="blue" style="font-family:FrauncesText;font-size:9.6pt">Tempo</b><div style="font-size:8.2pt;line-height:1.3;margin-top:.5mm"><b>Quando</b> acontece e <b>quanto dura</b>: uma noite, semanas, muitos anos.</div></div><div style="background:#fff;border-radius:2mm;padding:2mm 2.6mm;border-top:1.2mm solid var(--ink)"><b class="blue" style="font-family:FrauncesText;font-size:9.6pt">Ação</b><div style="font-size:8.2pt;line-height:1.3;margin-top:.5mm">O que acontece: a <b>situação inicial</b>, o <b>problema</b>, o <b>desenvolvimento</b> e o <b>desenlace</b>.</div></div></div></div>
<div class="panel" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker">Leitura integral · traz o teu livro</div><div class="small muted">Estes livros leem-se inteiros, na edição da turma.</div></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:2.6mm">{bh}</div>
</div>
''', "A rota")

# ---------------------------------------------------------------- 3 STATION 2.1 — before reading + map
def aeg(lon, lat):
    return ((lon - 22.6) * 100 * 0.79, (38.45 - lat) * 100)

def label(lon, lat, t, anchor="start", dx=5, dy=3, size=11, col="#17315A", w=700, it=False, dot=True):
    x, y = aeg(lon, lat)
    s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{col}"/>' if dot else ""
    st_ = ' font-style="italic"' if it else ""
    return s + f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anchor}" font-family="Grotesk" font-weight="{w}" font-size="{size}" fill="{col}"{st_}>{t}</text>'

route = [(25.15, 35.42), (25.45, 36.35), (25.62, 36.95), (25.85, 37.32), (26.15, 37.43)]
rp = " ".join(f"{aeg(*p)[0]:.1f},{aeg(*p)[1]:.1f}" for p in route)
fx, fy = aeg(26.2, 37.47)
AEG_SVG = f'''<svg viewBox="0 0 {AEG_W} {AEG_H}" style="width:100%;display:block;border-radius:2.4mm;background:#DCE5F0">
<path d="{AEG}" fill="#F4EDE1" stroke="#9FB0C6" stroke-width=".8" stroke-linejoin="round"/>
<polyline points="{rp}" fill="none" stroke="#E4502F" stroke-width="2.6" stroke-dasharray="7 5" stroke-linecap="round"/>
<circle cx="{fx:.1f}" cy="{fy:.1f}" r="7" fill="none" stroke="#E4502F" stroke-width="2"/><circle cx="{fx:.1f}" cy="{fy:.1f}" r="12" fill="none" stroke="#E4502F" stroke-width="1.2" opacity=".6"/>
{label(23.73, 37.98, "Atenas", dx=6, dy=-4)}
{label(25.27, 37.40, "Delos", dx=6, dy=-2)}
{label(25.15, 37.08, "Paros", anchor="end", dx=-6, dy=4)}
{label(26.85, 37.75, "Samos", dx=4, dy=-7)}
{label(26.15, 37.62, "Icária", anchor="end", dx=-6, dy=-5)}
{label(26.47, 36.99, "Lebinto", anchor="middle", dx=0, dy=16)}
{label(26.98, 36.98, "Calimno", dx=6, dy=16)}
{label(24.95, 35.22, "CRETA", anchor="middle", dx=0, dy=4, size=15, dot=False)}
{label(25.9, 36.2, "mar Egeu", anchor="middle", dx=0, dy=0, size=12, col="#2B4C7E", w=400, it=True, dot=False)}
{label(26.62, 37.36, "mar Icário", anchor="middle", dx=0, dy=0, size=11, col="#E4502F", w=700, it=True, dot=False)}
<text x="12" y="{AEG_H-14}" font-family="Grotesk" font-size="10" fill="#5B6475">&#8592; para a Sicília</text>
</svg>'''
P[3] = pg(3, f'''
<div class="kicker blue">Estação 2.1 · Mito</div>
<h2 style="margin-top:2mm">Asas de <em>cera</em></h2>
<p class="lead" style="margin-top:2.6mm;font-size:11pt">Há mais de dois mil anos, o poeta romano <b>Ovídio</b> reuniu num longo poema, as <i>Metamorfoses</i>, os mitos que os gregos contavam. Um deles fala de um pai inventor, de um filho que não o ouviu e de um mar que ficou com o nome do rapaz.</p>
<div class="grid2" style="grid-template-columns:1.02fr 1fr;gap:7mm;margin-top:4mm;align-items:start">
  <div>
    <div class="panel blue" style="padding:3.6mm 4.2mm">
      <div class="kicker blue">O que é um mito?</div>
      <p style="font-size:9.3pt;margin-top:1.4mm;line-height:1.42">É uma <b>narrativa muito antiga</b>, de origem oral, com deuses, heróis e seres extraordinários. Os povos contavam mitos para <b>explicar a origem</b> das coisas (porque se chama assim um mar, porque há estações) e para <b>transmitir valores</b>: o que acontece a quem desobedece, a quem é orgulhoso, a quem é esperto.</p>
    </div>
    {act(1, "Prever", 'Volta à imagem da página 1. Agora que sabes o título, o que achas que Dédalo vai fazer com as penas? E o que pode correr mal?' + lines(3), "blue")}
    {act(2, "Ativar", 'Que outros mitos gregos conheces? Escreve o nome de uma personagem e o que ela fez.' + lines(2), "blue")}
  </div>
  <div>
    {AEG_SVG}
    <p class="small muted" style="margin-top:1.6mm;line-height:1.35"><b class="coral">- - -</b> rota imaginada a partir de Ovídio: as ilhas de Delos e Paros ficam para trás, Samos à esquerda, Lebinto e Calimno à direita. O círculo marca onde, segundo o mito, Ícaro caiu.</p>
    {act(3, "Localizar", 'No mapa, rodeia a ilha onde Dédalo e Ícaro estão presos e a cidade onde Dédalo nasceu.', "blue")}
    {nums("Em números", [("43 a.C.", "ano em que nasceu Ovídio, em Sulmona (atual Itália)"), ("15", "livros das <i>Metamorfoses</i>"), ("250", "mitos contados no poema (aproximadamente)")])}
  </div>
</div>
<div class="kicker" style="margin-top:5mm">Palavras para levar na viagem</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:2mm">
  {"".join(f'<div style="border-top:1.2mm solid var(--ink);padding-top:1.6mm"><b class="blue" style="font-family:FrauncesText;font-size:10pt">{a}</b><div class="small muted" style="line-height:1.3;margin-top:.4mm">{b}</div></div>' for a, b in [("labirinto", "construção com caminhos tão enredados que é difícil sair"), ("cera", "substância mole das abelhas; derrete com o calor"), ("exílio", "viver longe da sua terra, sem poder voltar"), ("desobedecer", "não fazer o que alguém mandou ou aconselhou")])}
</div>
<div class="panel coral" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center">
  <div class="hand" style="font-size:16pt;line-height:1.05;max-width:36mm">Enquanto lês</div>
  <div style="font-size:9.5pt">Sublinha a lápis <b>três conselhos ou avisos</b> que Dédalo dá ao filho. Na margem, marca com <b class="coral">!</b> o momento em que Ícaro faz a sua <b>escolha</b>. Os números dos parágrafos vão ajudar-te nas perguntas.</div>
</div>
''', "2.1 · Ícaro")

# ---------------------------------------------------------------- 4–5 THE MYTH (full retelling)
T1 = [
 'Do alto da torre onde vivia, Dédalo passava horas a olhar o mar. Para lá daquela linha azul ficava Atenas, a cidade onde <b>nascera</b> e de onde <b>saíra</b> muitos anos antes. Agora, era um prisioneiro em Creta — e com ele estava o filho, Ícaro, ainda rapaz.',
 'Nem sempre <b>fora</b> assim. Quando <b>chegara</b> à ilha, o rei Minos <b>recebera</b>-o com honras. Dédalo era o inventor mais famoso do seu tempo, e o rei <b>encomendara</b>-lhe uma obra que ninguém antes <b>tinha imaginado</b>: o Labirinto, um edifício de corredores tão enredados que quem lá entrava nunca mais dava com a saída. Lá dentro, Minos <b>fechara</b> o Minotauro, um monstro metade homem, metade touro.',
 'Só Dédalo conhecia todos os segredos do Labirinto. Por isso, quando <b>pedira</b> licença para voltar a casa, o rei <b>recusara</b>. E, numa ilha, quem não tem navio não tem caminho.',
 '— Minos pode ser dono da terra e do mar — disse Dédalo, certa manhã, ao filho. — Mas o céu está aberto. É por ali que vamos.',
 'Durante semanas, juntou penas: primeiro as mais pequenas, depois as médias, por fim as maiores, arrumadas por ordem, como as canas de uma flauta de pastor. Atou-as ao meio com fio de linho e colou-lhes a base com cera. Depois, curvou-as devagar, até parecerem asas de ave verdadeira. Ícaro brincava ao lado dele: corria atrás das penas que o vento levantava e amolecia a cera amarela com o polegar, sem saber que estava a mexer no seu próprio destino.',
]
T2 = [
 'Quando a obra ficou pronta, Dédalo prendeu as asas aos ombros, bateu-as e ficou suspenso no ar. Depois, vestiu as asas ao filho e aconselhou-o: — Voa sempre a meio caminho, Ícaro. Se desceres muito, a água do mar torna as penas pesadas. Se subires muito, o calor do sol queima-as. Voa entre um e outro, e segue-me. Enquanto falava, as mãos tremiam-lhe e as lágrimas corriam-lhe pela cara. Beijou o filho — e esse beijo foi o último.',
 'Levantaram voo. Dédalo ia à frente, como a ave que ensina a cria a sair do ninho, e olhava para trás a cada instante. Lá em baixo, um pescador com a sua cana, um pastor apoiado no cajado e um lavrador agarrado ao arado ergueram os olhos, espantados, e julgaram que aqueles dois eram deuses. As ilhas de Delos e de Paros já <b>tinham ficado</b> para trás; à esquerda aparecia Samos e, à direita, Lebinto e Calimno, a ilha do mel.',
 'Foi então que Ícaro começou a gostar demasiado de voar. Esqueceu o conselho que o pai lhe <b>tinha dado</b>, afastou-se dele e subiu, cada vez mais alto, atraído pelo céu. Perto do sol, a cera amoleceu e derreteu-se. As penas soltaram-se, uma a uma. Ícaro agitou os braços nus, mas já não havia nada que o segurasse no ar. Ainda gritou pelo pai, antes de a água azul lhe calar a voz.',
 '— Ícaro! Ícaro, onde estás? — chamava Dédalo, que já não era pai de ninguém. Procurou-o por toda a parte, até ver as penas a boiar nas ondas. Então amaldiçoou a sua arte. Levou o corpo do filho para uma ilha próxima e ali o sepultou.',
 'Essa ilha chama-se, desde então, Icária, e o mar onde Ícaro caiu ficou a chamar-se mar Icário. Mais tarde, Dédalo chegou à Sicília, cansado da viagem. <b>Tinha conseguido</b> fugir de Minos e do Labirinto — mas <b>perdera</b> aquilo que mais amava.',
]
tx1 = "".join(para(i, t) for i, t in enumerate(T1, 1))
tx2 = "".join(para(i, t) for i, t in enumerate(T2, 6))
P[4] = pg(4, f'''
<div style="display:grid;grid-template-columns:1fr 46mm;gap:7mm;flex:1">
<div>
  <div class="kicker blue">Texto 1 · Mito · leitura integral</div>
  <h2 style="margin-top:2mm;font-size:27pt">O voo de Ícaro</h2>
  <p style="font-family:FrauncesText;font-style:italic;font-size:11pt;line-height:1.45;color:var(--ink);margin-top:2mm">Um pai que inventou asas. Um filho que quis tocar no céu.</p>
  <div class="reading" style="margin-top:3.4mm;padding-left:7.5mm;line-height:1.5">{tx1}</div>
</div>
<aside style="border-left:.6pt solid var(--rule);padding-left:5mm;display:flex;flex-direction:column">
  <div class="kicker blue" style="margin-top:12mm">Glossário</div>
  {gloss([("Minos", "rei lendário de Creta, ilha grega do mar Mediterrâneo."), ("enredados", "cruzados e misturados, difíceis de seguir."), ("Minotauro", "monstro do mito grego, com corpo de homem e cabeça de touro."), ("licença", "autorização."), ("flauta de pastor", "instrumento feito de canas de tamanhos diferentes, lado a lado."), ("destino", "aquilo que vai acontecer a alguém.")])}
  <div class="panel" style="margin-top:auto;padding:3mm 3.4mm"><div class="kicker blue">Repara</div><p class="small" style="margin-top:1.2mm">As formas a <b>negrito</b> contam o que tinha acontecido <b>antes</b> do início da história. Vais estudá-las na p. 6.</p></div>
</aside>
</div>
''', "2.1 · Ícaro")
P[5] = pg(5, f'''
<div style="display:grid;grid-template-columns:1fr 40mm;gap:6mm">
<div>
  <div class="reading" style="padding-left:7.5mm;line-height:1.5">{tx2}</div>
  <p class="src" style="margin-top:2.4mm;padding-left:7.5mm">Texto escrito para este manual: reconto a partir das <i>Metamorfoses</i> de Ovídio, livro VIII.</p>
</div>
<aside style="border-left:.6pt solid var(--rule);padding-left:5mm;display:flex;flex-direction:column">
  <div class="kicker blue">Glossário</div>
  {gloss([("cajado", "pau comprido que o pastor usa para se apoiar e guiar o gado."), ("arado", "instrumento para lavrar a terra."), ("amaldiçoou", "desejou mal a; lamentou com raiva."), ("sepultou", "enterrou.")])}
</aside>
</div>
<div class="kicker blue" style="margin-top:2.5mm">Depois de ler · primeiras impressões</div>
<div class="grid2" style="margin-top:.5mm;gap:7mm">
  <div>{act(1, "Reagir", 'Que sentimento te deixou o parágrafo 9? Explica porquê numa frase.' + lines(2), "blue")}
  {act(2, "Confirmar", 'A tua previsão da p. 3 estava certa? O que acertaste e o que te surpreendeu?' + lines(2), "blue")}</div>
  <div>{act(3, "Ordenar", 'Numera de 1 a 5, pela ordem da história.<div style="display:grid;grid-template-columns:7mm 1fr;gap:1.2mm 2mm;margin-top:1.8mm;font-size:9.2pt;align-items:center"><span class="chk"></span><span>A cera derrete-se.</span><span class="chk"></span><span>Minos não deixa Dédalo partir.</span><span class="chk"></span><span>Dédalo dá conselhos ao filho.</span><span class="chk"></span><span>Os camponeses julgam que viram deuses.</span><span class="chk"></span><span>Dédalo junta penas por ordem de tamanho.</span></div>', "blue")}
  {act(4, "Explicar", 'Um mito <b>explica a origem</b> de alguma coisa. Porque é que o mar se chama «Icário»? E que <b>aviso</b> nos deixa esta história?' + lines(2), "blue")}</div>
</div>
''', "2.1 · Ícaro")

# ---------------------------------------------------------------- 6 COMPREHENSION — five pieces + cause/consequence + oral
cat_rows = [("Narrador", "Participa na história? Em que pessoa conta?", "§ 1"), ("Personagens", "Principais e secundárias", "§ 2, § 7"),
            ("Espaço", "Três lugares onde a ação acontece", ""), ("Tempo", "Quanto tempo leva Dédalo a fazer as asas?", "§ 5"),
            ("Ação", "O problema · o plano · o desenlace", "")]
ct = "".join(f'<tr><td style="font-size:9pt;width:54mm">{a}<div class="small muted" style="font-weight:400;margin-top:.4mm">{b}</div></td><td style="width:14mm;font-size:8pt;color:var(--muted);text-align:center">{p}</td><td style="height:10.5mm"></td></tr>' for a, b, p in cat_rows)
chain = [("Minos não deixa Dédalo sair de Creta.", ""), ("", "Dédalo decide fugir pelo ar."), ("Ícaro sobe demasiado alto.", ""), ("", "")]
def cc(a, b):
    ca = a or ""
    cb = b or ""
    return (f'<div class="panel" style="padding:2.4mm 2.8mm;min-height:13mm;font-size:9pt">{ca}</div><b class="coral" style="text-align:center;font-family:Body">→</b>'
            f'<div class="panel coral" style="padding:2.4mm 2.8mm;min-height:13mm;font-size:9pt">{cb}</div>')
chh = "".join(cc(a, b) for a, b in chain)
P[6] = pg(6, f'''
<div class="kicker blue">Estação 2.1 · Compreender e contar</div>
<h2 style="margin-top:2mm">As peças do mito e o <em>peso</em> de uma escolha</h2>
{act(1, "Analisar", 'Completa a tabela com a caixa de ferramentas do leitor (p. 2). Usa os parágrafos indicados.', "blue")}
<table class="cmp ruled" style="margin-top:2mm"><tr><th style="background:var(--ink)">Categoria</th><th style="background:var(--ink);text-align:center">Onde?</th><th style="background:var(--ink)">No mito de Dédalo e Ícaro</th></tr>{ct}</table>
<div class="grid2" style="margin-top:4mm;grid-template-columns:1.12fr 1fr;gap:7mm">
  <div>
    {act(2, "Relacionar", 'Causa e consequência. Completa a cadeia: a consequência de um acontecimento é a causa do seguinte.', "blue")}
    <div style="display:grid;grid-template-columns:1fr 6mm 1fr;gap:2.4mm 0;align-items:center;margin-top:2mm">
      <div class="kicker blue">Causa</div><span></span><div class="kicker">Consequência</div>{chh}
    </div>
  </div>
  <div>
    {act(3, "Interpretar", 'Ícaro <b>escolheu</b> subir. O que o levou a essa escolha? Dá uma pista do texto (§ 8).' + lines(2), "blue")}
    {act(4, "Opinar", 'Dédalo também tem alguma responsabilidade? Justifica.' + lines(2), "blue")}
  </div>
</div>
<div class="panel" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{MICRO.replace('class="ico"', 'class="ico" style="width:8mm;height:8mm"')}<div><div class="kicker blue">Oralidade · Conta o mito em 2 minutos</div><div class="small muted">Sem ler. Usa o cartão como guia e termina a explicar a consequência da escolha de Ícaro.</div></div></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:2.6mm;font-size:8.8pt;line-height:1.3">
    <div style="border-top:1.2mm solid var(--ink);padding-top:1.4mm"><b class="blue">1 · Começo</b><br>«Há muito tempo, em Creta…»</div>
    <div style="border-top:1.2mm solid var(--ink);padding-top:1.4mm"><b class="blue">2 · O problema</b><br>Porque estão presos?</div>
    <div style="border-top:1.2mm solid var(--ink);padding-top:1.4mm"><b class="blue">3 · O plano e o voo</b><br>As asas, o conselho, a subida.</div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:1.4mm"><b class="coral">4 · A consequência</b><br>«Por ter escolhido…, Ícaro…»</div>
  </div>
  <div style="display:flex;gap:5mm;flex-wrap:wrap;margin-top:3mm;font-size:8.6pt;border-top:.6pt solid var(--rule);padding-top:2.4mm"><b class="blue">O colega avalia:</b><span><span class="chk"></span>ordem certa</span><span><span class="chk"></span>voz clara</span><span><span class="chk"></span>conectores de tempo</span><span><span class="chk"></span>explica a consequência</span><span><span class="chk"></span>olha para o público</span></div>
</div>
''', "2.1 · Ícaro")


# ================================================================ STATION 2.2 · ULISSES (pp. 7–10)
def cell(k, t, c=INK):
    return f'<div style="border-top:1.2mm solid {c};padding-top:1.6mm"><div class="kicker" style="color:{c}">{k}</div><div style="font-size:9pt;line-height:1.32;margin-top:.6mm">{t}</div></div>'

trk = [("Páginas", 'Na tua edição, o episódio vai da p. <span class="fill s"></span> à p. <span class="fill s"></span>.'),
       ("O lugar", "Três pormenores que descrevem a ilha e a gruta."),
       ("O obstáculo", "O que impede Ulisses e os companheiros de fugir?"),
       ("A artimanha", "Que nome diz Ulisses ao gigante? Porque é tão útil?"),
       ("A frase que guardo", "Copia uma frase curta de que gostaste e indica a página.")]
trk_rows = "".join(f'<tr><td style="font-size:9pt;width:62mm">{a}<div class="small muted" style="font-weight:400;margin-top:.4mm">{b}</div></td><td style="height:10mm"></td></tr>' for a, b in trk)
P[7] = pg(7, f"""
<div class="kicker blue">Estação 2.2 · Clássico</div>
<h2 style="margin-top:2mm">Ulisses, o herói que <em>pensa</em> antes de lutar</h2>
<div style="margin-top:3.4mm;height:36mm;border-radius:3mm;overflow:hidden"><img class="cover" src="img/ulisses.jpg" style="object-position:50% 55%"></div>
<div class="grid2" style="margin-top:4mm;grid-template-columns:1.05fr 1fr;gap:7mm;align-items:start">
  <div class="panel blue" style="padding:3.6mm 4.2mm">
    <div class="kicker blue">De Homero a Maria Alberta Menéres</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.42">A <b>Odisseia</b> é um longo poema grego, atribuído a <b>Homero</b> e dividido em 24 cantos. Conta o regresso de <b>Ulisses</b> (em grego, Odisseu), rei da ilha de Ítaca: depois de dez anos de guerra em Troia, leva outros dez a voltar para casa, para junto da mulher, Penélope, e do filho, Telémaco.</p>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.42"><b>Maria Alberta Menéres</b> (1930–2019), poeta e escritora, recontou estas aventuras para jovens leitores no livro <i>Ulisses</i>, que vais ler na edição da turma.</p>
    <div style="margin-top:2.6mm">{qr("q-odisseia", "Explorar", "A Odisseia na Wikipédia: os cantos, as personagens e a viagem.")}</div>
  </div>
  <div>
    {act(1, "Observar", 'Quem está dentro da gruta? E quem chega de barco? O que pode acontecer quando se encontrarem?' + lines(2), "blue")}
    {act(2, "Ativar", 'Um herói vence sempre pela força? Dá o exemplo de alguém (de um livro, filme ou jogo) que venceu com uma <b>ideia</b>.' + lines(2), "blue")}
  </div>
</div>
<div class="panel" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:4mm"><div class="kicker blue">Leitura integral · edição da turma · o episódio de Polifemo</div><div class="small muted">Lê o episódio inteiro e regista enquanto lês.</div></div>
  <table class="cmp ruled" style="margin-top:2.2mm;background:#fff;border-radius:2mm">{trk_rows}</table>
</div>
""", "2.2 · Ulisses")

N1 = [
 'Depois de muitos dias no mar, Ulisses chegou a uma ilha de montes verdes, onde cabras selvagens saltavam pelas rochas. Junto à praia, no alto de uma falésia coberta de loureiros, abria-se a boca escura de uma gruta. Ulisses escolheu doze companheiros e levou um odre de vinho tão forte que só se bebia misturado com muita água.',
 'A gruta estava vazia, mas cheia de coisas: cestos de queijos, baldes de leite, cordeiros e cabritos fechados em currais. — Levemos os queijos e fujamos! — pediram os companheiros. Ulisses não quis: tinha curiosidade de conhecer o dono daquela casa.',
 'Ao fim da tarde, o dono chegou. Era <b>Polifemo</b>, um Ciclope: um gigante com um só olho no meio da testa, filho de Posêidon, o deus do mar. Meteu o rebanho na gruta e tapou a entrada com uma pedra que nem vinte e dois carros de bois conseguiriam arrastar. Quando viu os estrangeiros, agarrou dois deles e comeu-os ao jantar. Depois, adormeceu.',
 'Ulisses pegou na espada, mas parou a tempo. Se matasse o gigante, quem afastaria a pedra? Ficariam ali presos para sempre. Era preciso um plano.',
 'No dia seguinte, enquanto Polifemo levava o rebanho ao pasto, Ulisses cortou um tronco de oliveira, afiou-lhe a ponta e endureceu-a no fogo. Depois, escondeu a estaca.',
]
N2 = [
 'À noite, ofereceu vinho ao Ciclope. Polifemo bebeu uma taça, e outra, e outra.<br>— Dá-me mais! E diz-me como te chamas, estrangeiro.<br>— Chamo-me <b>Ninguém</b> — respondeu Ulisses.<br>— Pois então, Ninguém, vou dar-te um presente: serás o último a ser comido!<br>O gigante riu-se e caiu, vencido pelo vinho e pelo sono.',
 'Ulisses aqueceu a estaca nas brasas até ficar em fogo e, com quatro companheiros, cravou-a no olho do Ciclope. Polifemo soltou um urro que fez tremer a montanha. Os outros Ciclopes acorreram.<br>— Porque gritas assim, Polifemo? Alguém te quer fazer mal?<br>— Ninguém! Ninguém me quer matar!<br>— Se ninguém te faz mal, dorme — responderam. E foram-se embora.',
 'Faltava sair. De manhã, o gigante cego afastou a pedra e sentou-se à entrada, de braços abertos. Ulisses atou os carneiros de três em três e prendeu um homem debaixo de cada carneiro do meio. Ele próprio agarrou-se à lã da barriga do maior carneiro de todos. Polifemo apalpou o dorso dos animais, um a um, mas não se lembrou de lhes apalpar a barriga. Assim saíram todos.',
 'Já no barco, Ulisses não resistiu e gritou:<br>— Ciclope! Se te perguntarem quem te cegou, diz que foi Ulisses, rei de Ítaca!<br>Furioso, Polifemo arrancou um penedo e atirou-o ao mar. Depois, pediu ao pai, Posêidon, que castigasse aquele homem. O deus ouviu-o — e a viagem de Ulisses para casa tornou-se ainda mais longa.',
]
nx1 = "".join(para(i, t) for i, t in enumerate(N1, 1))
nx2 = "".join(para(i, t) for i, t in enumerate(N2, 6))
gl8 = [("odre", "saco de pele para levar líquidos."), ("curral", "lugar fechado onde se guarda o gado."), ("Posêidon", "deus grego do mar."), ("estaca", "pau comprido com a ponta afiada."), ("urro", "grito forte, como o de uma fera."), ("penedo", "rocha grande.")]
P[8] = pg(8, f"""
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:6mm">
  <div><div class="kicker blue">Texto 2 · Reconto a partir de Homero</div><h2 style="margin-top:2mm;font-size:27pt">Ninguém</h2></div>
  <p style="font-family:FrauncesText;font-style:italic;font-size:10.6pt;line-height:1.4;color:var(--ink);max-width:88mm;text-align:right">A mesma aventura que leste em Maria Alberta Menéres, contada mais perto do poema antigo.</p>
</div>
<div class="grid2" style="margin-top:3mm;gap:7mm">
  <div class="reading" style="padding-left:7.5mm;line-height:1.5">{nx1}</div>
  <div class="reading" style="padding-left:7.5mm;line-height:1.5">{nx2}</div>
</div>
<p class="src" style="margin-top:1mm;padding-left:7.5mm">Texto escrito para este manual: reconto a partir da <i>Odisseia</i> de Homero, canto IX.</p>
<div style="margin-top:auto;border-top:.6pt solid var(--rule);padding-top:2.4mm;display:grid;grid-template-columns:repeat(6,1fr);gap:3mm">
  {"".join(f'<div><b class="blue" style="font-family:FrauncesText;font-size:9pt">{a}</b><div class="small muted" style="line-height:1.28">{b}</div></div>' for a, b in gl8)}
</div>
""", "2.2 · Ulisses")

obs = [("Estão fechados na gruta.", "Não matar o gigante que dorme: só ele move a pedra.", "§ 3–4"),
       ("O gigante é mais forte do que todos.", "", "§ 5–6"),
       ("Os outros Ciclopes vêm ajudar.", "", "§ 7"),
       ("Polifemo guarda a saída.", "", "§ 8")]
obs_rows = "".join(f'<tr><td style="font-size:9pt">{a}</td><td style="height:11mm;font-family:Caveat;font-size:13pt;color:var(--ink)">{b}</td><td style="width:13mm;text-align:center;font-size:8pt;color:var(--muted)">{c}</td></tr>' for a, b, c in obs)
P[9] = pg(9, f"""
<div class="kicker blue">Estação 2.2 · Educação literária</div>
<h2 style="margin-top:2mm">Herói, obstáculo e <em>artimanha</em></h2>
<div class="grid3" style="margin-top:3.4mm;gap:4mm">
  <div class="rule-card"><b class="blue">Herói</b><div class="small">a personagem principal que enfrenta perigos e mostra qualidades: coragem, inteligência, lealdade.</div></div>
  <div class="rule-card o"><b class="coral">Obstáculo</b><div class="small">tudo o que impede o herói de alcançar o seu objetivo: um inimigo, um lugar, uma prova.</div></div>
  <div class="rule-card c"><b class="sea">Artimanha</b><div class="small">um plano esperto, um truque para vencer quem é mais forte. É a arma preferida de Ulisses.</div></div>
</div>
{act(1, "Analisar", 'Para cada obstáculo, escreve a artimanha de Ulisses. A primeira já está feita.', "blue")}
<table class="cmp ruled" style="margin-top:2mm"><tr><th style="background:var(--coral)">Obstáculo</th><th style="background:var(--sea)">Artimanha</th><th style="background:var(--ink);text-align:center">Onde?</th></tr>{obs_rows}</table>
<div class="grid2" style="margin-top:1mm;gap:7mm">
  <div>{act(2, "Descrever", 'Nos § 1–2, sublinha as palavras que descrevem a ilha e a gruta. Copia as três que melhor te fazem <b>ver</b> o lugar.' + lines(2), "blue")}
  {act(3, "Avaliar", 'No § 9, Ulisses grita o seu verdadeiro nome. Foi uma boa ideia? Que consequência tem?' + lines(3), "blue")}</div>
  <div>{act(4, "Comparar", 'Relê o episódio na edição da turma. Encontra duas diferenças entre as duas versões.<table class="cmp ruled" style="margin-top:1.6mm;font-size:8.4pt"><tr><th style="background:var(--ink)">Menéres · p. ___</th><th style="background:var(--ink)">Texto 2 · § ___</th></tr><tr><td style="height:12mm"></td><td></td></tr><tr><td style="height:12mm"></td><td></td></tr></table>', "blue")}</div>
</div>
<div class="panel" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{MICRO.replace('class="ico"', 'class="ico" style="width:8mm;height:8mm"')}<div><div class="kicker blue">Oralidade · Expõe o plano de Ulisses em 2 minutos</div><div class="small muted">És o conselheiro do herói e explicas aos companheiros como vão sair da gruta. Prepara em tópicos; não leias.</div></div></div>
  <div style="display:grid;grid-template-columns:1fr 1.5fr 1fr;gap:4mm;margin-top:2.6mm">
    {cell("Abertura", "Capta a atenção com uma pergunta: «Como se foge de uma gruta fechada por um gigante?»")}
    {cell("Desenvolvimento", "O problema e os passos do plano, por ordem: <i>primeiro</i>, <i>depois</i>, <i>a seguir</i>, <i>por fim</i>.")}
    {cell("Fecho", "O resultado e uma frase final: «Assim, quem vence é…»", COR)}
  </div>
  <div style="display:flex;gap:5mm;flex-wrap:wrap;margin-top:3mm;font-size:8.6pt;border-top:.6pt solid var(--rule);padding-top:2.4mm"><b class="blue">O colega avalia:</b><span><span class="chk"></span>abertura que prende</span><span><span class="chk"></span>passos por ordem</span><span><span class="chk"></span>conectores</span><span><span class="chk"></span>fecho claro</span><span><span class="chk"></span>voz e olhar</span></div>
</div>
""", "2.2 · Ulisses")

P[10] = pg(10, f"""
<div class="kicker sea">Estação 2.2 · Gramática</div>
<h2 style="margin-top:2mm">Verbo transitivo, intransitivo e <em>complemento direto</em></h2>
<div class="grid2" style="margin-top:3.6mm;gap:5mm;align-items:stretch">
  <div class="panel sea" style="padding:3.4mm 4mm">
    <div class="kicker sea">Transitivo · precisa de um complemento</div>
    <p style="font-family:FrauncesText;font-size:10.2pt;margin-top:1.6mm">Ulisses <b class="sea">cegou</b> <span class="mk-c">o Ciclope</span>.</p>
    <p style="font-size:9pt;margin-top:1.4mm;line-height:1.38">«Ulisses cegou» fica incompleto. O que falta é o <b>complemento direto</b>: responde a <i>o quê?</i> ou <i>quem?</i> e pode ser substituído por <b>o, a, os, as</b>: <i>Ulisses cegou-<b>o</b>.</i></p>
  </div>
  <div class="panel" style="padding:3.4mm 4mm">
    <div class="kicker blue">Intransitivo · tem sentido completo</div>
    <p style="font-family:FrauncesText;font-size:10.2pt;margin-top:1.6mm">O gigante <b class="blue">adormeceu</b>. Os barcos <b class="blue">partiram</b>.</p>
    <p style="font-size:9pt;margin-top:1.4mm;line-height:1.38">Cuidado: o mesmo verbo pode ser das duas espécies. <i>O Ciclope <b>bebeu</b>.</i> (intransitivo) · <i>O Ciclope <b>bebeu</b> <span class="mk-c">o vinho</span>.</i> (transitivo)</p>
  </div>
</div>
<div class="grid2" style="gap:7mm">
  <div>{act(1, "Classificar", 'Escreve <b>T</b> (transitivo) ou <b>I</b> (intransitivo).<div style="display:grid;grid-template-columns:1fr 7mm;gap:1.7mm 2mm;margin-top:1.8mm;font-size:9.2pt;align-items:center"><span>Polifemo tapou a entrada.</span><span class="chk"></span><span>Os companheiros tremiam.</span><span class="chk"></span><span>Ulisses afiou a estaca.</span><span class="chk"></span><span>O gigante gritou.</span><span class="chk"></span></div>', "sea")}</div>
  <div>{act(2, "Substituir", 'Sublinha o complemento direto e substitui-o por um pronome.<div style="font-size:9.2pt;margin-top:1.6mm;line-height:1.5">Ulisses escolheu <u>doze homens</u>. <span style="font-family:Body">→</span> Ulisses escolheu-<b>os</b>.<br>Polifemo apalpou os carneiros. <span style="font-family:Body">→</span> <span class="fill l"></span><br>Ulisses aqueceu a estaca. <span style="font-family:Body">→</span> <span class="fill l"></span></div>', "sea")}</div>
</div>
<div class="kicker coral" style="margin-top:5mm">Estação 2.2 · Escrita</div>
<h3 style="margin-top:1mm">Uma nova ilha: narrativa com descrição de um lugar e diálogo</h3>
<p style="font-size:9.6pt;margin-top:1.4mm">Ulisses e os companheiros desembarcam numa ilha desconhecida. Escreve o episódio (<b>120 a 160 palavras</b>): descreve o lugar, cria um obstáculo e inclui um diálogo em que Ulisses explica a sua artimanha.</p>
<div class="grid3" style="margin-top:2.4mm;gap:3mm">
  <div class="panel" style="padding:2.8mm 3.2mm"><div class="kicker blue">O lugar</div><p class="small" style="margin-top:.6mm">O que se vê, ouve e cheira?</p>{lines(2)}</div>
  <div class="panel" style="padding:2.8mm 3.2mm"><div class="kicker blue">O obstáculo</div><p class="small" style="margin-top:.6mm">Quem ou o que os ameaça?</p>{lines(2)}</div>
  <div class="panel coral" style="padding:2.8mm 3.2mm"><div class="kicker">A artimanha</div><p class="small" style="margin-top:.6mm">Qual é o truque de Ulisses?</p>{lines(2)}</div>
</div>
{lines(9)}
<div style="display:flex;gap:4mm;flex-wrap:wrap;margin-top:auto;font-size:8.6pt;border-top:.6pt solid var(--rule);padding-top:2.4mm">
  <span><span class="chk"></span>descrição com 2 sentidos</span><span><span class="chk"></span>travessão em cada fala</span><span><span class="chk"></span>verbos que introduzem as falas (<i>disse</i>, <i>perguntou</i>)</span><span><span class="chk"></span>2 verbos transitivos com complemento direto</span>
</div>
""", "2.2 · Ulisses")

# ================================================================ STATION 2.3 · A FADA ORIANA (pp. 11–13)
stops = [("Paragem 1 · A promessa", "Que tarefa recebe Oriana da Rainha das Fadas? A quem ajuda logo no início?", INK),
         ("Paragem 2 · O peixe", "Como conhece Oriana o peixe? O que lhe diz ele, dia após dia?", INK),
         ("Paragem 3 · O castigo", "O que perde Oriana e porquê?", COR),
         ("Paragem 4 · O desenlace", "Que gesto faz Oriana no fim? O que recebe de volta?", COR)]
stops_h = "".join(f'<div style="border-top:1.2mm solid {c};padding-top:1.6mm"><div style="display:flex;justify-content:space-between"><div class="kicker" style="color:{c}">{a}</div><span class="small muted">pp. <span class="fill s"></span></span></div><div style="font-size:9pt;line-height:1.32;margin-top:.8mm">{b}</div>{lines(2)}</div>' for a, b, c in stops)
P[11] = pg(11, f"""
<div class="kicker">Estação 2.3 · Conto de autor</div>
<h2 style="margin-top:2mm">A Fada Oriana e a <em>promessa</em></h2>
<div style="margin-top:3.4mm;height:62mm;border-radius:3mm;overflow:hidden"><img class="cover" src="img/oriana.jpg" style="object-position:50% 50%"></div>
<div class="grid2" style="margin-top:4mm;grid-template-columns:1.05fr 1fr;gap:7mm;align-items:start">
  <div class="panel coral" style="padding:3.6mm 4.2mm">
    <div class="kicker">Quem escreveu?</div>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.42"><b>Sophia de Mello Breyner Andresen</b> (Porto, 1919 – Lisboa, 2004) foi uma das maiores poetas portuguesas do século XX e a primeira mulher portuguesa a receber o <b>Prémio Camões</b>, em 1999.</p>
    <p style="font-size:9.2pt;margin-top:1.4mm;line-height:1.42">Escreveu também contos para crianças. <i>A Fada Oriana</i> foi publicado em 1958; <i>O Cavaleiro da Dinamarca</i>, outro conto seu, espera-te na p. 15.</p>
  </div>
  <div>
    {act(1, "Prever", 'A fada olha para o lago, para a casa e para a cidade ao longe. Qual destes lugares achas que vai ser importante na história? Porquê?' + lines(3))}
    {act(2, "Refletir", 'Já fizeste uma promessa difícil de cumprir? O que te ajudou (ou não) a cumpri-la?' + lines(2))}
  </div>
</div>
<div class="panel" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:4mm"><div class="kicker">Leitura integral · edição da turma · diário de leitura</div><div class="small muted">Lê o conto inteiro. Em cada paragem, responde.</div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm 6mm;margin-top:2.4mm">{stops_h}</div>
</div>
""", "2.3 · Oriana")

ppl = ["A velha", "O lenhador", "O moleiro", "O Homem Muito Rico", "O Poeta"]
ppl_rows = "".join(f'<tr><td style="font-size:9pt">{a}</td><td style="height:10mm"></td><td></td></tr>' for a in ppl)
arc = [("A promessa", "O que promete Oriana, e a quem?", INK), ("A prova", "Que tentação aparece? O que esquece Oriana?", COR), ("O desenlace", "Como se resolve a história? O que aprendeu Oriana?", SEA)]
arc_h = "".join(f'<div class="panel" style="padding:3mm 3.4mm;border-top:1.4mm solid {c};border-radius:0 0 3mm 3mm"><div class="kicker" style="color:{c}">{i} · {a}</div><p class="small" style="margin-top:.6mm">{b}</p>{lines(3)}</div>' for i, (a, b, c) in enumerate(arc, 1))
P[12] = pg(12, f"""
<div class="kicker">Estação 2.3 · Educação literária</div>
<h2 style="margin-top:2mm">A promessa, a prova e o <em>desenlace</em></h2>
<p style="font-size:9.8pt;margin-top:2.4mm;max-width:170mm">Em muitos contos, a personagem <b>promete</b> alguma coisa, é posta à <b>prova</b> por uma tentação ou um perigo e, no <b>desenlace</b>, mostra se aprendeu. Segue este caminho na história de Oriana.</p>
{act(1, "Esquematizar", 'Completa as três etapas do conto.')}
<div class="grid3" style="margin-top:2mm;gap:3.4mm">{arc_h}</div>
{act(2, "Relacionar", 'Oriana prometeu cuidar dos homens, dos animais e das plantas da floresta. Completa com o que leste.')}
<table class="cmp ruled" style="margin-top:2mm"><tr><th style="background:var(--coral)">Quem?</th><th style="background:var(--coral)">O que Oriana fazia por ele(a)</th><th style="background:var(--coral)">O que lhe acontece quando Oriana o(a) esquece</th></tr>{ppl_rows}</table>
<div style="margin-top:4mm">{act(3, "Opinar", 'Oriana perdeu as asas e os poderes por ter esquecido a promessa. Achas que foi um castigo justo? Dá uma razão.' + lines(3))}</div>
<div class="panel coral" style="margin-top:auto;padding:4mm 4.5mm">
  <div style="display:flex;gap:3mm;align-items:center">{MICRO.replace('class="ico"', 'class="ico" style="width:8mm;height:8mm"')}<div><div class="kicker">Oralidade · Lê uma passagem e justifica a tua escolha</div><div class="small muted">Escolhe na edição da turma uma passagem de 5 a 8 linhas que te pareça essencial.</div></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:2.6mm">
    <div style="font-size:9pt;line-height:1.4">
      <b class="coral">Preparar</b><br>1 · Indica a página: <span class="fill s"></span> e o momento da história.<br>2 · Marca com <b>/</b> as pausas curtas e com <b>//</b> as longas.<br>3 · Sublinha as palavras a dizer com mais força.<br>4 · Ensaia três vezes, a última para um colega.
    </div>
    <div style="font-size:9pt;line-height:1.4">
      <b class="coral">Justificar</b> (depois de leres)<br><i>Escolhi esta passagem porque…</i><br><i>Neste momento, Oriana…</i><br><i>Mostra que…</i>{lines(2)}
    </div>
  </div>
</div>
""", "2.3 · Oriana")

parts_ = [("prometer", "prometido"), ("cuidar", "cuidado"), ("partir", "partido"), ("fazer", "feito"), ("dizer", "dito"), ("ver", "visto"), ("pôr", "posto"), ("abrir", "aberto")]
pt_h = "".join(f'<div style="border-top:.6pt solid var(--rule);padding:.9mm 0;display:flex;justify-content:space-between;font-size:9pt"><span>{a}</span><b class="sea">{b}</b></div>' for a, b in parts_)
P[13] = pg(13, f"""
<div class="kicker sea">Estação 2.3 · Gramática</div>
<h2 style="margin-top:2mm">Verbo auxiliar e <em>particípio passado</em></h2>
<div class="grid2" style="margin-top:3.6mm;grid-template-columns:1.35fr 1fr;gap:5mm;align-items:stretch">
  <div class="panel sea" style="padding:3.4mm 4mm">
    <div class="kicker sea">Dois verbos a trabalhar juntos</div>
    <p style="font-family:FrauncesText;font-size:10.2pt;margin-top:1.6mm">Oriana <span class="mk-c">tinha</span> <b class="sea">prometido</b> cuidar da floresta.</p>
    <p style="font-size:9pt;margin-top:1.4mm;line-height:1.38">Nos tempos compostos, o verbo <b>auxiliar</b> (<b>ter</b> ou, mais raramente, <b>haver</b>) é o que se conjuga; o verbo principal vai para o <b>particípio passado</b>. <b>Ser</b> e <b>estar</b> também podem ser auxiliares: <i>As asas <b>foram devolvidas</b> a Oriana.</i></p>
    <p style="font-size:9pt;margin-top:1.4mm;line-height:1.38">Lembras-te de «nascera» e «saíra» (p. 4)? É o <b>pretérito mais-que-perfeito</b>: <i>nascera</i> = <i>tinha nascido</i>.</p>
  </div>
  <div class="panel" style="padding:3.4mm 4mm">
    <div class="kicker blue">O particípio passado</div>
    <p class="small" style="margin-top:1mm">Regulares em <b>-ado</b> e <b>-ido</b>; alguns são irregulares.</p>
    <div style="margin-top:1mm">{pt_h}</div>
  </div>
</div>
<div class="grid2" style="gap:7mm">
  <div>{act(1, "Identificar", 'Sublinha o verbo auxiliar e rodeia o particípio.<div style="font-family:FrauncesText;font-size:10pt;line-height:1.65;margin-top:1.4mm">O peixe tinha caído na margem.<br>Oriana tinha esquecido a velha.<br>A floresta foi abandonada.</div>', "sea")}</div>
  <div>{act(2, "Transformar", 'Reescreve com <b>tinha</b> + particípio.<div style="font-size:9.2pt;line-height:1.5;margin-top:1.4mm">Oriana <i>esquecera</i> a promessa.<br><span style="font-family:Body">→</span> <span class="fill l" style="min-width:52mm"></span><br>A Rainha <i>vira</i> tudo.<br><span style="font-family:Body">→</span> <span class="fill l" style="min-width:52mm"></span></div>', "sea")}</div>
</div>
<div class="kicker coral" style="margin-top:5mm">Estação 2.3 · Escrita</div>
<h3 style="margin-top:1mm">Texto de opinião: a decisão de Oriana</h3>
<p style="font-size:9.6pt;margin-top:1.4mm">No fim do conto, para salvar a velha, Oriana lança-se no abismo, sem asas. <b>Foi uma decisão corajosa ou imprudente?</b> Escreve um texto de opinião (<b>100 a 140 palavras</b>) com <b>dois argumentos</b>, cada um com um exemplo do conto.</p>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:2.4mm">
  {cell("1 · Opinião", "Na minha opinião, …", COR)}{cell("2 · Argumento 1", "Em primeiro lugar, … Por exemplo, …")}{cell("3 · Argumento 2", "Além disso, … Prova disso é …")}{cell("4 · Conclusão", "Em conclusão, … / Por isso, …", COR)}
</div>
{lines(9)}
<div style="display:flex;gap:4mm;flex-wrap:wrap;margin-top:auto;font-size:8.6pt;border-top:.6pt solid var(--rule);padding-top:2.4mm">
  <span><span class="chk o"></span>opinião no início</span><span><span class="chk o"></span>2 argumentos com exemplos</span><span><span class="chk o"></span>conectores</span><span><span class="chk o"></span>conclusão</span><span><span class="chk o"></span>1 tempo composto (<i>tinha</i> + particípio)</span>
</div>
""", "2.3 · Oriana")

# ================================================================ 2.4 · LITERATURAS DE LÍNGUA PORTUGUESA (p. 14)
def w(lon, lat):
    return ((lon + 86) * 2, (47 - lat) * 2)
marks = [(1, -8.2, 39.6, 141, 18), (2, -51, -10, 70, 112), (3, -23.8, 15.1, 108, 55), (4, -15.2, 12, 126, 84),
         (5, 6.7, 0.3, 172, 106), (6, 10.3, 1.6, 207, 80), (7, 17.5, -12.5, 207, 119), (8, 35, -18, 244, 131), (9, 125.7, -8.8, 432, 126)]
mk = ""
for n, lon, lat, bx, by in marks:
    x, y = w(lon, lat)
    mk += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{bx}" y2="{by}" stroke="#17315A" stroke-width=".8"/><circle cx="{x:.1f}" cy="{y:.1f}" r="1.6" fill="#17315A"/><circle cx="{bx}" cy="{by}" r="6.4" fill="#17315A" stroke="#fff" stroke-width="1.2"/><text x="{bx}" y="{by+2.9}" text-anchor="middle" font-family="Grotesk" font-weight="700" font-size="8" fill="#fff">{n}</text>'
MAP = (f'<svg viewBox="0 0 {WW} {WH}" style="width:100%;display:block;border-radius:2.4mm;background:#DCE5F0">'
       f'<path d="{WORLD}" fill="#F4EDE1" stroke="#C9CFD9" stroke-width=".4"/><path d="{LUSO}" fill="#E4502F" stroke="#fff" stroke-width=".4"/>{mk}'
       f'<text x="8" y="{WH-8}" font-family="Grotesk" font-size="7" fill="#5B6475">Países da CPLP a coral · os números correspondem aos cartões</text></svg>')
auth = [(1, "Portugal", "Sophia de Mello Breyner Andresen", "1919–2004", "Já a conheces: <i>A Fada Oriana</i> (p. 11) e <i>O Cavaleiro da Dinamarca</i> (p. 15).", ""),
        (2, "Brasil", "Monteiro Lobato", "1882–1948", "Criou o Sítio do Picapau Amarelo. Em <i>O Saci</i> (1921), Pedrinho conhece a figura que vais encontrar na p. 25.", "ponte 2.9"),
        (3, "Cabo Verde", "Germano Almeida", "n. 1945", "Nasceu na ilha da Boa Vista. <i>A Ilha Fantástica</i> (1994) recria a infância nessa ilha. Prémio Camões 2018.", ""),
        (4, "Guiné-Bissau", "Abdulai Sila", "n. 1958", "Nasceu em Catió. <i>Eterna Paixão</i> (1994) é considerado o primeiro romance guineense.", "para mais tarde"),
        (5, "São Tomé e Príncipe", "Conceição Lima", "1961–2026", "Poeta e jornalista. O seu primeiro livro de poemas, <i>O Útero da Casa</i>, saiu em 2004.", ""),
        (6, "Guiné Equatorial", "Um país, três línguas", "CPLP desde 2014", "O português é língua oficial, a par do espanhol e do francês. Os seus escritores mais conhecidos escrevem em espanhol.", ""),
        (7, "Angola", "Ondjaki", "n. 1977", "Nasceu em Luanda. Em <i>Os da Minha Rua</i>, conta em pequenas histórias a sua infância nessa cidade.", ""),
        (8, "Moçambique", "Mia Couto", "n. 1955", "Nasceu na Beira. Prémio Camões 2013. Vais ler <i>O Beijo da Palavrinha</i> na p. 19.", "ponte 2.6"),
        (9, "Timor-Leste", "Luís Cardoso", "n. 1958", "Nasceu em Cailaco. <i>Crónica de uma Travessia</i> (1997) é um romance de memórias sobre Timor.", "para mais tarde")]
def acard(n, pais, a, d, t, tag):
    tg = ""
    if tag:
        tg = (f'<span class="tag o" style="margin-left:1.4mm">{tag}</span>' if tag.startswith("ponte")
              else f'<span class="tag line" style="margin-left:1.4mm;color:var(--muted)">{tag}</span>')
    return (f'<div style="border-top:1.2mm solid var(--ink);padding-top:1.4mm;display:grid;grid-template-columns:6.4mm 1fr;gap:2mm">'
            f'<div style="width:6.4mm;height:6.4mm;border-radius:50%;background:var(--ink);color:#fff;font-family:Grotesk;font-weight:700;font-size:7.6pt;line-height:6.4mm;text-align:center">{n}</div>'
            f'<div><div class="kicker coral" style="font-size:6.6pt">{pais}{tg}</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.8pt;color:var(--ink);line-height:1.2;margin-top:.4mm">{a} <span class="small muted" style="font-family:Body;font-weight:400">· {d}</span></div>'
            f'<div class="small" style="line-height:1.32;margin-top:.5mm">{t}</div></div></div>')
P[14] = pg(14, f"""
<div class="kicker">2.4 · Explorar</div>
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:6mm;margin-top:2mm">
  <h2>Uma língua, <em>nove</em> países</h2>
  <div style="width:62mm">{qr("q-cplp", "Conhecer", "Os Estados-membros da CPLP, no sítio oficial da comunidade.")}</div>
</div>
<p style="font-size:9.8pt;margin-top:2.4mm">A <b>Comunidade dos Países de Língua Portuguesa</b> (CPLP) foi criada em Lisboa, a 17 de julho de 1996. Hoje reúne nove países, em quatro continentes. Em cada um deles se escrevem histórias e poemas em português. Aqui tens um autor por país: um convite para leres.</p>
<div style="margin-top:3mm">{MAP}</div>
<div class="grid3" style="margin-top:3.6mm;gap:3.2mm 4.5mm">{"".join(acard(*a) for a in auth)}</div>
<p class="small muted" style="margin-top:2mm"><span class="tag line" style="color:var(--muted)">para mais tarde</span> livros escritos para adultos: guarda o nome do autor para quando fores mais crescido.</p>
<div class="grid2" style="margin-top:auto;grid-template-columns:1fr 1.2fr;gap:6mm;align-items:start">
  {act(1, "Localizar", 'Quantos países da CPLP ficam em cada continente?<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;margin-top:1.8mm;font-size:8.8pt;text-align:center"><div>África<br><span class="fill s"></span></div><div>América<br><span class="fill s"></span></div><div>Europa<br><span class="fill s"></span></div><div>Ásia<br><span class="fill s"></span></div></div>')}
  {act(2, "Escolher", 'Qual destes autores gostavas de ler primeiro? Procura um livro dele na biblioteca e escreve o título e porque o escolheste.' + lines(2))}
</div>
""", "2.4 · Nove países")
