import parts
from parts import *
parts.UNIT.update(n=6, total=10)

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea)"
U = lambda h=6.5: f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'
UL = lambda k, h=7.4: "".join(U(h) for _ in range(k))

# ---------------------------------------------------------------- shared furniture (scoped by the u6- prefix)
STY = '''<style>
.u6-it{display:grid;grid-template-columns:8mm 1fr 11mm;column-gap:2.6mm;margin-top:3.4mm}
.u6-it>.n{font-family:Fraunces;font-weight:700;font-size:14pt;line-height:1;color:var(--coral);text-align:right}
.u6-it.blue>.n{color:var(--ink)} .u6-it.sea>.n{color:var(--sea)}
.u6-it>.q{font-size:9.6pt;line-height:1.42}
.u6-it>.q .verb{font-family:Grotesk;font-size:6.2pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:.4mm}
.u6-pt{align-self:start;border:1pt solid var(--rule);border-radius:1.4mm;text-align:center;padding:.6mm 0 .5mm;background:#fff}
.u6-pt b{display:block;font-family:Fraunces;font-weight:700;font-size:11pt;line-height:1;color:var(--ink)}
.u6-pt span{display:block;font-family:Grotesk;font-size:5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:.3mm}
.u6-mc{display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 5mm;margin-top:1.2mm}
.u6-mc div{display:grid;grid-template-columns:4.4mm 4mm 1fr;gap:1.2mm;align-items:start;font-size:9.2pt;line-height:1.32}
.u6-mc b{font-family:Grotesk;font-size:7.6pt;color:var(--ink);padding-top:.35mm}
.u6-grp{display:flex;align-items:center;gap:3mm;margin-top:3.4mm;padding:1.6mm 3mm;border-radius:1.6mm;color:#fff;font-family:Grotesk;font-weight:700;font-size:7.4pt;letter-spacing:.16em;text-transform:uppercase}
.u6-grp i{font-style:normal;margin-left:auto;font-family:Fraunces;letter-spacing:0;text-transform:none;font-size:10pt}
.u6-sub{display:grid;grid-template-columns:7mm 1fr;gap:1.6mm;margin-top:1.4mm}
.u6-sub>b{color:var(--coral);font-size:9pt}
.u6-tbl{width:100%;border-collapse:collapse;font-size:9pt}
.u6-tbl th{font-family:Grotesk;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:var(--ink);padding:1.4mm 2mm;text-align:left}
.u6-tbl td{border-bottom:.6pt solid var(--rule);padding:1.6mm 2mm;vertical-align:top}
.u6-tbl td+td,.u6-tbl th+th{border-left:.6pt solid var(--rule)}
.u6-code{display:inline-block;font-family:Grotesk;font-weight:700;font-size:6.2pt;color:#fff;border-radius:.8mm;padding:.1mm 1mm;vertical-align:1.4mm;margin-left:.4mm;line-height:1.3}
</style>'''

BOX = '<svg viewBox="0 0 10 10" style="width:3.8mm;height:3.8mm;display:block"><rect x=".7" y=".7" width="8.6" height="8.6" rx="1.7" fill="#fff" stroke="#17315A" stroke-width="1.1"/></svg>'
def star(c="#E4502F", s=5):
    return (f'<svg viewBox="0 0 20 20" style="width:{s}mm;height:{s}mm;display:inline-block;vertical-align:-1.2mm">'
            f'<path d="M10 1.4l2.6 5.5 6 .8-4.4 4.2 1.1 6-5.3-2.9-5.3 2.9 1.1-6L1.4 7.7l6-.8z" fill="{c}"/></svg>')
TICK = ('<svg viewBox="0 0 12 12" style="width:3.4mm;height:3.4mm;display:inline-block;vertical-align:-.6mm">'
        '<path d="M2 6.4l2.6 2.6L10 3.2" fill="none" stroke="#2E8C7B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def it(n, verb, html, p, color=""):
    return (f'<div class="u6-it {color}"><div class="n">{n}</div><div class="q"><span class="verb">{verb}</span>{html}</div>'
            f'<div class="u6-pt"><b>{p}</b><span>pontos</span></div></div>')

def mc(opts):
    return '<div class="u6-mc">' + "".join(f'<div><b>{"ABCD"[i]}</b>{BOX}<span>{o}</span></div>' for i, o in enumerate(opts)) + '</div>'

def sub(k, html):
    return f'<div class="u6-sub"><b>{k}</b><div>{html}</div></div>'

def grp(label, pts, color):
    return f'<div class="u6-grp" style="background:{color}">{label}<i>{pts} pontos</i></div>'

def testhead(kicker, title, color, extra=""):
    f = lambda lab, w: f'<span style="display:flex;align-items:flex-end;gap:1.6mm;font-size:8.2pt;color:var(--muted)">{lab}<span style="display:block;width:{w}mm;border-bottom:.6pt solid #9AA4B3;height:4.6mm"></span></span>'
    return f'''<div style="display:grid;grid-template-columns:1fr 30mm;gap:5mm;align-items:end">
  <div><div class="kicker" style="color:{color}">{kicker}</div><h2 style="margin-top:1.4mm;font-size:22pt">{title}</h2></div>
  <div style="border:1.4pt solid {color};border-radius:2mm;padding:1.6mm 2mm;text-align:center"><div style="font-family:Grotesk;font-size:5.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Classificação</div><div class="display" style="font-size:15pt;line-height:1.1;color:var(--ink)"><span style="display:inline-block;width:12mm;border-bottom:.8pt solid #9AA4B3;height:5.4mm;vertical-align:-1mm"></span> / 100</div></div>
</div>
<div style="display:flex;gap:4mm;margin-top:2.6mm;padding-bottom:2mm;border-bottom:.6pt solid var(--rule)">{f("Nome", 74)}{f("N.º", 9)}{f("Turma", 10)}{f("Data", 22)}{extra}</div>'''

# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, STY + '''
<div class="abs" style="left:0;right:0;top:0;height:150mm"><img class="cover" src="img/apresentacao.jpg" style="object-position:50% 40%"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:160mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">6</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 6 · Avaliação</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">Mostrar o que <em>sei</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:5mm;font-size:12.4pt">Um teste não mede quem és: mostra o caminho que já fizeste. Nesta unidade vais preparar-te com calma, resolver dois testes, apresentar um trabalho à turma e, no fim, usar os teus erros para aprender mais.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:6mm">
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">p. 2</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10pt;margin-top:.8mm;line-height:1.2">Preparar-me</div><div class="small muted">estratégias e pontos</div></div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:2mm"><div class="kicker">p. 3–6</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10pt;margin-top:.8mm;line-height:1.2">Testes A e B</div><div class="small muted">leitura, gramática, escrita</div></div>
    <div style="border-top:1.2mm solid var(--sea);padding-top:2mm"><div class="kicker sea">p. 7–8</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10pt;margin-top:.8mm;line-height:1.2">Exposição oral</div><div class="small muted">3 a 4 minutos, com cartões</div></div>
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">p. 9–10</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10pt;margin-top:.8mm;line-height:1.2">Corrigir e refletir</div><div class="small muted">erros, resultados, metas</div></div>
  </div>
  <div class="panel" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4mm 5mm">
    <div class="display" style="font-size:24pt;color:var(--ink);line-height:1">2 min</div>
    <div style="font-size:9.8pt"><b class="blue">Respirar antes de começar.</b> Pensa num texto deste ano que gostaste de ler e numa coisa que hoje fazes melhor do que em setembro. Diz ambas ao colega do lado. É isso que vais mostrar nesta unidade.</div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 HOW TO PREPARE + STRATEGIES + POINTS
verbs = [("Identifica / Indica", "diz o nome ou a informação, sem explicar."),
         ("Transcreve", "copia do texto, palavra por palavra, entre aspas."),
         ("Explica", "diz como ou porquê, por palavras tuas."),
         ("Justifica", "dá a razão e apoia-te numa passagem do texto."),
         ("Classifica", "usa o nome gramatical certo (ex.: CD, frase complexa)."),
         ("Ordena", "numera os acontecimentos pela sequência.")]
vh = "".join(f'<tr><td style="width:34mm;font-weight:700;color:var(--ink)">{a}</td><td>{b}</td></tr>' for a, b in verbs)
strat = [("Lê o teste todo", "antes de escreveres. Vê quantas perguntas há e quanto vale cada uma."),
         ("Sublinha o verbo", "da instrução: é ele que diz o que tens de fazer."),
         ("Começa pelo que sabes", "e volta depois às perguntas difíceis. Não deixes nada em branco."),
         ("Olha para os pontos", "uma pergunta de 8 pontos pede mais do que uma de 2."),
         ("Guarda 5 minutos", "no fim para rever acentos, pontuação e concordâncias.")]
sh = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2mm;margin-top:2.2mm"><div class="display" style="font-size:15pt;color:var(--coral);line-height:1">{i}</div><div style="font-size:9.2pt;line-height:1.38"><b class="blue">{a}</b> {b}</div></div>' for i, (a, b) in enumerate(strat, 1))
week = ["Relê os resumos e as caixas de regras das Unidades 1, 2 e 4.", "Refaz dois exercícios de gramática de cada tema.", "Escreve um texto curto e pede a alguém que o leia.", "Dorme bem na véspera e prepara o material."]
wh = "".join(f'<div style="display:grid;grid-template-columns:5.4mm 1fr;gap:1.4mm;margin-top:1.8mm;font-size:9pt;line-height:1.35"><span class="chk"></span><span>{w}</span></div>' for w in week)
# time bar for a 60-minute test (illustrative)
seg = [(5, "Ler o teste", "#DCE5F0", INK), (10, "Ler o texto", "#D5EEE7", SEA), (20, "Leitura", "#17315A", "#fff"), (15, "Gramática", "#2E8C7B", "#fff"), (5, "Rever", "#FBE1D8", COR)]
x, bars = 0, ""
for m, lab, bg, fg in seg:
    w = m / 55 * 100
    bars += f'<div style="width:{w:.2f}%;background:{bg};color:{fg};padding:1.4mm 1.4mm;font-size:7.4pt;line-height:1.15;border-right:.8mm solid var(--paper)"><b style="font-family:Fraunces;font-size:10pt">{m}</b> min<br>{lab}</div>'
lv = [("8", "Resposta completa: a ideia certa, explicada, com uma passagem do texto, bem escrita."),
      ("5", "A ideia está certa, mas falta explicar melhor ou falta o exemplo do texto."),
      ("2", "A resposta toca no assunto, mas fica vaga ou confusa."),
      ("0", "A resposta está errada ou em branco.")]
lh = "".join(f'<div style="display:grid;grid-template-columns:9mm 1fr;gap:2mm;margin-top:1.6mm;align-items:start"><span class="display" style="font-size:13pt;color:var(--ink);line-height:1;text-align:right">{a}</span><span style="font-size:8.8pt;line-height:1.35">{b}</span></div>' for a, b in lv)
scale = "".join('<tr><td style="height:6.6mm"></td><td></td></tr>' for _ in range(5))
P[2] = page(2, STY + f'''
<div class="kicker">Antes do teste</div>
<h2 style="margin-top:2mm">Como me preparo — <em>com calma</em></h2>
<p class="lead" style="margin-top:2.4mm;font-size:10.8pt">Estar preparado não é saber tudo de cor: é saber o que te vão pedir, como vais organizar o tempo e o que fazer quando uma pergunta parece difícil.</p>
<div class="grid2" style="margin-top:4mm;gap:7mm;grid-template-columns:1fr 1.08fr">
  <div>
    <div class="panel sea" style="padding:3.4mm 4mm"><div class="kicker sea">Na semana antes</div>{wh}</div>
    <h3 style="margin-top:4mm">Durante o teste: cinco estratégias</h3>
    {sh}
  </div>
  <div>
    <h3>Os verbos das perguntas</h3>
    <p class="small muted" style="margin-top:.8mm">Cada verbo pede uma coisa diferente. Aprende-os como ferramentas.</p>
    <table class="u6-tbl" style="margin-top:1.8mm"><tr><th>Se a pergunta diz…</th><th>…então tens de</th></tr>{vh}</table>
    <div style="margin-top:3.6mm"><div class="kicker blue">Gerir o tempo · exemplo num teste de 55–60 minutos</div>
    <div style="display:flex;margin-top:1.8mm;border-radius:1.6mm;overflow:hidden">{bars}</div></div>
  </div>
</div>
<div class="grid2" style="margin-top:5mm;gap:7mm;grid-template-columns:1.35fr 1fr;align-items:start">
  <div class="panel blue" style="padding:3.6mm 4.2mm">
    <div class="kicker blue">Como funcionam os pontos</div>
    <p style="font-size:9pt;line-height:1.4;margin-top:1.4mm">Cada teste vale <b>100 pontos</b>. Ao lado de cada pergunta está a sua <b>cotação</b>. Uma resposta pode ter os pontos todos ou só uma parte. Exemplo: <i>«Explica o sentido da última frase do texto.»</i> (8 pontos)</p>
    {lh}
  </div>
  <div>
    <div class="kicker">A escala da minha escola</div>
    <p class="small muted" style="margin-top:.8mm">Copia-a do quadro: cada menção e os pontos que lhe correspondem.</p>
    <table class="u6-tbl" style="margin-top:1.6mm"><tr><th>Menção</th><th>Pontos</th></tr>{scale}</table>
  </div>
</div>
{act(1, "Aplicar", 'Numa das últimas fichas que fizeste, escolhe uma pergunta em que perdeste pontos. Qual era o <b>verbo</b> da instrução? O que faltou na tua resposta?' + UL(2), "blue")}
''', station="Preparar")

# ---------------------------------------------------------------- 3 TEST A: THE TEXT + ITEMS 1-2
def para(n, html):
    return (f'<p style="position:relative"><span style="position:absolute;left:-7.5mm;top:.2mm;width:5mm;height:5mm;border-radius:50%;'
            f'background:var(--ink);color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>')
TEXT = "".join([
    para(1, 'Naquela manhã de outubro, a vila acordou dentro de uma nuvem. O nevoeiro tinha chegado durante a noite, sem fazer barulho, e agora cobria tudo: os telhados vermelhos, as redes estendidas no cais, os barcos pintados de azul e amarelo. Até o farol, alto e branco no cimo da falésia, tinha desaparecido. Só se ouvia o mar, lá em baixo, a bater nas rochas como um tambor cansado.'),
    para(2, 'Leonor desceu a rua de pedra até à casa do avô, que fora faroleiro durante trinta anos. Encontrou-o à janela, com os olhos pequenos e atentos presos no branco. O barco do Ti Zé, que saíra de madrugada, ainda não tinha voltado.<br>— Com este nevoeiro, ele não vê a entrada do porto — murmurou o avô.'),
    para(3, 'Leonor lembrou-se do velho sino que o avô guardava no barracão. Era de bronze, pesado e frio, com manchas verdes nas bordas e uma corda grossa, gasta por muitas mãos. Os dois levaram-no até ao fim do molhe, onde as ondas rebentavam em espuma. O avô entregou a corda à neta.<br>— Toca devagar, como um coração — explicou.'),
    para(4, 'Leonor tocou. O som espalhou-se pela água, grave e redondo, e o nevoeiro pareceu engoli-lo. Os minutos passavam, compridos como horas. As mãos dela já estavam dormentes quando, ao longe, uma buzina respondeu. Pouco depois, a proa azul do barco surgiu do nada, como um desenho que alguém fosse pintando devagar.'),
    para(5, 'Nessa noite, o Ti Zé bateu à porta e ofereceu um saco de sardinhas à Leonor.<br>— Foste o meu farol — disse-lhe, a sorrir.<br>Ela nunca tinha pensado que um som também pudesse iluminar.'),
])
gloss = [("faroleiro", "pessoa que trabalha num farol e cuida da sua luz."),
         ("barracão", "construção simples, de arrumos."),
         ("molhe", "paredão construído no mar, à entrada de um porto, que o protege das ondas."),
         ("dormente", "sem sensibilidade, por causa do frio ou de estar parado."),
         ("proa", "parte da frente de um barco.")]
gl = "".join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in gloss)
order = ["Uma buzina responde ao longe.", "A Leonor e o avô levam o sino até ao molhe.", "O nevoeiro cobre a vila.", "O Ti Zé oferece sardinhas à Leonor.", "O avô repara que o barco não voltou."]
oh = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2mm 5mm;margin-top:1mm">' + "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:1.6mm;align-items:center;font-size:9.2pt"><span style="display:block;width:6mm;height:5mm;border:1pt solid var(--ink);border-radius:1mm;background:#fff"></span><span>{t}</span></div>' for t in order) + '</div>'
P[3] = page(3, STY + f'''
{testhead("Teste A · Leitura e Gramática", "O sino do nevoeiro", COR, '<span style="margin-left:auto;font-size:8.2pt;color:var(--muted)">Duração: <b class="blue">60 min</b></span>')}
<div style="display:grid;grid-template-columns:1fr 39mm;gap:5mm;margin-top:3mm">
  <div>
    {grp("Grupo I · Leitura", 50, INK)}
    <div class="reading" style="margin-top:2mm;padding-left:7.5mm;font-size:10.1pt;line-height:1.5">{TEXT}</div>
    <p class="src" style="margin-top:2mm;padding-left:7.5mm">Texto escrito para este manual.</p>
  </div>
  <div style="padding-top:7mm">
    <div class="kicker blue">Vocabulário</div>
    <dl class="gloss" style="margin-top:2mm">{gl}</dl>
    <div class="panel" style="margin-top:3mm;padding:3mm 3.4mm">
      <div class="kicker">Cotações</div>
      <table style="width:100%;font-size:8.2pt;margin-top:1.4mm;border-collapse:collapse;line-height:1.5">
        <tr><td>Grupo I · Leitura</td><td style="text-align:right"><b>50</b></td></tr>
        <tr><td>Grupo II · Gramática</td><td style="text-align:right"><b>50</b></td></tr>
        <tr><td style="border-top:.6pt solid var(--rule)"><b>Total</b></td><td style="text-align:right;border-top:.6pt solid var(--rule)"><b class="coral">100</b></td></tr>
      </table>
    </div>
  </div>
</div>
{it(1, "Escolha múltipla · assinala a opção correta", sub("1.1", 'A ação passa-se' + mc(["numa cidade do interior.", "numa vila piscatória junto ao mar.", "a bordo do barco do Ti Zé.", "no interior do farol."])) + sub("1.2", 'O avô estava preocupado porque' + mc(["o farol se tinha avariado.", "a Leonor tinha saído sozinha.", "o barco do Ti Zé ainda não voltara.", "o sino se tinha partido."])) + sub("1.3", 'Em «a bater nas rochas como um tambor cansado» (§ 1), há' + mc(["uma metáfora.", "uma comparação.", "uma enumeração.", "uma interjeição."])), 12)}
{it(2, "Ordenar · numera os acontecimentos de 1 a 5", oh, 5)}
''', station="Teste A")

# ---------------------------------------------------------------- 4 TEST A: ITEMS 2-10
vf = [("O nevoeiro chegou de manhã, com muito barulho.",), ("O avô da Leonor tinha sido faroleiro.",), ("A Leonor tocou o sino depressa e com força.",), ("O Ti Zé agradeceu com um presente.",)]
vfh = "".join(f'<div style="display:grid;grid-template-columns:5mm 1fr 14mm;gap:1.6mm;align-items:end;margin-top:1.2mm;font-size:9.2pt"><b class="coral">{"abcd"[i]})</b><span>{t}</span><span style="display:flex;gap:1.6mm;font-family:Grotesk;font-size:7.4pt;color:var(--ink);align-items:center">V{BOX}F{BOX}</span></div>' for i, (t,) in enumerate(vf))
tb = "".join(f'<tr><td style="font-weight:700;color:var(--ink)">{v}</td><td style="height:6.4mm"></td><td></td></tr>' for v in ("ouvir", "fazer", "pôr"))
ss = [("Leonor tocou.",), ("As mãos dela já estavam dormentes quando, ao longe, uma buzina respondeu.",), ("O som espalhou-se pela água.",), ("Os dois levaram-no até ao fim do molhe, onde as ondas rebentavam em espuma.",)]
ssh = "".join(f'<div style="display:grid;grid-template-columns:5mm 1fr 14mm;gap:1.6mm;align-items:start;margin-top:1.2mm;font-size:9.1pt;line-height:1.35"><b class="coral">{"abcd"[i]})</b><i style="font-family:FrauncesText">{t}</i><span style="display:flex;gap:1.6mm;font-family:Grotesk;font-size:7.4pt;color:var(--ink);align-items:center">S{BOX}C{BOX}</span></div>' for i, (t,) in enumerate(ss))
def rw(t):
    return f'<div style="display:grid;grid-template-columns:56mm 1fr;gap:2mm;align-items:end;margin-top:1.4mm;font-size:9.1pt"><i style="font-family:FrauncesText">{t}</i>{U(5.4)}</div>'
P[4] = page(4, STY + f'''
<div class="grid2" style="gap:6mm;align-items:start">
  <div>
    {it(3, "Verdadeiro ou falso · corrige as falsas", vfh + UL(2, 6.6), 8)}
    {it(4, "Descrição", 'Transcreve do § 3 três adjetivos que caracterizam o sino. A que sentidos apelam?' + UL(2, 6.6), 6)}
  </div>
  <div>
    {it(5, "Explicar", 'Explica o sentido da última frase: «um som também pudesse iluminar».' + UL(3, 6.6), 8)}
    {it(6, "Justificar", 'O narrador participa na história? Justifica com uma palavra do texto.' + UL(2, 6.6), 5)}
    {it(7, "Estrutura", 'Indica os parágrafos da introdução, do desenvolvimento e da conclusão.' + UL(2, 6.6), 6)}
  </div>
</div>
{grp("Grupo II · Gramática", 50, SEA)}
<div class="grid2" style="gap:6mm;align-items:start">
  <div>
    {it(8, "Pretérito mais-que-perfeito", sub("8.1", 'Transcreve do texto uma forma <b>simples</b> e uma <b>composta</b>.' + U(5.6)) + sub("8.2", 'Completa (3.ª pessoa do singular).<table class="u6-tbl" style="margin-top:1mm"><tr><th>Verbo</th><th>Simples</th><th>Composto</th></tr>' + tb + '</table>') + sub("8.3", 'Completa com o composto: Quando a Leonor chegou, as ondas já <span class="fill"></span> (molhar) o molhe.'), 14, "sea")}
    {it(9, "Complemento direto e indireto", sub("9.1", '<i style="font-family:FrauncesText">O avô entregou a corda à neta.</i> CD: <span class="fill"></span> CI: <span class="fill"></span>') + sub("9.2", 'Substitui a parte sublinhada por um pronome.' + rw('Leonor tocou <u>o sino</u>.') + rw('Ofereceu sardinhas <u>à Leonor</u>.') + rw('Vou avisar <u>os pescadores</u>.')) + sub("9.3", 'Em «O Ti Zé deu-<b>lho</b>», <i>lho</i> substitui' + mc(["só o CD.", "só o CI.", "o CI e o CD.", "o sujeito."])), 18, "sea")}
  </div>
  <div>
    {it(10, "Frase simples e complexa", sub("10.1", 'Classifica: <b>S</b> (simples) ou <b>C</b> (complexa).' + ssh) + sub("10.2", 'Justifica a classificação da frase b).' + UL(2, 6.2)) + sub("10.3", 'Junta numa só frase complexa: <i style="font-family:FrauncesText">O barco apareceu. Os pescadores aplaudiram.</i>' + UL(2, 6.2)), 18, "sea")}
    <div class="rule-card c" style="margin-top:4mm;font-size:8.6pt;line-height:1.4"><b class="sea">Antes de entregares:</b> respondeste a todas? Releste os acentos e a pontuação? Verificaste os pontos de cada grupo?</div>
  </div>
</div>
''', station="Teste A")

# ---------------------------------------------------------------- 5 TEST B: OPINION
def plan_box(label, hint, color, h=15):
    return (f'<div style="border:1pt solid {color};border-radius:1.8mm;padding:1.8mm 2.4mm;min-height:{h}mm;background:#fff">'
            f'<div style="font-family:Grotesk;font-weight:700;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:{color}">{label}</div>'
            f'<div class="small muted" style="font-size:7.6pt;line-height:1.3">{hint}</div></div>')
conn = ["Na minha opinião", "Em primeiro lugar", "Além disso", "pois", "porque", "Por exemplo", "Há quem diga que…", "porém", "Por isso", "Em conclusão"]
ch = "".join(f'<span class="chip">{c}</span>' for c in conn)
def crit(rows, color):
    r = "".join(f'<tr><td style="font-weight:700;color:var(--ink);width:38mm">{a}</td><td>{b}</td><td style="text-align:center;width:13mm"><b>{p}</b></td><td style="width:13mm"></td></tr>' for a, b, p in rows)
    return f'<table class="u6-tbl" style="font-size:8.4pt"><tr><th style="background:{color}">Critério</th><th style="background:{color}">O que conta</th><th style="background:{color};text-align:center">Máx.</th><th style="background:{color};text-align:center">Tive</th></tr>{r}</table>'
C1 = [("Tese", "a tua opinião está clara logo no início.", 8), ("Argumentos", "dois argumentos diferentes, cada um com um exemplo.", 16),
      ("Conclusão", "retoma a tese e fecha o texto.", 6), ("Conectores e parágrafos", "um parágrafo por ideia, ligados por conectores.", 10),
      ("Correção da língua", "ortografia, acentos, pontuação, concordâncias.", 10)]
P[5] = page(5, STY + f'''
{testhead("Teste B · Escrita · Tarefa 1", "Defender uma opinião", COR, '<span style="margin-left:auto;font-size:8.2pt;color:var(--muted)">Duração: <b class="blue">2 × 45 min</b></span>')}
<div style="display:grid;grid-template-columns:1fr auto;gap:5mm;margin-top:3.4mm;align-items:start">
  <p class="lead" style="font-size:11pt">A escola vai decidir se cada turma deve <b>«adotar» uma praia, um rio ou um jardim</b> perto da escola, e cuidar dele durante todo o ano. Escreve um <b>texto de opinião</b>, entre <b>120 e 180 palavras</b>, para o jornal da escola.</p>
  <div class="u6-pt" style="width:15mm"><b>50</b><span>pontos</span></div>
</div>
<div class="kicker" style="margin-top:3mm">Planifica · 5 minutos <span class="muted" style="letter-spacing:.06em;text-transform:none;font-family:Body;font-weight:400">— lembra-te do esqueleto da Unidade 1</span></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2.6mm;margin-top:1.8mm">
  {plan_box("Tese", "concordo ou discordo?", COR, 22)}{plan_box("Argumento 1 + exemplo", "uma razão e um facto", INK, 22)}{plan_box("Argumento 2 + exemplo", "outra razão, outro exemplo", INK, 22)}{plan_box("Conclusão", "retomo a tese", COR, 22)}
</div>
<div class="opts" style="margin-top:2.4mm">{ch}</div>
<div style="margin-top:2.6mm">{UL(13, 7.6)}</div>
<div style="margin-top:auto;padding-top:3mm">{crit(C1, COR)}</div>
''', station="Teste B")

# ---------------------------------------------------------------- 6 TEST B: NARRATIVE WITH DESCRIPTION
senses = [("Vejo", INK), ("Ouço", SEA), ("Cheiro", COR), ("Toco", INK), ("Sinto", SEA)]
sh6 = "".join(f'<div style="border-top:1mm solid {c};padding-top:1.4mm"><div style="font-family:Grotesk;font-weight:700;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;color:{c}">{s}</div>{U(5.2)}{U(5.2)}</div>' for s, c in senses)
C2 = [("Estrutura", "situação inicial, problema, desenvolvimento, desfecho.", 12), ("Descrição", "um lugar ou uma personagem descritos com vários sentidos.", 12),
      ("Tempos verbais", "passado coerente; pelo menos dois mais-que-perfeitos.", 8), ("Diálogo", "uma fala, com travessão e verbo introdutor.", 6),
      ("Correção da língua", "ortografia, acentos, pontuação, concordâncias.", 12)]
P[6] = page(6, STY + f'''
<div style="display:grid;grid-template-columns:1fr auto;gap:5mm;align-items:start">
  <div><div class="kicker">Teste B · Escrita · Tarefa 2</div><h2 style="margin-top:1.4mm;font-size:22pt">Contar e descrever</h2></div>
  <div class="u6-pt" style="width:15mm"><b>50</b><span>pontos</span></div>
</div>
<p class="lead" style="margin-top:2.4mm;font-size:11pt">Escreve uma <b>narrativa com descrição</b>, entre <b>150 e 200 palavras</b>, que comece assim:</p>
<p style="font-family:FrauncesText;font-style:italic;font-size:12pt;color:var(--ink);margin-top:1.8mm;border-left:1.4mm solid var(--coral);padding-left:3.4mm">«Quando abri a porta do farol, percebi logo que alguém lá tinha estado antes de mim.»</p>
<div style="display:grid;grid-template-columns:1.15fr 1fr;gap:6mm;margin-top:3.4mm;align-items:start">
  <div>
    <div class="kicker">Planifica a história · Unidade 2</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:2.4mm;margin-top:1.8mm">
      {plan_box("Quem? Onde? Quando?", "personagens, lugar, tempo", INK, 17)}{plan_box("O problema", "o que tinha acontecido?", COR, 17)}
      {plan_box("O que fazem", "dois ou três momentos", INK, 17)}{plan_box("O desfecho", "como se resolve?", COR, 17)}
    </div>
  </div>
  <div>
    <div class="kicker sea">Descreve com os cinco sentidos</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 3mm;margin-top:1.8mm">{sh6}</div>
  </div>
</div>
<div style="margin-top:2.6mm">{UL(14, 7.6)}</div>
<div style="margin-top:auto;padding-top:3mm">{crit(C2, SEA)}</div>
''', station="Teste B")

# ---------------------------------------------------------------- 7 ORAL PRESENTATION
steps = [("Escolher", "um tema e uma pergunta: o que quero explicar?"), ("Pesquisar", "em duas fontes de confiança; anotar de onde vem cada dado."),
         ("Organizar", "introdução, dois ou três pontos, conclusão (Unidade 1)."), ("Escrever cartões", "palavras-chave, não frases inteiras."),
         ("Ensaiar", "em voz alta, com cronómetro, três vezes."), ("Apresentar", "olhar para a turma, falar devagar, responder a perguntas.")]
st = "".join(f'<div style="border-top:1.2mm solid {[INK, SEA, COR][i % 3]};padding-top:1.6mm"><div class="display" style="font-size:14pt;line-height:1;color:{[INK, SEA, COR][i % 3]}">{i + 1}</div><div style="font-weight:700;color:var(--ink);font-size:8.8pt;margin-top:.8mm">{a}</div><div style="font-size:7.8pt;line-height:1.3;color:var(--muted)">{b}</div></div>' for i, (a, b) in enumerate(steps))
def card7(no, t, hint, c):
    return (f'<div style="background:#fff;border:1pt solid var(--rule);border-top:2.4mm solid {c};border-radius:1.6mm;padding:2mm 3mm 1mm;box-shadow:0 .6mm 0 var(--sand-2)">'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-family:Grotesk;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:{c}">Cartão {no} · {t}</b><span class="small muted" style="font-size:7.2pt">{hint}</span></div>'
            + "".join(f'<div style="display:grid;grid-template-columns:3mm 1fr;align-items:end"><span style="width:1.4mm;height:1.4mm;border-radius:50%;background:{c};margin-bottom:1.2mm"></span>{U(6)}</div>' for _ in range(4)) + '</div>')
rub = [("Conteúdo", "informação certa, rica, com fontes", "certa, mas pouca", "com erros ou vaga", "sem informação"),
       ("Estrutura", "introdução, pontos e conclusão claros", "falta uma parte", "ideias soltas", "sem ordem"),
       ("Voz e postura", "fala alto, devagar, olha a turma", "às vezes lê os cartões", "lê quase tudo", "não se ouve"),
       ("Língua", "vocabulário exato, sem «tipo» nem «pronto»", "alguns tiques", "muitas repetições", "frases incompletas"),
       ("Tempo", "3 a 4 minutos", "entre 2,5 e 3 ou entre 4 e 4,5 min", "menos de 2,5 ou mais de 4,5 min", "menos de 1 minuto")]
rh = "".join(f'<tr><td style="font-weight:700;color:var(--ink);width:24mm">{r[0]}</td>' + "".join(f'<td style="font-size:7.8pt;line-height:1.3">{x}</td>' for x in r[1:]) + '<td style="width:10mm"></td></tr>' for r in rub)
P[7] = page(7, STY + f'''
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div><div class="kicker sea">Trabalho · Oralidade</div><h2 style="margin-top:2mm">Uma exposição oral de <em>3 a 4 minutos</em></h2></div>
  <div>{MICRO.replace('class="ico"', 'class="ico" style="width:14mm;height:14mm"')}</div>
</div>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Vais apresentar à turma um tema que te interesse — por exemplo, um animal do mar, um farol português, um livro que leste este ano ou uma profissão ligada ao mar. Uma boa exposição é um <b>texto expositivo dito em voz alta</b>: rigoroso, organizado e claro.</p>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:3mm;margin-top:3.4mm">{st}</div>
<div style="display:flex;flex-wrap:wrap;gap:1.6mm;align-items:center;margin-top:3.4mm"><span class="kicker sea" style="margin-right:1mm">Frases que ajudam</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Hoje vou falar-vos de…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Escolhi este tema porque…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Em primeiro lugar…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Outro aspeto importante é…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Para concluir…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Obrigado. Alguém tem perguntas?»</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm;align-items:start">
  <div>
    <div class="kicker">Os meus cartões</div>
    <div style="display:grid;gap:2.6mm;margin-top:1.8mm">{card7(1, "Introdução", "tema + pergunta", COR)}{card7(2, "Desenvolvimento", "2 ou 3 pontos", INK)}{card7(3, "Conclusão", "resumo + frase final", SEA)}</div>
  </div>
  <div>
    <div class="kicker blue">Planeio</div>
    <div style="font-size:9pt;margin-top:1.6mm"><b class="blue">O meu tema:</b>{U(6)}</div>
    <div style="font-size:9pt;margin-top:2mm"><b class="blue">A pergunta a que respondo:</b>{U(6)}</div>
    <div style="font-size:9pt;margin-top:2mm"><b class="blue">Fonte 1:</b>{U(6)}<b class="blue" style="display:block;margin-top:2mm">Fonte 2:</b>{U(6)}</div>
    <div style="font-size:9pt;margin-top:2mm"><b class="blue">Imagem ou objeto que vou mostrar:</b>{U(6)}</div>
    <div class="panel sea" style="margin-top:3mm;padding:2.6mm 3.2mm;font-size:8.4pt;line-height:1.4"><b class="sea">Ensaios cronometrados:</b> 1.º <span class="fill s"></span> min · 2.º <span class="fill s"></span> min · 3.º <span class="fill s"></span> min</div>
  </div>
</div>
<div style="margin-top:auto">
  <div class="kicker">Grelha de avaliação · cada critério vale de 1 a 4 pontos · total /20</div>
  <table class="u6-tbl" style="margin-top:1.6mm"><tr><th>Critério</th><th style="background:var(--sea)">4 · Muito bem</th><th style="background:var(--sea)">3 · Bem</th><th style="background:var(--coral)">2 · Quase</th><th style="background:var(--coral)">1 · Ainda não</th><th style="text-align:center">Pts</th></tr>{rh}</table>
</div>
''', station="Trabalho")

# ---------------------------------------------------------------- 8 FEEDBACK SHEET (peer + teacher, two presentations)
fcrit = ["A introdução apresentou o tema", "As ideias seguiram uma ordem", "Falou alto e devagar", "Olhou para a turma", "Cumpriu o tempo"]
def fb(k):
    rows = "".join(f'<div style="display:grid;grid-template-columns:1fr 9mm 9mm 9mm;gap:1mm;align-items:center;padding:1.2mm 0;border-bottom:.6pt solid var(--rule);font-size:8.6pt"><span>{c}</span><span style="justify-self:center">{BOX}</span><span style="justify-self:center">{BOX}</span><span style="justify-self:center">{BOX}</span></div>' for c in fcrit)
    return f'''<div class="panel" style="background:#fff;border:1pt solid var(--rule);padding:3.4mm 4mm">
  <div style="display:flex;align-items:baseline;gap:3mm"><span class="display" style="font-size:20pt;line-height:1;color:var(--coral)">{k}</span><div class="kicker blue">Apresentação {k}</div></div>
  <div style="font-size:8.6pt;margin-top:1.6mm"><b class="blue">Orador:</b>{U(5.6)}</div>
  <div style="font-size:8.6pt;margin-top:1.2mm"><b class="blue">Tema:</b>{U(5.6)}</div>
  <div class="kicker" style="margin-top:3mm">Colega · observa e assinala</div>
  <div style="display:grid;grid-template-columns:1fr 9mm 9mm 9mm;gap:1mm;margin-top:1.4mm;font-family:Grotesk;font-size:6pt;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:center"><span></span><span>Sim</span><span>Quase</span><span>Ainda não</span></div>
  {rows}
  <div style="margin-top:2.4mm;font-size:8.6pt"><b class="coral">{star()}{star()} Duas estrelas</b> — o que correu muito bem</div>{UL(2, 6.2)}
  <div style="margin-top:2mm;font-size:8.6pt"><b class="blue">{star("#17315A")} Um desejo</b> — uma sugestão para melhorar</div>{UL(1, 6.2)}
  <div style="margin-top:2mm;font-size:8.6pt"><b class="sea">A pergunta que eu faria ao orador:</b></div>{UL(1, 6.2)}
  <div style="margin-top:3mm;background:var(--ink-soft);border-radius:1.6mm;padding:2.4mm 3mm">
    <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="kicker blue">Professor</span><span style="font-size:8.6pt">Grelha da p. 7: <b class="blue">____ / 20</b></span></div>
    {UL(4, 6.2)}
  </div>
</div>'''
P[8] = page(8, STY + f'''
<div class="kicker sea">Trabalho · Dar e receber feedback</div>
<h2 style="margin-top:2mm">Duas estrelas <em>e um desejo</em></h2>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Enquanto os colegas apresentam, és um ouvinte atento. O teu feedback é útil quando é <b>concreto</b> («olhaste para nós no fim») e <b>gentil</b>. Critica a apresentação, nunca a pessoa.</p>
<div style="display:flex;flex-wrap:wrap;gap:1.6mm;align-items:center;margin-top:3mm"><span class="kicker sea" style="margin-right:1mm">Frases para dar feedback</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Gostei quando…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Percebi bem a parte sobre… porque…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Da próxima vez, podias…»</span><span class="chip" style="font-family:FrauncesText;font-weight:400;font-style:italic">«Uma ideia: experimenta…»</span></div>
<div class="grid2" style="margin-top:3.4mm;gap:6mm;align-items:start">{fb(1)}{fb(2)}</div>
<div class="panel coral" style="margin-top:auto;padding:3.6mm 4.4mm">
  <div class="kicker">Eu, orador · depois de ler o feedback que recebi</div>
  <div class="grid2" style="margin-top:1.4mm;gap:6mm;font-size:9pt">
    <div><b class="blue">O comentário que mais me ajudou:</b>{UL(2, 6.4)}</div>
    <div><b class="blue">Na próxima apresentação, vou…</b>{UL(2, 6.4)}</div>
  </div>
</div>
''', station="Trabalho")

# ---------------------------------------------------------------- 9 CORRECT TO LEARN
codes = [("O", "Ortografia", "acentos, letras trocadas", "á praia → à praia", INK),
         ("P", "Pontuação", "vírgulas, pontos, travessões", "grande mas, o → grande, mas o", COR),
         ("C", "Concordância", "sujeito e verbo, nome e adjetivo", "as ondas era → as ondas eram", SEA),
         ("V", "Vocabulário", "palavra vaga ou repetida", "uma coisa bonita → um reflexo", "#8A5A9E"),
         ("E", "Estrutura", "frases soltas, ideias fora de ordem", "juntar duas frases numa só", "#B7791F")]
ARW = '<span style="font-family:Body;color:var(--muted)">→</span>'
cc = "".join(f'''<div style="border-top:1.4mm solid {c};padding-top:1.8mm">
  <div style="display:flex;align-items:center;gap:2mm"><span style="display:inline-block;width:7mm;height:7mm;border-radius:1.4mm;background:{c};color:#fff;font-family:Fraunces;font-weight:700;font-size:13pt;line-height:7mm;text-align:center">{k}</span><b style="color:var(--ink);font-size:9pt;line-height:1.1">{n}</b></div>
  <div class="small muted" style="margin-top:1mm;font-size:7.8pt">{d}</div><div style="font-family:FrauncesText;font-size:8.4pt;margin-top:.8mm;line-height:1.3">{e.replace("→", ARW)}</div></div>''' for k, n, d, e, c in codes)
cmap = {k: c for k, _, _, _, c in codes}
m = lambda w, k: f'<span style="text-decoration:underline;text-decoration-color:{cmap[k]};text-decoration-thickness:1.2pt;text-underline-offset:1mm">{w}</span><span class="u6-code" style="background:{cmap[k]}">{k}</span>'
wrong = (f'Ontem, fomos {m("á", "O")} praia com a minha avó. As ondas {m("era", "C")} pequenas e o mar fazia {m("umas coisas", "V")} bonitas com a luz. '
         f'Eu e o meu irmão construímos um castelo enorme {m("mas,", "P")} o mar levou-o. {m("Depois comemos um gelado. Depois fomos para casa.", "E")} '
         f'A avó disse que nos {m("tinhamos", "O")} portado muito bem.')
logr = "".join('<tr><td style="height:9.4mm"></td><td style="width:13mm"></td><td></td><td></td></tr>' for _ in range(5))
P[9] = page(9, STY + f'''
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div><div class="kicker blue">Depois do teste</div><h2 style="margin-top:2mm">Corrigir para <em>aprender</em></h2></div>
  <div>{LAPIS.replace('class="ico"', 'class="ico" style="width:14mm;height:14mm"')}</div>
</div>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Um erro corrigido é uma regra que fica. Quando o professor devolver o teu texto, vais encontrar letras na margem: cada uma diz-te <b>que tipo de erro</b> procurar.</p>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3.4mm;margin-top:3.6mm">{cc}</div>
{act(1, "Corrigir", 'Este parágrafo já foi marcado pelo professor. Reescreve-o sem erros.<div class="panel" style="margin-top:2mm;font-family:FrauncesText;font-size:10.4pt;line-height:1.95;padding:3mm 4mm">' + wrong + '</div>' + UL(5, 7.4), "blue")}
{act(2, "Registar", 'O meu registo de erros. Copia os erros dos teus testes e escreve a regra por palavras tuas. O primeiro está feito.')}
<table class="u6-tbl" style="margin-top:2mm">
  <tr><th>O erro que dei</th><th style="text-align:center">Código</th><th>A regra</th><th>A forma certa</th></tr>
  <tr><td style="font-family:FrauncesText;font-size:9.2pt">fomos á praia</td><td style="text-align:center;font-weight:700;color:var(--ink)">O</td><td style="font-size:8.6pt">a + a = <b>à</b>, com acento grave</td><td style="font-family:FrauncesText;font-size:9.2pt">fomos à praia</td></tr>
  {logr}
</table>
<div class="panel sea" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:3mm 4.4mm">
  <div style="font-size:9pt"><b class="sea">Os meus erros mais frequentes</b><br><span class="small muted">faz um risco por cada erro</span></div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm">{"".join(f'<div style="display:flex;align-items:flex-end;gap:1.6mm"><b style="color:{c};font-family:Fraunces;font-size:12pt;line-height:1">{k}</b>{U(6)}</div>' for k, _, _, _, c in codes)}</div>
</div>
''', station="Corrigir")

# ---------------------------------------------------------------- 10 RESULTS + REFLECTION
tr = [("Teste A · Leitura e Gramática", "/100"), ("Teste B · Escrita", "/100"), ("Exposição oral", "/20"), ("", ""), ("", ""), ("", "")]
trh = "".join(f'<tr><td style="font-size:8.6pt;font-weight:700;color:var(--ink);height:8.4mm">{a}</td><td></td><td style="text-align:right;color:var(--muted);font-size:8pt;vertical-align:bottom">{b}</td><td></td><td></td></tr>' for a, b in tr)
# plotting grid for the year's results (0-100, eight slots)
gw, gh = 170, 44
svg = [f'<svg viewBox="0 0 {gw + 12} {gh + 10}" style="width:100%;display:block">']
for v in range(0, 101, 25):
    y = gh - v / 100 * gh + 2
    svg.append(f'<line x1="10" y1="{y:.1f}" x2="{gw + 10}" y2="{y:.1f}" stroke="{"#AEB7C4" if v % 50 == 0 else "#DDE2EA"}" stroke-width=".35"/><text x="7.5" y="{y + 1.2:.1f}" font-family="Grotesk" font-size="3.2" fill="#5B6475" text-anchor="end">{v}</text>')
for i in range(8):
    x = 10 + (i + .5) * gw / 8
    svg.append(f'<line x1="{x:.1f}" y1="2" x2="{x:.1f}" y2="{gh + 2}" stroke="#DDE2EA" stroke-width=".35"/><text x="{x:.1f}" y="{gh + 7}" font-family="Grotesk" font-size="3.2" fill="#5B6475" text-anchor="middle">{i + 1}</text>')
svg.append('</svg>')
obj = [("Leio uma narrativa e distingo narração, descrição e diálogo.", "U2"),
       ("Escrevo um texto de opinião com tese, dois argumentos e conclusão.", "U1"),
       ("Uso conectores: <i>porque, pois, mas, porém, por isso</i>.", "U1"),
       ("Escrevo uma narrativa com descrição, usando os sentidos.", "U2"),
       ("Uso o pretérito mais-que-perfeito, simples e composto.", "U2"),
       ("Identifico o CD e o CI e substituo-os por pronomes.", "U4"),
       ("Distingo frase simples de frase complexa.", "U4"),
       ("Faço uma exposição oral de 3 a 4 minutos, com cartões.", "U6")]
oh10 = "".join(f'<div style="display:grid;grid-template-columns:1fr 9mm 11mm 9mm 9mm;gap:1mm;align-items:center;padding:1.3mm 0;border-bottom:.6pt solid var(--rule);font-size:8.8pt;line-height:1.3"><span>{t}</span><span class="small muted" style="text-align:center">{u}</span><span style="justify-self:center">{BOX}</span><span style="justify-self:center">{BOX}</span><span style="justify-self:center">{BOX}</span></div>' for t, u in obj)
nx = [("Vou treinar…", INK), ("Vou pedir ajuda a…", SEA), ("Vou saber que melhorei quando…", COR)]
nxh = "".join(f'<div style="border-top:1.2mm solid {c};padding-top:1.6mm"><b style="color:{c};font-size:9pt">{a}</b>{UL(2, 6.4)}</div>' for a, c in nx)
P[10] = page(10, STY + f'''
<div class="kicker">Chegada</div>
<h2 style="margin-top:2mm">Os meus resultados, <em>o meu caminho</em></h2>
<div class="grid2" style="margin-top:3.4mm;gap:6mm;grid-template-columns:1.2fr 1fr;align-items:start">
  <div>
    <div class="kicker blue">Registo do ano</div>
    <table class="u6-tbl" style="margin-top:1.6mm"><tr><th>Teste ou trabalho</th><th style="width:15mm">Data</th><th style="width:14mm;text-align:right">Pontos</th><th>Correu bem</th><th>A melhorar</th></tr>{trh}</table>
  </div>
  <div>
    <div class="kicker blue">A minha linha do ano</div>
    <p class="small muted" style="margin-top:.8mm">Marca um ponto por cada teste (1, 2, 3…) e une-os. Nos trabalhos cotados para 20, multiplica por 5.</p>
    <div style="margin-top:1.4mm">{"".join(svg)}</div>
  </div>
</div>
<div style="margin-top:4.6mm">
  <div style="display:grid;grid-template-columns:1fr 9mm 11mm 9mm 9mm;gap:1mm;align-items:end;padding-bottom:1.2mm;border-bottom:1pt solid var(--ink)"><span class="kicker blue">Autoavaliação · já consigo…</span>{"".join(f'<span style="font-family:Grotesk;font-size:6pt;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:center">{h}</span>' for h in ("Unid.", "Sim", "Quase", "Ainda não"))}</div>
  {oh10}
</div>
<div class="grid2" style="margin-top:4.4mm;gap:6mm">
  <div>{act(1, "Refletir", 'Em que resultado deste ano estás mais orgulhoso? Porquê?' + UL(3, 6.8), "blue")}</div>
  <div>{act(2, "Comparar", 'Relê o que escreveste na p. 2 (atividade 1). O que fazes hoje de maneira diferente?' + UL(3, 6.8), "blue")}</div>
</div>
<div style="margin-top:auto">
  <div class="kicker">Os meus próximos passos</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:1.8mm">{nxh}</div>
  <div class="hand" style="margin-top:3.4mm;text-align:center;font-size:16pt">Aprender é ver mais longe do que ontem — como um farol.</div>
</div>
''', station="Chegada")
