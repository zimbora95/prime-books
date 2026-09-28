"""Generate src/u5.html — Unidade 5 · Revisões anuais (Y8 PT)."""
import pathlib, re, html as H
R = pathlib.Path(__file__).parent
T = R / "texts"


def rail(t): return f'<div class="rail"><span>{t}</span></div>'
def folio(t): return f'<div class="folio"><span class="n"></span><span class="t">{t}</span></div>'
def ref(i): return f'<span class="ref" data-ref="{i}"></span>'


def page(id_, cls, railt, inner, foliot=None):
    return f'''
<section id="{id_}" class="page v-rev {cls}">
  {rail(railt)}
  <div class="inner">
{inner}
  </div>
  {folio(foliot or railt)}
</section>'''


def poem(txt):
    out, n = [], 0
    for st in [s for s in txt.split("\n\n") if s.strip()]:
        ls = []
        for l in st.split("\n"):
            n += 1
            num = f'<span class="vln">{n}</span>' if n in (1, 5, 10, 14) else ''
            ls.append(f'<span class="vl">{num}{H.escape(l, quote=False)}</span>')
        out.append('<div class="vst">' + "".join(ls) + '</div>')
    return '<div class="vpoem two">' + "".join(out) + '</div>'


P = []
# ------------------------------------------------------------------ OPENER
P.append('''
<section id="u5" class="page v-rev opener u5-opener">
  <div class="bleed" style="background-image:url(../art/jpg/u5_opener.jpg); background-position: 50% 60%;"></div>
  <div class="opener-card">
    <div class="kicker"><b>Unidade 5</b> Revisões anuais</div>
    <h1 class="title">Sessão <em>de encerramento</em></h1>
    <p class="lede">Última noite do ano no Cinema Aurora. Na praça, cinco bancas iluminadas esperam por ti — um anúncio, uma crítica, um conto, um soneto e uma cena. Nenhum destes textos é conhecido: vais lê-los pela primeira vez, com tudo o que aprendeste desde setembro. Depois, dois circuitos de gramática, um teste de treino e uma conversa contigo próprio sobre o leitor que és agora.</p>
    <div class="opener-qs">
      <div><span>?</span>O que sabes fazer hoje que não sabias em setembro?</div>
      <div><span>?</span>Consegues ler um texto novo sem ajuda — e explicar como funciona?</div>
      <div><span>?</span>Qual foi o texto do ano que vais levar contigo?</div>
    </div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Unidade 5</span></div>
</section>''')

# ------------------------------------------------------------------ PROGRAMA / CIRCUITO
st = [('1', 'Publicidade', 'Um anúncio de bicicletas', 'u5-e1', 'u5-red'),
      ('2', 'Crítica', 'Uma crítica de cinema', 'u5-e2', 'u5-sea'),
      ('3', 'Narrativa', '«O Tesouro», de Eça de Queirós', 'u5-e3', 'u5-grn'),
      ('4', 'Poesia', 'Um soneto de Camões', 'u5-e4', 'u5-plm'),
      ('5', 'Teatro', 'A última bobina', 'u5-e5', 'u5-ind')]
sh = "".join(f'<div class="u5-st {c}"><span class="n">{n}</span><b>{g}</b><small>{t}</small><span class="p">p. {ref(r)}</span></div>' for n, g, t, r, c in st)
P.append(page('u5-prog', '', 'Programa', f'''
    <div class="kicker"><b>Unidade 5</b> O circuito da última noite</div>
    <h1 class="title">Cinco bancas, <em>um ano inteiro</em></h1>
    <p class="lede sm">Cada banca revê uma unidade com um <b>texto novo</b>. Trabalha a pares; em cada banca tens uma página de leitura e uma de oficina. Quando acabares uma banca, pede ao teu professor um carimbo no passaporte (p. {ref('u5-refl')}).</p>
    <div class="u5-sts">{sh}</div>
    <div class="u5-more">
      <div><b>Antes das bancas</b><span>O mapa do ano · p. {ref('u5-mapa')}</span></div>
      <div><b>Circuitos de gramática</b><span>Frase e verbo · frase complexa e funções · p. {ref('u5-g1')}</span></div>
      <div><b>Teste de treino</b><span>Prova mista, como nos testes · p. {ref('u5-t')}</span></div>
      <div><b>No fim</b><span>O leitor que és agora · p. {ref('u5-refl')}</span></div>
    </div>
    <div class="u5-cal">
      <div class="cl-h">Em três aulas</div>
      <div><b>Aula 1</b><span>Mapa do ano · bancas 1 e 2</span></div>
      <div><b>Aula 2</b><span>Bancas 3, 4 e 5</span></div>
      <div><b>Aula 3</b><span>Circuitos de gramática · teste de treino · reflexão</span></div>
    </div>
    <div class="u5-how">
      <div class="h-h">Como trabalhar numa banca</div>
      <div><i>1</i><span><b>Lê</b> o texto duas vezes: a primeira, de seguida; a segunda, a sublinhar.</span></div>
      <div><i>2</i><span><b>Responde</b> sem voltar às unidades. Só depois consultas o mapa do ano.</span></div>
      <div><i>3</i><span><b>Corrige</b> com as soluções (p. {ref('u5-sol')}) e regista o que falhaste.</span></div>
      <div><i>4</i><span><b>Volta</b> à página da unidade indicada para rever o que não sabias.</span></div>
    </div>'''))

# ------------------------------------------------------------------ MAPA DO ANO (2 pp.)
def mcard(n, cls, title, gen, items, gram, refs):
    it = "".join(f'<li>{x}</li>' for x in items)
    gr = "".join(f'<li>{x}</li>' for x in gram)
    rf = " · ".join(f'{a} p. {ref(b)}' for a, b in refs)
    return f'''<div class="u5-m {cls}"><div class="mh"><span>{n}</span><div><b>{title}</b><small>{gen}</small></div></div>
      <div class="mb"><div><h4>O essencial</h4><ul>{it}</ul></div><div><h4>Gramática</h4><ul>{gr}</ul></div></div>
      <div class="mr">Rever: {rf}</div></div>'''

P.append(page('u5-mapa', '', 'Mapa do ano', f'''
    <div class="kicker"><b>Unidade 5</b> Referência · 1 de 2</div>
    <h1 class="title">O mapa <em>do ano</em></h1>
    {mcard('1', 'u5-red', 'Promessa &amp; Veredicto', 'Publicidade e crítica',
      ['Publicidade comercial (vende) e não comercial (muda comportamentos)', 'Elementos do anúncio: imagem, título, texto, slogan, marca, público-alvo', 'Recursos da persuasão: hipérbole, enumeração, imperativo, trocadilho, apelo às emoções', 'Crítica: tese, argumentos, exemplos, facto e opinião, classificação'],
      ['Frase ativa e frase passiva', 'Hipérbole e enumeração'],
      [('Persuasão', 's8'), ('Slogan', 's13'), ('Crítica', 's18'), ('Ativa e passiva', 's21')])}
    {mcard('2', 'u5-grn', 'Quem nos faz crescer?', 'Texto narrativo',
      ['Narrador: participante ou não participante; presente ou ausente', 'Categorias: ação, personagens, espaço, tempo', 'Estrutura: situação inicial, desenvolvimento, desenlace', 'Modos de expressão: narração, descrição, diálogo; discurso direto e indireto'],
      ['Frase simples e complexa · oração relativa', 'Subordinadas condicionais e finais', 'Conjuntivo · tempos do indicativo', 'Modificador do nome e do grupo verbal · pronome átono'],
      [('Mapa da narrativa', 'u2-map'), ('Relativas', 'u2-n2-g'), ('Conjuntivo', 'u2-n4-g'), ('Modificadores', 'u2-n6-g')])}
    <div class="u5-auth">
      <div class="au-h">Os autores do ano</div>
      <span>Luís de Camões</span><span>Alexandre Herculano</span><span>Eça de Queirós</span><span>Trindade Coelho</span><span>Fernando Pessoa</span><span>Florbela Espanca</span><span>Lima Barreto</span><span>Miguel Torga</span><span>Manuel da Fonseca</span><span>António Gedeão</span><span>Alexandre O'Neill</span><span>David Mourão-Ferreira</span><span>Ana Hatherly</span><span>Manuel Alegre</span><span>Alice Vieira</span><span>Ondjaki</span><span>Júlio Verne</span><span>Oscar Wilde</span>
      <p>Assinala os que leste. Escolhe um para ler mais durante as férias.</p>
    </div>'''))

P.append(page('u5-mapa2', '', 'Mapa do ano', f'''
    <div class="kicker"><b>Unidade 5</b> Referência · 2 de 2</div>
    {mcard('3', 'u5-plm', 'O que cabe num verso?', 'Texto poético',
      ['Verso, estrofe (quadra, terceto…), soneto', 'Rima emparelhada, cruzada, interpolada; esquema rimático', 'Sílabas métricas: redondilha menor (5), maior (7), decassílabo (10)', 'Recursos: anáfora, metáfora, comparação, personificação, apóstrofe, antítese, paradoxo'],
      ['Oração subordinada completiva', 'Advérbio e locução adverbial', 'Sujeito e predicado · pleonasmo'],
      [('Oficina do verso', 'u3-v1'), ('Recursos', 'u3-rec'), ('Comentário', 'u3-com')])}
    {mcard('4', 'u5-ind', 'Sobe o pano', 'Texto dramático',
      ['Texto principal (falas) e secundário (didascálias)', 'Diálogo, monólogo, aparte', 'Ato, cena, quadro; exposição, conflito, desenlace', 'Da narrativa ao palco: cortar, dividir, dar voz, encenar'],
      ['Sujeito, complemento direto, complemento indireto, modificador', 'Língua das didascálias e das falas'],
      [('Mapa do texto dramático', 'u4-map'), ('Funções sintáticas', 'u4-l2-g')])}
    <div class="u5-self">
      <div class="sc-h"><span>Antes das bancas: como estou?</span><span>preciso de rever</span><span>mais ou menos</span><span>domino</span></div>
      <div class="sc-r"><span>Publicidade e crítica</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>Narrativa</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>Poesia e métrica</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>Texto dramático</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>Gramática da frase</span><i></i><i></i><i></i></div>
    </div>'''))

# ------------------------------------------------------------------ E1 · ANÚNCIO
P.append(page('u5-e1', '', 'Banca 1 · Publicidade', '''
    <div class="kicker"><b>Banca 1</b> <span class="skill sk-lei">Leitura</span> Texto novo · publicidade</div>
    <h1 class="title">Vai com <em>a corrente</em></h1>
    <div class="u5-ad">
      <div class="ad-top"><span class="ad-brand">MARÉ</span><span class="ad-tag">bicicletas desde 1962</span></div>
      <div class="ad-h">Pedala mais longe<br>do que o mar.</div>
      <p class="ad-b">A nova <b>Maré 8</b> é leve como uma gaivota, forte como o farol e mais rápida do que o vento norte. Quadro de alumínio, sete mudanças, luzes LED, travões de disco e um cesto para levares o mundo contigo. Experimenta-a este sábado na Praça do Cinema Aurora — e ganha um capacete na compra de qualquer bicicleta até 31 de maio.</p>
      <div class="ad-s">Maré. <em>Vai com a corrente.</em></div>
      <small>*Oferta limitada ao stock existente. Capacete de modelo único, sujeito a disponibilidade.</small>
    </div>
    <ol class="qs">
      <li>É publicidade comercial ou não comercial? Justifica com duas marcas do texto.<div class="lines l2"></div></li>
      <li>Qual é o público-alvo? Que palavras e imagens o mostram?<div class="lines l2"></div></li>
      <li>Transcreve uma <b>hipérbole</b>, uma <b>comparação</b> e uma <b>enumeração</b>. Explica o efeito de uma delas.<div class="lines l3"></div></li>
      <li>Identifica duas formas verbais no <b>imperativo</b>. A quem se dirige o anúncio?<div class="lines l1"></div></li>
      <li>O slogan tem duplo sentido (<b>trocadilho</b>). Explica os dois sentidos de «corrente».<div class="lines l2"></div></li>
      <li>Porque é que as letras pequenas estão… pequenas? O que escondem?<div class="lines l2"></div></li>
    </ol>'''))

P.append(page('u5-e1-o', 'v-oficina-r', 'Banca 1 · Oficina', '''
    <div class="kicker"><b>Banca 1</b> <span class="skill sk-esc">Escrita</span> <span class="skill sk-gra">Gramática</span> Do comercial ao não comercial</div>
    <h1 class="title">Vender ou <em>mudar?</em></h1>
    <p class="lede sm">A Câmara Municipal de Vila Nova do Farol quer que mais alunos vão de bicicleta para a escola. Usa o que aprendeste com o anúncio da Maré para criar uma <b>campanha não comercial</b>.</p>
    <table class="fill plan5">
      <tr><th style="width:40mm"></th><th>Anúncio Maré</th><th>A tua campanha</th></tr>
      <tr><td><b>Emissor</b></td><td>a marca Maré</td><td></td></tr>
      <tr><td><b>Objetivo</b></td><td>vender bicicletas</td><td></td></tr>
      <tr><td><b>Público-alvo</b></td><td></td><td></td></tr>
      <tr><td><b>Argumento principal</b></td><td></td><td></td></tr>
      <tr><td><b>Slogan</b></td><td>Maré. Vai com a corrente.</td><td></td></tr>
      <tr><td><b>Imagem</b></td><td></td><td></td></tr>
    </table>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escreve o texto da campanha (60 a 80 palavras), com um título, uma hipérbole, uma enumeração, dois imperativos e o slogan.</p>
      <div class="lines l8"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Passa à passiva: <b>a)</b> Os ciclistas recomendam a Maré 8. <b>b)</b> A marca oferece um capacete. <b>c)</b> A Câmara lançará a campanha em setembro.</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Na frase «Pedala mais longe do que o mar», qual é o sujeito? Porque não está escrito? <span class="pill stretch">Desafio</span></p>
      <div class="lines l2"></div>
    </div></div>'''))

# ------------------------------------------------------------------ E2 · CRÍTICA
P.append(page('u5-e2', '', 'Banca 2 · Crítica', '''
    <div class="kicker"><b>Banca 2</b> <span class="skill sk-lei">Leitura</span> Texto novo · crítica de cinema</div>
    <div class="u5-rev">
      <div class="rv-top"><span>A Lupa · Cinema</span><span class="stars">★★★☆☆</span></div>
      <h2 class="rv-t">A Última Sessão</h2>
      <p class="rv-m">Realização de Inês Barros · Portugal, 2026 · 98 minutos · M/12</p>
      <p class="rv-by">por Marta Seixas</p>
      <div class="rv-b">
        <p><span class="pn">1</span>Há filmes que se veem com os olhos e filmes que se veem com a memória. <i>A Última Sessão</i>, a segunda longa-metragem de Inês Barros, quer ser das duas espécies — e só às vezes consegue.</p>
        <p><span class="pn">2</span>A história passa-se numa vila do Alentejo, em 1998, na semana em que o único cinema vai fechar. O projecionista, Sr. Alberto (Rui Mendes), tem setenta anos e uma sala vazia; a neta, Carolina (a estreante Sara Lopes), tem catorze e nenhuma vontade de ali estar. Ao longo de sete noites, os dois projetam os filmes preferidos do avô para uma plateia que, pouco a pouco, volta a encher.</p>
        <p><span class="pn">3</span>O melhor do filme está na imagem. A fotografia de Tiago Reis transforma a sala escura num lugar mágico: o feixe do projetor atravessa o fumo como um farol, e cada rosto da plateia parece um retrato antigo. As cenas entre avô e neta, quase sem palavras, são das mais belas do cinema português recente.</p>
        <p><span class="pn">4</span>O problema é o argumento. A partir de meio, o filme repete-se: cada noite traz mais um vizinho, mais uma lágrima, mais uma lembrança. Sabemos, desde a primeira cena, como tudo vai acabar, e a realizadora não nos surpreende nem uma vez. Os noventa e oito minutos parecem cento e vinte.</p>
        <p><span class="pn">5</span>Ainda assim, vale a pena ir. Por Rui Mendes, que diz mais com as mãos do que muitos atores com a voz; por uma banda sonora que dá vontade de ouvir de novo; e porque um filme sobre o amor ao cinema merece ser visto numa sala escura — de preferência, cheia.</p>
      </div>
    </div>
    <ol class="qs two">
      <li>Qual é a <b>tese</b> da crítica? Em que parágrafo aparece com mais clareza?<div class="lines l3"></div></li>
      <li>Transcreve dois <b>factos</b> e duas <b>opiniões</b>.<div class="lines l4"></div></li>
      <li>Que aspeto do filme é elogiado? Que argumento o sustenta?<div class="lines l3"></div></li>
      <li>Que aspeto é criticado? Com que exemplo?<div class="lines l3"></div></li>
      <li>«Os noventa e oito minutos parecem cento e vinte.» Que recurso? Com que intenção?<div class="lines l3"></div></li>
      <li>A classificação (três estrelas) está de acordo com o texto? Justifica.<div class="lines l3"></div></li>
    </ol>'''))

P.append(page('u5-e2-o', 'v-oficina-r', 'Banca 2 · Oficina', '''
    <div class="kicker"><b>Banca 2</b> <span class="skill sk-esc">Escrita</span> Reconstruir e responder</div>
    <h1 class="title">O teu <em>veredicto</em></h1>
    <div class="u5-arg">
      <div class="ag-h">A estrutura da crítica de Marta Seixas</div>
      <div class="ag-r"><b>§1</b><span>Introdução e tese</span><i></i></div>
      <div class="ag-r"><b>§2</b><span>Apresentação (factos)</span><i></i></div>
      <div class="ag-r"><b>§3</b><span>Argumento a favor</span><i></i></div>
      <div class="ag-r"><b>§4</b><span>Argumento contra</span><i></i></div>
      <div class="ag-r"><b>§5</b><span>Conclusão e recomendação</span><i></i></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Resume, em cada linha do quadro, a ideia principal do parágrafo (máx. 12 palavras).</p>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Um leitor d'<i>A Lupa</i> discorda: acha que o filme merece cinco estrelas. Escreve a crítica dele (120 a 150 palavras): tese, dois argumentos com exemplos do filme (usa as informações do texto), conclusão e classificação.</p>
      <div class="lines l12"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Transforma em frases passivas: <b>a)</b> Tiago Reis assina a fotografia. <b>b)</b> A plateia aplaudiu o projecionista.</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="chk"><b>Revê</b><span>tese clara</span><span>factos e opiniões distinguidos</span><span>conectores de oposição (mas, no entanto, ainda assim)</span><span>classificação coerente</span></div>'''))

# ------------------------------------------------------------------ E3 · O TESOURO (flow, full text)
paras = (T / 'tesouro.txt').read_text().split('\n\n')
body = "\n".join(f'<p><span class="pn">{i+1}</span>{H.escape(p, quote=False)}</p>' if (i % 5 == 0) else f'<p>{H.escape(p, quote=False)}</p>' for i, p in enumerate(paras))
P.append(f'''
<section id="u5-e3" class="page v-rev flow">
  {rail('Banca 3 · Narrativa')}
  <div class="inner">
    <div class="flow-head">
      <div class="kicker"><b>Banca 3</b> <span class="skill sk-lei">Leitura</span> Texto novo · conto integral · ortografia atualizada</div>
      <div class="u5-th">
        <div><h2 class="tx-title">O Tesouro</h2>
        <p class="tx-by">Eça de Queirós · <i>Contos</i> (1902)</p>
        <p class="u5-intro">Eça de Queirós (1845–1900) é um dos maiores romancistas portugueses. Este conto, que se passa num Reino das Astúrias medieval, tem a forma de uma fábula moral: três irmãos pobres encontram um cofre de ouro. O que fariam três irmãos com um tesouro para dividir?</p></div>
        <div class="u5-timg" style="background-image:url(../art/jpg/u5_tesouro.jpg)"></div>
      </div>
    </div>
    <div class="flow-body cols2">
{body}
<p class="src">Eça de Queirós, «O Tesouro», em <i>Contos</i> (1902). Domínio público. Texto da Wikisource, ortografia atualizada.</p>
<div class="u5-voc"><div class="vc-h">Vocabulário</div>
<p><b>pelote</b> casaco antigo, sem mangas · <b>camelão</b> tecido grosseiro · <b>engelhados</b> encolhidos, enrugados · <b>lazarentas</b> doentes, magras · <b>tortulhos</b> cogumelos · <b>robles</b> carvalhos · <b>dobrões</b> antigas moedas de ouro · <b>lívidos</b> muito pálidos · <b>círios</b> velas grandes · <b>alforges</b> sacos duplos para levar na montada · <b>droguista</b> vendedor de drogas e remédios</p></div>
<div class="u5-voc u5-plans"><div class="vc-h">Antes de responder · três planos</div>
<div class="pl-r"><b>Rui</b><i></i></div><div class="pl-r"><b></b><i></i></div>
<div class="pl-r"><b>Rostabal</b><i></i></div><div class="pl-r"><b></b><i></i></div>
<div class="pl-r"><b>Guanes</b><i></i></div><div class="pl-r"><b></b><i></i></div>
<p>O que planeou cada irmão? Quem morre primeiro? Porque é que ninguém fica com o ouro?</p></div>
    </div>
  </div>
  {folio('Banca 3 · Narrativa')}
</section>''')

P.append(page('u5-e3-q', 'v-oficina-r', 'Banca 3 · Oficina', '''
    <div class="kicker"><b>Banca 3</b> <span class="skill sk-lit">Ed. literária</span> <span class="skill sk-gra">Gramática</span> As categorias da narrativa</div>
    <h1 class="title">Três irmãos, <em>um cofre</em></h1>
    <table class="fill cat5">
      <tr><th style="width:30mm">Categoria</th><th>No conto</th><th style="width:38mm">Prova (§)</th></tr>
      <tr><td><b>Narrador</b><small>participante? presente?</small></td><td></td><td></td></tr>
      <tr><td><b>Espaço físico</b></td><td></td><td></td></tr>
      <tr><td><b>Espaço social</b></td><td></td><td></td></tr>
      <tr><td><b>Tempo</b><small>época · duração</small></td><td></td><td></td></tr>
      <tr><td><b>Personagens</b><small>principais · caracterização</small></td><td></td><td></td></tr>
    </table>
    <ol class="qs two">
      <li>Divide o conto em <b>situação inicial</b>, <b>desenvolvimento</b> e <b>desenlace</b>. Indica os parágrafos.<div class="lines l3"></div></li>
      <li>Que traço de caráter une os três irmãos? Justifica com uma frase do conto.<div class="lines l2"></div></li>
      <li>Rui é «o mais avisado». No fim, o narrador chama-lhe «D. Rui, o avisado». Que efeito tem esta repetição? (Pensa na <b>ironia</b>.)<div class="lines l3"></div></li>
      <li>«O tesouro ainda lá está, na mata de Roquelanes.» Qual é a lição (moralidade) do conto?<div class="lines l3"></div></li>
      <li>Transcreve uma <b>comparação</b> do 1.º ou do 2.º parágrafo e explica-a.<div class="lines l2"></div></li>
      <li>Identifica e classifica a oração subordinada: «Ele entendia <u>que o mano Guanes, como mais leve, devia trotar para a vila vizinha de Retortilho</u>.»<div class="lines l1"></div></li>
      <li>Classifica a oração sublinhada: «[Guanes foi comprar] o veneno <u>que, misturado ao vinho, o tornaria a ele, a ele somente, dono de todo o tesouro</u>.»<div class="lines l1"></div></li>
      <li>Reescreve no <b>discurso indireto</b>: «— É veneno!», berrou Rui.<div class="lines l2"></div></li>
    </ol>'''))

# ------------------------------------------------------------------ E4 · CAMÕES
amor = (T / 'amor_fogo.txt').read_text()
P.append(page('u5-e4', '', 'Banca 4 · Poesia', f'''
    <div class="kicker"><b>Banca 4</b> <span class="skill sk-lit">Ed. literária</span> Texto novo · soneto integral · ortografia atualizada</div>
    <div class="fan-h"><div><h1 class="title">Amor é <em>um fogo</em></h1>
      <p class="byline">Luís de Camões (c. 1524–1580) · <i>Rimas</i>, edição póstuma</p></div>
      <p class="u5-intro narrow">Camões, o poeta de <i>Os Lusíadas</i>, escreveu também dezenas de sonetos. Este é, talvez, o mais conhecido da língua portuguesa: uma tentativa de <b>definir</b> o amor.</p></div>
    <div class="fan-p">{poem(amor)}</div>
    <p class="src">Luís de Camões, soneto. Domínio público. Texto da Wikisource, ortografia atualizada.</p>
    <div class="fan-q">
      <ol class="qs two">
        <li>Confirma que é um soneto: estrofes, versos e esquema rimático.<div class="lines l3"></div></li>
        <li>Faz a escansão do verso 1. Quantas sílabas métricas tem? Como se chama este verso?<div class="scan-blank ten"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></li>
        <li>Que palavra se repete no início de quase todos os versos? Como se chama o recurso?<div class="lines l1"></div></li>
        <li>«contentamento descontente», «dor que desatina sem doer»: que recurso predomina? Porquê usá-lo para falar do amor?<div class="lines l4"></div></li>
        <li>Os tercetos terminam com uma pergunta. O que pergunta o sujeito poético?<div class="lines l3"></div></li>
        <li>Compara com «Fanatismo», de Florbela (p. <span class="ref" data-ref="u3-p9"></span>): que visão do amor tem cada um?<div class="lines l4"></div></li>
      </ol>
    </div>'''))

# ------------------------------------------------------------------ E5 · CENA
P.append(page('u5-e5', '', 'Banca 5 · Teatro', '''
    <div class="kicker"><b>Banca 5</b> <span class="skill sk-lit">Ed. literária</span> <span class="skill sk-ora">Oralidade</span> Texto novo · cena</div>
    <h1 class="title">A última <em>bobina</em></h1>
    <div class="mini-play u5-play">
      <p class="did">(Cabina de projeção do Cinema Aurora. Noite. O projetor está desligado; só uma lâmpada pequena ilumina a mesa, cheia de latas de filme. O SR. ALBERTO, projecionista, enrola devagar uma bobina. Entra INÊS, 13 anos, com um caderno.)</p>
      <p class="fala"><b>INÊS</b> Sr. Alberto? A professora disse que o senhor me podia mostrar como se projeta um filme a sério. Para o trabalho de Português.</p>
      <p class="fala"><b>SR. ALBERTO</b> <i class="di">(Sem se voltar.)</i> Um filme a sério… Hoje já ninguém sabe o que isso é. Senta-te ali. Não mexas em nada.</p>
      <p class="did">(INÊS senta-se num banco. Abre o caderno.)</p>
      <p class="fala"><b>INÊS</b> Há quanto tempo trabalha aqui?</p>
      <p class="fala"><b>SR. ALBERTO</b> Quarenta e dois anos. Entrei no dia em que estreou <i>Os Pássaros</i>. <i class="di">(Pausa. Pousa a bobina.)</i> Amanhã passam tudo para digital. Carregam num botão e pronto.</p>
      <p class="fala"><b>INÊS</b> <i class="di">(À parte.)</i> Então é por isso que está tão triste.</p>
      <p class="fala"><b>SR. ALBERTO</b> Queres ver a última? A última bobina de verdade?</p>
      <p class="did">(Liga o projetor. Ouve-se o ruído do motor. Um feixe de luz atravessa a cabina e sai pela janelinha para a sala vazia. INÊS levanta-se e espreita.)</p>
      <p class="fala"><b>INÊS</b> <i class="di">(Baixinho, maravilhada.)</i> Parece um farol.</p>
      <p class="fala"><b>SR. ALBERTO</b> <i class="di">(Sorri pela primeira vez.)</i> É um farol. Durante quarenta e dois anos, guiou toda a gente desta vila para o mesmo sítio. <i class="di">(Estende-lhe a manivela.)</i> Anda. A última, projetas tu.</p>
      <p class="did">(INÊS pega na manivela. A luz do feixe ilumina-lhes os rostos. Escuro lento.)</p>
    </div>
    <ol class="qs two">
      <li>Transcreve uma didascália de <b>espaço</b>, uma de <b>luz</b> e uma de <b>tom</b>.<div class="lines l3"></div></li>
      <li>Onde está o <b>aparte</b>? Que informação dá ao público?<div class="lines l3"></div></li>
      <li>Como muda o Sr. Alberto do início para o fim da cena? Que didascália o mostra?<div class="lines l3"></div></li>
      <li>«É um farol.» Explica a <b>metáfora</b>.<div class="lines l3"></div></li>
      <li>Identifica o sujeito, o CD e o CI: «O Sr. Alberto estende a manivela à Inês.»<div class="lines l1"></div></li>
      <li>A pares, leiam a cena em voz alta. Depois, escrevam mais três falas para a continuar. <span class="pill oral">Oralidade</span><div class="lines l3"></div></li>
    </ol>'''))

# ------------------------------------------------------------------ CIRCUITOS DE GRAMÁTICA
P.append(page('u5-g1', 'v-oficina-r', 'Circuito de gramática 1', f'''
    <div class="kicker"><b>Circuito 1</b> <span class="skill sk-gra">Gramática</span> O verbo e a frase</div>
    <h1 class="title">Frase ativa, conjuntivo <em>e relativas</em></h1>
    <div class="u5-gc">
      <div class="gc"><div class="gc-h"><b>A</b> Ativa e passiva <span>p. {ref('s21')}</span></div>
        <p>Passa à passiva ou à ativa, mantendo o tempo verbal.</p>
        <ol class="mini" type="a"><li>O narrador descreve o castelo.</li><li>Violeta foi expulsa pelo rei.</li><li>Os três irmãos encontraram um cofre.</li><li>O júri escolherá o melhor anúncio.</li></ol>
        <div class="lines l4"></div></div>
      <div class="gc"><div class="gc-h"><b>B</b> Conjuntivo <span>p. {ref('u2-n4-g')}</span></div>
        <p>Completa com o verbo no conjuntivo.</p>
        <ol class="mini" type="a"><li>Espero que tu <span class="blank w2"></span> (ler) o conto até sexta.</li><li>Talvez o cinema <span class="blank w2"></span> (reabrir) no verão.</li><li>Se eu <span class="blank w2"></span> (encontrar) um tesouro, dividia-o.</li><li>Quando <span class="blank w2"></span> (chegar) ao palco, respira fundo.</li></ol>
        <div class="lines l1"></div></div>
      <div class="gc"><div class="gc-h"><b>C</b> Pronome relativo <span>p. {ref('u2-n2-g')}</span></div>
        <p>Junta as frases com um pronome relativo (<i>que, quem, o qual, onde, cujo</i>).</p>
        <ol class="mini" type="a"><li>Li um conto. O conto passa-se nas Astúrias.</li><li>Esta é a vila. Na vila fica o Cinema Aurora.</li><li>O poeta escreveu «Sísifo». O nome verdadeiro do poeta era Adolfo.</li></ol>
        <div class="lines l3"></div></div>
      <div class="gc"><div class="gc-h"><b>D</b> Tempos do indicativo <span>p. {ref('u2-n7-g')}</span></div>
        <p>Identifica o tempo das formas sublinhadas.</p>
        <ol class="mini" type="a"><li>Os irmãos <u>eram</u> os fidalgos mais famintos.</li><li>Guanes <u>partiu</u> para Retortilho.</li><li>O tesouro ainda lá <u>está</u>.</li><li>Rui <u>tinha pensado</u> em tudo.</li><li>Amanhã <u>projetarás</u> tu.</li></ol>
        <div class="lines l2"></div></div>
      <div class="gc wide"><div class="gc-h"><b>I</b> Formação de palavras <span>p. {ref('u2-n5-g')}</span></div>
        <p>Indica o processo de formação: <b>derivação</b> (prefixação, sufixação, parassíntese), <b>composição</b> ou outro.</p>
        <ol class="mini two" type="a"><li>projecionista</li><li>descontente</li><li>guarda-chuva</li><li>entristecer</li><li>bilheteira</li><li>desconfiança</li><li>madrugada <i>(atenção: não é formada!)</i></li><li>luso-descendente</li></ol>
        <div class="lines l2"></div></div>
    </div>'''))

P.append(page('u5-g2', 'v-oficina-r', 'Circuito de gramática 2', f'''
    <div class="kicker"><b>Circuito 2</b> <span class="skill sk-gra">Gramática</span> A frase complexa e as funções sintáticas</div>
    <h1 class="title">Orações <em>e funções</em></h1>
    <div class="u5-gc">
      <div class="gc wide"><div class="gc-h"><b>E</b> Classificar orações <span>p. {ref('u2-n1-g')} · {ref('u2-n3-g')} · {ref('u3-p1-g')}</span></div>
        <p>Classifica a oração sublinhada: <b>relativa</b>, <b>completiva</b>, <b>condicional</b> ou <b>final</b>.</p>
        <ol class="mini two" type="a"><li>Rui disse <u>que o tesouro era dos três</u>.</li><li><u>Se o sabes</u>, cumpre o teu dever.</li><li>Guanes foi à vila <u>para comprar os alforges</u>.</li><li>O cofre <u>que encontraram</u> estava cheio de ouro.</li><li>Não sei <u>se o filme vale cinco estrelas</u>.</li><li><u>Caso chova</u>, o sarau é no ginásio.</li></ol>
        <div class="lines l2"></div></div>
      <div class="gc wide"><div class="gc-h"><b>F</b> Funções sintáticas <span>p. {ref('u4-l2-g')} · {ref('u2-n5-g')} · {ref('u2-n6-g')}</span></div>
        <p>Identifica: sujeito (S), complemento direto (CD), complemento indireto (CI), modificador do grupo verbal (MGV), modificador do nome (MN).</p>
        <ol class="mini" type="a"><li>Na primavera, os três irmãos encontraram um velho cofre de ferro.</li><li>O projecionista mostrou a cabina à rapariga curiosa.</li><li>Violeta ofereceu ao pai um jantar sem sal.</li><li>A crítica d'<i>A Lupa</i> elogiou a fotografia do filme.</li></ol>
        <div class="lines l4"></div></div>
      <div class="gc"><div class="gc-h"><b>G</b> Pronomes átonos <span>p. {ref('u2-n6-g')}</span></div>
        <p>Substitui os complementos por pronomes.</p>
        <ol class="mini" type="a"><li>Rostabal matou Guanes.</li><li>Guanes deu o vinho aos irmãos.</li><li>Vou contar a história à turma.</li></ol>
        <div class="lines l3"></div></div>
      <div class="gc"><div class="gc-h"><b>H</b> Frase simples ou complexa? <span>p. {ref('u2-n1-g')}</span></div>
        <p>Conta os verbos e classifica.</p>
        <ol class="mini" type="a"><li>O tesouro ainda lá está.</li><li>Rui ergueu o braço e começou a falar.</li><li>Quando anoiteceu, dois corvos pousaram no corpo.</li></ol>
        <div class="lines l3"></div></div>
    </div>'''))

# ------------------------------------------------------------------ TESTE DE TREINO
P.append(page('u5-t', '', 'Teste de treino', '''
    <div class="kicker"><b>Teste de treino</b> 45 minutos · individual · sem consulta</div>
    <h1 class="title">Prova <em>mista</em></h1>
    <div class="u5-tx">
      <div class="tx-h">Texto · Carta de um espectador</div>
      <p><span class="pn">1</span>Caro Sr. Alberto: escrevo-lhe porque ontem, na última sessão em película, percebi finalmente por que razão o meu avô me trazia ao Aurora todos os domingos. Não era pelos filmes. Era pela escuridão partilhada, por aquele minuto em que a sala inteira respira ao mesmo tempo.</p>
      <p><span class="pn">5</span>O senhor foi, durante quarenta anos, o homem invisível desta vila. Ninguém o via, mas todos víamos o que o senhor nos mostrava. Se um dia a cabina ficar vazia, espero que alguém se lembre de que houve uma luz que nunca se apagou. Obrigada. — Ana, 13 anos</p>
    </div>
    <div class="u5-tq">
      <div class="tq-g"><b>Grupo I · Leitura</b><span>40%</span></div>
      <ol class="qs">
        <li>Qual é o motivo da carta? <span class="pt">(8)</span><div class="lines l1"></div></li>
        <li>«Não era pelos filmes.» Então, era porquê? Explica por palavras tuas. <span class="pt">(10)</span><div class="lines l2"></div></li>
        <li>Explica o sentido de «o homem invisível desta vila». <span class="pt">(10)</span><div class="lines l2"></div></li>
        <li>Transcreve uma antítese e uma metáfora. <span class="pt">(12)</span><div class="lines l1"></div></li>
      </ol>
      <div class="tq-g"><b>Grupo II · Gramática</b><span>30%</span></div>
      <ol class="qs" start="5">
        <li>Classifica a oração «Se um dia a cabina ficar vazia». <span class="pt">(6)</span><div class="lines l1"></div></li>
        <li>Identifica o tempo e o modo de «ficar» em «Se um dia a cabina ficar vazia». <span class="pt">(6)</span><div class="lines l1"></div></li>
        <li>Passa à passiva: «O avô trazia a neta ao Aurora.» <span class="pt">(6)</span><div class="lines l1"></div></li>
        <li>Indica a função sintática de «o meu avô» e de «todos os domingos» (§1). <span class="pt">(6)</span><div class="lines l1"></div></li>
        <li>Classifica a palavra «invisível» quanto ao processo de formação. <span class="pt">(6)</span><div class="lines l1"></div></li>
      </ol>
    </div>'''))

P.append(page('u5-t2', '', 'Teste de treino', '''
    <div class="kicker"><b>Teste de treino</b> Continuação</div>
    <div class="u5-tq">
      <div class="tq-g"><b>Grupo III · Escrita</b><span>30%</span></div>
      <div class="u5-pl"><b>Planifica antes de escrever</b>
        <div class="pl-r"><b>Saudação</b><i></i></div><div class="pl-r"><b>Agradeço…</b><i></i></div><div class="pl-r"><b>O momento</b><i></i></div><div class="pl-r"><b>O conselho</b><i></i></div><div class="pl-r"><b>Despedida</b><i></i></div></div>
      <ol class="qs" start="10">
        <li>Responde à Ana como se fosses o Sr. Alberto (120 a 160 palavras): agradece, conta um momento marcante da tua vida no cinema e dá-lhe um conselho. <span class="pt">(30)</span><div class="lines l18"></div></li>
      </ol>
    </div>
    <table class="fill rub u5-rb">
      <tr><th>Critérios do Grupo III</th><th style="width:22mm">Pontos</th><th style="width:22mm">Os meus</th></tr>
      <tr><td>Formato de carta: saudação, corpo, despedida, assinatura</td><td>5</td><td></td></tr>
      <tr><td>Conteúdo: agradecimento, momento narrado, conselho</td><td>10</td><td></td></tr>
      <tr><td>Organização em parágrafos e uso de conectores</td><td>5</td><td></td></tr>
      <tr><td>Correção linguística: ortografia, pontuação, concordâncias</td><td>7</td><td></td></tr>
      <tr><td>Extensão (120–160 palavras)</td><td>3</td><td></td></tr>
    </table>'''))

# ------------------------------------------------------------------ REFLEXÃO + PASSAPORTE
P.append(page('u5-refl', '', 'O leitor que és agora', '''
    <div class="kicker"><b>Unidade 5</b> <span class="skill sk-esc">Escrita</span> <span class="skill sk-ora">Oralidade</span> Reflexão</div>
    <h1 class="title">O leitor <em>que és agora</em></h1>
    <div class="u5-pass">
      <div class="ps-h"><b>Passaporte da última noite</b><span>carimbo do professor em cada banca</span></div>
      <div class="ps-g"><div><i>1</i>Publicidade</div><div><i>2</i>Crítica</div><div><i>3</i>Narrativa</div><div><i>4</i>Poesia</div><div><i>5</i>Teatro</div></div>
    </div>
    <div class="u5-top">
      <div class="tp-h">O meu ano em cinco escolhas</div>
      <div class="tp"><b>O texto que mais gostei de ler</b><i></i></div>
      <div class="tp"><b>O verso que sei de cor</b><i></i></div>
      <div class="tp"><b>A personagem que me ensinou alguma coisa</b><i></i></div>
      <div class="tp"><b>O trabalho de que mais me orgulho</b><i></i></div>
      <div class="tp"><b>O que ainda tenho de melhorar</b><i></i></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escreve uma carta ao aluno que vai começar o 8.º ano no próximo setembro (120 a 150 palavras): o que vai encontrar, o que vai adorar, o que vai achar difícil, e um conselho de leitor para leitor.</p>
      <div class="lines l12"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Lê a tua carta à turma em 1 minuto. Ouve as dos colegas: que conselho repetiram mais? <span class="pill oral">Oralidade</span></p>
      <div class="lines l2"></div>
    </div></div>'''))

# ------------------------------------------------------------------ SOLUÇÕES (2 pp.)
P.append(page('u5-sol', 'backmatter', 'Soluções', f'''
    <div class="kicker"><b>Unidade 5</b> Soluções · 1 de 2</div>
    <div class="bm-cols">
      <div class="sol">
        <p><b>p. {ref('u5-e1')} · Banca 1.</b> 1. Comercial: há uma marca (Maré), um produto e um preço/promoção («ganha um capacete na compra»). 2. Jovens e famílias que gostam de andar ao ar livre: «levares o mundo contigo», «pedala», a praça do cinema. 3. Hipérbole: «Pedala mais longe do que o mar» · comparação: «leve como uma gaivota», «forte como o farol» · enumeração: «Quadro de alumínio, sete mudanças, luzes LED…» — acumula vantagens e faz o produto parecer completo. 4. <i>Pedala</i>, <i>Experimenta</i>, <i>ganha</i>, <i>Vai</i>: dirige-se diretamente ao leitor (tu). 5. A corrente da bicicleta e a corrente do mar (ou «ir com a corrente» = seguir a moda). 6. Para não chamarem a atenção: limitam a oferta (stock, modelo único).</p>
        <p><b>p. {ref('u5-e1-o')} · Oficina 1.</b> 2. a) A Maré 8 é recomendada pelos ciclistas. b) Um capacete é oferecido pela marca. c) A campanha será lançada pela Câmara em setembro. 3. Sujeito nulo subentendido: <i>tu</i> (imperativo).</p>
        <p><b>p. {ref('u5-e2')} · Banca 2.</b> 1. O filme vale a pena, apesar de um argumento repetitivo (§1 e §5). 2. Factos: realização de Inês Barros; 98 minutos; passa-se no Alentejo em 1998 · Opiniões: «O melhor do filme está na imagem»; «O problema é o argumento». 3. A imagem/fotografia: o feixe do projetor, os rostos como retratos antigos. 4. O argumento: repete-se e não surpreende. 5. Hipérbole: sublinha que o filme parece longo e aborrecido. 6. Sim: há elogios e críticas equilibrados — nem ótimo, nem mau.</p>
        <p><b>p. {ref('u5-e2-o')} · Oficina 2.</b> 3. a) A fotografia é assinada por Tiago Reis. b) O projecionista foi aplaudido pela plateia.</p>
        <div class="u5-model"><b>Modelo · campanha (Oficina 1)</b><p><i>Vai à escola com as tuas pernas!</i> Todas as manhãs, mil carros enchem a rua da escola. Tu podes mudar isso. A bicicleta é silenciosa, barata, saudável e não deita fumo. Pega na tua, chama um amigo e pedala até às aulas: chegas mais acordado do que o sol. A Câmara oferece estacionamento seguro em todas as escolas. <b>Vila Nova do Farol. Aqui, quem pedala chega primeiro.</b></p></div>
      </div>
      <div class="sol">
        <p><b>p. {ref('u5-e3-q')} · Banca 3.</b> Narrador não participante, ausente, que comenta («Oh! D. Rui, o avisado, era veneno!»). Espaço físico: Paços de Medranhos, mata de Roquelanes, Retortilho. Espaço social: fidalgos pobres, famintos. Tempo: Idade Média; a ação principal dura um dia de primavera (de manhã ao anoitecer). Personagens: os três irmãos — ambiciosos, desconfiados, violentos. 1. Situação inicial: a miséria dos irmãos (§1–2) · desenvolvimento: a descoberta e os planos de traição · desenlace: as três mortes e a frase final. 2. A ganância/ambição: «a miséria tornara estes senhores mais bravios que lobos». 3. Ironia: o «avisado» é enganado e morre envenenado. 4. A ganância destrói quem a tem; o ouro não serviu a ninguém. 5. «mais bravios que lobos»: a fome tornou-os ferozes como animais. 6. Subordinada substantiva completiva. 7. Subordinada adjetiva relativa. 8. Rui berrou que era veneno.</p>
        <p><b>p. {ref('u5-e4')} · Banca 4.</b> 1. Duas quadras e dois tercetos; ABBA ABBA CDC DCD. 2. A / mor / é_um / fo / go / que_ar / de / sem / se / ver = 10 · decassílabo. 3. «é» — anáfora. 4. Antítese/paradoxo: o amor é feito de contrários, não se define com lógica. 5. Como pode o amor criar concordância nos corações, se é contraditório em si mesmo? 6. Camões define o amor em geral, com contradições; Florbela vive um amor absoluto, por uma pessoa, quase religioso.</p>
        <p><b>p. {ref('u5-e5')} · Banca 5.</b> 1. Espaço: «Cabina de projeção do Cinema Aurora» · luz: «Um feixe de luz atravessa a cabina» · tom: «(Baixinho, maravilhada.)». 2. «Então é por isso que está tão triste.»: o público percebe o que Inês pensa. 3. De fechado e triste para sorridente e generoso: «(Sorri pela primeira vez.)», «(Estende-lhe a manivela.)». 4. O projetor, como um farol, guiava as pessoas para o cinema. 5. S: O Sr. Alberto · CD: a manivela · CI: à Inês.</p>
        <div class="u5-model"><b>Modelo · crítica de cinco estrelas (Oficina 2)</b><p>Há filmes que nos devolvem uma coisa que julgávamos perdida. <i>A Última Sessão</i> é um deles, e merece as cinco estrelas. Em primeiro lugar, pela imagem: o feixe do projetor, filmado por Tiago Reis como um farol, é das mais belas metáforas do cinema português. Em segundo lugar, porque a repetição das sete noites não é um defeito, é o próprio tema — a vila regressa, noite após noite, tal como nós regressamos aos filmes de que gostamos. Rui Mendes, que diz tudo com as mãos, fecha o filme com uma dignidade rara. Sim, sabemos como acaba. Mas também sabemos como acaba um pôr do sol, e não deixamos de olhar. Obrigatório.</p></div>
      </div>
    </div>'''))

P.append(page('u5-sol2', 'backmatter', 'Soluções', f'''
    <div class="kicker"><b>Unidade 5</b> Soluções · 2 de 2</div>
    <div class="bm-cols">
      <div class="sol">
        <p><b>p. {ref('u5-g1')} · Circuito 1.</b> A. a) O castelo é descrito pelo narrador. b) O rei expulsou Violeta. c) Um cofre foi encontrado pelos três irmãos. d) O melhor anúncio será escolhido pelo júri. B. a) leias · b) reabra · c) encontrasse · d) chegares. C. a) Li um conto que se passa nas Astúrias. b) Esta é a vila onde fica o Cinema Aurora. c) O poeta cujo nome verdadeiro era Adolfo escreveu «Sísifo». D. a) pretérito imperfeito · b) pretérito perfeito · c) presente · d) pretérito mais-que-perfeito composto · e) futuro. I. a) sufixação · b) prefixação · c) composição · d) parassíntese (en- + triste + -ecer) · e) sufixação · f) prefixação e sufixação (des- + confiar + -ança) · g) palavra simples (não formada) · h) composição.</p>
        <p><b>p. {ref('u5-g2')} · Circuito 2.</b> E. a) completiva · b) condicional · c) final · d) relativa · e) completiva · f) condicional. F. a) MGV: Na primavera · S: os três irmãos · CD: um velho cofre de ferro (MN: velho, de ferro). b) S: O projecionista · CD: a cabina · CI: à rapariga curiosa (MN: curiosa). c) S: Violeta · CI: ao pai · CD: um jantar sem sal (MN: sem sal). d) S: A crítica d'A Lupa (MN: d'A Lupa) · CD: a fotografia do filme (MN: do filme). G. a) Rostabal matou-o. b) Guanes deu-lho. c) Vou contar-lha. H. a) simples · b) complexa (coordenação) · c) complexa (subordinação).</p>
      </div>
      <div class="sol">
        <p><b>p. {ref('u5-t')} · Teste de treino.</b> 1. Agradecer ao projecionista, depois da última sessão em película. 2. Pela experiência de estar com os outros no escuro, a sentir o mesmo ao mesmo tempo. 3. Ninguém o via na cabina, mas era ele quem mostrava os filmes a todos. 4. Antítese: «Ninguém o via, mas todos víamos» · metáfora: «uma luz que nunca se apagou». 5. Subordinada adverbial condicional. 6. Futuro do conjuntivo. 7. A neta era trazida ao Aurora pelo avô. 8. «o meu avô»: sujeito · «todos os domingos»: modificador do grupo verbal. 9. Derivação por prefixação (in- + visível). 10. Resposta pessoal; critérios: formato de carta, agradecimento, momento narrado, conselho, 120–160 palavras.</p>
        <div class="u5-model"><b>Modelo · Grupo III</b><p>Querida Ana: a tua carta está pregada na porta da cabina, onde a leio todas as manhãs. Obrigado. Durante quarenta anos pensei que ninguém sabia que eu existia — afinal, havia pelo menos uma espectadora atenta. O meu momento preferido foi em 1985, numa noite de temporal: faltou a luz na vila, mas o gerador da cabina aguentou-se, e a sala inteira ficou a ver o filme como se estivesse num barco, no meio do mar. Ninguém saiu. O meu conselho é simples: nunca deixes de ir ao cinema com outras pessoas. Um filme visto sozinho é uma história; visto com os outros, é uma memória. Um abraço do teu projecionista, Alberto.</p></div>
        <div class="u5-crit"><b>Grelha do teste</b><span>I · 40</span><span>II · 30</span><span>III · 30</span><span>Total · 100</span></div>
      </div>
    </div>
    <div class="memo sm">
      <div class="memo-h">Cartão de memória · o ano numa página</div>
      <div class="memo-g">
        <div class="m-s"><b>Ler</b><ul><li>Publicidade: quem vende? a quem? como?</li><li>Crítica: tese, argumentos, factos e opiniões.</li><li>Narrativa: narrador, ação, personagens, espaço, tempo.</li><li>Poesia: estrofe, rima, métrica, recursos.</li><li>Teatro: falas, didascálias, aparte, monólogo.</li></ul></div>
        <div class="m-r"><b>Escrever</b><ul><li>Planifica · escreve · revê.</li><li>Opinião: tese + 2 argumentos + exemplos + conclusão.</li><li>Comentário: tema + recurso + efeito + citação.</li><li>Cena: personagens, didascálias, falas.</li></ul></div>
        <div class="m-g"><b>Gramática</b><ul><li>Ativa/passiva · conjuntivo · tempos.</li><li>Relativas, completivas, condicionais, finais.</li><li>S, CD, CI, modificadores, pronomes átonos.</li></ul></div>
      </div>
    </div>'''))

(R / 'src' / 'u5.html').write_text("\n".join(P))
print(len(P), 'pages')
