"""Generate src/u6.html — Unidade 6 · Avaliação (Y8 PT). 20 pp."""
import pathlib, html as H
R = pathlib.Path(__file__).parent
T = R / "texts"
C = "https://commons.wikimedia.org/wiki/File:"


def rail(t): return f'<div class="rail"><span>{t}</span></div>'
def folio(t): return f'<div class="folio"><span class="n"></span><span class="t">{t}</span></div>'
def ref(i): return f'<span class="ref" data-ref="{i}"></span>'


def page(id_, cls, railt, inner, foliot=None):
    return f'''
<section id="{id_}" class="page v-ava {cls}">
  {rail(railt)}
  <div class="inner">
{inner}
  </div>
  {folio(foliot or railt)}
</section>'''


def q(n, text, pts, lines=2, extra=''):
    ln = f'<div class="lines l{lines}"></div>' if lines else ''
    return f'<li value="{n}">{text} <span class="pt">({pts})</span>{extra}{ln}</li>'


def head(n, sem, mins):
    return f'''<div class="u6-th">
      <div class="th-l"><span class="th-k">Teste de avaliação {n}</span><b>Português · 8.º ano</b><small>{sem} · {mins} minutos · sem consulta</small></div>
      <div class="th-r"><div><span>Nome</span><i></i></div><div class="two"><div><span>N.º</span><i></i></div><div><span>Turma</span><i></i></div><div><span>Data</span><i></i></div></div></div>
    </div>
    <div class="u6-cot"><span>Cotações</span><b>I · 35</b><b>II · 15</b><b>III · 20</b><b>IV · 30</b><b class="tot">Total · 100</b><em>Classificação <i></i></em></div>'''


def grp(n, title, pts):
    return f'<div class="tq-g u6-g"><b>Grupo {n} · {title}</b><span>{pts} pontos</span></div>'


P = []
# ------------------------------------------------------------------ OPENER
P.append('''
<section id="u6" class="page v-ava opener u6-opener">
  <div class="bleed" style="background-image:url(../art/jpg/u6_opener.jpg); background-position: 50% 55%;"></div>
  <div class="opener-card">
    <div class="kicker"><b>Unidade 6</b> Avaliação</div>
    <h1 class="title">O teu <em>veredicto</em></h1>
    <p class="lede">Chegou a vez de mostrares o que sabes. Nesta unidade estão os dois testes do ano, as tarefas de oralidade, de escrita e de teatro, os critérios com que vais ser avaliado — e exemplos de respostas a três níveis, para perceberes o que separa um trabalho razoável de um trabalho excelente. Não há surpresas: tudo o que se avalia aqui, já o treinaste.</p>
    <div class="opener-qs">
      <div><span>?</span>Sabes exatamente o que te vai ser pedido — e como vai ser avaliado?</div>
      <div><span>?</span>Consegues corrigir o teu próprio teste e descobrir porque erraste?</div>
      <div><span>?</span>Que nota dás ao teu ano como leitor?</div>
    </div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Unidade 6</span></div>
</section>''')

# ------------------------------------------------------------------ PROGRAMA
P.append(page('u6-prog', '', 'Programa', f'''
    <div class="kicker"><b>Unidade 6</b> O que está nesta unidade</div>
    <h1 class="title">Seis provas, <em>regras claras</em></h1>
    <div class="u6-pk">
      <div class="pk w"><span>1</span><b>Teste 1</b><small>1.º semestre · 90 min</small><p>Narrativa e publicidade · gramática · artigo de opinião</p><em>p. {ref('u6-t1')}</em></div>
      <div class="pk w"><span>2</span><b>Teste 2</b><small>2.º semestre · 90 min</small><p>Poesia e teatro · gramática · escrita de uma cena</p><em>p. {ref('u6-t2')}</em></div>
      <div class="pk"><span>3</span><b>Apresentação oral</b><small>individual · 3 min</small><p>Um livro, três minutos</p><em>p. {ref('u6-oral')}</em></div>
      <div class="pk"><span>4</span><b>Texto escrito</b><small>individual · em aula</small><p>Crítica ou artigo de opinião</p><em>p. {ref('u6-esc')}</em></div>
      <div class="pk"><span>5</span><b>Cena de teatro</b><small>em grupo · 2 semanas</small><p>Escrever e representar</p><em>p. {ref('u6-dra')}</em></div>
      <div class="pk"><span>6</span><b>Veredicto do ano</b><small>autoavaliação</small><p>O teu balanço final</p><em>p. {ref('u6-fim')}</em></div>
    </div>
    <div class="u6-two">
      <div class="u6-box">
        <div class="bx-h">Como vais ser avaliado</div>
        <table class="fill u6-w"><tr><th>Domínio</th><th style="width:22mm">Peso</th></tr>
          <tr><td>Leitura e Educação literária (testes)</td><td>35%</td></tr>
          <tr><td>Gramática (testes)</td><td>20%</td></tr>
          <tr><td>Escrita (testes e texto escrito)</td><td>25%</td></tr>
          <tr><td>Oralidade (apresentação e cena)</td><td>20%</td></tr></table>
        <p class="tiny">Pesos de referência: cada escola ajusta-os aos seus critérios.</p>
      </div>
      <div class="u6-box">
        <div class="bx-h">Escala de classificação</div>
        <div class="u6-sc"><div><b>0–19</b><span>Muito insuficiente</span></div><div><b>20–49</b><span>Insuficiente</span></div><div><b>50–69</b><span>Suficiente</span></div><div><b>70–89</b><span>Bom</span></div><div><b>90–100</b><span>Muito bom</span></div></div>
      </div>
    </div>
    <div class="u6-rules">
      <div class="bx-h">Antes de qualquer teste</div>
      <div><i>1</i><span>Lê <b>todas</b> as perguntas antes de começares. Começa pelo grupo em que te sentes mais seguro.</span></div>
      <div><i>2</i><span>Olha para a cotação: uma pergunta de 6 pontos pede mais do que uma linha.</span></div>
      <div><i>3</i><span>Responde com <b>frases completas</b> e prova tudo com o texto (cita entre aspas).</span></div>
      <div><i>4</i><span>Guarda 10 minutos para reler: acentos, concordâncias, pontuação.</span></div>
      <div><i>5</i><span>Depois da correção, preenche a <b>grelha de autocorreção</b> (p. {ref('u6-auto')}).</span></div>
    </div>
    <div class="note-f">As soluções e os critérios de correção dos testes estão na <b>secção do professor</b> (p. {ref('u6-prof1')}): o professor decide quando os mostra.</div>'''))

# ------------------------------------------------------------------ TESTE 1 · texto A (flow)
suave = (T / 'suave_fim.txt').read_text().split('\n\n')
body = "\n".join(f'<p><span class="pn">{i+1}</span>{H.escape(p, quote=False)}</p>' if i in (0, 4, 9) else f'<p>{H.escape(p, quote=False)}</p>' for i, p in enumerate(suave))
P.append(f'''
<section id="u6-t1" class="page v-ava flow">
  {rail('Teste 1 · Grupo I')}
  <div class="inner">
    <div class="flow-head">
      {head(1, '1.º semestre', 90)}
      {grp('I', 'Leitura e Educação literária', 35)}
      <div class="u6-ctx"><div><h2 class="tx-title">O Suave Milagre <small>(final)</small></h2>
        <p class="tx-by">Eça de Queirós · <i>Contos</i> (1902) · domínio público</p>
        <p class="u6-sum"><b>O início do conto.</b> Na Galileia, corre a notícia de um Rabi que faz milagres. Dois homens poderosos querem encontrá-lo: Obed, um velho rico que perdeu os rebanhos e as vinhas, e Públio Sétimo, um centurião romano cuja filha única está doente. Mandam servos e soldados à sua procura — mas ninguém o encontra. Lê agora o final.</p></div>
        <div class="qr-inline u6-qr"><div class="qr" style="width:21mm;height:21mm">{{{{QR:https://commons.wikimedia.org/?curid=27852383}}}}</div><span><b>Depois do teste</b>, ouve o conto inteiro (LibriVox, Wikimedia Commons, domínio público).</span></div>
      </div>
    </div>
    <div class="flow-body cols2">
{body}
<p class="src">Eça de Queirós, «O Suave Milagre», em <i>Contos</i> (1902). Texto da Wikisource, ortografia atualizada.</p>
<div class="u6-fq-h">Grupo I · questões</div>
<div class="u6-fq"><ol class="qs u6-q">{q(1, 'Onde e como vivem a viúva e o filho? Transcreve duas expressões que mostrem a sua pobreza.', 5, 2)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(2, '«espessamente a miséria cresceu como o bolor sobre cacos perdidos num ermo» (§1). Identifica o recurso expressivo e explica o seu efeito.', 5, 2)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(3, 'Que papel tem o mendigo no desenvolvimento da ação?', 4, 2)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(4, 'Porque é que a mãe não quer partir à procura do Rabi? Apresenta duas razões.', 5, 2)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(5, 'Classifica o narrador quanto à presença na história. Justifica.', 4, 1)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(6, 'Divide o excerto em três momentos e dá um título a cada um.', 6, 2)}</ol></div>
<div class="u6-fq"><ol class="qs u6-q">{q(7, 'Os ricos e os fortes não encontraram Jesus; foi ele que veio ter com a criança pobre. Explica o título do conto a partir do final.', 6, 3)}</ol></div>
<div class="u5-voc"><div class="vc-h">Vocabulário</div><p><b>enxerga</b> colchão pobre · <b>jazer</b> estar deitado · <b>mirrar</b> secar, definhar · <b>engelhar</b> enrugar · <b>ermo</b> lugar deserto · <b>quinteiro</b> pátio · <b>farnel</b> provisões para a viagem · <b>entrevado</b> que não se pode mexer · <b>trôpega</b> que anda com dificuldade · <b>Rabi</b> mestre (tratamento dado a Jesus)</p></div>
    </div>
  </div>
  {folio('Teste 1 · Grupo I')}
</section>''')

P.append(page('u6-t1-q', '', 'Teste 1 · Grupos II e III', f'''
    {grp('II', 'Leitura · texto publicitário', 15)}
    <div class="u6-ad">
      <div class="ad-h2">Uma feira onde os livros<br>te escolhem a ti.</div>
      <p><b>Feira do Livro de Vila Nova do Farol</b> · Praça do Cinema Aurora · 1 a 10 de junho. Mais de 5000 livros, 30 editoras, sessões de autógrafos todos os dias às 18 h. Traz a tua família, descobre um autor novo e leva para casa uma história que nunca mais vais esquecer. Entrada livre.</p>
      <div class="ad-s2">Ler é a viagem mais barata do mundo.</div>
      <small>Uma iniciativa da Câmara Municipal e da Biblioteca Municipal.</small>
    </div>
    <ol class="qs u6-q two">
      {q(8, 'É publicidade comercial ou não comercial? Justifica.', 3, 2)}
      {q(9, 'Identifica o recurso expressivo do slogan e explica-o.', 4, 2)}
      {q(10, 'Transcreve dois verbos no imperativo. A quem se dirige o anúncio?', 4, 2)}
      {q(11, 'Transcreve um facto e uma opinião do anúncio.', 4, 2)}
    </ol>
    {grp('III', 'Gramática', 20)}
    <ol class="qs u6-q">
      {q(12, 'Passa à frase passiva: «O mendigo contou a história à viúva.»', 3, 1)}
      {q(13, 'Classifica as orações sublinhadas: <b>a)</b> <u>Se o Rabi viesse</u>, o menino sararia. <b>b)</b> A mãe saiu de casa <u>para procurar o Rabi</u>.', 4, 1)}
      {q(14, 'Junta as duas frases numa só, usando um pronome relativo: «A viúva vivia num casebre. O casebre ficava na prega dum cerro.»', 3, 1)}
      {q(15, 'Completa com o verbo no conjuntivo: <b>a)</b> Espero que o Rabi <span class="blank w2"></span> (vir) depressa. <b>b)</b> Quando tu <span class="blank w2"></span> (encontrar) o Rabi, fala-lhe de mim.', 4, 0)}
      {q(16, 'Identifica as funções sintáticas dos constituintes: «Um dia, um mendigo deu pão à viúva.»', 4, 2)}
      {q(17, 'Classifica a palavra «devagar» em «abrindo devagar a porta» e indica o seu valor.', 2, 1)}
    </ol>'''))

P.append(page('u6-t1-g', '', 'Teste 1 · Grupo IV', f'''
    {grp('IV', 'Escrita', 30)}
    <div class="u6-task">
      <p>Escolhe <b>um</b> dos temas e escreve um texto de <b>180 a 240 palavras</b>.</p>
      <div class="tk"><b>A · Artigo de opinião</b><span>«Os ricos e os fortes não encontraram Jesus; encontrou-o uma criança pobre.» A humildade abre portas que o poder fecha? Defende a tua posição com dois argumentos e exemplos.</span></div>
      <div class="tk"><b>B · Crítica</b><span>Escreve a crítica de um livro ou filme que tenhas conhecido este semestre: apresentação, tese, dois argumentos (um pode ser uma reserva), conclusão e classificação.</span></div>
    </div>
    <div class="u6-plan"><div class="bx-h">Planificação (não conta para a classificação)</div>
      <div class="u6pw"><b>Tese</b><i></i></div><div class="u6pw"><b>Argumento 1</b><i></i></div><div class="u6pw"><b>Argumento 2</b><i></i></div><div class="u6pw"><b>Conclusão</b><i></i></div></div>
    <div class="lines l16"></div>
    <div class="u6-mini-crit"><span>Critérios</span><b>Tema e tese · 8</b><b>Argumentação · 10</b><b>Estrutura e coesão · 6</b><b>Correção linguística · 6</b></div>'''))

P.append(page('u6-t1-e', '', 'Teste 1 · Grupo IV', '''
    <div class="kicker"><b>Teste 1</b> Grupo IV · continuação</div>
    <div class="lines l30"></div>
    <div class="u6-count"><span>Número de palavras</span><i></i><span>Revi: acentos</span><i class="ck"></i><span>concordâncias</span><i class="ck"></i><span>pontuação</span><i class="ck"></i><span>parágrafos</span><i class="ck"></i></div>
    <div class="u6-end">Fim do Teste 1</div>'''))

# ------------------------------------------------------------------ TESTE 2
desc = (T / 'descalca.txt').read_text().split('\n\n')
vn = 0
stz = []
for i, st in enumerate(desc):
    ls = []
    for l in st.split('\n'):
        vn += 1
        num = f'<span class="vln">{vn}</span>' if vn in (1, 5, 10, 15) else ''
        ls.append(f'<span class="vl">{num}{H.escape(l, quote=False)}</span>')
    lab = 'Mote' if i == 0 else f'{i}.ª volta'
    stz.append(f'<div class="vst"><span class="u6-lab">{lab}</span>{"".join(ls)}</div>')
P.append(page('u6-t2', '', 'Teste 2 · Grupo I', f'''
    {head(2, '2.º semestre', 90)}
    {grp('I', 'Educação literária · texto poético', 35)}
    <div class="u6-poem">
      <div class="u6-pl"><h2 class="tx-title">Descalça vai para a fonte</h2><p class="tx-by">Luís de Camões · vilancete · domínio público</p>
        <div class="vpoem u6-vp">{"".join(stz)}</div>
        <p class="src">Luís de Camões, <i>Rimas</i>. Texto da Wikisource; mantém-se a grafia antiga de «Lianor» e «fermosa».</p></div>
      <div class="u6-pr">
        <div class="u5-voc"><div class="vc-h">Vocabulário</div><p><b>Lianor</b> Leonor · <b>fermosa</b> formosa · <b>segura</b> tranquila, sem perigo · <b>testo</b> tampa · <b>escarlata</b> tecido vermelho, fino · <b>sainho</b> casaquinho curto · <b>chamerlote</b> tecido de pelo de cabra · <b>vasquinha de cote</b> saia de todos os dias · <b>touca</b> pano que cobre a cabeça</p></div>
        <div class="qr-inline u6-qr"><div class="qr" style="width:21mm;height:21mm">{{{{QR:https://commons.wikimedia.org/?curid=49885164}}}}</div><span><b>Depois do teste</b>, ouve o poema (Carlos Gomes, Wikimedia Commons, domínio público).</span></div>
      </div>
    </div>
    <ol class="qs u6-q two">
      {q(1, 'O poema é um <b>vilancete</b>: um mote seguido de voltas. Indica quantos versos tem o mote e quantos tem cada volta.', 4, 2)}
      {q(2, 'Faz a escansão do verso 1 e classifica o verso quanto ao número de sílabas métricas.', 5, 0, '<div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>')}
      {q(3, 'Indica o esquema rimático da 1.ª volta.', 5, 1)}
      {q(4, 'Que verso se repete no fim de cada volta? Que efeito tem essa repetição?', 5, 2)}
      {q(5, 'Transcreve uma metáfora e uma comparação usadas para descrever Lianor e explica uma delas.', 6, 2)}
      {q(6, '«Tão linda que o mundo espanta» (v. 14): identifica o recurso expressivo.', 4, 1)}
      {q(7, '«Vai fermosa, e não segura.» Porque é que Lianor, sendo tão bela, «não vai segura»? Apresenta a tua interpretação.', 6, 3)}
    </ol>'''))

P.append(page('u6-t2-d', '', 'Teste 2 · Grupo II', f'''
    {grp('II', 'Educação literária · texto dramático', 15)}
    <div class="mini-play u6-play">
      <p class="tx-title sm">O ensaio geral</p>
      <p class="did">(Palco do auditório da escola, na véspera da estreia. Um trono de cartão, uma coroa de papel dourado caída no chão. MARTA, a encenadora, 14 anos, tem o guião na mão. RUI, que faz de rei, está sentado na beira do palco, de braços cruzados. Entra SOFIA, a correr, com o figurino de princesa ainda por abotoar.)</p>
      <p class="fala"><b>SOFIA</b> Desculpem, desculpem! O autocarro…</p>
      <p class="fala"><b>MARTA</b> <i class="di">(Sem levantar os olhos do guião.)</i> Vinte minutos, Sofia. Amanhã vêm os pais todos.</p>
      <p class="fala"><b>RUI</b> Pois. E o rei, amanhã, também não entra. <i class="di">(Levanta-se e pontapeia a coroa.)</i> Já disse: não digo aquela fala.</p>
      <p class="fala"><b>MARTA</b> Que fala?</p>
      <p class="fala"><b>RUI</b> «Minha filha, perdoa a este velho louco.» Toda a gente se vai rir de mim.</p>
      <p class="fala"><b>SOFIA</b> <i class="di">(À parte, a abotoar o vestido.)</i> Ninguém se ri de quem diz uma coisa daquelas a sério.</p>
      <p class="fala"><b>MARTA</b> <i class="di">(Fecha o guião. Pausa longa.)</i> Rui, é a fala mais importante da peça. É o momento em que o rei deixa de ser rei.</p>
      <p class="fala"><b>RUI</b> <i class="di">(Baixinho.)</i> É por isso mesmo.</p>
      <p class="did">(Silêncio. SOFIA apanha a coroa do chão, sacode-lhe o pó e estende-a a RUI.)</p>
      <p class="fala"><b>SOFIA</b> Então diz-ma a mim. Só uma vez. Sem público.</p>
      <p class="did">(RUI hesita. Olha para MARTA, que se senta na plateia vazia. A luz desce até ficarem só os dois no centro do palco.)</p>
    </div>
    <p class="src">Texto escrito para este manual.</p>
    <ol class="qs u6-q two">
      {q(8, 'Transcreve uma didascália de <b>espaço</b>, uma de <b>movimento</b> e uma de <b>luz</b>.', 4, 4)}
      {q(9, 'Identifica o <b>aparte</b> e explica o que revela sobre Sofia.', 4, 4)}
      {q(10, 'Qual é o conflito da cena? Entre que personagens?', 4, 4)}
      {q(11, 'Como achas que a cena termina? Justifica com um pormenor do texto.', 3, 4)}
    </ol>'''))

P.append(page('u6-t2-g', '', 'Teste 2 · Grupos III e IV', f'''
    {grp('III', 'Gramática', 20)}
    <ol class="qs u6-q">
      {q(12, 'Classifica a oração sublinhada: «Marta sabe <u>que a fala é a mais importante da peça</u>.»', 3, 1)}
      {q(13, 'Substitui os constituintes sublinhados por pronomes: <b>a)</b> Sofia estende <u>a coroa</u> <u>ao Rui</u>. <b>b)</b> Marta explica <u>a cena</u> <u>aos atores</u>.', 4, 1)}
      {q(14, 'Sublinha os advérbios e as locuções adverbiais e indica o seu valor: «De repente, Rui falou baixinho e nunca mais olhou para a plateia.»', 3, 1)}
      {q(15, 'Identifica o sujeito e o predicado: <b>a)</b> Chegou a Sofia. <b>b)</b> Desculpem! (Que tipo de sujeito tem?)', 4, 1)}
      {q(16, 'Identifica as funções sintáticas: «Na véspera da estreia, a encenadora deu o guião aos atores.»', 4, 2)}
      {q(17, 'Indica o processo de formação da palavra «encenadora».', 2, 1)}
    </ol>
    {grp('IV', 'Escrita', 30)}
    <div class="u6-task">
      <p>Escreve a <b>cena seguinte</b> de «O ensaio geral» (<b>150 a 200 palavras</b>). A cena deve ter:</p>
      <div class="req"><span>título e lista de personagens</span><span>pelo menos quatro didascálias (espaço, luz, tom, movimento)</span><span>um aparte ou um monólogo</span><span>a resolução do conflito: Rui diz a fala — ou não</span></div>
    </div>
    <div class="lines l12"></div>
    <div class="u6-mini-crit"><span>Critérios</span><b>Adequação ao género · 10</b><b>Coerência com a cena · 8</b><b>Criatividade · 6</b><b>Correção linguística · 6</b></div>'''))

P.append(page('u6-t2-e', '', 'Teste 2 · Grupo IV', '''
    <div class="kicker"><b>Teste 2</b> Grupo IV · continuação</div>
    <div class="lines l30"></div>
    <div class="u6-count"><span>Número de palavras</span><i></i><span>Revi: didascálias em itálico ou entre parênteses</span><i class="ck"></i><span>nomes antes das falas</span><i class="ck"></i><span>pontuação</span><i class="ck"></i></div>
    <div class="u6-end">Fim do Teste 2</div>'''))

# ------------------------------------------------------------------ AUTOCORREÇÃO
def auto_rows(items):
    return "".join(f'<tr><td>{n}</td><td>{t}</td><td>{p}</td><td></td><td class="rv">{r}</td></tr>' for n, t, p, r in items)

t1 = [('1–7', 'Narrativa: espaço, narrador, estrutura, recursos', 35, f"p. {ref('u2-map')}"), ('8–11', 'Publicidade: tipo, slogan, imperativo, facto/opinião', 15, f"p. {ref('s8')}"),
      ('12', 'Frase passiva', 3, f"p. {ref('s21')}"), ('13', 'Subordinadas condicionais e finais', 4, f"p. {ref('u2-n3-g')}"), ('14', 'Pronome relativo', 3, f"p. {ref('u2-n2-g')}"),
      ('15', 'Conjuntivo', 4, f"p. {ref('u2-n4-g')}"), ('16', 'Funções sintáticas', 4, f"p. {ref('u4-l2-g')}"), ('17', 'Advérbio', 2, f"p. {ref('u3-p2-g')}"), ('IV', 'Escrita', 30, f"p. {ref('u6-esc')}")]
t2 = [('1–4', 'Poesia: forma, métrica, rima, refrão', 19, f"p. {ref('u3-v1')}"), ('5–7', 'Recursos expressivos e interpretação', 16, f"p. {ref('u3-rec')}"), ('8–11', 'Texto dramático', 15, f"p. {ref('u4-map')}"),
      ('12', 'Oração completiva', 3, f"p. {ref('u3-p1-g')}"), ('13', 'Pronomes átonos', 4, f"p. {ref('u2-n6-g')}"), ('14', 'Advérbio e locução adverbial', 3, f"p. {ref('u3-p2-g')}"),
      ('15', 'Sujeito e predicado', 4, f"p. {ref('u3-p2-g')}"), ('16', 'Funções sintáticas', 4, f"p. {ref('u4-l2-g')}"), ('17', 'Formação de palavras', 2, f"p. {ref('u2-n5-g')}"), ('IV', 'Escrita de uma cena', 30, f"p. {ref('u4-l2-e')}")]
th = '<tr><th style="width:12mm">Item</th><th>O que se avalia</th><th style="width:14mm">Cot.</th><th style="width:18mm">Tive</th><th style="width:22mm">Rever</th></tr>'
P.append(page('u6-auto', 'v-oficina-a', 'Autocorreção', f'''
    <div class="kicker"><b>Depois dos testes</b> <span class="skill sk-gra">Metacognição</span> Grelhas de autocorreção</div>
    <h1 class="title">Onde <em>falhei?</em></h1>
    <p class="lede sm">Depois de receberes o teste corrigido, preenche a grelha. Na coluna «Rever» está a página do livro onde podes voltar a estudar o que falhaste.</p>
    <div class="u6-two">
      <div><div class="bx-h">Teste 1</div><table class="fill u6-at">{th}{auto_rows(t1)}</table></div>
      <div><div class="bx-h">Teste 2</div><table class="fill u6-at">{th}{auto_rows(t2)}</table></div>
    </div>
    <div class="u6-why">
      <div class="bx-h">Porque errei? Assinala</div>
      <span>não li a pergunta até ao fim</span><span>não sabia a matéria</span><span>não justifiquei com o texto</span><span>faltou tempo</span><span>confundi dois conceitos</span><span>erros de ortografia</span><span>escrevi pouco para a cotação</span>
    </div>
    <div class="act"><div class="num">✎</div><div class="body"><p class="q">O meu plano para o próximo teste (três ações concretas):</p><div class="lines l3"></div></div></div>'''))

# ------------------------------------------------------------------ ORAL
P.append(page('u6-oral', '', 'Apresentação oral', '''
    <div class="kicker"><b>Prova 3</b> <span class="skill sk-ora">Oralidade</span> Individual · 3 minutos</div>
    <h1 class="title">Um livro, <em>três minutos</em></h1>
    <p class="lede sm">Apresenta à turma um livro que leste este ano (pode ser do teu contrato de leitura) e convence os colegas a lê-lo — ou a não o ler. Tens três minutos, nem mais, nem menos.</p>
    <div class="u6-time">
      <div><b>0:00</b><span class="ph">Gancho</span><p>Uma pergunta, uma frase do livro, um objeto. Agarra o público.</p></div>
      <div><b>0:30</b><span class="ph">O livro</span><p>Título, autor, género, época. O enredo em quatro frases — sem revelar o final.</p></div>
      <div><b>1:30</b><span class="ph">A tua opinião</span><p>Dois argumentos com exemplos. Lê um excerto curto (20 segundos).</p></div>
      <div><b>2:30</b><span class="ph">Veredicto</span><p>Recomendação clara: a quem, porquê. Termina com força.</p></div>
    </div>
    <div class="u6-two">
      <div class="u6-box"><div class="bx-h">Podes usar</div><p class="tiny">um cartão com cinco palavras-chave · o próprio livro · uma imagem</p></div>
      <div class="u6-box"><div class="bx-h">Não podes</div><p class="tiny">ler um texto escrito · ultrapassar 3 min 15 s · contar o final</p></div>
    </div>
    <div class="u6-cards"><div class="bx-h">O teu cartão · cinco palavras-chave</div><div class="cd"><i>1</i><span>gancho</span></div><div class="cd"><i>2</i><span>o livro</span></div><div class="cd"><i>3</i><span>argumento</span></div><div class="cd"><i>4</i><span>argumento</span></div><div class="cd"><i>5</i><span>veredicto</span></div></div>
    <table class="fill rub u6-rub">
      <tr><th>Critério</th><th>1 · Em construção</th><th>2 · Consolidado</th><th>3 · Excelente</th><th style="width:13mm">Pts</th></tr>
      <tr><td><b>Conteúdo</b></td><td>informação vaga ou incorreta</td><td>livro bem apresentado</td><td>apresentação rigorosa e seletiva</td><td>/6</td></tr>
      <tr><td><b>Argumentação</b></td><td>«gostei porque sim»</td><td>dois argumentos com exemplos</td><td>argumentos fortes, excerto bem escolhido</td><td>/6</td></tr>
      <tr><td><b>Estrutura e tempo</b></td><td>sem gancho, fora do tempo</td><td>quatro partes, no tempo</td><td>transições naturais, final memorável</td><td>/4</td></tr>
      <tr><td><b>Voz e corpo</b></td><td>lê, voz baixa, sem contacto visual</td><td>audível, algum contacto visual</td><td>expressivo, pausas, olha o público</td><td>/4</td></tr>
      <tr><td><b>Língua</b></td><td>muitos bordões («tipo», «pronto»)</td><td>registo cuidado</td><td>vocabulário rico e preciso</td><td>/4</td></tr>
    </table>
    <div class="u6-peer">
      <div class="bx-h">Avaliação pelos colegas · dois estrelas e um desejo</div>
      <div class="prw"><span>★</span><i></i></div><div class="prw"><span>★</span><i></i></div><div class="prw"><span>Desejo</span><i></i></div>
    </div>'''))

# ------------------------------------------------------------------ ESCRITA
P.append(page('u6-esc', '', 'Texto escrito', '''
    <div class="kicker"><b>Prova 4</b> <span class="skill sk-esc">Escrita</span> Individual · em aula · 60 minutos</div>
    <h1 class="title">Crítica ou <em>opinião</em></h1>
    <div class="u6-task big">
      <div class="tk"><b>Opção A · Artigo de opinião</b><span>«Os telemóveis devem ficar à porta da sala de aula.» Concordas? Escreve um artigo de opinião para o jornal da escola (200 a 260 palavras).</span></div>
      <div class="tk"><b>Opção B · Crítica</b><span>Escreve a crítica de um livro que leste este ano para a revista <i>A Lupa</i> (200 a 260 palavras), com classificação de uma a cinco estrelas.</span></div>
    </div>
    <div class="u6-steps">
      <div><i>1</i><b>Planificar</b><span>10 min · tese, dois argumentos, exemplos, conclusão</span></div>
      <div><i>2</i><b>Escrever</b><span>35 min · um parágrafo por ideia, conectores</span></div>
      <div><i>3</i><b>Rever</b><span>15 min · lê em voz baixa, corrige, conta as palavras</span></div>
    </div>
    <table class="fill rub u6-rub">
      <tr><th>Critério</th><th>1 · Em construção</th><th>2 · Consolidado</th><th>3 · Excelente</th><th style="width:13mm">Pts</th></tr>
      <tr><td><b>Tema e tese</b></td><td>tese ausente ou confusa</td><td>tese clara no início</td><td>tese clara, retomada na conclusão com força</td><td>/5</td></tr>
      <tr><td><b>Argumentação</b></td><td>opiniões sem razões</td><td>dois argumentos com exemplos</td><td>argumentos variados, contra-argumento refutado</td><td>/7</td></tr>
      <tr><td><b>Estrutura e coesão</b></td><td>um bloco de texto; «e depois»</td><td>parágrafos; conectores simples</td><td>progressão clara; conectores variados e precisos</td><td>/4</td></tr>
      <tr><td><b>Correção linguística</b></td><td>erros frequentes que dificultam a leitura</td><td>erros pontuais</td><td>texto correto, vocabulário rico</td><td>/4</td></tr>
    </table>
    <div class="u6-plan big"><div class="bx-h">Planificação</div>
      <div class="u6pw"><b>Tese</b><i></i></div><div class="u6pw"><b>Argumento 1 + exemplo</b><i></i></div><div class="u6pw"><b>Argumento 2 + exemplo</b><i></i></div><div class="u6pw"><b>Contra-argumento</b><i></i></div><div class="u6pw"><b>Refutação</b><i></i></div><div class="u6pw"><b>Conclusão</b><i></i></div></div>
    <div class="u6-conn"><b>Conectores que fazem a diferença</b><span>Em primeiro lugar</span><span>Além disso</span><span>Por exemplo</span><span>No entanto</span><span>Há quem defenda que… mas</span><span>Por conseguinte</span><span>Em suma</span></div>
    <p class="tiny">Três respostas-modelo a esta tarefa (Opção A), uma de cada nível, estão nas pp. <span class="ref" data-ref="u6-mod"></span>–<span class="ref" data-ref="u6-mod2"></span>.</p>'''))

# ------------------------------------------------------------------ MODELOS (3 níveis, 2 pp.)
def model(lvl, name, pts, text, notes):
    ns = "".join(f'<li><b>{a}</b> {b}</li>' for a, b in notes)
    return f'''<div class="u6-md lv{lvl}"><div class="md-h"><span>Nível {lvl}</span><b>{name}</b><em>{pts}</em></div>
      <div class="md-b"><div class="md-t">{text}</div><ul class="md-n">{ns}</ul></div></div>'''

m1 = model(1, 'Em construção', '8 / 20 pontos',
    '<p>Eu acho que os telemóveis não devem ficar à porta porque são muito uteis. Por exemplo eu uso o telemovel para ver as horas e para falar com a minha mãe. E tambem da para pesquisar coisas. Os profesores dizem que distrai mas eu acho que não distrai nada se a gente tiver juízo. E depois se houver uma emergência como é que a gente liga?</p><p>Por isso os telemóveis deviam ficar na sala.</p>',
    [('Tese', 'existe, mas «eu acho» repetido enfraquece-a.'), ('Argumentos', 'exemplos pessoais; o contra-argumento («distrai») é recusado sem razões.'),
     ('Estrutura', 'quase sem introdução; conclusão de uma linha; «E depois».'), ('Língua', '«uteis», «telemovel», «tambem», «profesores», «da» sem acento; «a gente» é registo oral.'), ('Extensão', 'cerca de 90 palavras: muito abaixo do pedido.')])
m2 = model(2, 'Consolidado', '14 / 20 pontos',
    '<p>Muitas escolas portuguesas já proibiram os telemóveis nas salas de aula. Na minha opinião, essa é uma boa decisão.</p><p>Em primeiro lugar, o telemóvel distrai. Basta uma notificação para um aluno deixar de ouvir a explicação e, quando volta a prestar atenção, já perdeu metade da matéria. Eu próprio já me distraí muitas vezes assim.</p><p>Além disso, sem telemóveis, os alunos falam mais uns com os outros. Nos intervalos, em vez de estarem todos a olhar para o ecrã, conversam, jogam e resolvem problemas juntos.</p><p>Há quem diga que o telemóvel é útil para pesquisar. No entanto, a escola tem computadores e biblioteca para isso.</p><p>Em suma, os telemóveis devem ficar à porta da sala, para aprendermos melhor e convivermos mais.</p>',
    [('Tese', 'clara logo no 1.º parágrafo.'), ('Argumentos', 'dois argumentos com exemplos; contra-argumento refutado, embora de forma breve.'),
     ('Estrutura', 'um parágrafo por ideia; conectores adequados («Em primeiro lugar», «Além disso», «No entanto»).'), ('A melhorar', 'exemplos pouco desenvolvidos; conclusão repete a tese sem a enriquecer; 150 palavras, abaixo do mínimo.')])
m3 = model(3, 'Excelente', '19 / 20 pontos',
    '<p>Quantas vezes, numa aula, olhaste para o ecrã «só um segundo» e voltaste dez minutos depois? A pergunta não é se o telemóvel é útil — é evidente que é —, mas se a sala de aula é o lugar certo para ele. Defendo que não: os telemóveis devem ficar à porta.</p><p>Em primeiro lugar, porque a atenção é o material escolar mais caro que temos, e o telemóvel foi desenhado para a roubar. Cada notificação é um pequeno anúncio que grita «olha para mim!». Ninguém aprende a comentar um soneto de Camões com uma mensagem a vibrar no bolso.</p><p>Em segundo lugar, porque a escola é um dos poucos lugares onde ainda aprendemos a estar juntos. Quando os ecrãs se apagam, há conversas, discussões, gargalhadas — e é aí que muitas vezes se aprende mais.</p><p>Há quem defenda que o telemóvel é uma ferramenta de pesquisa indispensável. É verdade; mas, quando for preciso, o professor pode pedir que o tragam para uma tarefa concreta. Ficar à porta não é desaparecer: é esperar pela sua vez.</p><p>Em suma, guardar o telemóvel durante a aula não é voltar ao passado. É escolher, durante cinquenta minutos, estar inteiramente presente — e isso, hoje, é quase revolucionário.</p>',
    [('Tese', 'introduzida por uma pergunta retórica; delimitada com precisão.'), ('Argumentos', 'dois argumentos fortes, com imagens expressivas (metáfora da atenção, personificação da notificação).'),
     ('Contra-argumento', 'apresentado com justiça e refutado com uma proposta.'), ('Estrutura', 'progressão clara; conectores variados; conclusão que retoma e amplia a tese.'), ('Língua', 'vocabulário rico, pontuação expressiva; 240 palavras.')])
P.append(page('u6-mod', 'v-oficina-a', 'Modelos · escrita', f'''
    <div class="kicker"><b>Prova 4</b> <span class="skill sk-esc">Escrita</span> Respostas-modelo anotadas · Opção A</div>
    <h1 class="title">Três respostas, <em>três níveis</em></h1>
    <p class="lede sm">Lê as três respostas à mesma pergunta. As notas à direita mostram o que pesa na avaliação. Antes de leres as notas, classifica cada texto com a grelha da p. {ref('u6-esc')} e usa os códigos de correção para marcar os erros.</p>
    {m1}
    {m2}
    <div class="u6-codes"><div class="bx-h">Códigos de correção do professor</div>
      <span><b>Ort</b> ortografia</span><span><b>Ac</b> acentuação</span><span><b>Pont</b> pontuação</span><span><b>Conc</b> concordância</span><span><b>Rep</b> repetição</span><span><b>Reg</b> registo oral</span><span><b>¶</b> falta parágrafo</span><span><b>?</b> ideia pouco clara</span><span><b>+</b> muito bem</span></div>'''))
P.append(page('u6-mod2', 'v-oficina-a', 'Modelos · escrita', f'''
    {m3}
    <div class="u6-diff">
      <div class="bx-h">O que separa os níveis</div>
      <div class="df"><b>Do 1 ao 2</b><span>tese logo no início · um parágrafo por ideia · exemplos gerais, não só pessoais · ortografia revista</span></div>
      <div class="df"><b>Do 2 ao 3</b><span>abertura que prende · argumentos desenvolvidos com imagens · contra-argumento levado a sério · conclusão que acrescenta</span></div>
    </div>
    <div class="act"><div class="num">✎</div><div class="body"><p class="q">Reescreve a resposta de nível 1 até ela chegar ao nível 2. Mantém as ideias do aluno; muda a organização, os conectores e a correção.</p><div class="lines l6"></div></div></div>'''))

# ------------------------------------------------------------------ DRAMA
P.append(page('u6-dra', '', 'Cena de teatro', '''
    <div class="kicker"><b>Prova 5</b> <span class="skill sk-ora">Oralidade</span> <span class="skill sk-esc">Escrita</span> Em grupos de 3 ou 4 · 2 semanas</div>
    <h1 class="title">Escrever <em>e representar</em></h1>
    <p class="lede sm">O grupo escreve uma cena original de 3 a 5 minutos, inspirada num texto lido este ano — uma personagem, um conflito ou um lugar — e representa-a para a turma.</p>
    <div class="u6-insp"><div class="bx-h">Pontos de partida</div><span>Leandro e o sal</span><span>Os três irmãos de Medranhos</span><span>O projecionista do Cinema Aurora</span><span>O homem que sabia javanês</span><span>Sísifo e a pedra</span><span>Lianor a caminho da fonte</span></div>
    <div class="u6-ent">
      <div><b>Entrega 1 · guião</b><span>Semana 1 · título, personagens, 1 a 2 páginas com didascálias; cada aluno assina as falas que escreveu.</span></div>
      <div><b>Entrega 2 · ensaio</b><span>Semana 2 · ensaio com o professor; lista de adereços, luz e som.</span></div>
      <div><b>Entrega 3 · estreia</b><span>Apresentação e dois minutos de conversa com o público sobre as escolhas do grupo.</span></div>
    </div>
    <div class="u6-plan"><div class="bx-h">Ficha do guião</div>
      <div class="u6pw"><b>Título</b><i></i></div><div class="u6pw"><b>Texto de partida</b><i></i></div><div class="u6pw"><b>Personagens e atores</b><i></i></div><div class="u6pw"><b>Lugar e tempo</b><i></i></div><div class="u6pw"><b>O conflito, numa frase</b><i></i></div></div>
    <table class="fill rub u6-rub">
      <tr><th>Critério</th><th>1 · Em construção</th><th>2 · Consolidado</th><th>3 · Excelente</th><th style="width:13mm">Pts</th></tr>
      <tr><td><b>Guião</b></td><td>falas sem didascálias; conflito pouco claro</td><td>estrutura clara, didascálias de espaço e tom</td><td>conflito forte, didascálias expressivas, aparte ou monólogo bem usado</td><td>/6</td></tr>
      <tr><td><b>Ligação ao texto de partida</b></td><td>ligação superficial</td><td>ligação clara</td><td>releitura original do texto de partida</td><td>/4</td></tr>
      <tr><td><b>Interpretação</b></td><td>falas lidas, sem intenção</td><td>de cor, tom adequado</td><td>personagens vivas: voz, corpo, olhar, pausas</td><td>/6</td></tr>
      <tr><td><b>Encenação</b></td><td>sem cenário, luz ou som</td><td>elementos simples e coerentes</td><td>soluções criativas ao serviço da cena</td><td>/2</td></tr>
      <tr><td><b>Trabalho de grupo</b></td><td>participação desigual</td><td>todos contribuem</td><td>equipa coordenada, papéis claros</td><td>/2</td></tr>
    </table>
    <div class="u6-peer"><div class="bx-h">Diário do grupo · uma linha por sessão</div>
      <div class="prw"><span>Sessão 1</span><i></i></div><div class="prw"><span>Sessão 2</span><i></i></div><div class="prw"><span>Sessão 3</span><i></i></div><div class="prw"><span>Sessão 4</span><i></i></div></div>'''))

# ------------------------------------------------------------------ SECÇÃO DO PROFESSOR (3 pp.)
def key(rows):
    return "".join(f'<tr><td class="it">{n}</td><td>{a}</td><td class="ct">{c}</td></tr>' for n, a, c in rows)

k1 = [('1', 'Num casebre isolado, num cerro, entre Enganim e Cesareia; na miséria. Ex.: «farrapos da enxerga apodrecida», «Dentro da arca pintada não restava grão ou côdea», «ervas […] cozidas sem sal».', '5 = local + duas transcrições corretas; 3 = local + uma'),
      ('2', 'Comparação (e metáfora: a miséria «cresce»): a pobreza é apresentada como algo vivo, que se espalha e apodrece tudo, sugerindo abandono total.', '5 = recurso + efeito; 2 = só recurso'),
      ('3', 'Leva a notícia do Rabi à viúva: é o elemento que desencadeia a esperança e o conflito final (ir ou não ir).', '4 / 2'),
      ('4', 'Não pode deixar o filho doente; é pobre e fraca («tão rota, tão trôpega»); ninguém lhe daria atenção; nem os ricos o encontraram; talvez Jesus tivesse morrido.', '5 = duas razões fundamentadas'),
      ('5', 'Narrador ausente (não participa na história): narra na 3.ª pessoa («vivia», «contou»).', '4 = classificação + justificação'),
      ('6', 'Ex.: 1) A miséria da viúva e do filho (§1); 2) A esperança trazida pelo mendigo e o desânimo da mãe (§2 até ao diálogo); 3) O desejo da criança e o milagre (final).', '6 = três momentos delimitados e titulados'),
      ('7', 'O milagre é «suave» porque acontece sem esforço nem poder: Jesus aparece por si, à porta, a quem nada tem e apenas deseja vê-lo — o contrário dos poderosos, que o procuraram com servos e soldados.', '6 = relação título/final + contraste com o início'),
      ('8', 'Não comercial: não vende um produto; promove a leitura; emissor institucional (Câmara, Biblioteca); entrada livre.', '3'),
      ('9', 'Metáfora (ler = viagem) e hipérbole («a mais barata do mundo»): sugere que ler leva longe sem custar nada.', '4 = recurso + explicação'),
      ('10', '«Traz», «descobre», «leva»; dirige-se ao leitor jovem (tu) e às famílias.', '4'),
      ('11', 'Facto: «1 a 10 de junho», «30 editoras», «Entrada livre». Opinião: «uma história que nunca mais vais esquecer», slogan.', '4 = 2 + 2'),
      ('12', 'A história foi contada à viúva pelo mendigo.', '3'),
      ('13', 'a) subordinada adverbial condicional; b) subordinada adverbial final.', '2 + 2'),
      ('14', 'A viúva vivia num casebre que ficava na prega dum cerro.', '3'),
      ('15', 'a) venha; b) encontrares.', '2 + 2'),
      ('16', 'Um dia: modificador do grupo verbal · um mendigo: sujeito · pão: complemento direto · à viúva: complemento indireto.', '1 por função'),
      ('17', 'Advérbio de modo.', '2')]
P.append(page('u6-prof1', 'u6-teach', 'Secção do professor', f'''
    <div class="u6-prof-h"><b>Secção do professor</b><span>Teste 1 · soluções e critérios de classificação</span></div>
    <table class="fill u6-key"><tr><th style="width:10mm">Item</th><th>Resposta esperada (cenário de resposta)</th><th style="width:42mm">Critérios</th></tr>{key(k1)}</table>
    <div class="u6-pn"><b>Grupo IV</b> Tema e tese (8) · argumentação (10) · estrutura e coesão (6) · correção (6). Desvalorizar 1 ponto por cada 10 palavras abaixo do limite mínimo (máx. 5). Textos com menos de 60 palavras: classificação 0 em todos os critérios exceto correção.</div>'''))

k2 = [('1', 'Mote de 3 versos; duas voltas de 7 versos cada.', '4'),
      ('2', 'Des / cal / ça / vai / pa / ra_a / fon(te) = 7 sílabas métricas · redondilha maior.', '3 escansão + 2 classificação'),
      ('3', 'ABBAACC (pote / prata / escarlata / chamerlote / cote / pura / segura).', '5 · aceitar ABBAA + CC'),
      ('4', '«Vai fermosa e não segura.» Refrão: cria musicalidade, insiste na ideia central e liga as voltas ao mote.', '5 = verso + efeito'),
      ('5', 'Metáfora: «mãos de prata» (brancura, delicadeza) ou «Cabelos de ouro»; comparação: «Mais branca que a neve pura».', '6 = 2 + 2 + explicação 2'),
      ('6', 'Hipérbole.', '4'),
      ('7', 'Interpretação aberta. Ex.: a sua beleza atrai olhares e perigos; vai insegura, talvez apaixonada ou inquieta; a beleza não a protege.', '6 = interpretação coerente e fundamentada'),
      ('8', 'Espaço: «Palco do auditório da escola» · movimento: «Levanta-se e pontapeia a coroa» · luz: «A luz desce até ficarem só os dois».', '4'),
      ('9', '«Ninguém se ri de quem diz uma coisa daquelas a sério.» Revela sensibilidade e maturidade: percebe o valor da fala.', '4'),
      ('10', 'Rui recusa dizer a fala por vergonha; conflito entre Rui e Marta (e consigo próprio).', '4'),
      ('11', 'Resposta aberta, coerente com a cena (ex.: Rui diz a fala a Sofia; a luz a descer sugere intimidade).', '3'),
      ('12', 'Subordinada substantiva completiva.', '3'),
      ('13', 'a) Sofia estende-lha. b) Marta explica-lha.', '2 + 2'),
      ('14', 'De repente: locução adverbial de tempo · baixinho: advérbio de modo · nunca mais: locução adverbial de tempo (negação).', '3'),
      ('15', 'a) S: a Sofia (posposto) · P: Chegou. b) Sujeito nulo subentendido (vós/vocês) · P: Desculpem.', '2 + 2'),
      ('16', 'Na véspera da estreia: MGV · a encenadora: S · o guião: CD · aos atores: CI.', '1 por função'),
      ('17', 'Derivação por sufixação (encenar + -dora).', '2')]
P.append(page('u6-prof2', 'u6-teach', 'Secção do professor', f'''
    <div class="u6-prof-h"><b>Secção do professor</b><span>Teste 2 · soluções e critérios de classificação</span></div>
    <table class="fill u6-key"><tr><th style="width:10mm">Item</th><th>Resposta esperada (cenário de resposta)</th><th style="width:42mm">Critérios</th></tr>{key(k2)}</table>
    <div class="u6-pn"><b>Grupo IV</b> Adequação ao género (10): título, personagens, didascálias, nomes antes das falas, aparte ou monólogo · coerência com a cena (8) · criatividade (6) · correção (6).</div>'''))

P.append(page('u6-prof3', 'u6-teach', 'Secção do professor', '''
    <div class="u6-prof-h"><b>Secção do professor</b><span>Registo da turma · conversão de classificações · notas</span></div>
    <table class="fill u6-reg">
      <tr><th>Aluno</th><th>T1</th><th>T2</th><th>Oral</th><th>Escrita</th><th>Cena</th><th>Final</th></tr>
      <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    </table>
    <div class="u6-two">
      <div class="u6-box"><div class="bx-h">Conversão para 100</div><p class="tiny">Oral: pontos × 4 (máx. 24 → 96, arredondar a 100 com bonificação de tempo exato) · Escrita: pontos × 5 · Cena: pontos × 5. Média ponderada com os pesos da p. <span class="ref" data-ref="u6-prog"></span>.</p></div>
      <div class="u6-box"><div class="bx-h">Adaptações</div><p class="tiny">Tempo suplementar de 25%; enunciado ampliado; leitura do enunciado em voz alta; Grupo IV com planificação guiada (p. <span class="ref" data-ref="u6-esc"></span>).</p></div>
    </div>
    <div class="u6-box"><div class="bx-h">Notas para a correção</div>
      <p class="tiny">Valorizar respostas completas e fundamentadas com citações. Nas perguntas abertas (I-7, II-11, IV) aceitar interpretações diferentes das do cenário, desde que coerentes com o texto. Na gramática, a terminologia segue o Dicionário Terminológico. Os testes usam textos em domínio público (Eça de Queirós, Luís de Camões) e textos escritos para este manual.</p></div>
    <div class="lines l6"></div>'''))

# ------------------------------------------------------------------ VEREDICTO DO ANO
units = [('1', 'Promessa &amp; Veredicto', 'u5-red'), ('2', 'Quem nos faz crescer?', 'u5-grn'), ('3', 'O que cabe num verso?', 'u5-plm'),
         ('4', 'Sobe o pano', 'u5-ind'), ('5', 'Sessão de encerramento', 'u6-tea'), ('6', 'O teu veredicto', 'u6-olv'), ('7', 'Contrato de leitura', 'u6-amb')]
ur = "".join(f'<div class="vr {c}"><span>{n}</span><b>{t}</b><div class="st5"><i></i><i></i><i></i><i></i><i></i></div></div>' for n, t, c in units)
P.append(page('u6-fim', '', 'Veredicto do ano', f'''
    <div class="kicker"><b>Prova 6</b> Autoavaliação final</div>
    <h1 class="title">Veredicto <em>do ano</em></h1>
    <p class="lede sm">No primeiro dia, o bilhete dizia «Admite 1 leitor crítico». Agora és tu o crítico — de ti próprio. Dá de uma a cinco estrelas a cada unidade: o quanto aprendeste, não o quanto gostaste.</p>
    <div class="u6-vr">{ur}</div>
    <div class="u6-rep">
      <div class="rp"><b>O meu maior progresso</b><i></i><i></i></div>
      <div class="rp"><b>O que ainda me custa</b><i></i><i></i></div>
      <div class="rp"><b>O livro que vou ler nas férias</b><i></i></div>
      <div class="rp"><b>A classificação que acho que mereço, e porquê</b><i></i><i></i></div>
    </div>
    <div class="u6-sig">
      <div><i></i><span>O aluno</span></div><div><i></i><span>O encarregado de educação</span></div><div><i></i><span>O professor</span></div>
    </div>
    <div class="u6-ticket"><span class="tk-l">Admite</span><b>1 leitor</b><em>que já não precisa de bilhete</em></div>'''))

(R / 'src' / 'u6.html').write_text("\n".join(P))
print(len(P), 'pages')
