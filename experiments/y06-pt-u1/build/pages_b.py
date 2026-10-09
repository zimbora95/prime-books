import re
import parts
from parts import *
parts.UNIT.update(n=1, total=28)

P = {}
U = lambda h=6: f'<span style="display:block;border-bottom:.6pt solid #AEB7C4;height:{h}mm"></span>'

def para(n, html):
    return (f'<p style="position:relative"><span style="position:absolute;left:-7.5mm;top:.2mm;width:5mm;height:5mm;border-radius:50%;'
            f'background:var(--ink);color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{n}</span>{html}</p>')

def pg(n, body, station):
    return page(n, body, station=station, cls="flex")

# ---------------------------------------------------------------- 8 STATION 2 — the text that delights (before reading)
feat = [("Um título que desperta curiosidade", "muitas vezes com uma pergunta ou um jogo de palavras"),
        ("Perguntas ao leitor", "«Sabias que…?», «Imagina que…»"),
        ("Comparações com o dia a dia", "«mais comprido do que uma porta»"),
        ("Factos e números verdadeiros", "tal como no texto expositivo"),
        ("Linguagem viva", "frases curtas, exclamações, intertítulos")]
fh = "".join(f'<div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2.2mm"><b class="display blue" style="font-size:13pt;line-height:1">{i}</b><div style="font-size:9.2pt;line-height:1.35"><b class="blue">{a}</b><br><span class="muted">{b}</span></div></div>' for i, (a, b) in enumerate(feat, 1))
P[8] = pg(8, f'''
<div class="abs" style="left:0;right:0;top:0;height:84mm"><img class="cover" src="img/golfinhos.jpg"></div>
<div style="height:90mm"></div>
<div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div><div class="kicker blue">Estação 2 · O texto que encanta</div><h2 style="margin-top:2mm">Ciência para toda a gente</h2></div>
  <div>{LUPA.replace('class="ico"','class="ico" style="width:14mm;height:14mm"')}</div>
</div>
<p class="lead" style="margin-top:2.6mm;font-size:10.8pt">O <b>texto de divulgação</b> também informa com rigor — mas escreve para leitores que não são especialistas e quer que eles fiquem com <b>vontade de saber mais</b>. Por isso, usa truques para prender a atenção.</p>
<div class="grid2" style="grid-template-columns:1.1fr 1fr;gap:7mm;margin-top:3mm;align-items:start">
  <div class="panel blue" style="padding:3.6mm 4mm"><div class="kicker blue">Os truques da divulgação</div>{fh}</div>
  <div>
    {act(1, "Prever", 'O texto seguinte chama-se <b>«Os vizinhos do canhão»</b>. Quem achas que são estes «vizinhos»?' + lines(2), "blue")}
    {act(2, "Ativar", 'Escreve duas coisas que já sabes sobre golfinhos.' + lines(2), "blue")}
    {act(3, "Ler com um objetivo", 'Enquanto lês, sublinha a lápis <b>cada truque</b> da caixa azul que encontrares e escreve o seu número na margem.', "blue")}
    {act(4, "Vocabulário", 'O que achas que quer dizer <b>cetáceo</b>? Escreve a tua ideia e confirma-a no glossário da página 9.' + lines(2), "blue")}
  </div>
</div>
''', "Est. 2 · Encantar")

# ---------------------------------------------------------------- 9 TEXT 2 — popular science
P[9] = pg(9, f'''
<div style="display:grid;grid-template-columns:1fr 46mm;gap:7mm;flex:1">
<div>
  <div class="kicker blue">Texto 2 · Texto de divulgação</div>
  <h2 style="margin-top:2mm;font-size:27pt">Os vizinhos do canhão</h2>
  <p style="font-family:FrauncesText;font-style:italic;font-size:11.4pt;line-height:1.45;color:var(--ink);margin-top:2mm">Por baixo das ondas mais famosas do mundo, vive gente — quer dizer, vivem golfinhos. Vem conhecê-los.</p>
  <div class="reading" style="margin-top:3.4mm;padding-left:7.5mm;font-size:10.3pt;line-height:1.52">
  {para(1, 'Imagina que estás num barco, ao largo da Nazaré. De repente, uma barbatana corta a água. Depois outra. E mais outra! Não, não são tubarões: é um grupo de golfinhos. Aqui, há empresas que organizam passeios só para os observar.')}
  <h3 style="font-size:11pt;margin-top:3mm">Uma em cada quatro</h3>
  {para(2, 'Nas águas portuguesas vivem mais de 20 espécies de <b>cetáceos</b>, o grupo de mamíferos marinhos a que pertencem os golfinhos, as baleias e os cachalotes. No mundo inteiro, conhecem-se cerca de 80. Ou seja: cerca de uma em cada quatro espécies do planeta pode ser vista no nosso mar!')}
  {para(3, 'Um dos mais frequentes é o golfinho-comum. Pode atingir 2,3 metros — é mais comprido do que a altura de uma porta! — e vive em grupos. Como todos os golfinhos, orienta-se pelo som: emite estalidos e escuta o eco que regressa. Chama-se a isto <b>ecolocalização</b>.')}
  <h3 style="font-size:11pt;margin-top:3mm">Um bilhete de identidade nas costas</h3>
  {para(4, 'Sabias que os cientistas conseguem reconhecer cada golfinho? Fotografam a <b>barbatana dorsal</b>, a que fica nas costas: os cortes e as marcas de cada uma são únicos, como uma impressão digital.')}
  {para(5, 'Assim, descobriram que as famílias são muito unidas. As mães têm uma cria de cada vez e cuidam dela durante vários anos. No estuário do Sado, vive uma comunidade de golfinhos-roazes que, em 2023, teve seis crias e chegou aos 30 animais.')}
  <h3 style="font-size:11pt;margin-top:3mm">Vizinhos em perigo</h3>
  {para(6, 'Nem tudo são boas notícias. O ruído dos barcos e as redes de pesca, onde alguns golfinhos ficam presos por acidente, são grandes ameaças. Da próxima vez que olhares para o mar da Nazaré, lembra-te: por baixo das ondas, há vizinhos que precisam do nosso respeito.')}
  </div>
  <p class="src" style="margin-top:2.6mm;padding-left:7.5mm">Texto criado para esta unidade, com base em informação do MARE — Centro de Ciências do Mar e do Ambiente, do ICNF (via <i>Expresso</i>, 20/12/2023) e da SECEM.</p>
</div>
<aside style="border-left:.6pt solid var(--rule);padding-left:5mm;display:flex;flex-direction:column">
  <div class="kicker blue" style="margin-top:12mm">Glossário</div>
  <dl class="gloss" style="margin-top:2.4mm">
    <dt>cetáceo</dt><dd>mamífero que vive sempre no mar, como o golfinho e a baleia; respira ar à superfície.</dd>
    <dt>ecolocalização</dt><dd>orientação através do eco dos sons emitidos pelo próprio animal.</dd>
    <dt>barbatana dorsal</dt><dd>barbatana situada nas costas do animal.</dd>
    <dt>estuário</dt><dd>zona onde um rio se encontra com o mar.</dd>
    <dt>roaz</dt><dd>espécie de golfinho de grande porte, cinzento, comum no Sado.</dd>
  </dl>
  <div class="panel" style="padding:3mm 3.4mm;margin-top:2mm">
    <div class="kicker blue">Em números</div>
    <div style="border-top:.6pt solid var(--rule);padding:1.4mm 0;margin-top:1.4mm"><div class="display" style="font-size:15pt;line-height:1;color:var(--ink)">+ 20</div><div class="small muted">espécies de cetáceos em Portugal</div></div>
    <div style="border-top:.6pt solid var(--rule);padding:1.4mm 0"><div class="display" style="font-size:15pt;line-height:1;color:var(--ink)">2,3 m</div><div class="small muted">comprimento máximo do golfinho-comum</div></div>
    <div style="border-top:.6pt solid var(--rule);padding:1.4mm 0"><div class="display" style="font-size:15pt;line-height:1;color:var(--ink)">30</div><div class="small muted">roazes residentes no Sado (2023)</div></div>
  </div>
  <div style="margin-top:auto">{qr("q-cetaceos", "Ouvir os cientistas", "Os cetáceos em Portugal, segundo o MARE.")}</div>
</aside>
</div>
''', "Est. 2 · Encantar")

# ---------------------------------------------------------------- 10 COMPREHENSION + COMPARE
cmp_rows = [("Para quem escreve?", ""), ("Qual é a intenção?", ""), ("Título", "«O Canhão da Nazaré»"),
            ("Faz perguntas ao leitor?", ""), ("Usa comparações?", ""), ("Apresenta factos e números?", "")]
ct = "".join(f'<tr><td style="font-size:9pt">{a}</td><td style="font-weight:400;font-size:8.8pt;height:12.5mm">{b}</td><td></td></tr>' for a, b in cmp_rows)
P[10] = pg(10, f'''
<div class="kicker blue">Texto 2 · Compreender</div>
<h2 style="margin-top:2mm">Informar a explicar, informar a encantar</h2>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:7mm;margin-top:2mm">
<div>
{act(1, "Localizar", 'Quantas espécies de cetáceos se conhecem no mundo? E em Portugal?' + lines(2), "blue")}
{act(2, "Explicar", 'Como é que os cientistas reconhecem cada golfinho? Explica por palavras tuas.' + lines(3), "blue")}
{act(3, "Vocabulário", 'No parágrafo 3, a palavra <b>ecolocalização</b> é explicada no próprio texto. Copia a explicação.' + lines(2), "blue")}
</div>
<div>
{act(4, "Truques", 'Copia do texto um exemplo de cada truque.<div style="display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;margin-top:1.6mm;font-size:9pt;align-items:end"><span>pergunta ao leitor:</span>' + U(5) + '<span>comparação:</span>' + U(5) + '<span>exclamação:</span>' + U(5) + '<span>intertítulo:</span>' + U(5) + '</div>', "blue")}
{act(5, "Pensar", 'A última frase do texto tem uma opinião? Porque achas que o autor a escreveu?' + lines(3), "blue")}
</div>
</div>
<h3 style="margin-top:4mm">Frente a frente: Texto 1 e Texto 2</h3>
<table class="cmp ruled" style="margin-top:1.6mm">
  <tr><th style="background:var(--ink)"></th><th style="background:var(--ink)">Texto 1 · expositivo</th><th style="background:var(--ink)">Texto 2 · divulgação</th></tr>
  {ct}
</table>
<div style="margin-top:auto">{act(6, "Concluir", 'Completa: <i>Os dois textos querem que o leitor ______________, mas o Texto 2 também quer que o leitor ______________.</i>', "blue")}</div>
''', "Est. 2 · Encantar")

# ---------------------------------------------------------------- 11 STATION 3 — the text that asks (before reading)
qtypes = [("Pergunta fechada", "responde-se com poucas palavras", "«Há quantos anos estuda o canhão?»"),
          ("Pergunta aberta", "pede uma explicação ou uma opinião", "«Porque é que escolheu esta profissão?»")]
qt = "".join(f'<div class="rule-card{" o" if i else ""}" style="font-size:9.2pt;line-height:1.45"><b class="{"coral" if i else "blue"}">{a}</b> — {b}.<div style="font-family:FrauncesText;font-style:italic;margin-top:1.2mm">{c}</div></div>' for i, (a, b, c) in enumerate(qtypes))
struct = [("Título", "muitas vezes, uma frase marcante do entrevistado"), ("Introdução", "apresenta a pessoa: quem é, o que faz, porque vale a pena ouvi-la"),
          ("Perguntas e respostas", "a pergunta do entrevistador destaca-se (a negrito ou com o nome); a resposta vem a seguir"),
          ("Fecho", "a última pergunta e, por vezes, um agradecimento")]
sh = "".join(f'<div style="display:grid;grid-template-columns:34mm 1fr;gap:3mm;padding:2mm 0;border-top:.6pt solid var(--rule);font-size:9.2pt;line-height:1.35"><b class="blue">{a}</b><span>{b}</span></div>' for a, b in struct)
P[11] = pg(11, f'''
<div style="display:grid;grid-template-columns:1fr 70mm;gap:7mm;align-items:start">
  <div>
    <div class="kicker blue">Estação 3 · O texto que pergunta</div>
    <h2 style="margin-top:2mm">Conhecer alguém<br>através de perguntas</h2>
    <p class="lead" style="margin-top:3mm;font-size:10.8pt">Numa <b>entrevista</b>, um <b>entrevistador</b> faz perguntas a um <b>entrevistado</b> — alguém que sabe muito sobre um assunto ou que viveu algo especial. O leitor fica a conhecer a pessoa e aquilo que ela sabe, pelas suas próprias palavras.</p>
  </div>
  <div style="height:62mm;border-radius:2.4mm;overflow:hidden"><img class="cover" src="img/oceanografa.jpg"></div>
</div>
<h3 style="margin-top:5mm">Como se organiza uma entrevista escrita</h3>
<div style="margin-top:1.4mm;border-bottom:.6pt solid var(--rule)">{sh}</div>
<h3 style="margin-top:5mm">Dois tipos de pergunta</h3>
<div class="grid2" style="margin-top:2mm;gap:5mm">{qt}</div>
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(1, "Prever", 'Vais ler uma entrevista a uma <b>oceanógrafa</b>. O que achas que faz uma oceanógrafa?' + lines(2), "blue")}</div>
  <div>{act(2, "Perguntar", 'Se pudesses entrevistá-la, que pergunta lhe farias primeiro? É aberta ou fechada?' + lines(2), "blue")}</div>
</div>
<div style="margin-top:3mm">{act(3, "Transformar", 'Transforma estas perguntas fechadas em perguntas abertas: <i>«Gosta do mar?»</i> · <i>«O canhão é fundo?»</i>' + lines(3), "blue")}</div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center">
  <div class="kicker blue" style="max-width:30mm">Enquanto lês</div>
  <div style="font-size:9.4pt">Marca com <b class="blue">F</b> as perguntas fechadas e com <b class="coral">A</b> as perguntas abertas. No fim, conta-as: qual é o tipo mais usado? Porquê?</div>
</div>
''', "Est. 3 · Perguntar")

# ---------------------------------------------------------------- 12–13 TEXT 3 — interview (model, fictional interviewee)
def qa(q, a):
    return (f'<div style="margin-top:3mm"><p style="font-family:Body;font-weight:700;color:var(--ink);font-size:9.8pt;line-height:1.4">{q}</p>'
            f'<p style="margin-top:1mm">{a}</p></div>')
P[12] = pg(12, f'''
<div class="kicker blue">Texto 3 · Entrevista</div>
<h2 style="margin-top:2mm;font-size:25pt">«O mar da Nazaré guarda um segredo no fundo»</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:3.6mm;flex:1">
<div class="reading" style="font-size:10.2pt;line-height:1.52">
  <p style="font-family:Body;font-size:9.6pt;line-height:1.45;color:var(--ink)"><b>Inês Carvalho é oceanógrafa: estuda o mar, as ondas e o fundo do oceano. Passou os últimos anos a observar o Canhão da Nazaré. O Rui Matos, do 6.º B, entrevistou-a para o jornal da escola, <i>O Farol</i>.</b></p>
  {qa('Rui Matos — O que faz, exatamente, uma oceanógrafa?', 'Inês Carvalho — Tenta perceber como funciona o oceano. Há oceanógrafos que estudam os animais, outros a química da água. Eu estudo as ondas e a forma do fundo do mar — e a Nazaré é um laboratório perfeito!')}
  {qa('Porquê perfeito?', 'Por causa do canhão. É um vale submarino com mais de cinco mil metros de profundidade, e começa a menos de um quilómetro da praia. Quase não há sítios assim no mundo. É por causa dele que se formam as ondas gigantes.')}
  {qa('Mas como é que se estuda uma coisa que não se vê?', 'Com instrumentos! Os barcos de investigação enviam sons para o fundo e medem quanto tempo demora o eco a voltar. Quanto mais tempo, mais fundo. É parecido com o que fazem os golfinhos.')}
</div>
<div class="reading" style="font-size:10.2pt;line-height:1.52">
  {qa('Os golfinhos?', 'Sim! Eles orientam-se pelo eco dos sons que emitem. Nós copiámos a ideia. Às vezes, quando estamos no mar a trabalhar, aparecem grupos de golfinhos a nadar ao lado do barco. É o melhor momento do dia.')}
  {qa('É possível saber quando vai haver uma onda gigante?', 'Com alguns dias de antecedência, sim. O Instituto Hidrográfico usa modelos de computador que juntam a informação das tempestades no Atlântico com a forma do fundo. Assim, os surfistas, os pescadores e as autoridades sabem quando o mar vai estar perigoso.')}
  <div style="margin-top:4mm;height:52mm;border-radius:2.4mm;overflow:hidden"><img class="cover" src="img/canhao.jpg"></div>
</div>
</div>
''', "Est. 3 · Perguntar")

P[13] = pg(13, f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:7mm">
<div class="reading" style="font-size:10.2pt;line-height:1.52">
  {qa('Qual foi a coisa mais surpreendente que descobriu?', 'Que o fundo do mar muda! As tempestades arrastam areia e lama pelo canhão abaixo, como se fosse um escorrega gigante. O fundo que mapeámos num ano pode estar diferente no ano seguinte.')}
  {qa('Tem medo das ondas?', 'Tenho respeito, que é diferente. Quem conhece o mar sabe que ele é mais forte do que nós. Por isso, nunca vou para o mar sem consultar a previsão e sem avisar alguém.')}
  {qa('Sempre quis ser oceanógrafa?', 'Não! Aos onze anos, queria ser veterinária. Mas, numa visita de estudo a um navio de investigação, vi pela primeira vez um mapa do fundo do mar. Nunca mais me esqueci.')}
</div>
<div class="reading" style="font-size:10.2pt;line-height:1.52">
  {qa('Que conselho dá a um aluno do 6.º ano que queira seguir esta profissão?', 'Que faça muitas perguntas — como tu estás a fazer agora! E que goste de Matemática, de Ciências… e de Português. Um cientista passa muito tempo a escrever: se não conseguirmos explicar o que descobrimos, é como se não tivéssemos descoberto nada.')}
  {qa('Obrigado pela entrevista.', 'Obrigada eu. E, da próxima vez que fores à Nazaré, olha para o mar e lembra-te do que está lá em baixo.')}
</div>
</div>
<div class="panel" style="margin-top:5mm;display:grid;grid-template-columns:1fr auto;gap:6mm;align-items:center">
  <div style="font-size:9pt;line-height:1.45"><b class="blue">Nota.</b> Entrevista-modelo escrita para esta unidade: Inês Carvalho e Rui Matos são personagens fictícias. As informações científicas foram confirmadas junto do Instituto Hidrográfico e da Nazaré Qualifica, e estão de acordo com o Texto 1 (p. 6).</div>
  <div style="display:grid;gap:3mm">{qr("q-hidro", "Verificar", "O Instituto Hidrográfico e a Praia do Norte.")}{qr("q-ondas", "Explorar", "Como o canhão cria as ondas.")}</div>
</div>
<div class="grid2" style="margin-top:5mm;gap:7mm">
  <div>{act(1, "Contar", 'Quantas perguntas abertas e quantas fechadas encontraste? Qual é o tipo mais usado e porquê?' + lines(5), "blue")}</div>
  <div>{act(2, "Reagir", 'Que resposta da Inês te surpreendeu mais? Porquê?' + lines(5), "blue")}</div>
</div>
<div style="margin-top:auto">{act(3, "Ligar", 'A Inês fala dos golfinhos. Que informação do <b>Texto 2</b> confirma o que ela diz?' + lines(2), "blue")}</div>
''', "Est. 3 · Perguntar")

# ---------------------------------------------------------------- 14 INTERVIEW — comprehension & structure
P[14] = pg(14, f'''
<div class="kicker blue">Texto 3 · Compreender</div>
<h2 style="margin-top:2mm">Por dentro de uma entrevista</h2>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:7mm;margin-top:2mm">
<div>
{act(1, "Identificar", 'Quem é o entrevistador? E a entrevistada? Onde vai ser publicada a entrevista?' + lines(3), "blue")}
{act(2, "Localizar", 'Onde está a <b>introdução</b>? Que três informações nos dá sobre a entrevistada?' + lines(3), "blue")}
{act(3, "Explicar", 'Porque é que a Inês diz que a Nazaré é «um laboratório perfeito»?' + lines(3), "blue")}
</div>
<div>
{act(4, "Comparar", 'Qual é a semelhança entre o trabalho dos barcos de investigação e a ecolocalização dos golfinhos?' + lines(3), "blue")}
{act(5, "Distinguir", 'Encontra na entrevista um <b>facto</b> e uma <b>opinião</b> da Inês.<div style="display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;margin-top:1.6mm;align-items:end;font-size:9pt"><span>facto:</span>' + U(5) + '<span></span>' + U(5) + '<span>opinião:</span>' + U(5) + '<span></span>' + U(5) + '</div>', "blue")}
</div>
</div>
<h3 style="margin-top:4.6mm">A pontuação da entrevista</h3>
<div class="grid2" style="margin-top:1.6mm;gap:5mm">
  <div class="rule-card" style="font-size:9.2pt;line-height:1.5">Na entrevista escrita, cada fala começa numa <b>linha nova</b>. O nome de quem fala aparece na primeira pergunta e na primeira resposta, seguido de <b>travessão</b>; depois, a diferença de letra (negrito) basta para o leitor saber quem fala.</div>
  <div class="rule-card o" style="font-size:9.2pt;line-height:1.5">As perguntas terminam com <b>ponto de interrogação</b>. As respostas usam a <b>1.ª pessoa</b> («eu estudo», «nós copiámos»), porque é o entrevistado a falar.</div>
</div>
<div style="margin-top:3mm">{act(6, "Criar", 'Escreve uma pergunta <b>aberta</b> e uma pergunta <b>fechada</b> que o Rui podia ter feito à Inês.' + lines(3), "blue")}</div>
<div style="margin-top:auto">{act(7, "Transformar", 'Esta pergunta está escrita de forma indireta. Reescreve-a como pergunta de entrevista: <i>O Rui quis saber se a Inês alguma vez tinha visto uma onda gigante.</i>' + lines(2), "blue")}</div>
''', "Est. 3 · Perguntar")

# ---------------------------------------------------------------- 15 WRITING — six-question interview
six = "".join(f'''<div style="display:grid;grid-template-columns:8mm 1fr 19mm;gap:2.4mm;align-items:end;margin-top:2.2mm">
  <b class="display blue" style="font-size:14pt;line-height:1;align-self:start;padding-top:2mm">{i}</b><span>{U(6.5)}{U(6.5)}</span>
  <span style="display:flex;gap:1.4mm;align-items:center;font-size:8pt" class="muted"><span class="chk"></span>A<span class="chk o"></span>F</span></div>''' for i in range(1, 7))
P[15] = pg(15, f'''
<div style="display:flex;gap:4mm;align-items:center">{LAPIS}<div><div class="kicker blue">Estação 3 · Escrever</div><h2 style="margin-top:1mm">Seis perguntas para alguém especial</h2></div></div>
<p class="lead" style="margin-top:2.6mm;font-size:10.6pt">Vais preparar uma entrevista de <b>seis perguntas</b> a uma pessoa da tua família, da escola ou da tua terra que saiba muito sobre um assunto ligado ao mar, à natureza ou a uma profissão.</p>
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:3mm">
  <div class="panel blue" style="padding:3.4mm 4mm"><div class="kicker blue">1 · Quem vou entrevistar?</div>
    <div style="display:grid;grid-template-columns:auto 1fr;gap:1.6mm 3mm;margin-top:1.6mm;align-items:end;font-size:9pt"><span>Nome:</span>{U(5)}<span>O que faz:</span>{U(5)}<span>Porque escolhi:</span>{U(5)}</div></div>
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">2 · O que quero descobrir?</div>
    <p class="small" style="margin-top:1.2mm">O objetivo da entrevista, numa frase.</p>{U(6)}{U(6)}</div>
</div>
<h3 style="margin-top:4mm">3 · As minhas seis perguntas <span class="small muted" style="font-family:Body;font-weight:400">— assinala se é aberta (A) ou fechada (F)</span></h3>
{six}
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:4mm">
  <div class="panel" style="padding:3.4mm 4mm"><div class="kicker">4 · Introdução</div><p class="small" style="margin-top:1.2mm">Três frases que apresentem o entrevistado ao leitor.</p>{U(6)}{U(6)}{U(6)}</div>
  <div class="panel" style="padding:3.4mm 4mm;font-size:9pt;line-height:1.55"><div class="kicker">Antes de entrevistar, verifica</div>
    <div style="display:grid;grid-template-columns:5mm 1fr;gap:.8mm 2mm;margin-top:1.4mm">
      <span class="chk"></span><span>Tenho pelo menos <b>quatro</b> perguntas abertas.</span>
      <span class="chk"></span><span>A primeira pergunta é fácil e acolhedora.</span>
      <span class="chk"></span><span>A última pergunta fecha a conversa.</span>
      <span class="chk"></span><span>Nenhuma pergunta se repete.</span>
      <span class="chk"></span><span>Pedi autorização para publicar.</span></div></div>
</div>
<div class="panel blue" style="margin-top:4mm;padding:3.4mm 4mm"><div class="kicker blue">5 · Durante a entrevista</div>
  <div style="font-size:9pt;line-height:1.5;margin-top:1.2mm">Toma notas com <b>palavras-chave</b> ou, com autorização, grava a conversa. Se uma resposta te surpreender, faz uma <b>pergunta extra</b>: escreve-a aqui.</div>{U(6.5)}{U(6.5)}</div>
<div style="margin-top:auto" class="rule-card o"><b class="coral">Depois da entrevista:</b> passa as respostas a limpo, com a pontuação da página 14, e lê-as ao entrevistado antes de as publicares no jornal da turma.</div>
''', "Est. 3 · Perguntar")

# ---------------------------------------------------------------- 16–17 STATION 4 — two opinion columns
def col(body):
    ps = re.findall(r"<p>(.*?)</p>", body, re.S)
    rows = "".join(f'''<div style="display:grid;grid-template-columns:1fr 36mm;gap:5mm;margin-top:{'0' if i == 0 else '2.6mm'}">
  <p style="position:relative;padding-left:7.5mm"><span style="position:absolute;left:0;top:.3mm;width:5mm;height:5mm;border-radius:50%;background:var(--coral);color:#fff;font-family:Grotesk;font-weight:700;font-size:7pt;line-height:5mm;text-align:center">{i+1}</span>{t}</p>
  <div style="border-left:.6pt solid var(--rule);padding-left:3mm;align-self:stretch"><div style="font-family:Grotesk;font-size:6.8pt;letter-spacing:.1em;color:var(--muted);text-transform:uppercase">Parágrafo {i+1} é…</div><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div>
</div>''' for i, t in enumerate(ps))
    return f'<div class="reading" style="font-size:11.2pt;line-height:1.62">{rows}</div>'
P[16] = pg(16, f'''
<div style="display:flex;justify-content:space-between;align-items:flex-start">
  <div><div class="kicker">Estação 4 · O texto que defende</div><h2 style="margin-top:2mm">Duas opiniões, o mesmo mar</h2></div>
  <div>{MEGA.replace('class="ico"','class="ico" style="width:15mm;height:15mm"')}</div>
</div>
<div class="panel coral" style="margin-top:3mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:3.4mm 4mm">
  <div class="kicker" style="max-width:26mm">Antes de ler</div>
  <div style="font-size:9.6pt">Os golfinhos devem viver em parques aquáticos? Escreve <b>sim</b>, <b>não</b> ou <b>depende</b> — e guarda a tua resposta para o fim.<div style="display:inline-block;width:30mm;border-bottom:.6pt solid #AEB7C4;margin-left:2mm"></div></div>
</div>
<div class="kicker" style="margin-top:5mm">Texto 4A · Texto de opinião</div>
<h3 style="font-size:17pt;margin-top:1.4mm">Um golfinho não cabe num tanque</h3>
<p class="small muted" style="margin-top:.6mm;margin-bottom:3mm">por Clara Santos, 6.º A · <span class="coral">Na margem, escreve: tese, argumento, exemplo, contra-argumento ou conclusão.</span></p>
{col('''<p>Na minha opinião, os golfinhos não devem viver em cativeiro, nem em parques aquáticos nem em nenhum outro lugar fechado.</p>
<p>Em primeiro lugar, os golfinhos são animais do mar aberto. No oceano, nadam longas distâncias, mergulham fundo e vivem em grupos familiares. Os cientistas do MARE explicam que as mães cuidam de cada cria durante vários anos. Um tanque, por maior que seja, nunca poderá ser o oceano.</p>
<p>Além disso, não precisamos de os fechar para os conhecer. Ao largo da Nazaré e no estuário do Sado, há passeios para observar golfinhos em liberdade, no seu ambiente natural. Assim, aprendemos como eles vivem de verdade, e não como se comportam num espetáculo.</p>
<p>Há quem diga que os parques aquáticos ensinam as crianças a gostar dos animais. Mas um espetáculo com saltos e bolas ensina, sobretudo, que os animais existem para nos divertir.</p>
<p>Alguns países já perceberam isto. Em França, uma lei de 2021 decidiu acabar, a partir de 2026, com os espetáculos de golfinhos e orcas e, em 2025, o maior parque marinho do país fechou as portas. Por isso, defendo que Portugal deve seguir o mesmo caminho: o lugar dos golfinhos é o mar.</p>''')}
<div class="grid2" style="margin-top:4mm;gap:7mm">
  <div>{act(1,"Identificar", 'Escreve, numa só frase, a <b>tese</b> da Clara.'+lines(2))}</div>
  <div>{act(2,"Avaliar", 'Qual é o argumento mais forte da Clara? Porquê?'+lines(2))}</div>
</div>
<div class="panel" style="margin-top:auto;display:grid;grid-template-columns:auto 1fr 1fr;gap:5mm;align-items:start;padding:3.2mm 4mm;font-size:8.8pt;line-height:1.45">
  <div class="kicker" style="max-width:24mm">Palavras-sinal</div>
  <div><b class="coral">Sublinha a coral</b> as marcas de opinião: <i>na minha opinião, defendo, acho, considero, eu</i>.</div>
  <div><b style="color:var(--sea-d,#2E8C7B)">Sublinha a verde</b> as palavras que ligam ideias: <i>em primeiro lugar, além disso, mas, porém, por isso</i>.</div>
</div>
<p class="src" style="margin-top:2mm">Texto de opinião escrito para esta unidade. Factos: MARE; lei francesa n.º 2021-1539, de 30 de novembro de 2021 (fim dos espetáculos com cetáceos a partir de 2026); encerramento do Marineland de Antibes (5 de janeiro de 2025).</p>
''', "Est. 4 · Defender")

P[17] = pg(17, f'''
<div class="kicker" style="margin-top:21mm">Texto 4B · Texto de opinião</div>
<h3 style="font-size:17pt;margin-top:1.4mm">Conhecer para proteger</h3>
<p class="small muted" style="margin-top:.6mm;margin-bottom:3mm">por Tiago Rocha, 6.º C · <span class="coral">Faz o mesmo exercício na margem.</span></p>
{col('''<p>Eu acho que fechar todos os parques com golfinhos não é a melhor solução. Considero que os bons parques, com regras apertadas, podem ajudar a proteger estes animais.</p>
<p>Em primeiro lugar, muitas crianças nunca vão ter a oportunidade de andar de barco em alto mar. Ver um golfinho de perto, ouvir os seus estalidos e perceber o seu tamanho pode ser o início de uma paixão pelo oceano — e quem gosta de uma coisa, protege-a.</p>
<p>Em segundo lugar, os passeios de barco também têm problemas. Os investigadores do MARE observaram que, quando há demasiados barcos turísticos, os golfinhos passam menos tempo a alimentar-se e a conviver. Ou seja, observar golfinhos em liberdade também pode incomodá-los.</p>
<p>É verdade que um tanque não é o oceano, e concordo que os espetáculos com truques não fazem sentido. Porém, um parque pode dedicar-se à educação e ao estudo, em vez do espetáculo.</p>
<p>Por isso, em vez de proibir, defendo que se criem regras mais exigentes: tanques maiores, nenhum truque de circo e visitas que ensinem a proteger os golfinhos que vivem no mar.</p>''')}
<p class="src" style="margin-top:3mm">Texto de opinião escrito para esta unidade. Factos: MARE — Centro de Ciências do Mar e do Ambiente (programa <i>Biosfera</i>, RTP).</p>
<div class="grid2" style="margin-top:auto;gap:6mm">
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">Numa frase</div><p class="small" style="margin-top:1mm">O que defende a Clara?</p>{U(6.5)}{U(6.5)}{U(6.5)}</div>
  <div class="panel coral" style="padding:3.4mm 4mm"><div class="kicker">Numa frase</div><p class="small" style="margin-top:1mm">O que defende o Tiago?</p>{U(6.5)}{U(6.5)}{U(6.5)}</div>
</div>
<div class="panel" style="margin-top:4mm;padding:3.4mm 4mm"><div class="kicker">Afinal, concordam em alguma coisa?</div><p class="small" style="margin-top:1mm">Procura nos dois textos uma ideia que a Clara e o Tiago partilham.</p>{U(6.5)}{U(6.5)}</div>
''', "Est. 4 · Defender")
