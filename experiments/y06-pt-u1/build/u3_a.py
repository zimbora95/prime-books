import parts
from parts import *
parts.UNIT.update(n=3, total=16)

P = {}
NAR, INF, CAP = "var(--ink)", "var(--coral)", "var(--sea)"

# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, '''
<div class="abs" style="left:0;right:0;top:0;height:140mm"><img class="cover" src="img/infanta.jpg"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:150mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">3</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 3 · Texto poético</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">Vozes que o<br><em>tempo</em> guardou</h1>
    </div>
  </div>
  <p class="lead" style="margin-top:6mm;font-size:12.6pt">Antes de haver livros em todas as casas, as histórias viajavam de boca em boca: cantavam-se nos campos, nos serões, junto ao mar. Nesta unidade, vais ler um desses poemas antigos que ninguém sabe quem escreveu — e depois vais descobrir como os poetas de hoje transformam uma árvore, um rio ou um ofício em <b class="coral">imagens</b> que não se esquecem.</p>
  <div class="panel" style="margin-top:7mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4.5mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">2 min</div>
    <div style="font-size:10.2pt"><b class="blue">Em grupo.</b> Recitem ou cantem uma lengalenga, uma cantiga ou uma quadra que tenham aprendido com alguém mais velho. <b>Quem vo-la ensinou? E a quem a ensinou essa pessoa?</b> Acabaram de descobrir a tradição oral.</div>
  </div>
  <div style="margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm">
    <div style="border-top:1.2mm solid var(--ink);padding-top:2mm"><div class="kicker blue">3</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.4pt;margin-top:.8mm">O romance tradicional</div></div>
    <div style="border-top:1.2mm solid var(--coral);padding-top:2mm"><div class="kicker coral">3.1</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.4pt;margin-top:.8mm">A linguagem das imagens</div></div>
    <div style="border-top:1.2mm solid var(--sea);padding-top:2mm"><div class="kicker sea">3.2</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10.4pt;margin-top:.8mm">O poema de um ofício</div></div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 ROUTE
st = [("3","O romance tradicional","Bela Infanta · leitura em voz alta · resumo em prosa","3","var(--ink)"),
      ("3.1","A linguagem das imagens","Eugénio de Andrade · metáfora e comparação · o teu poema","8","var(--coral)"),
      ("3.2","O poema de um ofício","refrão, enumeração e ritmo · poema da turma","12","var(--sea)"),
      ("<svg viewBox=\"0 0 20 20\" style=\"width:9mm;height:9mm\"><path d=\"M3 10.5l4.5 4.5L17 5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>","Consegues?","revisão e autoavaliação","16","var(--ink)")]
sthtml = "".join(f'''<div style="display:grid;grid-template-columns:17mm 1fr 12mm;gap:4mm;align-items:center;padding:3.4mm 0;border-top:.6pt solid var(--rule)">
  <div class="display" style="font-size:24pt;line-height:1;color:{c}">{n}</div>
  <div><div style="font-family:FrauncesText;font-weight:700;font-size:12pt;color:var(--ink)">{t}</div><div class="small muted">{g}</div></div>
  <div style="font-family:Grotesk;font-weight:700;font-size:8pt;color:{c};text-align:right">p. {p}</div></div>''' for n,t,g,p,c in st)
P[2] = page(2, f'''
<div class="kicker">Antes de começar</div>
<h2 style="margin-top:2mm">A rota desta unidade</h2>
<div style="margin-top:5mm">{sthtml}</div>
<div class="grid2" style="margin-top:7mm;grid-template-columns:1fr 1fr;align-items:stretch">
  <div class="panel blue">
    <div class="kicker blue">O que é um romance tradicional?</div>
    <p style="margin-top:2.4mm;font-size:9.8pt">É um <b>poema que conta uma história</b>. Tem personagens, ação e, muitas vezes, diálogo. Chama-se <b>tradicional</b> porque foi transmitido <b>oralmente</b>, de geração em geração, durante séculos — por isso não se conhece o autor e existem várias versões do mesmo romance.</p>
    <p style="margin-top:2.4mm;font-size:9.8pt">No século XIX, o escritor <b>Almeida Garrett</b> recolheu muitos destes romances e publicou-os num livro chamado <i>Romanceiro</i>. A <i>Bela Infanta</i> era, segundo ele, o mais cantado de todos.</p>
  </div>
  <div>
    <h3>No fim da unidade, vais conseguir…</h3>
    <ul style="list-style:none;margin-top:2.6mm;font-size:9.5pt;line-height:1.36">
      <li style="margin-top:1.8mm"><span class="chk"></span>identificar as <b>personagens</b>, a <b>ausência</b> e o <b>reconhecimento</b> num romance tradicional;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span><b>ler em voz alta</b> um poema com várias vozes;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>resumir um poema <b>em prosa</b>, organizado em parágrafos;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>distinguir <b>verso</b>, <b>estrofe</b> e <b>rima</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>reconhecer e criar <b>metáforas</b> e <b>comparações</b>;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>usar o <b>refrão</b> e a <b>enumeração</b> num poema;</li>
      <li style="margin-top:1.8mm"><span class="chk"></span>usar <b>formas de tratamento</b>, <b>advérbios de modo</b>, o <b>particípio passado</b> e o <b>gerúndio</b>.</li>
    </ul>
  </div>
</div>
<div class="panel" style="margin-top:6mm;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;font-size:9pt">
  <div><span class="tag" style="background:{NAR};color:#fff">Narrador</span><p class="small" style="margin-top:1.4mm">conta a história.</p></div>
  <div><span class="tag" style="background:{INF};color:#fff">Infanta</span><p class="small" style="margin-top:1.4mm">a senhora que espera.</p></div>
  <div><span class="tag" style="background:{CAP};color:#fff">Capitão</span><p class="small" style="margin-top:1.4mm">o homem que chega do mar.</p></div>
  <p class="small muted" style="grid-column:1/-1">Nas páginas seguintes, cada voz do romance tem a sua cor. Assim, podem lê-lo a três vozes.</p>
</div>
<div class="grid2" style="margin-top:5mm;grid-template-columns:1.25fr 1fr;gap:6mm;align-items:stretch">
  <div><div class="kicker">Os textos que vais ler</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:3mm 4mm;margin-top:2.4mm"><div style="border-left:1.2mm solid var(--ink);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--ink)">P. 3 · ROMANCE</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">Bela Infanta</div><div class="small muted">tradicional, recolha de Garrett</div></div><div style="border-left:1.2mm solid var(--coral);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--coral)">P. 8 · POEMA-MODELO</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">O vento</div><div class="small muted">metáfora e comparação</div></div><div style="border-left:1.2mm solid var(--coral);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--coral)">P. 9 · POESIA</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">Quatro poemas de Eugénio de Andrade</div><div class="small muted">na edição da turma</div></div><div style="border-left:1.2mm solid var(--sea-d,#2E8C7B);padding:.6mm 0 .6mm 3mm"><div style="font-family:Grotesk;font-weight:700;font-size:7pt;letter-spacing:.12em;color:var(--sea-d,#2E8C7B)">P. 12 · POEMA COM REFRÃO</div><div style="font-family:FrauncesText;font-weight:700;font-size:9.6pt;color:var(--ink)">Canção do calceteiro</div><div class="small muted">refrão e enumeração</div></div></div></div>
  <div class="panel" style="padding:3.6mm 4mm;display:flex;flex-direction:column"><div class="kicker blue">Quem foi Almeida Garrett?</div><p style="font-size:9pt;line-height:1.45;margin-top:1.6mm">Escritor, poeta e dramaturgo, nasceu no Porto em 1799 e morreu em Lisboa em 1854. É considerado um dos fundadores do <b>Romantismo</b> português. Escreveu também <i>Viagens na Minha Terra</i>.</p><div style="margin-top:auto;padding-top:2mm">{qr("q-garrett", "Conhecer", "Almeida Garrett na Wikipédia.")}</div></div>
</div>
''', station="A rota")

# ---------------------------------------------------------------- 3-4 THE ROMANCE
N, I, C = "n", "i", "c"
stanzas = [
 (N, ["Estava a bela Infanta","No seu jardim assentada,","Com o pente de oiro fino","Seus cabelos penteava.","Deitou os olhos ao mar,","Viu uma nobre armada;","Capitão que nela vinha,","Muito bem que a governava."]),
 (I, ["— «Dize-me, ó capitão","Dessa tua nobre armada,","Se encontraste meu marido","Na terra que Deus pisava.»"]),
 (C, ["— «Anda tanto cavaleiro","Naquela terra sagrada…","Diz-me tu, ó senhora,","As senhas que ele levava.»"]),
 (I, ["— «Levava cavalo branco,","Selim de prata doirada;","Na ponta da sua lança","A cruz de Cristo levava.»"]),
 (C, ["— «Pelos sinais que me deste","Lá o vi numa estacada","Morrer morte de valente:","Eu sua morte vingava.»"]),
 (I, ["— «Ai triste de mim viúva,","Ai triste de mim coitada!","De três filhinhas que tenho,","Sem nenhuma ser casada!…»"]),
 (C, ["— «Que darias tu, senhora,","A quem no trouxera aqui?»"]),
 (I, ["— «Dera-lhe oiro e prata fina,","Quanta riqueza há por aí.»"]),
 (C, ["— «Não quero oiro nem prata,","Não nos quero para mim:","Que darias mais, senhora,","A quem no trouxera aqui?»"]),
 (I, ["— «De três moinhos que tenho,","Todos três tos dera a ti;","Um mói o cravo e a canela,","Outro mói do gerzeli:","Rica farinha que fazem!","Tomara-os el-rei para si.»"]),
 (C, ["— «Os teus moinhos não quero,","Não nos quero para mim:","Que darias mais, senhora,","A quem no trouxera aqui?»"]),
 (I, ["— «As telhas do meu telhado","Que são de oiro e marfim.»"]),
 (C, ["— «As telhas do teu telhado","Não nas quero para mim:","Que darias mais, senhora,","A quem no trouxera aqui?»"]),
 (I, ["— «De três filhas que tenho,","Todas três te dera a ti:","Uma para te calçar,","Outra para te vestir,","A mais formosa de todas","Para contigo dormir.»"]),
 (C, ["— «As tuas filhas, infanta,","Não são damas para mim:","Dá-me outra coisa, senhora,","Se queres que o traga aqui.»"]),
 (I, ["— «Não tenho mais que te dar,","Nem tu mais que me pedir.»"]),
 (C, ["— «Tudo, não, senhora minha,","Que inda não te deste a ti.»"]),
 (I, ["— «Cavaleiro que tal pede,","Que tão vilão é de si,","Por meus vilões arrastado","O farei andar aí","Ao rabo do meu cavalo,","À volta do meu jardim.","Vassalos, os meus vassalos,","Acudi-me agora aqui!»"]),
 (C, ["— «Este anel de sete pedras","Que eu contigo reparti…","Que é dela a outra metade?","Pois a minha, vê-la aí!»"]),
 (I, ["— «Tantos anos que chorei,","Tantos sustos que tremi!…","Deus te perdoe, marido,","Que me ias matando aqui.»"]),
]
COL = {N: NAR, I: INF, C: CAP}
LBL = {N: "Narrador", I: "Infanta", C: "Capitão"}
def render(sts, start):
    out, ln = [], start
    for who, vs in sts:
        c = COL[who]
        rows = [f'<div style="display:grid;grid-template-columns:7mm 1.1mm 1fr;column-gap:0"><span></span><span style="background:{c}"></span><span style="padding-left:3mm;font-family:Grotesk;font-weight:700;font-size:6.2pt;letter-spacing:.14em;text-transform:uppercase;color:{c};line-height:1;padding-top:.8mm;padding-bottom:1.2mm">{LBL[who]}</span></div>']
        for v in vs:
            num = str(ln) if ln % 5 == 0 else ""
            rows.append(f'<div style="display:grid;grid-template-columns:7mm 1.1mm 1fr"><span style="font-family:Grotesk;font-size:6.4pt;color:var(--muted);text-align:right;padding-right:2.2mm;padding-top:1.3mm">{num}</span><span style="background:{c}"></span><span style="padding-left:3mm">{v}</span></div>')
            ln += 1
        out.append(f'<div style="margin-bottom:3.4mm">{"".join(rows)}</div>')
    return "".join(out), ln

cols_sts = [stanzas[0:5], stanzas[5:11], stanzas[11:15], stanzas[15:]]
html_cols, ln = [], 1
for cs in cols_sts:
    h, ln = render(cs, ln); html_cols.append(h)
verse = 'font-family:FrauncesText;font-size:11pt;line-height:1.44;color:#1d2433'
P[3] = page(3, f'''
<div class="kicker blue">Texto 1 · Romance tradicional</div>
<h2 style="margin-top:2mm;font-size:30pt">Bela Infanta</h2>
<p class="small muted" style="margin-top:1.4mm">Romance tradicional português, na versão recolhida por Almeida Garrett no <i>Romanceiro</i> (século XIX).</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:5mm;{verse}"><div>{html_cols[0]}</div><div>{html_cols[1]}</div></div>
<div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:4mm;align-items:end;font-size:9pt"><b class="blue" style="font-size:9.4pt">Palavras que não conheço:</b><span style="border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div>
    <div class="panel blue" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.4pt">
  <div><div class="kicker blue">Antes de ler</div><p style="margin-top:1.6mm">Uma mulher espera, há muitos anos, o marido que partiu para a guerra. Um dia, um desconhecido chega do mar. <b>O que pode acontecer?</b></p></div>
  <div><div class="kicker blue">Enquanto lês</div><p style="margin-top:1.6mm">Segue as cores: cada voz tem a sua. Os números na margem contam os versos, de cinco em cinco — vais precisar deles nas perguntas.</p></div>
</div>
''', station="3 · Romance")
P[4] = page(4, f'''
<div style="display:grid;grid-template-columns:1fr 1fr 44mm;gap:6mm;height:100%">
  <div style="{verse}">{html_cols[2]}</div>
  <div style="{verse}">{html_cols[3]}</div>
  <aside style="border-left:.6pt solid var(--rule);padding-left:4.5mm;display:flex;flex-direction:column">
    <div class="kicker blue">Palavras de outro tempo</div>
    <dl class="gloss" style="margin-top:2.4mm">
      <dt>assentada</dt><dd>sentada.</dd>
      <dt>armada</dt><dd>conjunto de navios de guerra.</dd>
      <dt>a terra que Deus pisava</dt><dd>a Terra Santa, para onde partiam os cavaleiros das cruzadas.</dd>
      <dt>senhas</dt><dd>sinais para reconhecer alguém.</dd>
      <dt>selim</dt><dd>sela do cavalo.</dd>
      <dt>estacada</dt><dd>recinto cercado onde se combatia.</dd>
      <dt>no trouxera · não nos quero</dt><dd>o trouxera · não os quero (formas antigas).</dd>
      <dt>gerzeli</dt><dd>sésamo.</dd>
      <dt>vilão</dt><dd>pessoa sem nobreza de carácter; grosseiro.</dd>
      <dt>vassalos</dt><dd>os que servem um senhor.</dd>
      <dt>vê-la aí</dt><dd>ei-la aqui.</dd>
    </dl>
    <div class="hand" style="margin-top:4mm">Repara no pedido que se repete. Quantas vezes o ouves?</div>
    <div class="panel coral" style="margin-top:4mm;padding:3mm 3.4mm"><div class="kicker">Primeira impressão</div><p class="small" style="margin-top:1mm">Numa palavra, como te sentiste no fim?</p><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
    <p class="src" style="margin-top:auto">Texto: Almeida Garrett, <i>Romanceiro</i> (domínio público).</p>
  </aside>
</div>
''', station="3 · Romance")

# ---------------------------------------------------------------- 5 COMPREHENSION
offers = 5
stair = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;align-items:center;margin-top:2mm"><b style="color:{"var(--coral)" if i==5 else "var(--ink)"}">{i}.</b><div style="position:relative;height:8mm;background:linear-gradient(90deg,{"var(--coral-soft)" if i==5 else "var(--ink-soft)"} {40+i*12}%,transparent {40+i*12}%);border-radius:1.2mm"><div style="position:absolute;left:2mm;right:2mm;bottom:1.4mm;border-bottom:.6pt solid #8E99AA"></div></div></div>' for i in range(5,0,-1))
P[5] = page(5, f'''
<div class="kicker blue">Texto 1 · Compreender</div>
<h2 style="margin-top:2mm">A espera, a prova<br>e o <em>reconhecimento</em></h2>
<div class="grid2" style="margin-top:3mm;gap:7mm;grid-template-columns:1fr 1fr">
<div>
{act(1,"Localizar", 'Onde está a infanta e o que está a fazer quando a história começa? (versos 1-4)'+lines(3),"blue")}
{act(2,"Inferir", 'Porque é que o marido estava <b>ausente</b>? Que expressões do texto o mostram?'+lines(3),"blue")}
{act(3,"Descobrir", 'Quem é, na verdade, o capitão? Em que verso tens a certeza? Qual é o objeto que o prova?'+lines(3),"blue")}
</div>
<div>
{act(4,"Ordenar", 'O capitão recusa tudo o que a infanta oferece. Escreve as ofertas por ordem, do degrau mais baixo ao mais alto.',"blue")}
<div style="margin:2mm 0 0 12mm"><div class="small muted">1 = a primeira oferta · 5 = a última</div>{stair}</div>
<p class="small muted" style="margin-left:12mm;margin-top:1mm">Cada oferta vale mais do que a anterior: chama-se <b>gradação</b>.</p>
<div style="margin-left:12mm;margin-top:2mm;font-size:9.6pt">Porque é que a última oferta é a mais difícil de dar?{lines(2)}</div>
</div>
</div>
{act(5,"Pensar", 'O pedido «Que darias mais, senhora, / A quem no trouxera aqui?» repete-se. Funciona como um <b>refrão</b>. Que efeito tem essa repetição em quem ouve a história?'+lines(3),"blue")}
<div class="panel coral" style="margin-top:5mm">
{act(6,"Opinar", 'O marido pôs a mulher à prova antes de se dar a conhecer. Achas que agiu bem? Dá a tua <b>opinião</b> com <b>dois argumentos</b> — tal como aprendeste na Unidade 1.'+lines(3))}
</div>
''', station="3 · Romance")

# ---------------------------------------------------------------- 6 READ ALOUD + FORMS OF ADDRESS
P[6] = page(6, f'''
<div class="kicker">Oralidade · Gramática</div>
<h2 style="margin-top:2mm">Dar voz ao romance</h2>
<div class="grid2" style="margin-top:4mm;gap:6mm;grid-template-columns:1.1fr 1fr">
<div>
  <div class="panel">
    <div class="kicker blue">Guião da leitura a três vozes</div>
    <ol style="margin:2.4mm 0 0 4.5mm;font-size:9.6pt;line-height:1.42">
      <li>Formem grupos de três e distribuam as vozes pelas cores.</li>
      <li>Leiam em silêncio e marquem no texto: <b>/</b> pausa curta · <b>//</b> pausa longa.</li>
      <li>Sublinhem as <b>perguntas</b> (a voz sobe no fim) e as <b>exclamações</b> (mais força).</li>
      <li>Nas <b>reticências</b> (…), deixem a frase suspensa, como quem hesita.</li>
      <li>Ensaiem duas vezes. Na segunda, olhem para o público no fim de cada fala.</li>
    </ol>
  </div>
  {act(1,"Ler", 'Onde muda o tom da infanta? Indica o verso em que ela passa da <b>tristeza</b> à <b>ira</b>, e o verso em que passa da ira ao <b>alívio</b>.'+lines(2))}
  {act(2,"Avaliar", 'Ouve outro grupo e dá-lhe uma estrela (algo que resultou) e um desejo (algo a melhorar).<div style="display:grid;grid-template-columns:8mm 1fr;margin-top:1mm;align-items:end"><b class="coral"><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg></b><div class="lines"><i></i></div><b class="blue">→</b><div class="lines"><i></i></div></div>')}
  {act(3,"Improvisar", 'Em pares, inventem uma fala nova da infanta para o momento em que vê o anel. Digam-na em voz alta, com a entoação certa, e escrevam-na aqui.'+lines(4))}
</div>
<div>
  <div class="kicker sea">Formas de tratamento</div>
  <p style="margin-top:1.6mm;font-size:9.8pt">São as palavras com que nos dirigimos a alguém. Mostram <b>respeito</b>, <b>proximidade</b> ou a <b>posição</b> de cada pessoa.</p>
  <table class="cmp" style="margin-top:3mm">
    <tr><th style="background:var(--sea)">Forma</th><th style="background:var(--sea)">Quem fala a quem?</th></tr>
    <tr><td>«ó capitão»</td><td><span class="fill" style="min-width:40mm"></span></td></tr>
    <tr><td>«senhora», «senhora minha»</td><td><span class="fill" style="min-width:40mm"></span></td></tr>
    <tr><td>«infanta»</td><td><span class="fill" style="min-width:40mm"></span></td></tr>
    <tr><td>«Vassalos, os meus vassalos»</td><td><span class="fill" style="min-width:40mm"></span></td></tr>
    <tr><td>«marido»</td><td><span class="fill" style="min-width:40mm"></span></td></tr>
  </table>
  <div class="rule-card c" style="margin-top:4mm;font-size:9.2pt"><b class="sea">Tu, vós e senhora.</b> A infanta trata o capitão por <b>tu</b> («Dize-me»). Aos vassalos, fala na forma <b>vós</b> («Acudi-me»), que hoje quase não usamos. Atualmente, em situações formais, dizemos <b>o senhor / a senhora</b>.</div>
  {act(4,"Adequar", 'Reescreve este pedido para o dirigir, por escrito, à diretora da escola: <i>«Dá-nos a biblioteca na sexta, para ensaiarmos o romance.»</i>'+lines(3),"sea")}
  {act(5,"Tratar hoje", 'Como começarias uma mensagem para cada uma destas pessoas?<div style="display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;margin-top:1.6mm;align-items:end;font-size:9pt"><span>a tua avó:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span>o diretor da escola:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span>um colega da turma:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span></div>',"sea")}
</div>
</div>
''', station="3 · Romance")

# ---------------------------------------------------------------- 7 FROM VERSE TO PROSE
plan = [("1","Situação inicial","Onde está a infanta? O que vê?"),("2","O encontro","O que pergunta? Que notícia recebe?"),("3","A prova","O que oferece? Porque é recusada cada oferta?"),("4","O reconhecimento","Como reage ela? O que revela o capitão?")]
planhtml = "".join(f'<div style="display:grid;grid-template-columns:8mm 1fr;gap:2mm;margin-top:3mm"><div class="display" style="font-size:16pt;color:var(--coral);line-height:1">{n}</div><div><b class="blue">{t}</b> <span class="small muted">— {q}</span>{lines(3)}</div></div>' for n,t,q in plan)
P[7] = page(7, f'''
<div class="kicker">Escrita</div>
<h2 style="margin-top:2mm">Do verso à prosa</h2>
<div class="grid2" style="margin-top:4mm;gap:5mm;align-items:stretch">
  <div class="panel blue" style="font-family:FrauncesText;font-size:10pt;line-height:1.4"><div class="kicker blue" style="font-family:Grotesk">Em verso</div><div style="margin-top:2mm">Estava a bela Infanta<br>No seu jardim assentada,<br>Com o pente de oiro fino<br>Seus cabelos penteava.</div></div>
  <div class="panel" style="font-size:9.8pt"><div class="kicker">Em prosa</div><p style="margin-top:2mm">A bela infanta estava sentada no seu jardim<b class="coral">,</b> a pentear os cabelos com um pente de ouro fino<b class="coral">.</b> De repente<b class="coral">,</b> olhou para o mar e viu chegar uma grande armada<b class="coral">.</b></p></div>
</div>
<div class="rule-card o" style="margin-top:4mm;font-size:9.4pt"><b class="coral">Pontuação da prosa.</b> Em prosa, as linhas vão até à margem e o texto divide-se em <b>parágrafos</b>. Cada frase começa com maiúscula e termina com ponto; a vírgula separa expressões como <i>de repente</i>. Se quiseres usar as falas, abre parágrafo e usa o <b>travessão</b> (—), ou conta-as por palavras tuas: <i>A infanta perguntou-lhe se tinha visto o marido.</i></div>
{act(1,"Planear e escrever", 'Resume o romance <b>em prosa</b>, em quatro parágrafos. Usa as perguntas para te guiares. Escreve no presente ou no pretérito, mas não mudes a meio.')}
<div style="display:flex;gap:3mm;align-items:flex-end;margin-top:2.4mm"><b class="blue" style="font-size:9.6pt">Título do resumo:</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
{planhtml}
<div style="display:flex;gap:5mm;flex-wrap:wrap;margin-top:4mm;font-size:8.8pt">
  <span><span class="chk"></span>4 parágrafos</span><span><span class="chk"></span>sem versos nem rimas</span><span><span class="chk"></span>as falas contadas por palavras minhas</span><span><span class="chk"></span>maiúsculas e pontos finais</span><span><span class="chk"></span>li em voz alta para rever</span>
</div>
''', station="3 · Romance")

# ---------------------------------------------------------------- 8 LANGUAGE OF IMAGES
poem = [("O vento <span class='mk-o'>é um carteiro sem morada</span>:",""),("entrega folhas a quem não as pede,",""),("bate às janelas <span class='mk-f'>como quem tem pressa</span>",""),("e foge antes que a porta se abra.",""),("",""),("À noite, cansado, deita-se no rio",""),("<span class='mk-f'>como um cão que volta para casa</span>;",""),("e o rio, <span class='mk-o'>que é um espelho acordado</span>,",""),("guarda-lhe o sono até de madrugada.","")]
poemhtml = "".join(f'<div>{v}</div>' if v else '<div style="height:3mm"></div>' for v,_ in poem)
P[8] = page(8, f'''
<div class="abs" style="left:0;right:0;top:0;height:112mm"><img class="cover" src="img/arvore.jpg" style="object-position:50% 60%"></div>
<div class="abs" style="left:21mm;right:23.5mm;top:120mm;bottom:15mm">
  <div class="kicker coral">Estação 3.1 · A linguagem das imagens</div>
  <h2 style="margin-top:2mm">O que o poeta vê <em>a mais</em></h2>
  <div class="grid2" style="margin-top:4mm;gap:7mm;grid-template-columns:1fr 1fr">
    <div>
      <div style="font-family:FrauncesText;font-size:11pt;line-height:1.5">
        <div class="kicker blue" style="font-family:Grotesk">Poema-modelo</div>
        <div style="font-family:Fraunces;font-weight:600;font-size:15pt;color:var(--ink);margin:1mm 0 2.4mm">O carteiro sem morada</div>
        {poemhtml}
      </div>
      <p class="src" style="margin-top:2mm">Poema escrito para esta unidade.</p>
    </div>
    <div>
      <div class="rule-card" style="font-size:9.4pt"><b class="blue">Verso</b> é cada linha do poema. <b class="blue">Estrofe</b> é um grupo de versos: este poema tem uma estrofe de 4 versos (<b>quadra</b>) e outra de 4. Quando o som final de dois versos se repete (<i>pente / gente</i>), há <b class="blue">rima</b>.</div>
      <div class="rule-card" style="margin-top:3mm;font-size:9.4pt"><span class="mk-f"><b>Comparação</b></span> — aproxima duas coisas com uma palavra de ligação: <b>como</b>, <b>tal como</b>, <b>parece</b>. <i>Bate às janelas como quem tem pressa.</i></div>
      <div class="rule-card o" style="margin-top:3mm;font-size:9.4pt"><span class="mk-o"><b>Metáfora</b></span> — diz que uma coisa <b>é</b> outra, sem palavra de ligação. <i>O vento é um carteiro sem morada.</i></div>
      {act(1,"Observar", 'Este poema tem rima? Justifica com dois exemplos de sons finais.'+lines(2))}
      {act(2,"Classificar", 'Escreve <b class="blue">C</b> (comparação) ou <b class="coral">M</b> (metáfora).<div style="display:grid;grid-template-columns:1fr 9mm;gap:1.6mm 2mm;margin-top:1.6mm;font-size:9.2pt"><span>A lua é uma moeda esquecida.</span><span class="chk"></span><span>O mar ruge como um leão.</span><span class="chk"></span><span>A estrada parece uma fita.</span><span class="chk"></span></div>')}
    </div>
  </div>
</div>
''', station="3.1 · Imagens", bleed=True, rh=False)
