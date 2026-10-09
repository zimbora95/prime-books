import parts
from parts import *
parts.UNIT.update(n=3, total=16)

P = {}

# ---------------------------------------------------------------- 9 READING EUGÉNIO DE ANDRADE
cols = ["Poema 1","Poema 2","Poema 3","Poema 4"]
rowsdef = [("Título",""),("De que fala? (árvore, rio, vento…)",""),("N.º de estrofes · de versos",""),("Tem rima? Dá um exemplo",""),("Uma imagem que guardo","tall"),("Metáfora ou comparação?","")]
th = "".join(f'<th style="background:var(--coral)">{c}</th>' for c in cols)
trs = "".join(f'<tr><td style="font-size:8.6pt">{r}</td>' + "".join(f'<td style="height:{"16mm" if k=="tall" else "9mm"}"></td>' for _ in cols) + '</tr>' for r,k in rowsdef)
P[9] = page(9, f'''
<div class="kicker">Estação 3.1 · Educação literária</div>
<h2 style="margin-top:2mm">Ler Eugénio de Andrade</h2>
<div class="grid2" style="margin-top:4mm;grid-template-columns:1fr 62mm;gap:7mm">
  <div>
    <p class="lead">Eugénio de Andrade escreveu sobre as coisas mais simples — a água, uma árvore, o vento, a luz — com tão poucas palavras que cada uma parece pesar o dobro.</p>
    <p style="margin-top:3mm;font-size:9.8pt">O teu professor vai entregar-te <b>quatro poemas integrais</b> do autor, sobre a árvore, o rio ou o vento. Lê cada um <b>duas vezes</b>: primeiro em silêncio, depois em voz alta, devagar. Depois, preenche o teu diário de leitura.</p>
  </div>
  <div class="panel coral" style="font-size:8.9pt;line-height:1.38">
    <div class="kicker">Quem foi?</div>
    <p style="margin-top:1.8mm"><b>Eugénio de Andrade</b> é o pseudónimo de <b>José Fontinhas</b> (1923-2005). Nasceu em Póvoa de Atalaia, no concelho do Fundão, e viveu grande parte da vida no Porto.</p>
    <p style="margin-top:1.4mm">Recebeu o <b>Prémio Camões</b> em 2001, o mais importante da língua portuguesa. Para os mais novos, escreveu <i>História da Égua Branca</i> (1977) e <i>Aquela Nuvem e Outras</i> (1986).</p>
  </div>
</div>
<div class="kicker coral" style="margin-top:6mm">Diário de leitura</div>
<table class="cmp ruled" style="margin-top:2mm;table-layout:fixed"><tr><th style="background:var(--coral);width:40mm"></th>{th}</tr>{trs}</table>
{act(1,"Comparar", 'Qual dos quatro poemas preferes? Justifica com um verso que copies do poema e com uma razão tua.'+lines(2))}
{act(2,"Ler em voz alta", 'Escolhe um dos poemas e lê-o à turma. Antes, marca as pausas no fim de cada verso e no fim de cada estrofe.')}
{act(3,"Perguntar", 'Se pudesses fazer uma pergunta a Eugénio de Andrade sobre um destes poemas, qual seria?'+lines(1))}
''', station="3.1 · Imagens")

# ---------------------------------------------------------------- 10 METAPHOR WORKSHOP + GRAMMAR
comps = ["A árvore é alta como uma torre.","O rio corre como uma cobra prateada.","O vento uiva como um lobo.","As nuvens parecem ovelhas no céu."]
comphtml = "".join(f'<div style="display:grid;grid-template-columns:62mm 1fr;gap:3mm;align-items:end;margin-top:2.4mm;font-size:9.6pt"><span class="mk-f">{c}</span><div style="border-bottom:.6pt solid #AEB7C4;height:6mm"></div></div>' for c in comps)
P[10] = page(10, f'''
<div class="kicker">Estação 3.1 · Oficina · Gramática</div>
<h2 style="margin-top:2mm">A oficina das <em>metáforas</em></h2>
{act(1,"Transformar", 'Tira a palavra de ligação e transforma cada <b class="blue">comparação</b> numa <b class="coral">metáfora</b>. <span class="small muted">Ex.: O vento uiva como um lobo → <i>O vento é um lobo que uiva no telhado.</i></span>'+comphtml)}
{act(2,"Inventar", 'Completa as metáforas com uma imagem tua.<div style="display:grid;gap:2.4mm;margin-top:2.4mm"><div>A chuva é <span class="fill l" style="min-width:110mm"></span></div><div>O silêncio da noite é <span class="fill l" style="min-width:96mm"></span></div></div>')}
<div class="grid2" style="margin-top:6mm;gap:6mm">
  <div class="panel sea">
    <div class="kicker sea">Advérbio de modo</div>
    <p style="margin-top:1.8mm;font-size:9.4pt">Diz <b>como</b> acontece a ação. Muitos formam-se juntando <b>-mente</b> ao adjetivo no feminino: <i>lenta → lentamente</i>, <i>doce → docemente</i>. Outros: <i>bem, mal, depressa, devagar</i>.</p>
    {act("a","Identificar", 'Sublinha os advérbios de modo.<div style="font-family:FrauncesText;margin-top:1.6mm;font-size:9.8pt;line-height:1.5">O rio passa devagar. O vento sopra furiosamente e a árvore balança suavemente, como quem dança bem.</div>',"sea")}
    {act("b","Formar", '<div style="display:grid;grid-template-columns:auto 1fr;gap:2mm 2mm;align-items:end"><span>calmo →</span><span class="fill" style="min-width:0;width:100%"></span><span>feliz →</span><span class="fill" style="min-width:0;width:100%"></span><span>triste →</span><span class="fill" style="min-width:0;width:100%"></span></div>',"sea")}
  </div>
  <div class="panel sea">
    <div class="kicker sea">Particípio passado</div>
    <p style="margin-top:1.8mm;font-size:9.4pt">Forma do verbo que termina, em regra, em <b>-ado</b> ou <b>-ido</b>: <i>cansar → cansado</i>, <i>acordar → acordado</i>. Alguns são irregulares: <i>abrir → aberto, escrever → escrito, pôr → posto, ver → visto</i>.</p>
    {act("c","Encontrar", 'No poema da página 8, há dois particípios passados. Quais?<div style="margin-top:1.4mm"><span class="fill l"></span> &nbsp; <span class="fill l"></span></div>',"sea")}
    {act("d","Completar", '<div style="line-height:2">A janela estava <span class="fill s"></span> (abrir).<br>O poema foi <span class="fill s"></span> (escrever) à noite.<br>A mesa já está <span class="fill s"></span> (pôr).</div>',"sea")}
  </div>
</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(3,"Classificar", 'Metáfora (<b class="coral">M</b>) ou comparação (<b class="blue">C</b>)?<div style="display:grid;grid-template-columns:1fr 7mm;gap:1.8mm 3mm;margin-top:1.6mm;font-family:FrauncesText;font-size:9.6pt;align-items:center"><span>A lua é uma moeda esquecida.</span><span class="chk"></span><span>O mar brilha como vidro partido.</span><span class="chk"></span><span>A tua voz é um cobertor quente.</span><span class="chk"></span><span>Corria como o vento.</span><span class="chk"></span></div>')}</div>
  <div>{act(4,"Escrever", 'Escreve uma frase sobre o mar com uma <b>metáfora</b>, um <b>advérbio de modo</b> e um <b>particípio passado</b>.'+lines(3))}</div>
</div>
''', station="3.1 · Imagens")

# ---------------------------------------------------------------- 11 WRITE A POEM
P[11] = page(11, f'''
<div class="kicker">Estação 3.1 · Escrita</div>
<h2 style="margin-top:2mm">O teu poema: duas estrofes, <em>uma metáfora</em></h2>
<div class="grid3" style="margin-top:4mm">
  <div class="panel"><div class="kicker blue">1 · Escolhe</div><p class="small" style="margin-top:1.6mm">Uma árvore, um rio ou o vento — de preferência um que conheças: a árvore do recreio, o rio da tua terra…</p><div class="lines"><i></i></div></div>
  <div class="panel"><div class="kicker blue">2 · Observa</div><p class="small" style="margin-top:1.6mm">Escreve o que vês, ouves e sentes. Só palavras soltas.</p><div class="lines"><i></i><i></i></div></div>
  <div class="panel coral"><div class="kicker">3 · Transforma</div><p class="small" style="margin-top:1.6mm">Se fosse outra coisa, o que seria? <b>____ é ____</b> porque…</p><div class="lines"><i></i><i></i></div></div>
</div>
{act(1,"Escrever o rascunho", 'Escreve duas estrofes de quatro versos. Põe a tua metáfora na primeira estrofe. Dá um título ao poema.')}
<div style="display:flex;gap:3mm;align-items:flex-end;margin-top:3mm"><span class="small muted">Título</span><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:2mm">
  <div><div class="small muted" style="margin-top:2mm">1.ª estrofe</div>{lines(4)}</div>
  <div><div class="small muted" style="margin-top:2mm">2.ª estrofe</div>{lines(4)}</div>
</div>
<div class="panel" style="margin-top:4mm;padding:3.6mm 4.4mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="kicker">Passar a limpo</div><div class="small muted">depois de rever com o colega</div></div>
  <div style="display:flex;gap:3mm;align-items:flex-end;margin-top:2mm"><span class="small muted">Título</span><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:1mm"><div>{lines(6)}</div><div>{lines(6)}</div></div>
</div>
<div class="grid2" style="margin-top:auto;gap:6mm">
  <div class="panel blue">
    <div class="kicker blue">Rever com um colega</div>
    <ul style="list-style:none;margin-top:2mm;font-size:9.2pt;line-height:1.6">
      <li><span class="chk"></span>2 estrofes de 4 versos</li><li><span class="chk"></span>pelo menos 1 metáfora</li><li><span class="chk"></span>1 advérbio de modo</li><li><span class="chk"></span>um título que não conta tudo</li><li><span class="chk"></span>li o poema em voz alta</li>
    </ul>
  </div>
  <div class="panel">
    <div class="kicker">A opinião do colega</div>
    <p class="small" style="margin-top:1.6mm">A imagem de que mais gostei foi…</p>{lines(2)}
    <p class="small" style="margin-top:2mm">Podias melhorar…</p>{lines(2)}
  </div>
</div>
''', station="3.1 · Imagens")

# ---------------------------------------------------------------- 12 POEM OF A CRAFT
REF = '<div style="padding-left:9mm;color:var(--sea);font-style:italic">Bate, bate, calceteiro,<br>que a cidade vai passar!<br>Pedra a pedra, dia inteiro,<br>desenhas ondas do mar.</div>'
REFs = '<div style="padding-left:9mm;color:var(--sea);font-style:italic">Bate, bate, calceteiro…</div>'
P[12] = page(12, f'''
<div class="abs" style="left:0;right:0;top:0;height:108mm"><img class="cover" src="img/calceteiro.jpg" style="object-position:50% 45%"></div>
<div class="abs" style="left:21mm;right:23.5mm;top:116mm;bottom:15mm">
  <div class="kicker sea">Estação 3.2 · O poema de um ofício</div>
  <div class="grid2" style="grid-template-columns:1.15fr 1fr;gap:8mm;margin-top:2mm">
    <div>
      <h2 style="font-size:22pt">Canção do calceteiro</h2>
      <div style="font-family:FrauncesText;font-size:10.4pt;line-height:1.42;margin-top:3mm;display:grid;gap:2.4mm">
        <div>De joelhos, cantarolando,<br>pedra a pedra, bate o martelo:<br>uma branca, uma preta, uma branca,<br>e o passeio vai ficando mais belo.</div>
        {REF}
        <div>Traz areia, traz o maço,<br>traz a corda e o esquadro,<br>traz paciência no braço<br>e um desenho bem pensado.</div>
        {REFs}
        <div>Passam botas, passam rodas,<br>passam noivos, passa a chuva,<br>passam meninos às voltas —<br>e ninguém repara na curva.</div>
        {REFs}
        <div>Mas quando a tarde se deita<br>e a praça fica calada,<br>a lua lê, satisfeita,<br>a onda que deixou desenhada.</div>
      </div>
      <p class="src" style="margin-top:2mm">Poema escrito para esta unidade.</p>
    </div>
    <div>
      <div class="rule-card c" style="font-size:9.3pt"><b class="sea">Refrão</b> — estrofe ou verso que se repete ao longo do poema. Dá ritmo e ajuda a memorizar: é a parte que todos cantam juntos.</div>
      <div class="rule-card c" style="margin-top:3mm;font-size:9.3pt"><b class="sea">Enumeração</b> — lista de elementos seguidos, separados por vírgulas: <i>Traz areia, traz o maço, traz a corda…</i></div>
      <div class="panel" style="margin-top:4mm;font-size:8.9pt;line-height:1.38">
        <div class="kicker">Sabias que…</div>
        <p style="margin-top:1.4mm">A <b>calçada portuguesa</b> faz-se à mão, pedra a pedra, com calcário branco e basalto negro. Desde 2021, a «Arte e Saber-Fazer da Calçada Portuguesa» está inscrita no <b>Inventário Nacional do Património Cultural Imaterial</b>.</p>
      </div>
      {act(1,"Descobrir", 'O verso 1 diz <i>cantarolando</i> e o verso 4 diz <i>vai ficando</i>. Que terminação têm estas palavras?'+lines(1),"sea")}
      {act(2,"Ouvir a rima", 'Que palavras rimam com <i>martelo</i>, <i>calceteiro</i> e <i>maço</i>?'+lines(2),"sea")}
    </div>
  </div>
</div>
''', station="3.2 · Ofício", bleed=True, rh=False)

# ---------------------------------------------------------------- 13 UNDERSTAND + DECLAIM
P[13] = page(13, f'''
<div class="kicker sea">Estação 3.2 · Compreender · Oralidade</div>
<h2 style="margin-top:2mm">Ritmo, repetição e <em>voz</em></h2>
<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>
{act(1,"Contar", 'Quantas estrofes tem o poema, contando com o refrão? Quantas vezes aparece o refrão?'+lines(1),"sea")}
{act(2,"Localizar", 'Transcreve as duas enumerações do poema.'+lines(2),"sea")}
{act(3,"Interpretar", 'Porque é que o calceteiro «desenha ondas do mar» num passeio da cidade? Pensa no padrão da calçada.'+lines(2),"sea")}
{act(4,"Inferir", 'Na última estrofe, ninguém está na praça. Quem «lê» o trabalho do calceteiro? O que nos diz isso sobre este ofício?'+lines(3),"sea")}
{act(5,"Relacionar", 'Encontra uma <b>personificação</b>: uma coisa que age como se fosse uma pessoa.'+lines(1),"sea")}
{act(6,"Continuar", 'Escreve mais uma estrofe de quatro versos para o poema, com uma <b>enumeração</b> de coisas que o calceteiro vê ao longo do dia.'+lines(4),"sea")}
</div>
<div>
  <div class="panel sea">
    <div class="kicker sea">Declamar em grupo</div>
    <ol style="margin:2.4mm 0 0 4.5mm;font-size:9.6pt;line-height:1.45">
      <li><b>Coro</b>: toda a turma diz o refrão.</li>
      <li><b>Solistas</b>: cada grupo diz uma estrofe.</li>
      <li>Marquem as <b>batidas</b>: batam com a mão na mesa nas sílabas fortes do refrão.<div style="font-family:FrauncesText;margin-top:1.4mm"><b>BA</b>-te, <b>BA</b>-te, cal-ce-<b>TEI</b>-ro</div></li>
      <li>Na enumeração, <b>acelerem</b> um pouco; na última estrofe, <b>abrandem</b>.</li>
      <li>Terminem em silêncio, três segundos, antes de agradecer.</li>
    </ol>
  </div>
  <div style="margin-top:5mm">
    <div class="kicker sea">Grelha de avaliação da turma</div>
    <table class="cmp" style="margin-top:2mm">
      <tr><th style="background:var(--sea)">Critério</th><th style="background:var(--sea);text-align:center;color:#fff"><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg></th><th style="background:var(--sea);text-align:center;color:#fff"><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg></th><th style="background:var(--sea);text-align:center;color:#fff"><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg><svg viewBox="0 0 20 20" style="width:3.4mm;height:3.4mm;vertical-align:-.5mm"><path d="M10 1.5l2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6L1.4 7.8l6-.7z" fill="currentColor"/></svg></th></tr>
      <tr><td>Dicção clara</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td></tr>
      <tr><td>Ritmo do refrão</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td></tr>
      <tr><td>Pausas e entoação</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td></tr>
      <tr><td>Olhar o público</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td></tr>
    </table>
  </div>
  <div class="panel" style="margin-top:5mm">
    <div class="kicker">Depois de declamar</div>
    <p class="small" style="margin-top:1.4mm">O que resultou melhor na nossa leitura? O que mudávamos numa próxima vez?</p>{lines(4)}
  </div>
</div>
</div>
''', station="3.2 · Ofício")

# ---------------------------------------------------------------- 14 GRAMMAR: GERUND + LIST COMMAS
P[14] = page(14, f'''
<div class="kicker sea">Estação 3.2 · Gramática</div>
<h2 style="margin-top:2mm">O gerúndio e as vírgulas da lista</h2>
<div class="grid2" style="margin-top:4mm;gap:6mm">
  <div class="panel sea">
    <div class="kicker sea">Gerúndio</div>
    <p style="margin-top:1.8mm;font-size:9.5pt">Forma do verbo terminada em <b>-ndo</b>. Mostra uma ação <b>a decorrer</b>.</p>
    <table class="cmp" style="margin-top:2.4mm;font-size:9pt">
      <tr><th style="background:var(--sea)">1.ª conj.</th><th style="background:var(--sea)">2.ª conj.</th><th style="background:var(--sea)">3.ª conj.</th></tr>
      <tr><td style="font-weight:400;color:var(--text)">cant<b>ando</b></td><td>bat<b>endo</b></td><td>part<b>indo</b></td></tr>
    </table>
    <p style="margin-top:2.4mm;font-size:9.2pt">Usa-se muito com <b>ir</b> e <b>estar</b>: <i>o passeio <b>vai ficando</b> mais belo</i>; <i>o calceteiro <b>está trabalhando</b></i> — no português de Portugal, dizemos mais vezes <i>está <b>a</b> trabalhar</i>.</p>
  </div>
  <div class="panel coral">
    <div class="kicker">Vírgulas na enumeração</div>
    <p style="margin-top:1.8mm;font-size:9.5pt">A vírgula separa os elementos de uma lista. Antes do último elemento, se houver <b>e</b>, <b>não</b> se põe vírgula.</p>
    <p style="margin-top:2mm;font-family:FrauncesText;font-size:10pt">Traz areia<b class="coral">,</b> o maço<b class="coral">,</b> a corda <b>e</b> o esquadro.</p>
    <p style="margin-top:2.4mm;font-size:9.2pt">Também se enumeram <b>ações</b>:</p>
    <p style="margin-top:1mm;font-family:FrauncesText;font-size:10pt">Mede<b class="coral">,</b> corta<b class="coral">,</b> alinhava <b>e</b> cose.</p>
    <p style="margin-top:2.4mm;font-size:9.2pt">A vírgula <b>nunca</b> separa o sujeito do verbo: <s style="color:var(--coral)">O calceteiro, bate</s> <i>O calceteiro bate.</i></p>
  </div>
</div>
{act(1,"Formar", 'Escreve o gerúndio.<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.6mm 6mm;margin-top:2mm;font-size:9.6pt"><div>martelar → <span class="fill"></span></div><div>correr → <span class="fill"></span></div><div>sorrir → <span class="fill"></span></div><div>pôr → <span class="fill"></span></div><div>ver → <span class="fill"></span></div><div>ir → <span class="fill"></span></div></div>',"sea")}
{act(2,"Transformar", 'Reescreve com <b>ir + gerúndio</b>, para mostrar que a ação avança aos poucos.<div style="display:flex;gap:4mm;align-items:baseline;margin-top:2.4mm;font-size:9.6pt"><i style="width:50mm;flex:none">a) A praça fica desenhada.</i><span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div><div style="display:flex;gap:4mm;align-items:baseline;margin-top:4mm;font-size:9.6pt"><i style="width:50mm;flex:none">b) A noite cai sobre a cidade.</i><span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div>',"sea")}
{act(3,"Pontuar", 'Coloca as vírgulas que faltam.<div style="font-family:FrauncesText;font-size:10.2pt;line-height:1.7;margin-top:1.6mm">Na mochila do pescador há redes anzóis uma faca e um termo de café.<br>O padeiro amassa tende coze e vende o pão antes de o sol nascer.</div>')}
{act(4,"Escrever", 'Escreve uma enumeração com <b>quatro</b> gestos de um ofício à tua escolha, usando o gerúndio. <span class="small muted">Ex.: A costureira passa a manhã medindo, cortando, alinhavando e cosendo.</span>'+lines(2),"sea")}
<div class="panel coral" style="margin-top:auto">
{act(5,"Corrigir", 'Cada frase tem <b>um</b> erro de pontuação na enumeração. Reescreve-as corretamente.<div style="font-family:FrauncesText;font-size:10pt;line-height:1.6;margin-top:1.4mm">Comprei pão, leite, e fruta.<br>O pescador, lança a rede, puxa os cabos e arruma o barco.</div>'+lines(2))}
</div>
''', station="3.2 · Ofício")

# ---------------------------------------------------------------- 15 CLASS POEM
steps = [("1","Votar o ofício","Façam uma lista de ofícios da vossa terra e votem num."),
         ("2","Banco de palavras","ferramentas&nbsp;· gestos (em gerúndio)&nbsp;· lugares&nbsp;· sons"),
         ("3","O refrão","Escrevam juntos quatro versos que todos consigam cantar."),
         ("4","As estrofes","Cada grupo escreve uma estrofe com uma enumeração."),
         ("5","Montar e declamar","Intercalem o refrão entre as estrofes e declamem.")]
steph = "".join(f'<div style="border-top:1.2mm solid var(--sea);padding-top:2mm"><div class="display" style="font-size:18pt;color:var(--sea);line-height:1">{n}</div><div style="font-weight:700;color:var(--ink);font-size:9.6pt;margin-top:1mm">{t}</div><div class="small muted" style="margin-top:.6mm">{d}</div></div>' for n,t,d in steps)
bank = "".join(f'<div class="panel" style="padding:3mm"><div class="kicker sea">{k}</div><div class="lines"><i></i><i></i><i></i><i></i></div></div>' for k in ["Ferramentas","Gestos (-ndo)","Lugares","Sons"])
P[15] = page(15, f'''
<div class="kicker sea">Estação 3.2 · Escrita coletiva</div>
<h2 style="margin-top:2mm">O poema do <em>nosso</em> ofício</h2>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3mm;margin-top:4mm">{steph}</div>
<div style="display:flex;gap:3mm;align-items:flex-end;margin-top:6mm"><b class="blue" style="white-space:nowrap">O ofício escolhido pela turma:</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4"></span></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:4mm">{bank}</div>
<div class="grid2" style="margin-top:5mm;gap:6mm">
  <div class="panel sea"><div class="kicker sea">O nosso refrão</div>{lines(5)}</div>
  <div class="panel"><div class="kicker">A estrofe do meu grupo</div>{lines(5)}</div>
</div>
<div class="grid2" style="margin-top:5mm;gap:6mm;grid-template-columns:1.3fr 1fr">
  <div class="panel" style="padding:3.4mm 4mm"><div class="kicker">Ensaio da declamação</div><div style="display:grid;grid-template-columns:auto 1fr;gap:1.8mm 3mm;margin-top:1.8mm;align-items:end;font-size:9pt"><span>Diz o refrão:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span>1.ª estrofe:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span>2.ª estrofe:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span><span>Bate o ritmo:</span><span style="border-bottom:.6pt solid #AEB7C4;height:5.5mm"></span></div></div>
  <div class="panel sea" style="padding:3.4mm 4mm;display:flex;flex-direction:column"><div class="kicker sea">Sabias que?</div><p class="small" style="margin-top:1.2mm;line-height:1.4">A arte da calçada portuguesa (p. 12) está no Inventário Nacional do Património Cultural Imaterial desde 2021.</p><div style="margin-top:auto;padding-top:2mm">{qr("q-calcada", "Verificar", "O anúncio no Diário da República.")}</div></div>
</div>
<div class="grid2" style="margin-top:5mm;gap:6mm">
  <div><b class="blue" style="font-size:9.6pt">Título do poema</b>{lines(1)}</div>
  <div><b class="blue" style="font-size:9.6pt">Onde e para quem o vamos declamar?</b>{lines(1)}</div>
</div>
<div style="display:flex;gap:5mm;flex-wrap:wrap;margin-top:auto;font-size:8.8pt;border-top:.6pt solid var(--rule);padding-top:3mm">
  <span><span class="chk"></span>o refrão repete-se igual</span><span><span class="chk"></span>cada estrofe tem uma enumeração</span><span><span class="chk"></span>vírgulas certas na lista</span><span><span class="chk"></span>pelo menos 2 gerúndios</span><span><span class="chk"></span>título escolhido pela turma</span>
</div>
''', station="3.2 · Ofício")

# ---------------------------------------------------------------- 16 CHECK YOURSELF
cando = ["Identifico personagens, ausência e reconhecimento num romance tradicional.","Leio em voz alta com pausas e entoação.","Resumo um poema em prosa, em parágrafos.","Distingo verso, estrofe e rima.","Distingo metáfora de comparação e crio as minhas.","Uso refrão e enumeração num poema.","Uso formas de tratamento, advérbios de modo, particípio e gerúndio."]
ch = "".join(f'<tr><td style="font-weight:400;color:var(--text);width:auto">{c}</td><td style="text-align:center;width:12mm"><span class="chk"></span></td><td style="text-align:center;width:12mm"><span class="chk"></span></td><td style="text-align:center;width:12mm"><span class="chk o"></span></td></tr>' for c in cando)
P[16] = page(16, f'''
<div class="kicker">Chegada</div>
<h2 style="margin-top:2mm">Consegues?</h2>
<div class="panel" style="margin-top:4mm;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-family:FrauncesText;font-size:10.4pt;line-height:1.45">
  <div>— «Ó moço da barca negra,<br>que trazes do mar salgado?»<br>— «Trago redes e saudade,<br>e um peixe todo prateado.»</div>
  <div>A tarde é um lenço azul<br>que o vento leva devagar;<br>a vila, como um barco,<br>adormece junto ao mar.</div>
</div>
<p class="src" style="margin-top:1.4mm">Estrofes escritas para esta revisão.</p>
<div class="grid2" style="margin-top:1mm;gap:7mm">
<div>
{act(1,"Classificar", 'A estrofe da esquerda tem <span class="fill s"></span> versos e chama-se <span class="fill"></span>. <br>Tem diálogo? <span class="fill s"></span> Quem fala? <span class="fill"></span>')}
{act(2,"Identificar", 'Na estrofe da direita, copia uma <b class="coral">metáfora</b> e uma <b class="blue">comparação</b>.'+lines(3))}
{act(3,"Gramática", 'Encontra um advérbio de modo, um particípio passado e uma forma de tratamento nas duas estrofes.'+lines(3))}
</div>
<div>
{act(4,"Escrever", 'Passa a estrofe da esquerda para prosa, sem usar o travessão.'+lines(4))}
{act(5,"Criar", 'Escreve um refrão de dois versos para um poema sobre o pescador.'+lines(2))}
{act(6,"Usar", 'Escreve uma frase sobre a vila com um <b>gerúndio</b> e uma <b>enumeração</b>.'+lines(2))}
</div>
</div>
<div class="kicker blue" style="margin-top:5mm">Autoavaliação</div>
<table class="cmp" style="margin-top:2mm"><tr><th style="background:var(--ink)">Consigo…</th><th style="background:var(--ink);text-align:center">Sim</th><th style="background:var(--ink);text-align:center">Quase</th><th style="background:var(--coral);text-align:center">Ainda não</th></tr>{ch}</table>
''', station="Chegada")
