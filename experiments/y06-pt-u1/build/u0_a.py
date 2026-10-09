import parts
from parts import *
parts.UNIT.update(n=0, total=6)

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea-d, #2E8C7B)"

def levels(labels=("Ainda não", "Quase", "Já sei")):
    """Three drawn circles with labels, for self- and peer-assessment (no font glyphs)."""
    c = '<svg viewBox="0 0 20 20" style="width:4.2mm;height:4.2mm;vertical-align:-1mm"><circle cx="10" cy="10" r="8" fill="none" stroke="#17315A" stroke-width="1.6"/></svg>'
    return "".join(f'<span style="display:inline-flex;align-items:center;gap:1.2mm;margin-right:3.4mm;font-size:8.4pt;white-space:nowrap">{c}{l}</span>' for l in labels)

def uline(h=6):
    return f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'

# ---------------------------------------------------------------- 1 OPENER
route = [("1", "Ouvir", "e registar as ideias principais", "p. 2", INK),
         ("2", "Ler em voz alta", "um parágrafo, com expressão", "p. 3", COR),
         ("3", "Gramática", "sujeito e predicado", "p. 4", SEA),
         ("4", "Escrever", "uma narrativa curta com descrição", "p. 5", INK),
         ("5", "O meu ponto de partida", "o que já sei e as minhas metas", "p. 6", COR)]
rt = "".join(f'''<div style="border-top:1.2mm solid {c};padding-top:2mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="display" style="font-size:17pt;color:{c};line-height:1">{n}</span><span class="small muted">{p}</span></div>
  <div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:9.8pt;margin-top:1mm;line-height:1.2">{t}</div>
  <div class="small muted" style="margin-top:.6mm;line-height:1.3">{s}</div></div>''' for n, t, s, p, c in route)
P[1] = page(1, f'''
<div class="abs" style="left:0;right:0;top:0;height:163mm"><img class="cover" src="img/partida.jpg"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:171mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">0</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 0 · Avaliação diagnóstica</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">Ponto de <em>partida</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:4mm;font-size:11.8pt">Bem-vindo ao 6.º ano! Antes de o barco sair do porto, o capitão verifica tudo o que leva a bordo. É isso que vais fazer nestas páginas: mostrar o que já sabes do 5.º ano, para que tu e o teu professor saibam por onde começar.</p>
  <div class="rule-card o" style="margin-top:4mm;font-size:9.8pt"><b class="coral">Isto não é um teste — é um ponto de partida.</b> Não há notas. Responde sozinho, com calma, e sem medo de errar: um erro aqui é uma pista para o ano que vem.</div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:auto">{rt}</div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 LISTENING
cols = [("Ideia principal 1", "Para que serve um farol?"), ("Ideia principal 2", "Os faróis de Portugal"), ("Ideia principal 3", "Os faroleiros, ontem e hoje")]
ch = "".join(f'''<div class="panel" style="padding:3.4mm 3.6mm">
  <div class="kicker">{k}</div><div class="small muted" style="margin-top:.8mm">Pista: {h}</div>
  <div style="margin-top:1.6mm;font-size:8.6pt;color:var(--muted)">Palavras-chave</div>{uline(6.2)}{uline(6.2)}{uline(6.2)}{uline(6.2)}{uline(6.2)}</div>''' for k, h in cols)
P[2] = page(2, f'''
<div style="display:flex;gap:4mm;align-items:center">{MICRO}<div><div class="kicker blue">1 · Ouvir</div><h2 style="margin-top:1mm">Luzes que guardam a costa</h2></div></div>
<p class="lead" style="margin-top:2.6mm;font-size:10.8pt">O teu professor vai ler, duas vezes, um texto expositivo sobre os faróis de Portugal. <b>Não o procures no livro antes de ouvir.</b></p>
{act(1, "Antes de ouvir", 'Escreve três palavras que esperas ouvir num texto sobre faróis.<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:1mm">' + uline(6)*3 + '</div>', "blue")}
<div style="margin-top:4mm">{act(2, "Enquanto ouves", 'Na <b>primeira</b> leitura, só ouve. Na <b>segunda</b>, regista apenas <b>palavras-chave</b> — não frases completas.', "blue")}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:2.6mm">{ch}</div>
<div class="grid2" style="margin-top:4mm;gap:6mm">
  <div class="panel blue" style="padding:3.4mm 3.6mm"><div class="kicker blue">Números e nomes que ouvi</div>
    <div style="display:grid;grid-template-columns:auto 1fr;gap:1mm 3mm;margin-top:1.4mm;font-size:8.8pt;align-items:end">
      <span>um ano:</span>{uline(5)}<span>um farol:</span>{uline(5)}<span>uma distância:</span>{uline(5)}<span>uma ilha:</span>{uline(5)}</div></div>
  <div>{act(3, "Depois de ouvir", 'Usando as tuas notas, escreve numa só frase o assunto principal do texto.' + lines(3), "blue")}</div>
</div>
<div style="margin-top:3.4mm">{act(4, "Verificar", 'Verdadeiro (V) ou falso (F)? Corrige as falsas.', "blue")}
<div style="display:grid;grid-template-columns:1fr 9mm;gap:1.6mm 3mm;margin-top:1.6mm;font-size:9.4pt;align-items:center;padding-left:9mm">
  <span>a) Todos os faróis acendem a luz da mesma maneira.</span><span class="chk"></span>
  <span>b) Em Portugal, os faróis estão a cargo da Marinha.</span><span class="chk"></span>
  <span>c) Hoje, já não há nenhum farol automático.</span><span class="chk"></span>
</div>{lines(3)}</div>
<div style="margin-top:3mm">{act(5, "Refletir", 'O que foi mais difícil de apanhar: os <b>números</b>, os <b>nomes</b> ou as <b>ideias</b>? Porquê?' + lines(2), "blue")}</div>
''', station="Ouvir")

# ---------------------------------------------------------------- 3 READING ALOUD
crit = [("Ritmo", "Leio sem ir depressa demais nem parar a cada palavra."),
        ("Pausas", "Respeito as vírgulas (pausa curta) e os pontos (pausa longa)."),
        ("Entoação", "A minha voz sobe nas perguntas e ganha força nas exclamações."),
        ("Articulação", "Pronuncio as palavras inteiras, sem «comer» sílabas."),
        ("Volume", "Toda a turma me ouve, mesmo ao fundo da sala.")]
cr = "".join(f'<tr><td style="font-size:8.8pt"><b>{a}</b><div class="small muted" style="font-weight:400;margin-top:.4mm">{b}</div></td><td>{levels()}</td></tr>' for a, b in crit)
P[3] = page(3, f'''
<div style="display:flex;gap:4mm;align-items:center">{MEGA}<div><div class="kicker">2 · Ler em voz alta</div><h2 style="margin-top:1mm">A noite do faroleiro</h2></div></div>
<div class="grid2" style="grid-template-columns:1.35fr 1fr;gap:7mm;margin-top:3.4mm;align-items:start">
  <div>
    <div class="panel" style="padding:5mm 5.4mm;font-family:FrauncesText;font-size:10.7pt;line-height:1.5">
      Naquela noite, o vento soprava com tanta força que as janelas do farol tremiam. O senhor Amaro subiu os cento e dois degraus da escada em caracol, devagar, com a lanterna na mão. Lá em cima, verificou a lâmpada, limpou os vidros e olhou para o mar escuro.<br>
      — Haverá algum barco lá fora, com um tempo destes? — perguntou, baixinho, ao gato que o seguia.<br>
      De repente, ao longe, viu uma pequena luz a balançar sobre as ondas. Era um barco de pesca! O faroleiro sorriu: enquanto a sua luz girasse, aqueles pescadores saberiam o caminho de casa.
    </div>
    <p class="src" style="margin-top:1.6mm">Texto escrito para este manual.</p>
    <div class="panel coral" style="margin-top:2.4mm;padding:2.6mm 3.6mm">
      <div class="kicker">Aquecer a voz · lê por sílabas, depois de seguida</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:1.4mm;font-family:FrauncesText;font-size:9.6pt;line-height:1.35">
        <span>ca·ra·col<br><b>caracol</b></span><span>ba·lan·çar<br><b>balançar</b></span><span>pes·ca·do·res<br><b>pescadores</b></span></div>
    </div>
  </div>
  <div>
    {act(1, "Preparar", 'Antes de leres em voz alta, lê o texto em silêncio. Depois, marca a lápis:<div style="margin-top:1.4mm;font-size:9pt;line-height:1.6"><b class="coral">/</b> onde fazes uma pausa curta;<br><b class="coral">//</b> onde fazes uma pausa longa;<br>um <b>círculo</b> nas palavras difíceis.</div>')}
    {act(2, "Ensaiar", 'Qual é a frase que deve ser lida com mais <b>suspense</b>? E com mais <b>alegria</b>?' + lines(2))}
    {act(3, "Ler", 'Lê o texto a um colega. Ele cronometra e preenche a grelha em baixo.<div style="display:grid;grid-template-columns:auto 1fr;gap:2mm;margin-top:1.4mm;align-items:end;font-size:9pt"><span>Tempo de leitura:</span>' + uline(5) + '<span>Palavras em que hesitei:</span>' + uline(5) + '</div>')}
  </div>
</div>
<h3 style="margin-top:3.4mm">Grelha de leitura <span class="small muted" style="font-family:Body;font-weight:400">— preenchida pelo colega</span></h3>
<table class="cmp ruled" style="margin-top:1.6mm"><tr><th style="background:var(--coral)">Critério</th><th style="background:var(--coral)">Nível</th></tr>{cr}</table>
<div style="display:grid;grid-template-columns:auto 1fr;gap:3mm;align-items:end;margin-top:2.6mm;font-size:9.4pt"><b class="coral">Um conselho do meu colega:</b>{uline(6)}</div>
''', station="Ler")

# ---------------------------------------------------------------- 4 GRAMMAR — SUBJECT AND PREDICATE
sent = ["O farol do Cabo da Roca funciona desde 1772.",
        "Os pescadores regressaram ao porto ao fim da tarde.",
        "A luz do farol gira durante toda a noite.",
        "O senhor Amaro e o gato subiram a escada em caracol.",
        "No alto do rochedo, brilha uma luz vermelha."]
sh = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2mm;margin-top:2.6mm;font-size:10.4pt;font-family:FrauncesText"><b class="display" style="color:var(--sea-d,#2E8C7B);font-size:12pt;line-height:1.2">{chr(97+i)})</b><span style="line-height:1.5">{s}</span></div>' for i, s in enumerate(sent))
P[4] = page(4, f'''
<div style="display:flex;gap:4mm;align-items:center">{PONTE}<div><div class="kicker sea">3 · Gramática</div><h2 style="margin-top:1mm">Quem faz? O que se diz?</h2></div></div>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:3.6mm;align-items:stretch">
  <div class="rule-card" style="font-size:9.6pt;line-height:1.5"><b class="blue">Sujeito</b> — a parte da frase que indica <b>de quem ou de que</b> se fala.<br>Para o encontrar, pergunta ao verbo: <i>Quem é que…? O que é que…?</i><div style="margin-top:1.6mm;font-family:FrauncesText"><u style="text-decoration-color:var(--ink);text-decoration-thickness:1.4pt;text-underline-offset:1.4mm">O faroleiro</u> limpou os vidros.</div></div>
  <div class="rule-card o" style="font-size:9.6pt;line-height:1.5"><b class="coral">Predicado</b> — a parte da frase que diz <b>o que</b> se afirma sobre o sujeito. Contém sempre o <b>verbo</b>.<div style="margin-top:1.6mm;font-family:FrauncesText">O faroleiro <span style="border-bottom:1.4pt dashed var(--coral);padding-bottom:.6mm">limpou os vidros</span>.</div><div class="small muted" style="margin-top:1.2mm">Atenção: o sujeito nem sempre está no início da frase!</div></div>
</div>
{act(1, "Identificar", 'Sublinha o <b>sujeito</b> com um traço contínuo e o <b>predicado</b> com um traço interrompido, como nos exemplos.', "sea")}
<div style="padding-left:9mm">{sh}</div>
<div class="grid2" style="margin-top:4.4mm;gap:7mm">
  <div>{act(2, "Explicar", 'Na frase <b>e)</b>, onde está o sujeito? Como o descobriste?' + lines(3), "sea")}</div>
  <div>{act(3, "Completar", 'Escreve um <b>predicado</b> para cada sujeito.<div style="display:grid;grid-template-columns:auto 1fr;gap:2mm 3mm;margin-top:1.4mm;align-items:end;font-family:FrauncesText;font-size:9.8pt"><span>As gaivotas</span>' + uline(5) + '<span>O mar</span>' + uline(5) + '</div>', "sea")}</div>
</div>
<div style="margin-top:3mm">{act(4, "Criar", 'Escreve uma frase sobre a fotografia da página de abertura. Depois, sublinha o sujeito e o predicado.' + lines(2), "sea")}</div>
<div style="margin-top:3mm">{act(5, "Juntar", 'Junta as duas frases numa só, com um sujeito formado por duas personagens: <i>O faroleiro subiu a escada. O gato subiu a escada.</i>' + lines(2), "sea")}</div>
<div class="panel sea" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center">
  <div class="kicker sea" style="max-width:32mm">Desafio</div>
  <div style="font-size:9.4pt">Em <i>«Chegámos ao farol ao pôr do sol.»</i>, o sujeito não está escrito. Quem chegou? Como o sabes?{uline(6)}{uline(6)}</div>
</div>
''', station="Gramática")

# ---------------------------------------------------------------- 5 WRITING — SHORT NARRATIVE WITH DESCRIPTION
plan = [("Quem?", "a personagem principal"), ("Onde?", "o lugar, descrito"), ("Quando?", "o momento do dia, o tempo"),
        ("O problema", "o que corre mal"), ("A solução", "como acaba")]
pl = "".join(f'<div style="border-top:1.1mm solid var(--ink);padding-top:1.6mm"><b class="blue" style="font-size:9.4pt">{a}</b><div class="small muted" style="height:8mm;line-height:1.3">{b}</div>{uline(5.5)}{uline(5.5)}</div>' for a, b in plan)
sens = [("vejo", "cinzento, a brilhar, espuma branca…"), ("ouço", "o vento a uivar, as gaivotas…"),
        ("cheiro", "a sal, a algas…"), ("sinto", "frio, o chão a tremer…")]
se = "".join(f'<div style="display:grid;grid-template-columns:14mm 1fr;gap:2mm;align-items:end;margin-top:1.6mm;font-size:9pt"><b class="coral">{a}</b><span class="small muted" style="border-bottom:.6pt solid #AEB7C4;padding-bottom:.6mm">{b}</span></div>' for a, b in sens)
P[5] = page(5, f'''
<div style="display:flex;gap:4mm;align-items:center">{LAPIS}<div><div class="kicker blue">4 · Escrever</div><h2 style="margin-top:1mm">Uma história à beira-mar</h2></div></div>
<p class="lead" style="margin-top:2.4mm;font-size:10.6pt">Escreve uma narrativa curta (entre 12 e 15 linhas) que se passe num farol, num porto ou numa praia. Inclui uma <b>descrição</b> do lugar, que faça o leitor sentir que está lá.</p>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3.4mm;margin-top:3mm">{pl}</div>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:3.6mm">
  <div class="panel coral" style="padding:3.4mm 3.8mm"><div class="kicker">Os cinco sentidos na descrição</div>{se}</div>
  <div class="panel" style="padding:3.4mm 3.8mm;font-size:9.2pt;line-height:1.55"><div class="kicker">Antes de entregar, verifica</div>
    <div style="display:grid;grid-template-columns:5mm 1fr;gap:.8mm 2mm;margin-top:1.4mm;align-items:start">
      <span class="chk"></span><span>A história tem <b>início, meio e fim</b>.</span>
      <span class="chk"></span><span>Há pelo menos <b>três</b> pormenores de descrição.</span>
      <span class="chk"></span><span>Os parágrafos estão marcados.</span>
      <span class="chk"></span><span>Usei pontuação e travessão no diálogo.</span></div></div>
</div>
<div style="display:flex;gap:3mm;align-items:flex-end;margin-top:4mm"><b class="blue" style="font-size:9.6pt">Título:</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
{lines(20)}
''', station="Escrever")

# ---------------------------------------------------------------- 6 SELF-DIAGNOSIS + TEACHER'S LISTENING TEXT (upside down)
areas = [("Ouvir", "Registo as ideias principais de um texto ouvido."),
         ("Ler em voz alta", "Leio com ritmo, pausas e entoação."),
         ("Gramática", "Identifico o sujeito e o predicado."),
         ("Escrever", "Escrevo uma narrativa com descrição.")]
ar = "".join(f'<tr><td style="font-size:9pt"><b>{a}</b><div class="small muted" style="font-weight:400;margin-top:.4mm">{b}</div></td><td>{levels()}</td></tr>' for a, b in areas)
goals = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;align-items:end;margin-top:2mm"><b class="coral">{i}.</b>{uline(5)}</div>' for i in (1, 2, 3))
listening = '''<p>Um farol é uma torre construída junto ao mar, com uma luz muito forte no topo. Serve para avisar os navegadores de que há terra, rochas ou perigos por perto, e para os ajudar a saber onde estão. De noite, cada farol acende a sua luz de uma maneira diferente — com clarões mais longos ou mais curtos, mais rápidos ou mais lentos —, e é assim que os marinheiros o reconhecem.</p>
<p style="margin-top:1.2mm">Em Portugal, contando com o continente e as ilhas, há mais de cinquenta faróis. Desde 1924, estão a cargo da Direção de Faróis, que pertence à Marinha. O farol do Cabo da Roca funciona desde 1772. No Cabo de São Vicente, no Algarve, a torre atual funciona desde 1846 e a sua luz chega a cerca de 32 milhas náuticas, quase 60 quilómetros. Nos Açores, na ilha das Flores, fica o farol de Albarnaz, o mais ocidental da Europa.</p>
<p style="margin-top:1.2mm">Durante muitos anos, os faróis precisaram de faroleiros: homens e mulheres que viviam junto à torre, acendiam a luz, limpavam as lentes e vigiavam o mar, noite após noite. Hoje, muitos faróis funcionam de forma automática, mas continuam a ser vigiados e cuidados pela Marinha.</p>'''
P[6] = page(6, f'''
<div class="kicker">5 · O meu ponto de partida</div>
<h2 style="margin-top:1.4mm">O que já sei — e para onde vou</h2>
<table class="cmp ruled" style="margin-top:3mm"><tr><th style="background:var(--ink)">Competência</th><th style="background:var(--ink)">Como me sinto</th></tr>{ar}</table>
<div class="grid2" style="margin-top:4mm;gap:6mm">
  <div class="panel blue" style="padding:3.4mm 3.8mm"><div class="kicker blue">Aquilo em que sou bom</div>{uline(6)}{uline(6)}</div>
  <div class="panel coral" style="padding:3.4mm 3.8mm"><div class="kicker">Três metas para o 6.º ano</div>{goals}</div>
</div>
<div class="panel" style="margin-top:4mm;padding:3.4mm 3.8mm"><div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker">O que o professor observou</div><div class="small muted">a preencher pelo professor</div></div>{uline(6.4)}{uline(6.4)}{uline(6.4)}</div>
<div style="margin-top:auto;border:.8pt dashed var(--muted);border-radius:2.4mm;padding:4mm 5mm;transform:rotate(180deg)">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker blue">Para o professor ler em voz alta · página 2</div><div class="small muted">Ler duas vezes, a ritmo natural.</div></div>
  <div style="font-family:FrauncesText;font-size:9.2pt;line-height:1.48;margin-top:1.6mm">{listening}</div>
  <p class="src" style="margin-top:1.4mm">Texto escrito para este manual. Fontes: Direção de Faróis (Autoridade Marítima Nacional); Público/Fugas, «Faróis de Portugal»; RTP, «Farol do Cabo da Roca faz 250 anos» (2022); SIC Notícias, «Albarnaz, o farol mais ocidental de Portugal e da Europa» (2025); Wikipédia, «Farol do Cabo de São Vicente».</p>
</div>
''', station="Chegada")
