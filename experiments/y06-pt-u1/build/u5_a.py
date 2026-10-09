import parts
from parts import *
parts.UNIT.update(n=5, total=12)

P = {}
INK, COR, SEA = "var(--ink)", "var(--coral)", "var(--sea)"

def card(color, intent, struct, marks):
    """Identity card of a text type: why it is written, how it is built, how to recognise it."""
    li = "".join(f'<li style="margin-top:1mm">{m}</li>' for m in marks)
    return f'''<div class="panel" style="border-top:1.4mm solid {color};padding:4mm 4.5mm">
  <div class="kicker" style="color:{color}">Cartão de identidade</div>
  <div style="margin-top:2mm;font-size:9pt;line-height:1.36"><b style="color:{color}">Para quê?</b> {intent}</div>
  <div style="margin-top:2mm;font-size:9pt;line-height:1.36"><b style="color:{color}">Como se organiza?</b> {struct}</div>
  <div style="margin-top:2mm;font-size:9pt;line-height:1.36"><b style="color:{color}">Como o reconheço?</b><ul style="margin:.6mm 0 0 4mm">{li}</ul></div>
</div>'''

def gpage(n, no, color, kicker, title, cardhtml, text, tasks, src, qrh=""):
    return page(n, f'''
<div style="display:flex;align-items:baseline;gap:4mm"><div class="display" style="font-size:34pt;line-height:.9;color:{color}">{no}</div><div><div class="kicker" style="color:{color}">{kicker}</div><h2 style="margin-top:1mm">{title}</h2></div></div>
<div style="display:grid;grid-template-columns:62mm 1fr;gap:6mm;margin-top:4mm;align-items:start">
  {cardhtml}
  <div style="font-family:FrauncesText;font-size:10.2pt;line-height:1.5">{text}<p class="src" style="margin-top:1.6mm;font-family:Body">{src}</p>{('<div style="margin-top:2.4mm;font-family:Body">' + qrh + '</div>') if qrh else ''}</div>
</div>
{tasks}
<div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:3mm;align-items:end"><b style="color:{color};font-size:9.6pt">Ponte:</b><span style="font-size:9.6pt">que outro texto deste ano se parece com este? Em quê?</span></div>
{lines(2)}
<div style="margin-top:auto;display:flex;gap:3mm;align-items:flex-end;border-top:.6pt solid var(--rule);padding-top:3mm"><b style="color:{color};font-size:9.6pt;white-space:nowrap">Numa frase: este género serve para…</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
''', station="Revisão")

# ---------------------------------------------------------------- 1 OPENER
P[1] = page(1, '''
<div class="abs" style="left:0;right:0;top:0;height:140mm"><img class="cover" src="img/farol-ano.jpg"></div>
<div class="abs" style="left:23.5mm;right:21mm;top:150mm;bottom:15mm;display:flex;flex-direction:column">
  <div style="display:flex;align-items:flex-start;gap:5mm">
    <div class="display" style="font-size:96pt;line-height:.78;color:var(--coral);font-weight:700">5</div>
    <div style="padding-top:1mm">
      <div class="kicker blue">Unidade 5 · Revisões anuais</div>
      <h1 style="font-size:40pt;margin-top:1.5mm">O ano num<br>só <em>mapa</em></h1>
    </div>
  </div>
  <p class="lead" style="margin-top:6mm;font-size:12.6pt">Ao longo do ano, leste textos que explicam, que defendem, que contam, que cantam e que se representam. Nesta unidade, vais revê-los todos: um género por página, com o seu cartão de identidade, um texto novo e perguntas para provares a ti mesmo que já sabes.</p>
  <div class="panel" style="margin-top:7mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:4.5mm 5mm">
    <div class="display" style="font-size:26pt;color:var(--ink);line-height:1">5 min</div>
    <div style="font-size:10.2pt"><b class="blue">Memória da turma.</b> Sem abrir o manual, escrevam no quadro todos os textos que leram este ano. Depois, agrupem-nos: quais <b>informam</b>? Quais <b>defendem uma opinião</b>? Quais <b>contam uma história</b>? Quais são <b>poemas</b>? Quais se <b>representam</b>?</div>
  </div>
</div>
''', station="Partida", bleed=True, rh=False)

# ---------------------------------------------------------------- 2 THE YEAR MAP + SELF-DIAGNOSIS
G = [("1","Texto expositivo",INK,"3"),("2","Texto de opinião",COR,"4"),("3","Mito",SEA,"5"),("4","Adaptação",SEA,"6"),
     ("5","Lenda",SEA,"7"),("6","Romance tradicional",COR,"8"),("7","Poema",COR,"9"),("8","Texto dramático",INK,"10")]
cards = "".join(f'<div style="border-top:1.2mm solid {c};padding-top:2mm"><div class="display" style="font-size:18pt;color:{c};line-height:1">{n}</div><div style="font-family:FrauncesText;font-weight:700;color:var(--ink);font-size:10pt;margin-top:1mm">{t}</div><div class="small muted">p. {p}</div></div>' for n,t,c,p in G)
diag = "".join(f'<tr><td>{t}</td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk o"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk"></span></td><td style="text-align:center"><span class="chk o"></span></td></tr>' for _,t,_,_ in G)
steps = [("Ler","o cartão de identidade e o texto."),("Sublinhar","as marcas do género no texto."),("Responder","sem voltar ao cartão."),("Corrigir","com o colega e voltar ao cartão.")]
sh = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2mm;margin-top:2mm"><div class="display" style="font-size:15pt;color:var(--coral);line-height:1">{i}</div><div style="font-size:9.4pt"><b class="blue">{a}</b> {b}</div></div>' for i,(a,b) in enumerate(steps,1))
P[2] = page(2, f'''
<div class="kicker">Antes de começar</div>
<h2 style="margin-top:2mm">Oito géneros, um ano</h2>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm 4mm;margin-top:5mm">{cards}</div>
<div class="grid2" style="margin-top:7mm;grid-template-columns:1fr 1.25fr;gap:7mm">
  <div>
    <h3>Como rever cada página</h3>
    {sh}
    <div class="rule-card o" style="margin-top:5mm;font-size:9.2pt"><b class="coral">Uma pergunta para todos os textos:</b> qual é a <b>intenção</b> de quem escreveu? Informar, convencer, contar, emocionar ou pôr em cena? Quase sempre, a resposta diz-te o género.</div>
  </div>
  <div>
    <h3>Diagnóstico: quanto sei?</h3>
    <p class="small muted" style="margin-top:1mm">Assinala <b>antes</b> de rever e <b>depois</b> de rever. Compara no fim.</p>
    <table class="cmp ruled" style="margin-top:2mm;font-size:8.6pt">
      <tr><th style="background:var(--ink)" rowspan="2">Género</th><th colspan="3" style="background:var(--ink);text-align:center">Antes</th><th colspan="3" style="background:var(--coral);text-align:center">Depois</th></tr>
      <tr><th style="background:var(--ink);text-align:center">Sei</th><th style="background:var(--ink);text-align:center">+/−</th><th style="background:var(--ink);text-align:center">Não</th><th style="background:var(--coral);text-align:center">Sei</th><th style="background:var(--coral);text-align:center">+/−</th><th style="background:var(--coral);text-align:center">Não</th></tr>
      {diag}
    </table>
  </div>
</div>
<div style="margin-top:6mm"><div class="kicker">O meu plano de revisão</div><p class="small" style="margin-top:1mm">Distribui os oito géneros pelos dias. Começa pelos que assinalaste com <b>Não</b> ou <b>+/−</b>. Risca cada um quando o rever.</p><table class="cmp ruled" style="margin-top:2mm;font-size:8.6pt"><tr><th style="background:var(--ink);width:24mm"></th><th style="background:var(--ink);text-align:center">Seg</th><th style="background:var(--ink);text-align:center">Ter</th><th style="background:var(--ink);text-align:center">Qua</th><th style="background:var(--ink);text-align:center">Qui</th><th style="background:var(--ink);text-align:center">Sex</th></tr><tr><td style="font-size:8.6pt">Semana 1</td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td></tr><tr><td style="font-size:8.6pt">Semana 2</td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td><td style="height:15mm"></td></tr></table></div>
''', station="A rota")

# ---------------------------------------------------------------- 3 EXPOSITORY
P[3] = gpage(3, "1", INK, "Revisão · Texto expositivo", "A árvore que se despe de nove em nove anos",
  card(INK, "Explicar um tema de forma rigorosa e objetiva.", "Introdução (apresenta o tema) · desenvolvimento (um subtema por parágrafo) · conclusão.",
       ["verbos no presente e 3.ª pessoa;","vocabulário exato, números e datas;","nenhuma opinião do autor."]),
  '''<p><b>(1)</b> O sobreiro é uma árvore da família dos carvalhos, muito comum no Alentejo. Da sua casca faz-se a cortiça, um material leve, impermeável e isolante.</p>
<p style="margin-top:1.6mm"><b>(2)</b> A cortiça é retirada à mão, com um machado, numa operação chamada <i>descortiçamento</i> ou <i>tiragem</i>. A primeira tiragem faz-se, em regra, quando a árvore tem cerca de 25 anos e o tronco já é suficientemente grosso. Depois, a lei portuguesa obriga a esperar pelo menos nove anos entre cada tiragem, para que a casca volte a crescer. A árvore não é cortada: um sobreiro pode viver cerca de 200 anos.</p>
<p style="margin-top:1.6mm"><b>(3)</b> Portugal é o maior produtor mundial de cortiça. Com ela fazem-se rolhas, pavimentos, isolamentos e até peças para a indústria aeroespacial.</p>
<p style="margin-top:1.6mm"><b>(4)</b> Desde 2011, o sobreiro é a árvore nacional de Portugal, por decisão da Assembleia da República.</p>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Estrutura", 'Que parágrafo é a introdução? Que subtema tem cada um dos outros?'+lines(3),"blue")}
{act(2,"Localizar", 'Porque é que se espera nove anos entre tiragens?'+lines(3),"blue")}</div>
<div>{act(3,"Marcas", 'Copia um número, um termo técnico e um verbo no presente.'+lines(3),"blue")}
{act(4,"Resumir", 'Resume o texto em duas frases, com no máximo 35 palavras.'+lines(3),"blue")}</div>
</div>''',
  "Texto escrito para esta revisão. Dados: legislação portuguesa sobre o sobreiro; Resolução da Assembleia da República n.º 15/2012 (árvore nacional).", qr("q-sobreiro", "Verificar", "A resolução que fez do sobreiro a árvore nacional."))

# ---------------------------------------------------------------- 4 OPINION
P[4] = gpage(4, "2", COR, "Revisão · Texto de opinião", "Aulas ao ar livre? Sim, pelo menos uma vez por semana",
  card(COR, "Defender uma posição e convencer o leitor.", "Tese · argumentos com exemplos · (contra-argumento) · conclusão.",
       ["1.ª pessoa: <i>acho, defendo, considero</i>;","conectores: <i>porque, pois, além disso, porém, por isso</i>;","palavras avaliativas."]),
  '''<p>Na minha opinião, todas as turmas deviam ter, pelo menos, uma aula por semana ao ar livre.</p>
<p style="margin-top:1.6mm">Em primeiro lugar, aprendemos melhor aquilo que vemos e tocamos. Na aula de Ciências em que fomos medir o sobreiro do recreio, percebi finalmente o que é o perímetro de um tronco. Além disso, o ar livre faz-nos bem, pois passamos quase todo o dia sentados, dentro de salas.</p>
<p style="margin-top:1.6mm">Há quem diga que lá fora há demasiadas distrações. É verdade que um pássaro ou um avião chamam a atenção; porém, com regras claras, a turma habitua-se depressa, como aconteceu connosco.</p>
<p style="margin-top:1.6mm">Por isso, defendo que a escola deve experimentar: uma aula por semana, com o céu como teto.</p>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Tese", 'Copia a tese.'+lines(4))}
{act(2,"Argumentos", 'Quais são os dois argumentos? Que exemplo apoia o primeiro?'+lines(4))}</div>
<div>{act(3,"Conectores", 'Sublinha cinco conectores e diz se indicam <b>causa</b>, <b>explicação</b>, <b>contraste</b>, <b>adição</b> ou <b>conclusão</b>.'+lines(4))}
{act(4,"Contra-argumentar", 'Escreve um parágrafo que defenda a posição contrária, com um argumento e um exemplo.'+lines(4))}</div>
</div>''', "Texto escrito para esta revisão.")

# ---------------------------------------------------------------- 5 MYTH
P[5] = gpage(5, "3", SEA, "Revisão · Mito", "Perséfone e as estações do ano",
  card(SEA, "Explicar a origem do mundo, de fenómenos naturais ou de costumes.", "Situação inicial · acontecimento que muda tudo · consequências · explicação final.",
       ["deuses e heróis;","elementos maravilhosos;","tempo muito antigo e indefinido;","explica um fenómeno (aqui: as estações)."]),
  '''<p>Deméter, deusa das colheitas, tinha uma filha, Perséfone, que passava os dias a colher flores. Um dia, a terra abriu-se e Hades, deus do mundo dos mortos, levou-a no seu carro para o reino subterrâneo.</p>
<p style="margin-top:1.6mm">Desesperada, Deméter percorreu a terra à procura da filha e esqueceu-se dos campos. As searas secaram, as árvores deixaram de dar fruto e os homens começaram a passar fome. Zeus, o rei dos deuses, ordenou então a Hades que devolvesse Perséfone à mãe.</p>
<p style="margin-top:1.6mm">Porém, no mundo subterrâneo, Perséfone já tinha comido algumas sementes de romã — e quem prova o alimento dos mortos tem de voltar. Assim, ficou decidido que passaria uma parte do ano com Hades e a outra com a mãe.</p>
<p style="margin-top:1.6mm">Desde então, quando Perséfone desce ao reino dos mortos, Deméter fica triste e a terra entra no inverno. Quando a filha regressa, a deusa alegra-se, e a terra enche-se de flores: é a primavera.</p>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Personagens", 'Quem são os deuses e qual é o poder de cada um?'+lines(3),"sea")}
{act(2,"Maravilhoso", 'Indica dois acontecimentos que não poderiam acontecer na realidade.'+lines(2),"sea")}</div>
<div>{act(3,"Explicar", 'Que fenómeno natural explica este mito? Como o explica?'+lines(3),"sea")}
{act(4,"Gramática", 'Na frase «Perséfone já <b>tinha comido</b> algumas sementes», que tempo verbal é usado? Porquê?'+lines(2),"sea")}</div>
</div>''', "Reconto escrito para esta revisão, a partir do mito grego (<i>Hino Homérico a Deméter</i>).", qr("q-persefone", "Saber mais", "Perséfone na Wikipédia."))

# ---------------------------------------------------------------- 6 ADAPTATION
P[6] = page(6, f'''
<div style="display:flex;align-items:baseline;gap:4mm"><div class="display" style="font-size:34pt;line-height:.9;color:var(--sea)">4</div><div><div class="kicker sea">Revisão · Adaptação</div><h2 style="margin-top:1mm">Duas versões do Ciclope</h2></div></div>
<div style="display:grid;grid-template-columns:62mm 1fr;gap:6mm;margin-top:4mm">
{card(SEA, "Pôr uma obra ao alcance de outros leitores (por exemplo, leitores mais novos) ou passá-la para outro género.", "Mantém a história e as personagens principais; muda a linguagem, a extensão ou a forma.", ["a obra original é indicada;","frases mais curtas e vocabulário mais simples;","episódios resumidos ou cortados."])}
<div class="grid2" style="gap:4mm;font-family:FrauncesText;font-size:9.4pt;line-height:1.45;align-items:start">
  <div class="panel"><div class="kicker" style="font-family:Grotesk">Versão A</div><p style="margin-top:1.6mm">Então o Ciclope, soltando um bramido medonho que fez estremecer as paredes da gruta, arrancou do olho a estaca ainda em brasa, arremessou-a para longe com as mãos a tremer e pôs-se a chamar em altos gritos os outros Ciclopes, que habitavam em cavernas espalhadas pelos cumes batidos pelo vento.</p></div>
  <div class="panel coral"><div class="kicker" style="font-family:Grotesk">Versão B</div><p style="margin-top:1.6mm">O Ciclope deu um grito enorme. Tirou a estaca do olho e atirou-a para longe. Depois, começou a chamar os outros Ciclopes, que viviam nas grutas do monte.</p></div>
  <p class="src" style="grid-column:1/-1;font-family:Body">As duas versões foram escritas para esta revisão, a partir do canto IX da <i>Odisseia</i>, de Homero.</p>
</div>
</div>
<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Identificar", 'Qual das versões é a adaptação para leitores mais novos? Dá duas razões.'+lines(3),"sea")}
{act(2,"Comparar", 'O que se <b>mantém</b> nas duas versões? O que <b>desaparece</b> na versão B?'+lines(3),"sea")}</div>
<div>{act(3,"Vocabulário", 'Que palavras da versão A foram trocadas por palavras mais simples? Faz três pares.<div style="display:grid;grid-template-columns:1fr 6mm 1fr;gap:2mm;margin-top:1.6mm;align-items:end">'+''.join('<span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span><span style="text-align:center">→</span><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span>' for _ in range(3))+'</div>',"sea")}
{act(4,"Adaptar", 'Adapta esta frase para um leitor de 7 anos: <i>Ulisses, cujo engenho era célebre entre os Gregos, concebeu um ardil para iludir o gigante.</i>'+lines(3),"sea")}</div>
</div>
<div style="margin-top:4mm;display:grid;grid-template-columns:auto 1fr;gap:3mm;align-items:end"><b style="color:var(--sea);font-size:9.6pt">Ponte:</b><span style="font-size:9.6pt">que obra leste este ano numa versão adaptada? O que achas que foi mudado?</span></div>
{lines(2)}
<div style="margin-top:auto;display:flex;gap:3mm;align-items:flex-end;border-top:.6pt solid var(--rule);padding-top:3mm"><b style="color:var(--sea);font-size:9.6pt;white-space:nowrap">Numa frase: uma adaptação serve para…</b><span style="flex:1;border-bottom:.6pt solid #AEB7C4;height:6mm"></span></div>
''', station="Revisão")

# ---------------------------------------------------------------- 7 LEGEND
P[7] = gpage(7, "5", SEA, "Revisão · Lenda", "A lenda das amendoeiras",
  card(SEA, "Contar uma história ligada a um lugar ou a um acontecimento real, que mistura verdade e imaginação.", "Situação inicial · problema · solução · final ligado a algo que ainda hoje se vê.",
       ["lugar concreto e conhecido;","elementos reais e imaginários;","transmitida oralmente;","autor desconhecido."]),
  '''<p>Há muitos séculos, quando os mouros viviam no sul de Portugal, reinava no Algarve Ibn-Almundim. Um dia, casou com Gilda, uma princesa de cabelos loiros vinda de um país do Norte, onde os invernos eram brancos de neve.</p>
<p style="margin-top:1.6mm">Ao princípio, Gilda foi feliz. Mas, com o passar do tempo, começou a entristecer. Não comia, não sorria, passava os dias à janela. O rei chamou os melhores médicos, e nenhum lhe encontrou doença. Até que Gilda confessou: tinha saudades da neve da sua terra.</p>
<p style="margin-top:1.6mm">O rei mandou então plantar milhares de amendoeiras por todo o reino. No inverno seguinte, levou Gilda à janela do castelo. Os campos estavam cobertos de flores brancas, como se tivesse nevado. A princesa sorriu e curou-se.</p>
<p style="margin-top:1.6mm">Diz-se que é por isso que, ainda hoje, no fim do inverno, o Algarve se veste de branco.</p>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Real e imaginário", 'Indica dois elementos que podem ser <b>reais</b> e um que é provavelmente <b>imaginado</b>.'+lines(3),"sea")}
{act(2,"Lugar", 'Onde se passa a lenda? Porque é importante esse lugar ser real?'+lines(3),"sea")}</div>
<div>{act(3,"Distinguir", 'Qual é a diferença entre esta <b>lenda</b> e o <b>mito</b> de Perséfone? Pensa nas personagens e nos lugares.'+lines(3),"sea")}
{act(4,"Oralidade", 'A última frase começa por «Diz-se que…». Que marca da transmissão oral mostra esta expressão?'+lines(3),"sea")}</div>
</div>''', "Reconto de uma lenda tradicional do Algarve, escrito para esta revisão.")

# ---------------------------------------------------------------- 8 ROMANCE
P[8] = gpage(8, "6", COR, "Revisão · Romance tradicional", "De volta à Bela Infanta",
  card(COR, "Contar uma história em verso, para ser dita ou cantada.", "Situação inicial · encontro · prova · desfecho (muitas vezes, um reconhecimento).",
       ["poema narrativo, com personagens e diálogo;","repetições que ajudam a memorizar;","transmitido oralmente, autor desconhecido;","várias versões do mesmo romance."]),
  '''<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm"><div>Estava a bela Infanta<br>No seu jardim assentada,<br>Com o pente de oiro fino<br>Seus cabelos penteava.<br>Deitou os olhos ao mar,<br>Viu uma nobre armada;<br>Capitão que nela vinha,<br>Muito bem que a governava.</div>
<div>— «Este anel de sete pedras<br>Que eu contigo reparti…<br>Que é dela a outra metade?<br>Pois a minha, vê-la aí!»<br><br>— «Tantos anos que chorei,<br>Tantos sustos que tremi!…<br>Deus te perdoe, marido,<br>Que me ias matando aqui.»</div></div>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Situar", 'Os versos da esquerda são do <b>início</b>. Os da direita, do <b>fim</b>. Resume, numa frase, o que acontece entre eles.'+lines(3))}
{act(2,"Reconhecimento", 'Que objeto permite o reconhecimento? Porque é que está dividido em duas metades?'+lines(3))}</div>
<div>{act(3,"Distinguir", 'O que tem o romance de <b>poema</b>? E o que tem de <b>narrativa</b>?'+lines(3))}
{act(4,"Prosa", 'Passa para prosa os quatro primeiros versos.'+lines(3))}</div>
</div>''', "Almeida Garrett, <i>Romanceiro</i> (domínio público).")

# ---------------------------------------------------------------- 9 POEM
P[9] = gpage(9, "7", COR, "Revisão · Poema", "Canção da maré",
  card(COR, "Exprimir sentimentos e ver o mundo de uma forma nova.", "Versos agrupados em estrofes; pode ter refrão.",
       ["rima e ritmo;","metáforas, comparações, personificações;","repetição e enumeração."]),
  '''<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">
<div>O mar é um cão cansado<br>que vem deitar-se na areia;<br>lambe as pedras devagar<br>como quem conta a maré cheia.<br><br><i style="color:var(--sea)">Vai e vem, vai e vem,<br>o mar não é de ninguém.</i></div>
<div>Traz conchas, algas, espuma,<br>traz garrafas e segredos,<br>e leva, quando se vai,<br>os castelos dos meus dedos.<br><br><i style="color:var(--sea)">Vai e vem, vai e vem,<br>o mar não é de ninguém.</i></div>
</div>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Estrutura", 'Quantas estrofes tem o poema? Quantos versos tem cada quadra? Qual é o refrão?'+lines(3))}
{act(2,"Rima", 'Encontra dois pares de palavras que rimam.'+lines(1))}
{act(3,"Recursos", 'Copia uma metáfora, uma comparação e uma enumeração.'+lines(3))}</div>
<div>{act(4,"Interpretar", 'Explica o verso «os castelos dos meus dedos».'+lines(3))}
{act(5,"Gramática", 'Encontra um advérbio de modo. Que pergunta responde?'+lines(1))}
{act(6,"Criar", 'Escreve uma terceira quadra para o poema, com uma personificação.'+lines(4))}</div>
</div>''', "Poema escrito para esta revisão.")

# ---------------------------------------------------------------- 10 DRAMA
P[10] = gpage(10, "8", INK, "Revisão · Texto dramático", "A última palavra",
  card(INK, "Ser representado num palco.", "Atos e cenas; lista de personagens no início.",
       ["não há narrador;","nome da personagem + fala;","indicações cénicas entre parênteses;","apartes para o público."]),
  '''<div class="play" style="font-size:10pt"><div class="stage" style="margin-left:0">Biblioteca da escola, ao fim da tarde. MARTA procura um livro. O SENHOR BENTO, bibliotecário, fecha as janelas.</div>
<div class="sp"><div class="who" style="color:var(--ink)">SR. BENTO</div><div>Marta, fechamos daqui a cinco minutos.</div></div>
<div class="sp"><div class="who" style="color:var(--coral)">MARTA</div><div><span class="did">(aflita)</span> Senhor Bento, o livro das lendas desapareceu! Tenho de apresentar o trabalho amanhã.</div></div>
<div class="sp"><div class="who" style="color:var(--ink)">SR. BENTO</div><div><span class="did">(tirando um livro da gaveta)</span> Este? Emprestei-o ao teu irmão ontem. Ele devolveu-mo hoje de manhã.</div></div>
<div class="sp"><div class="who" style="color:var(--coral)">MARTA</div><div><span class="aside"><span class="did">(à parte)</span> O meu irmão! E eu a pensar que o tinha perdido…</span></div></div>
<div class="stage" style="margin-left:0">MARTA pega no livro e abraça-o. Apagam-se as luzes.</div></div>''',
  f'''<div class="grid2" style="margin-top:3mm;gap:7mm">
<div>{act(1,"Identificar", 'Copia uma indicação cénica de <b>lugar</b>, uma de <b>gesto</b> e uma de <b>luz</b>.'+lines(5),"blue")}
{act(2,"Aparte", 'O que nos revela o aparte da Marta?'+lines(5),"blue")}</div>
<div>{act(3,"Gramática", 'Em «Ele devolveu-<b>mo</b>», que complementos estão juntos em <i>mo</i>? E qual é o vocativo na primeira fala?'+lines(5),"blue")}
{act(4,"Narrar", 'Passa a cena para narrativa, com narrador e travessões.'+lines(5),"blue")}</div>
</div>''', "Cena escrita para esta revisão.")

# ---------------------------------------------------------------- 11 YEAR GRAMMAR
gram = [
 ("Conjunções", INK, 'Liga com <b>porque</b>, <b>mas</b> ou <b>porém</b>: <i>O mar estava calmo. A previsão anunciava ondas grandes.</i>'+lines(1)),
 ("Pretérito mais-que-perfeito", SEA, 'Completa com a forma simples e a composta: Quando a mãe chegou, a Inês já <span class="fill s"></span> / <span class="fill s"></span> (sair).'),
 ("Formas de tratamento", SEA, 'Reescreve para a diretora: <i>Podes assinar a autorização?</i>'+lines(1)),
 ("Advérbio de modo", COR, 'Forma advérbios:<br>rápido → <span class="fill s"></span><br>suave → <span class="fill s"></span>'),
 ("Particípio passado", COR, 'O livro foi <span class="fill s"></span> (escrever).<br>A porta está <span class="fill s"></span> (abrir).'),
 ("Gerúndio", COR, 'Transforma com <b>ir + gerúndio</b>: <i>A cidade acorda.</i>'+lines(1)),
 ("Frase simples e complexa", INK, 'Classifica (S/C):<div style="display:grid;grid-template-columns:1fr 7mm;gap:1.4mm 2mm;margin-top:1mm"><i>Ícaro subiu demais.</i><span class="chk"></span><i>Ícaro subiu e o sol derreteu a cera.</i><span class="chk"></span></div>'),
 ("Vocativo", INK, 'Pontua:<br><i>Pai olha para mim!</i><br><i>Obrigada professora.</i>'),
 ("CD e CI", SEA, 'Substitui por pronomes: <i>Ariadne deu o novelo a Teseu.</i>'+lines(1)),
]
gh = "".join(f'<div style="border-top:1.1mm solid {c};padding-top:2mm;font-size:9.2pt;line-height:1.5"><div class="kicker" style="color:{c}">{t}</div><div style="margin-top:1.2mm">{q}</div></div>' for t,c,q in gram)
P[11] = page(11, f'''
<div class="kicker">Revisão · Gramática do ano</div>
<h2 style="margin-top:2mm">Nove ferramentas, <em>uma</em> página</h2>
<p class="lead" style="margin-top:2mm;font-size:11pt">Cada caixa revê um conteúdo gramatical do ano. Se hesitares, volta à unidade onde o aprendeste.</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6mm 5mm;margin-top:5mm">{gh}</div>
<div class="panel coral" style="margin-top:5mm">
{act(1,"Desafio final", 'Escreve <b>uma só frase complexa</b> sobre o ano que termina com: um <b>vocativo</b>, uma <b>conjunção</b> e um verbo no <b>pretérito mais-que-perfeito</b>.'+lines(3))}
</div>
<div style="margin-top:4mm">{act(2,"Corrigir", 'Cada frase tem um erro de gramática ou de pontuação. Reescreve-a corretamente.<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 7mm"><div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2mm"><b class="coral">a)</b><div><span style="font-family:FrauncesText;font-size:9.6pt">O pescador, lança a rede ao mar.</span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div></div><div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2mm"><b class="coral">b)</b><div><span style="font-family:FrauncesText;font-size:9.6pt">Quando cheguei, o barco já tinha partido-se.</span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div></div><div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2mm"><b class="coral">c)</b><div><span style="font-family:FrauncesText;font-size:9.6pt">Senhora professora posso ler o meu texto?</span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div></div><div style="display:grid;grid-template-columns:6mm 1fr;gap:2mm;margin-top:2mm"><b class="coral">d)</b><div><span style="font-family:FrauncesText;font-size:9.6pt">Ícaro subiu depressamente em direção ao sol.</span><span style="display:block;border-bottom:.6pt solid #AEB7C4;height:6.5mm"></span></div></div></div>')}</div>
<div class="panel blue" style="margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:9.4pt">
  <div><b class="blue">A ferramenta em que ainda hesito é…</b>{lines(1)}</div>
  <div><b class="blue">Vou revê-la na unidade…</b>{lines(1)}</div>
</div>
''', station="Revisão")

# ---------------------------------------------------------------- 12 GENRE DETECTIVE + CLOSING
ex = [("A","«Querida mãe, olha: a tarde é um lenço azul que o vento leva devagar.»"),
      ("B","«O sobreiro pode viver cerca de 200 anos.»"),
      ("C","«Há muitos séculos, no castelo de Silves, vivia uma princesa triste.»"),
      ("D","MARTA <i>(aflita)</i> Senhor Bento, o livro desapareceu!"),
      ("E","«Defendo que a escola deve experimentar aulas ao ar livre, pois aprendemos melhor.»"),
      ("F","«Zeus, rei dos deuses, ordenou a Hades que devolvesse Perséfone.»")]
eh = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr 34mm;gap:3mm;align-items:end;margin-top:2.6mm;font-size:9.4pt"><b class="coral display" style="font-size:13pt;line-height:1">{k}</b><span style="font-family:FrauncesText">{t}</span><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>' for k,t in ex)
goals = "".join(f'<div style="display:grid;grid-template-columns:7mm 1fr;gap:2mm;margin-top:2.4mm;align-items:end"><b class="blue">{i}.</b><span style="border-bottom:.6pt solid #AEB7C4;height:5mm"></span></div>' for i in (1,2,3))
P[12] = page(12, f'''
<div class="kicker">Chegada</div>
<h2 style="margin-top:2mm">Detetive de géneros</h2>
{act(1,"Classificar", 'Cada excerto pertence a um género que reviste. Escreve-o na linha.')}
{eh}
<p class="small muted" style="margin-top:1.4mm">Atenção: um dos excertos pode ser de mais de um género. Qual? Porquê?</p>{lines(1)}
<div class="grid2" style="margin-top:6mm;gap:7mm">
  <div class="panel blue">
    <div class="kicker blue">Volta à página 2</div>
    <p style="margin-top:1.6mm;font-size:9.6pt">Preenche a coluna <b>Depois</b> do diagnóstico. Em que género melhoraste mais? Em qual ainda tens dúvidas?</p>{lines(3)}
  </div>
  <div class="panel coral">
    <div class="kicker">Três objetivos para o próximo ano</div>
    <p class="small" style="margin-top:1.4mm">O que queres ler, escrever ou aprender a fazer melhor?</p>{goals}
  </div>
</div>
{act(2,"Opinar", 'Qual foi o teu texto preferido do ano? Defende a tua escolha com <b>dois argumentos</b> e um <b>exemplo</b> do texto.'+lines(11))}
<div class="hand" style="margin-top:auto;text-align:center;font-size:16pt">Bom verão — e boas leituras!</div>
''', station="Chegada")
