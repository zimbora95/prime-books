"""Generate src/u3.html — Unidade 3 · Texto poético (Y8 PT)."""
import html as H, pathlib
R = pathlib.Path(__file__).parent
T = R / "texts"


def rail(t): return f'<div class="rail"><span>{t}</span></div>'
def folio(t): return f'<div class="folio"><span class="n"></span><span class="t">{t}</span></div>'


def page(id_, cls, railt, inner, foliot=None):
    return f'''
<section id="{id_}" class="page v-poe {cls}">
  {rail(railt)}
  <div class="inner">
{inner}
  </div>
  {folio(foliot or railt)}
</section>'''


def poem(txt, numbered=True):
    out, n = [], 0
    for st in [s for s in txt.split("\n\n") if s.strip()]:
        lines = []
        for l in st.split("\n"):
            n += 1
            num = f'<span class="vln">{n}</span>' if numbered and (n % 5 == 0 or n == 1) else ''
            lines.append(f'<span class="vl">{num}{H.escape(l, quote=False)}</span>')
        out.append('<div class="vst">' + "".join(lines) + '</div>')
    return '<div class="vpoem">' + "".join(out) + '</div>'


def scan(syls, rest=''):
    """syllables list; the last is the stressed one; rest = unstressed tail not counted."""
    cells = "".join(f'<span class="sy{" t" if i == len(syls) - 1 else ""}"><i>{i+1}</i>{s}</span>' for i, s in enumerate(syls))
    tail = f'<span class="sy x">{rest}</span>' if rest else ''
    return f'<div class="scan">{cells}{tail}</div>'


def cite(lines, src):
    body = "<br>".join(H.escape(l, quote=False) for l in lines)
    return f'<blockquote class="cq"><p>{body}</p><cite>{src}</cite></blockquote>'


P = []
# ------------------------------------------------------------------ OPENER
P.append('''
<section id="u3" class="page v-poe opener u3-opener">
  <div class="bleed" style="background-image:url(../art/jpg/u3_opener.jpg); background-position: 50% 55%;"></div>
  <div class="opener-card">
    <div class="kicker"><b>Unidade 3</b> Texto poético · redondilha e esquema rimático</div>
    <h1 class="title">O que cabe<br>num <em>verso?</em></h1>
    <p class="lede">Um sonho que faz o mundo avançar. O medo de um país inteiro. Uma pergunta ao vento. Um rio que leva as mágoas para o mar. Nove poemas de oito poetas portugueses — e as ferramentas para perceberes <b>como</b> um poema funciona: o verso, a estrofe, a rima, o ritmo, as imagens.</p>
    <div class="opener-qs">
      <div><span>?</span>Porque é que um poema se lembra mais facilmente do que um texto em prosa?</div>
      <div><span>?</span>Pode um poema dizer uma coisa e querer dizer outra?</div>
      <div><span>?</span>Um poema serve para alguma coisa?</div>
    </div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Unidade 3</span></div>
</section>''')

# ------------------------------------------------------------------ PROGRAMA
rows = [
    ('1', 'António Gedeão', 'Pedra filosofal', 'O desejo de saber', 'Enumeração · anáfora · metáfora · opinião · pleonasmo, hipérbole, completiva', 'u3-p1'),
    ('2', "Alexandre O'Neill", 'O poema pouco original do medo', 'Ironia e enumeração', 'O que diz e o que deixa entender · recriação em prosa · advérbio, sujeito e predicado', 'u3-p2'),
    ('3', 'David Mourão-Ferreira', 'E por vezes', 'O tempo e o amor', 'Anáfora · hipérbole · ritmo', 'u3-p3'),
    ('4', 'Manuel Alegre', 'Trova do vento que passa', 'A liberdade', 'Redondilha maior · quadra · rima cruzada', 'u3-p4'),
    ('5', 'Ana Hatherly', 'Tisanas e poesia visual', 'A experiência da palavra', 'Poema em prosa · poema visual', 'u3-p5'),
    ('6', 'Miguel Torga', 'Sísifo', 'Recomeçar', 'Imperativo · apóstrofe · verso livre', 'u3-p6'),
    ('7', 'Manuel da Fonseca', 'Tejo que levas as águas', 'A cidade e a injustiça', 'Personificação · redondilha maior', 'u3-p7'),
    ('8·9', 'Florbela Espanca', 'Ser Poeta · Fanatismo', 'A paixão', 'Soneto · decassílabo · esquema rimático', 'u3-p8'),
]
lis = "".join(f'''
      <div class="u3-row"><span class="u3-n">{n}</span><div><b>{t}</b><small>{a}</small></div><span class="u3-g">{g}</span><span class="u3-s">{s}</span><span class="u3-p">p. <span class="ref" data-ref="{r}"></span></span></div>''' for n, a, t, g, s, r in rows)
P.append(page('u3-prog', '', 'Programa', f'''
    <div class="kicker"><b>Unidade 3</b> O programa</div>
    <h1 class="title">Nove poemas, <em>oito vozes</em></h1>
    <p class="lede sm">Primeiro, montas a tua <b>oficina do verso</b>: aprendes a contar sílabas, a desenhar esquemas rimáticos e a reconhecer a redondilha. Depois, cada poema é uma paragem para ler, ouvir, escrever e pensar a língua. No fim, o <b>Sarau</b> junta a turma à volta dos poemas.</p>
    <div class="u3-list">{lis}
    </div>
    <div class="u2-foot u3-foot">
      <div><b>Oficina do verso</b><span>Estrofe, rima, métrica · p. <span class="ref" data-ref="u3-v1"></span></span></div>
      <div><b>Recursos expressivos</b><span>O guia dos recursos · p. <span class="ref" data-ref="u3-rec"></span></span></div>
      <div><b>No fim</b><span>Sarau de poesia · p. <span class="ref" data-ref="u3-proj"></span></span></div>
    </div>
    <div class="note-f">Os poemas de Florbela Espanca estão em domínio público e reproduzem-se na íntegra. Dos outros sete poetas, cujas obras estão protegidas, citam-se apenas versos breves para fins de ensino: lê cada poema completo na antologia da turma ou na biblioteca.</div>'''))

# ------------------------------------------------------------------ OFICINA DO VERSO I
P.append(page('u3-v1', 'v-oficina-p', 'Oficina do verso', '''
    <div class="kicker"><b>Oficina do verso</b> <span class="skill sk-lit">Ed. literária</span> Referência · 1</div>
    <h1 class="title">Verso, estrofe <em>e rima</em></h1>
    <div class="vs-grid">
      <div class="vs-c"><b>Verso</b><p>Cada linha de um poema.</p></div>
      <div class="vs-c"><b>Estrofe</b><p>Grupo de versos separado por um espaço em branco.</p></div>
      <div class="vs-c"><b>Rima</b><p>Repetição de sons no fim dos versos, a partir da última vogal tónica: <i>m<u>ar</u> / lu<u>ar</u></i>.</p></div>
    </div>
    <table class="fill ptab est">
      <tr><th>Versos</th><th>Estrofe</th><th>Versos</th><th>Estrofe</th></tr>
      <tr><td>1</td><td>monóstico</td><td>6</td><td>sextilha</td></tr>
      <tr><td>2</td><td>dístico</td><td>7</td><td>sétima</td></tr>
      <tr><td>3</td><td>terceto</td><td>8</td><td>oitava</td></tr>
      <tr><td>4</td><td>quadra</td><td>9</td><td>nona</td></tr>
      <tr><td>5</td><td>quintilha</td><td>10</td><td>décima</td></tr>
    </table>
    <h2 class="sub">Esquema rimático</h2>
    <p class="lede sm">Dá-se a mesma letra aos versos que rimam entre si. Um verso que não rima com nenhum é um <b>verso solto</b> (usa-se uma letra nova ou um traço).</p>
    <div class="rm3">
      <div><b>Emparelhada</b><span class="sch">AABB</span><p>fo<u>gueira</u> <i>A</i><br>la<u>reira</u> <i>A</i><br>se<u>rão</u> <i>B</i><br>can<u>ção</u> <i>B</i></p></div>
      <div><b>Cruzada</b><span class="sch">ABAB</span><p>pas<u>sa</u> <i>A</i><br>pa<u>ís</u> <i>B</i><br>desgra<u>ça</u> <i>A</i><br><u>diz</u> <i>B</i></p></div>
      <div><b>Interpolada</b><span class="sch">ABBA</span><p>mai<u>or</u> <i>A</i><br>bei<u>ja</u> <i>B</i><br>se<u>ja</u> <i>B</i><br><u>Dor</u> <i>A</i></p></div>
    </div>
    <div class="twoR">
      <div><b>Rima consoante</b><p>Os sons coincidem por completo, vogais e consoantes: <i>vida / perdida</i>.</p></div>
      <div><b>Rima toante</b><p>Só coincidem as vogais: <i>prata / cama</i>.</p></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Liga as palavras que rimam e diz se a rima é consoante (C) ou toante (T): <i>coração · canção · cinzenta · lenta · casa · asa · sonho · risonho · vida · lida</i>.</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Volta às quadras da Unidade 1? Não: procura na tua memória uma canção que saibas de cor. Escreve uma estrofe, diz quantos versos tem, como se chama e qual é o esquema rimático.</p>
      <div class="lines l4"></div>
    </div></div>'''))

# ------------------------------------------------------------------ OFICINA DO VERSO II
P.append(page('u3-v2', 'v-oficina-p', 'Oficina do verso', f'''
    <div class="kicker"><b>Oficina do verso</b> <span class="skill sk-lit">Ed. literária</span> Referência · 2</div>
    <h1 class="title">Contar <em>sílabas métricas</em></h1>
    <p class="lede sm">No verso não se contam as sílabas gramaticais, mas as <b>sílabas métricas</b> — as que se ouvem quando o verso é dito. Três regras chegam para começar:</p>
    <div class="rules3">
      <div><i>1</i><b>Conta até à última sílaba tónica</b><p>O que vem depois dela não conta: <i>Pergunto ao vento que <u>pas</u>(sa)</i>.</p></div>
      <div><i>2</i><b>Junta as vogais que se encontram</b><p>Vogal final + vogal inicial fazem, muitas vezes, uma só sílaba (<b>elisão</b>): <i>to<u>_ao</u></i>, <i>cala<u>_a</u></i>.</p></div>
      <div><i>3</i><b>Diz o verso em voz alta</b><p>O ouvido é o melhor juiz. Bate as sílabas com os dedos.</p></div>
    </div>
    <h2 class="sub">Redondilha maior · 7 sílabas</h2>
    {scan(['Per','gun','to_ao','ven','to','que','pas'],'sa')}
    {scan(['no','tí','cias','do','meu','pa','ís'])}
    <p class="cite-s">Manuel Alegre, «Trova do vento que passa» (versos 1–2)</p>
    <h2 class="sub">Redondilha menor · 5 sílabas</h2>
    {scan(['Pas','to','ra','da','ser'],'ra')}
    {scan(['da','ser','ra','da_Es','tre'],'la')}
    <p class="cite-s">Luís de Camões, vilancete «Pastora da serra» (domínio público)</p>
    <div class="twoR">
      <div><b>Decassílabo · 10 sílabas</b><p>O verso do soneto: <i>Meus / o / lhos / an / dam / ce / gos / de / te / <u>ver</u></i>. (Florbela Espanca)</p></div>
      <div><b>Verso livre</b><p>Sem medida fixa e, muitas vezes, sem rima. Comum na poesia moderna (Torga, O'Neill, Mourão-Ferreira).</p></div>
    </div>
    <div class="warn"><b>Nem sempre há elisão</b> Quando a vogal seguinte é tónica, o poeta pode separá-las (<b>hiato</b>): <i>lu / a</i>, <i>pa / ís</i>. Na dúvida, diz o verso: o ritmo mostra-te a escolha certa.</div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Faz a escansão. Escreve uma sílaba métrica em cada caixa e sublinha a última tónica.</p>
      <p class="ex">correndo de par em par</p>
      <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      <p class="ex">perco-me por ela</p>
      <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span></div>
    </div></div>'''))

# ------------------------------------------------------------------ AQUECIMENTO
quadras = [
    ("Fui ao farol esta noite\nver a sua luz girar;\nnão há vento nem açoite\nque a possa um dia apagar.", 'q1'),
    ("Ó velho Cinema Aurora,\nabre as portas ao luar;\nquem entra não vai embora\nsem um sonho p'ra contar.", 'q2'),
    ("Tenho um livro na mochila\nque pesa mais do que o mar:\ncada página a virar\né uma porta que cintila.", 'q3'),
]
qh = "".join(f'<div class="qd"><span class="qd-n">{i+1}</span>{poem(q, numbered=False)}<div class="qd-s">Esquema: <span class="blank w2"></span></div></div>' for i, (q, _) in enumerate(quadras))
P.append(page('u3-aq', '', 'Aquecimento', f'''
    <div class="kicker"><b>Aquecimento</b> 20 minutos · a pares</div>
    <h1 class="title">Três quadras <em>de Vila Nova do Farol</em></h1>
    <p class="lede sm">Estas quadras foram escritas «ao gosto popular», como as que se cantam nas festas das aldeias portuguesas. Todas têm versos de sete sílabas.</p>
    <div class="qds">{qh}</div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escreve o esquema rimático de cada quadra. Qual é emparelhada, cruzada ou interpolada? Há alguma de cada tipo?</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Faz a escansão (conta as sílabas métricas) do primeiro verso da quadra 2 e do último verso da quadra 1. Mostra as elisões.</p>
      <div class="lines l5"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Escreve a tua quadra sobre a escola ou a tua rua: quatro versos de sete sílabas, com rima cruzada. <span class="pill stretch">Desafio</span></p>
      <div class="lines l6"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Diz a tua quadra à turma. Os colegas batem as sílabas com os dedos: são mesmo sete? Regista o que tiveste de mudar. <span class="pill oral">Oralidade</span></p>
      <div class="lines l3"></div>
    </div></div>'''))

# ------------------------------------------------------------------ P1 GEDEÃO
P.append(page('u3-p1', '', 'Poema 1 · Pedra filosofal', f'''
    <div class="kicker"><b>Poema 1</b> <span class="skill sk-lit">Ed. literária</span> Guia de leitura · lê o poema completo na antologia</div>
    <h1 class="title">Pedra <em>filosofal</em></h1>
    <p class="byline">António Gedeão · <i>Movimento Perpétuo</i> (1956)</p>
    <div class="hero-img short" style="background-image:url(../art/jpg/u3_sonho.jpg)"></div>
    <div class="guide">
      <div class="gd-c">
        <h3>O poeta</h3>
        <p><b>António Gedeão</b> era o nome de poeta de Rómulo de Carvalho (1906–1997), professor de Física e Química e divulgador de ciência. Na sua poesia, a ciência e o sonho andam de mãos dadas. O poema tornou-se famoso cantado por Manuel Freire.</p>
        {cite(['Eles não sabem que o sonho', 'é uma constante da vida', 'tão concreta e definida', 'como outra coisa qualquer,'], 'António Gedeão, «Pedra filosofal», versos 1–4')}
        {cite(['Eles não sabem, nem sonham,', 'que o sonho comanda a vida.'], 'versos finais')}
        <h3>A pedra filosofal</h3>
        <p>Os alquimistas da Idade Média procuravam uma «pedra filosofal» capaz de transformar metais em ouro. No poema, o que transforma o mundo é outra coisa.</p>
      </div>
      <div class="gd-c rd">
        <h3>Enquanto lês</h3>
        <ol class="qs">
          <li>Quem são «eles»? Porque é que o poeta não os nomeia?<div class="lines l2"></div></li>
          <li>O sonho é comparado a coisas concretas (uma pedra, um ribeiro…). Porquê?<div class="lines l2"></div></li>
          <li>Na segunda parte, o poeta faz uma longa <b>enumeração</b> de invenções e descobertas. Copia três.<div class="lines l2"></div></li>
          <li>Que palavra ou expressão se repete no início de vários versos (<b>anáfora</b>)? Que efeito cria?<div class="lines l2"></div></li>
          <li>Explica a <b>metáfora</b> «o sonho comanda a vida».<div class="lines l2"></div></li>
        </ol>
      </div>
    </div>'''))

P.append(page('u3-p1-e', 'v-oficina-p', 'Poema 1 · Escrita', '''
    <div class="kicker"><b>Poema 1</b> <span class="skill sk-esc">Escrita</span> Texto de opinião sobre a ideia do poema</div>
    <h1 class="title">O sonho <em>comanda a vida?</em></h1>
    <p class="lede sm">Gedeão defende que é o sonho — a imaginação, a curiosidade, o desejo de saber — que faz o mundo avançar. Concordas? Escreve um texto de opinião com <b>dois argumentos</b>, cada um com um exemplo concreto (da ciência, da história, da tua vida).</p>
    <div class="op">
      <div class="op-c"><span>1</span><b>Introdução</b><p>Apresenta a ideia do poema e a tua posição.</p></div>
      <div class="op-c"><span>2</span><b>Argumento 1</b><p>Uma razão + um exemplo (uma invenção, uma pessoa, um momento).</p></div>
      <div class="op-c"><span>3</span><b>Argumento 2</b><p>Outra razão + outro exemplo.</p></div>
      <div class="op-c"><span>4</span><b>Conclusão</b><p>Retoma a posição e fecha com uma frase forte — talvez um verso do poema.</p></div>
    </div>
    <div class="ideas"><b>Ideias para pensar</b><span>a ida à Lua</span><span>as vacinas</span><span>a internet</span><span>os Descobrimentos</span><span>um sonho teu que já cumpriste</span><span>sonhos que correram mal</span></div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escreve o teu texto (150 a 200 palavras). Título obrigatório.</p>
      <div class="lines l18"></div>
    </div></div>
    <div class="chk"><b>Revê</b><span>posição clara</span><span>dois argumentos, dois exemplos</span><span>conectores</span><span>conclusão forte</span><span>150–200 palavras</span></div>'''))

P.append(page('u3-p1-g', 'v-oficina-p', 'Poema 1 · Gramática', '''
    <div class="kicker"><b>Poema 1</b> <span class="skill sk-gra">Gramática</span> Pleonasmo e hipérbole · oração subordinada completiva</div>
    <h1 class="title">Dizer a mais, <em>de propósito</em></h1>
    <div class="gx">
      <div class="gx-c"><b>Pleonasmo</b><p>Repetição de uma ideia já contida noutra palavra, para <u>reforçar</u>.</p><p class="ex">Vi com os meus próprios olhos. · Subir lá acima.</p><p>Quando não tem intenção expressiva, é um erro: <i>entrar para dentro</i>.</p></div>
      <div class="gx-c"><b>Hipérbole</b><p>Exagero intencional (lembra-te da Unidade 1!).</p><p class="ex">Os meses oceanos. (Mourão-Ferreira) · Morrer de saudade.</p></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Classifica: <b>P</b> (pleonasmo expressivo), <b>E</b> (pleonasmo vicioso, erro) ou <b>H</b> (hipérbole).</p>
      <ol class="mini" type="a"><li>Chorei rios de lágrimas. <span class="blank w1"></span></li><li>Sobe lá para cima! <span class="blank w1"></span></li><li>Ouvi-o com estes ouvidos que a terra há de comer. <span class="blank w1"></span></li><li>Já te disse isto mil vezes. <span class="blank w1"></span></li></ol>
    </div></div>
    <div class="sub1"><b>Oração subordinada substantiva completiva</b><span>Completa o sentido de um verbo (quase sempre como complemento direto). É introduzida por <i>que</i> ou <i>se</i>.</span>
      <p class="ex">Eles não sabem <b>que o sonho é uma constante da vida</b>.</p>
      <p class="ex">Pergunto-me <b>se o vento sabe notícias do meu país</b>.</p>
      <div class="test"><b>Teste</b> Substitui a oração por <i>isso</i>: «Eles não sabem <u>isso</u>.» Se a frase continua a fazer sentido, é completiva.</div>
    </div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Sublinha as orações completivas.</p>
      <ol class="mini" type="a"><li>O poeta afirma que o sonho faz o mundo avançar.</li><li>Não sei se Gedeão era mais cientista ou mais poeta.</li><li>A professora disse que íamos ouvir o poema cantado.</li><li>Perguntei-lhe se o sonho comanda mesmo a vida.</li></ol>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Completa com uma oração completiva: <b>a)</b> Eu acredito <span class="blank w4"></span> <b>b)</b> Ninguém sabe <span class="blank w4"></span></p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Escreve duas frases sobre um sonho teu: uma com um <b>pleonasmo expressivo</b>, outra com uma <b>hipérbole</b>. Sublinha o recurso.</p>
      <div class="lines l3"></div>
    </div></div>'''))

# ------------------------------------------------------------------ P2 O'NEILL
P.append(page('u3-p2', '', "Poema 2 · O'Neill", f'''
    <div class="kicker"><b>Poema 2</b> <span class="skill sk-lit">Ed. literária</span> Guia de leitura · lê o poema completo na antologia</div>
    <h1 class="title">O poema pouco original <em>do medo</em></h1>
    <p class="byline">Alexandre O'Neill · <i>Abandono Vigiado</i> (1960)</p>
    <div class="hero-img short" style="background-image:url(../art/jpg/u3_medo.jpg)"></div>
    <div class="guide">
      <div class="gd-c">
        <h3>O poeta e o tempo</h3>
        <p><b>Alexandre O'Neill</b> (1924–1986) foi poeta e também publicitário (inventou slogans que ainda hoje se ouvem). Viveu sob a ditadura do Estado Novo, quando havia censura e uma polícia política, a PIDE, que vigiava e prendia quem discordava do regime.</p>
        {cite(['O medo vai ter tudo', 'pernas', 'ambulâncias', 'e o luxo blindado', 'de alguns automóveis'], "Alexandre O'Neill, «O poema pouco original do medo», versos 1–5")}
        <h3>A ironia</h3>
        <p>O título diz que o poema é «pouco original». Porque é que um poeta diria isso do seu próprio poema? Pensa que, naquele tempo, o medo era tão comum que falar dele já não era novidade.</p>
      </div>
      <div class="gd-c rd">
        <h3>O que diz · o que deixa entender</h3>
        <table class="fill dd">
          <tr><th>O poema diz…</th><th>…e deixa entender</th></tr>
          <tr><td>«O medo vai ter tudo»</td><td></td></tr>
          <tr><td>o medo vai ter olhos e ouvidos</td><td></td></tr>
          <tr><td>a enumeração de coisas que o medo terá</td><td></td></tr>
          <tr><td>o título «pouco original»</td><td></td></tr>
        </table>
        <ol class="qs">
          <li>O medo é tratado como se fosse uma pessoa (personificação). Dá um exemplo.<div class="lines l1"></div></li>
          <li>Porque é que a <b>enumeração</b> de coisas banais torna o medo mais assustador?<div class="lines l2"></div></li>
          <li>Relaciona o poema com o tempo em que foi escrito. Porque é que o medo podia «ter tudo»?<div class="lines l2"></div></li>
        </ol>
      </div>
    </div>'''))

P.append(page('u3-p2-e', 'v-oficina-p', "Poema 2 · Escrita", '''
    <div class="kicker"><b>Poema 2</b> <span class="skill sk-esc">Escrita</span> Recriação em prosa</div>
    <h1 class="title">Contar o poema <em>por outras palavras</em></h1>
    <p class="lede sm">Recriar um poema em prosa não é resumi-lo, nem explicá-lo: é contar, num pequeno texto, <b>o sentido</b> do poema — como se fosse uma cena, uma carta ou um diário. O leitor deve reconhecer o poema sem que copies um único verso.</p>
    <div class="rc3">
      <div><b>Uma cena</b><p>Uma rua de Lisboa em 1960. Descreve o que as pessoas fazem, o que não dizem, de que desconfiam.</p></div>
      <div><b>Uma carta</b><p>Alguém escreve a um amigo emigrado a contar como é viver com medo — com cuidado, porque as cartas podem ser abertas.</p></div>
      <div><b>Um diário</b><p>O próprio Medo escreve o seu diário: onde esteve hoje, a quem entrou em casa, o que conseguiu calar.</p></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escolhe um formato e escreve a tua recriação (150 a 200 palavras). Usa pelo menos uma <b>enumeração</b> e uma <b>personificação</b>.</p>
      <div class="lines l18"></div>
    </div></div>
    <div class="chk"><b>Revê</b><span>o sentido do poema está lá</span><span>nenhum verso copiado</span><span>uma enumeração</span><span>uma personificação</span><span>150–200 palavras</span></div>'''))

P.append(page('u3-p2-g', 'v-oficina-p', "Poema 2 · Gramática", '''
    <div class="kicker"><b>Poema 2</b> <span class="skill sk-gra">Gramática</span> Advérbio e locução adverbial · sujeito e predicado</div>
    <h1 class="title">Como, quando, onde <em>e quem</em></h1>
    <div class="gx">
      <div class="gx-c"><b>Advérbio</b><p>Palavra invariável que modifica um verbo, um adjetivo ou outro advérbio.</p><p class="ex">O medo entrou <mark>silenciosamente</mark>. · <mark>muito</mark> escuro · <mark>bem</mark> depressa</p></div>
      <div class="gx-c"><b>Locução adverbial</b><p>Grupo de palavras com o valor de um advérbio.</p><p class="ex"><mark>às escondidas</mark> · <mark>de repente</mark> · <mark>a pouco e pouco</mark> · <mark>de vez em quando</mark></p></div>
    </div>
    <table class="fill ptab"><tr><th>Valor</th><th>Advérbios</th><th>Locuções adverbiais</th></tr>
      <tr><td>modo</td><td>assim, bem, mal, depressa, devagar, -mente</td><td>às escondidas, à pressa, de cor</td></tr>
      <tr><td>tempo</td><td>hoje, ontem, já, sempre, nunca, cedo</td><td>de vez em quando, à noite, de repente</td></tr>
      <tr><td>lugar</td><td>aqui, ali, lá, perto, longe, dentro</td><td>por aqui, ao longe, em cima</td></tr>
      <tr><td>negação · afirmação · dúvida</td><td>não, sim, talvez, certamente</td><td>de modo nenhum, com certeza, se calhar</td></tr>
    </table>
    <div class="sp">
      <div class="sp-line"><span class="sj">O medo</span><span class="pd">vai ter tudo.</span></div>
      <div class="sp-key"><span class="sj">sujeito · de quem se fala</span><span class="pd">predicado · o que se diz do sujeito (tem o verbo)</span></div>
      <p>Para encontrar o sujeito, pergunta <b>quem?</b> ou <b>o quê?</b> antes do verbo: <i>Quem vai ter tudo? — O medo.</i> O sujeito pode vir depois do verbo: <i>Chegou <u>o medo</u>.</i></p>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Sublinha os advérbios e as locuções adverbiais e indica o valor: «De repente, as pessoas calaram-se. Falavam baixinho, às escondidas, e nunca diziam o que pensavam.»</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Separa o sujeito (S) do predicado (P): <b>a)</b> Os vizinhos desconfiavam uns dos outros. <b>b)</b> Nas paredes havia ouvidos. <b>c)</b> Entrou na sala um homem de chapéu.</p>
      <div class="lines l3"></div>
    </div></div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Acrescenta a cada frase um advérbio de modo e uma locução adverbial de tempo: <b>a)</b> O poeta escreveu. <b>b)</b> As pessoas falavam. <b>c)</b> O vento passa.</p>
      <div class="lines l3"></div>
    </div></div>'''))

# ------------------------------------------------------------------ P3 MOURÃO-FERREIRA
P.append(page('u3-p3', '', 'Poema 3 · E por vezes', f'''
    <div class="kicker"><b>Poema 3</b> <span class="skill sk-lit">Ed. literária</span> <span class="skill sk-ora">Oralidade</span> Guia de leitura · lê o poema completo na antologia</div>
    <h1 class="title">E por <em>vezes</em></h1>
    <p class="byline">David Mourão-Ferreira (1927–1996)</p>
    <div class="guide">
      <div class="gd-c">
        <p><b>David Mourão-Ferreira</b>, lisboeta, foi poeta, ficcionista, professor universitário e secretário de Estado da Cultura. Escreveu sobretudo sobre o amor e o tempo, com uma música muito própria.</p>
        {cite(['E por vezes as noites duram meses', 'E por vezes os meses oceanos'], 'David Mourão-Ferreira, «E por vezes», versos 1–2')}
        <div class="focus"><b>Três coisas a observar</b>
          <p><u>Anáfora</u> — «E por vezes» abre quase todos os versos. É o motor do poema: cria ritmo, insistência, quase uma respiração.</p>
          <p><u>Hipérbole</u> — «as noites duram meses», «os meses oceanos»: o tempo vivido por dentro (tempo psicológico) é maior do que o tempo do relógio.</p>
          <p><u>Verso livre</u> — os versos não têm todos a mesma medida; o ritmo nasce da repetição.</p>
        </div>
        <div class="tpsy"><b>Tempo do relógio · tempo por dentro</b>
          <div class="tp-row"><span>Uma hora à espera de alguém</span><i></i></div>
          <div class="tp-row"><span>Uma hora com os amigos</span><i></i></div>
          <div class="tp-row"><span>Uma noite sem dormir</span><i></i></div>
          <small>Diz quanto tempo «parece» durar cada uma. É deste tempo que o poema fala.</small>
        </div>
      </div>
      <div class="gd-c rd">
        <h3>Enquanto lês e ouves</h3>
        <ol class="qs">
          <li>Quantas vezes se repete «E por vezes»? O que muda nos versos que se seguem a cada repetição?<div class="lines l3"></div></li>
          <li>O que significa, para ti, que «as noites duram meses»? Em que situações o tempo parece mais longo?<div class="lines l3"></div></li>
          <li>O poema fala de coisas que se perdem e de coisas que se encontram. Dá um exemplo de cada.<div class="lines l3"></div></li>
          <li>O último verso é diferente dos outros? Que efeito tem no leitor?<div class="lines l3"></div></li>
        </ol>
        <div class="act"><div class="num">✎</div><div class="body"><p class="q">Escreve três versos teus que comecem por «E por vezes». Lê-os em voz alta, com pausas. <span class="pill oral">Oralidade</span></p><div class="lines l3"></div></div></div>
      </div>
    </div>'''))

# ------------------------------------------------------------------ P4 ALEGRE
P.append(page('u3-p4', '', 'Poema 4 · Trova do vento que passa', f'''
    <div class="kicker"><b>Poema 4</b> <span class="skill sk-lit">Ed. literária</span> Guia de leitura · lê e ouve o poema completo</div>
    <h1 class="title">Trova do vento <em>que passa</em></h1>
    <p class="byline">Manuel Alegre · <i>Praça da Canção</i> (1965)</p>
    <div class="hero-img slim" style="background-image:url(../art/jpg/u3_medo.jpg); background-position: 75% 40%;"></div>
    <div class="guide">
      <div class="gd-c">
        <p><b>Manuel Alegre</b> (n. 1936), poeta e político, escreveu este poema em 1963, no tempo da ditadura; pouco depois partiria para o exílio. Musicado por António Portugal e cantado por Adriano Correia de Oliveira, tornou-se um hino de resistência e de liberdade.</p>
        {cite(['Pergunto ao vento que passa', 'notícias do meu país', 'e o vento cala a desgraça', 'o vento nada me diz.'], 'Manuel Alegre, «Trova do vento que passa», 1.ª estrofe')}
        <h3>Uma trova</h3>
        <p>Trova é uma composição ao gosto popular, feita para ser cantada: quadras em <b>redondilha maior</b>, com rima e muitas repetições.</p>
        <div class="tl">
          <div><b>1933</b><span>Começa o Estado Novo: censura e polícia política.</span></div>
          <div><b>1963</b><span>Manuel Alegre escreve a «Trova»; é musicada por António Portugal.</span></div>
          <div><b>1964</b><span>Alegre parte para o exílio, em Argel.</span></div>
          <div><b>1974</b><span>25 de Abril: a Revolução dos Cravos devolve a liberdade.</span></div>
        </div>
        <div class="act"><div class="num">✎</div><div class="body"><p class="q">Ouve a canção. A música torna o poema mais triste, mais forte, mais esperançoso? <span class="pill oral">Oralidade</span></p><div class="lines l2"></div></div></div>
      </div>
      <div class="gd-c rd">
        <h3>Oficina</h3>
        <ol class="qs">
          <li>Faz a escansão do 3.º e do 4.º versos da estrofe citada. Confirma que são redondilhas maiores.
            <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
            <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></li>
          <li>Qual é o esquema rimático da quadra? Como se chama este tipo de rima?<div class="lines l1"></div></li>
          <li>O sujeito poético pergunta ao vento e, noutras estrofes, aos rios. Que figura de estilo é dirigir-se a quem não pode responder?<div class="lines l1"></div></li>
          <li>Porque é que o vento «cala a desgraça»? O que nos diz isto sobre o país daquele tempo?<div class="lines l3"></div></li>
          <li>O poema termina com esperança ou com desânimo? Justifica com versos do poema completo.<div class="lines l3"></div></li>
        </ol>
      </div>
    </div>'''))

# ------------------------------------------------------------------ P5 HATHERLY
P.append(page('u3-p5', '', 'Poema 5 · Ana Hatherly', '''
    <div class="kicker"><b>Poema 5</b> <span class="skill sk-lit">Ed. literária</span> <span class="skill sk-esc">Escrita</span> Poesia experimental</div>
    <h1 class="title">Quando o poema <em>se vê</em></h1>
    <p class="byline">Ana Hatherly (1929–2015) · <i>Tisanas</i> e poesia visual</p>
    <div class="guide">
      <div class="gd-c">
        <p><b>Ana Hatherly</b> foi poeta, artista plástica, cineasta e professora universitária. Nos anos 60, fez parte do grupo da <b>Poesia Experimental</b> portuguesa, que quis libertar o poema das regras: o poema podia ser desenho, colagem, letra espalhada pela página.</p>
        <h3>As Tisanas</h3>
        <p>São pequenos <b>poemas em prosa</b>, numerados, que Hatherly foi escrevendo ao longo de décadas: histórias absurdas, paradoxos, jogos com a lógica e com as palavras. Não têm verso nem rima — e, no entanto, são poesia. Porquê? Pela concentração, pela surpresa, pela imagem.</p>
        <h3>A poesia visual</h3>
        <p>Nos poemas visuais, a <b>forma</b> faz parte do sentido: as letras desenham, caem, sobem, apagam-se. O leitor lê e vê ao mesmo tempo.</p>
        <div class="vp">
          <div class="vp1">c<br>&nbsp;a<br>&nbsp;&nbsp;i<br>&nbsp;&nbsp;&nbsp;r</div>
          <div class="vp2">o mar o mar o mar o mar<br>o mar o mar o mar o mar<br>o mar o mar o <b>farol</b> o mar</div>
          <small>Dois exemplos criados para esta unidade.</small>
        </div>
      </div>
      <div class="gd-c rd">
        <h3>Na antologia</h3>
        <ol class="qs">
          <li>Lê duas <i>Tisanas</i>. O que te surpreendeu em cada uma?<div class="lines l2"></div></li>
          <li>Porque podemos chamar «poema» a um texto sem versos?<div class="lines l2"></div></li>
          <li>Observa um poema visual de Hatherly. O que vês antes de ler? E depois?<div class="lines l2"></div></li>
        </ol>
        <div class="act"><div class="num">✎</div><div class="body"><p class="q">Cria um <b>poema visual</b> com uma só palavra ou uma frase curta (por exemplo: <i>chuva, voar, medo, sonho</i>). A forma deve ajudar o sentido.</p><div class="drawbox tall2"></div></div></div>
      </div>
    </div>'''))

# ------------------------------------------------------------------ P6 TORGA
P.append(page('u3-p6', '', 'Poema 6 · Sísifo', f'''
    <div class="kicker"><b>Poema 6</b> <span class="skill sk-lit">Ed. literária</span> Guia de leitura · lê o poema completo na antologia</div>
    <h1 class="title"><em>Sísifo</em></h1>
    <p class="byline">Miguel Torga · <i>Diário XIII</i> (1983)</p>
    <div class="hero-img short" style="background-image:url(../art/jpg/u3_tejo.jpg); background-position: 20% 50%;"></div>
    <div class="guide">
      <div class="gd-c">
        <p><b>Miguel Torga</b> (1907–1995), pseudónimo de Adolfo Correia da Rocha, médico e escritor transmontano, escreveu um <i>Diário</i> em dezasseis volumes, com prosa e poemas.</p>
        <h3>O mito</h3>
        <p>Na mitologia grega, <b>Sísifo</b> foi condenado pelos deuses a empurrar uma enorme pedra até ao cimo de um monte. Sempre que lá chegava, a pedra rolava de novo para baixo — e ele tinha de recomeçar. Para sempre.</p>
        {cite(['Recomeça…', 'Se puderes,', 'Sem angústia', 'E sem pressa.'], 'Miguel Torga, «Sísifo», versos 1–4')}
      </div>
      <div class="gd-c rd">
        <h3>Enquanto lês</h3>
        <ol class="qs">
          <li>O poema começa com um verbo no <b>imperativo</b>. A quem se dirige o sujeito poético? (A si próprio? Ao leitor? A todos?)<div class="lines l2"></div></li>
          <li>Os versos são muito curtos. Que efeito tem esse ritmo?<div class="lines l1"></div></li>
          <li>Para Torga, recomeçar é um castigo ou uma forma de liberdade? Justifica.<div class="lines l2"></div></li>
          <li>Relaciona o título com o conselho do poema.<div class="lines l2"></div></li>
          <li>Dá um exemplo da tua vida em que tiveste de recomeçar.<div class="lines l2"></div></li>
        </ol>
      </div>
    </div>'''))

# ------------------------------------------------------------------ P7 FONSECA
P.append(page('u3-p7', '', 'Poema 7 · Tejo que levas as águas', f'''
    <div class="kicker"><b>Poema 7</b> <span class="skill sk-lit">Ed. literária</span> Guia de leitura · lê e ouve o poema completo</div>
    <h1 class="title">Tejo que levas <em>as águas</em></h1>
    <p class="byline">Manuel da Fonseca · <i>Poemas para Adriano</i> (1972)</p>
    <div class="hero-img short" style="background-image:url(../art/jpg/u3_tejo.jpg); background-position: 85% 45%;"></div>
    <div class="guide">
      <div class="gd-c">
        <p>Já conheces <b>Manuel da Fonseca</b> do conto «Mestre Finezas» (Unidade 2). Também foi poeta. Este poema foi cantado por Adriano Correia de Oliveira.</p>
        {cite(['Tejo que levas as águas', 'correndo de par em par', 'lava a cidade de mágoas', 'leva as mágoas para o mar'], 'Manuel da Fonseca, «Tejo que levas as águas», 1.ª estrofe')}
        <div class="focus"><b>A observar</b>
          <p><u>Apóstrofe</u> — o sujeito poético fala diretamente com o rio: «Tejo que levas…».</p>
          <p><u>Personificação</u> — o rio pode «lavar» e «levar»: é como alguém a quem se pede ajuda.</p>
          <p><u>Redondilha maior</u> e <u>rima cruzada</u> — o poema pede para ser cantado.</p>
        </div>
      </div>
      <div class="gd-c rd">
        <h3>Oficina</h3>
        <ol class="qs">
          <li>Faz a escansão dos versos 1 e 4 da estrofe citada.
            <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
            <div class="scan-blank"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></li>
          <li>Esquema rimático da estrofe: <span class="blank w2"></span></li>
          <li>Que «mágoas» da cidade pede o poeta ao rio que leve? Procura-as nas estrofes seguintes.<div class="lines l3"></div></li>
          <li>Compara com a «Trova do vento que passa»: o que têm em comum o vento e o rio nos dois poemas?<div class="lines l3"></div></li>
          <li>Escreve uma quadra tua em redondilha maior em que peças ao rio da tua terra que leve alguma coisa.<div class="lines l3"></div></li>
        </ol>
      </div>
    </div>'''))

# ------------------------------------------------------------------ P8/P9 FLORBELA
ser = (T / 'ser_poeta.txt').read_text()
fan = (T / 'fanatismo.txt').read_text()
P.append(page('u3-p8', '', 'Poema 8 · Ser Poeta', f'''
    <div class="kicker"><b>Poema 8</b> <span class="skill sk-lei">Leitura</span> <span class="skill sk-ora">Oralidade</span> Poema integral</div>
    <div class="fb">
      <div class="fb-l">
        <h1 class="title">Ser <em>Poeta</em></h1>
        <p class="byline">Florbela Espanca · <i>Charneca em Flor</i> (1931)</p>
        {poem(ser)}
        <p class="src">Florbela Espanca, «Ser Poeta», <i>Charneca em Flor</i> (1931). Domínio público.</p>
      </div>
      <div class="fb-r">
        <div class="fb-img" style="background-image:url(../art/jpg/u3_florbela.jpg)"></div>
        <div class="qr-inline"><div class="qr" style="width:25mm;height:25mm">{{{{QR:https://commons.wikimedia.org/?curid=27859175}}}}</div><span><b>Ouve o soneto</b> (Wikimedia Commons, leitura de Daniel Barbosa, com pronúncia do Brasil) e repara onde a voz para: no fim do verso ou a meio?</span></div>
        <p class="bio"><b>Florbela Espanca</b> (1894–1930), alentejana de Vila Viçosa, é uma das grandes vozes da poesia portuguesa. Escreveu sobretudo sonetos, com uma intensidade rara: o amor, a dor, o desejo de absoluto.</p>
      </div>
    </div>
    <div class="son">
      <div class="son-h">Anatomia de um soneto</div>
      <div><b>14 versos</b><span>2 quadras + 2 tercetos</span></div>
      <div><b>Decassílabos</b><span>10 sílabas métricas</span></div>
      <div><b>Esquema</b><span>ABBA ABBA CDC EDE</span></div>
      <div><b>Chave de ouro</b><span>o último verso fecha a ideia com força</span></div>
    </div>
    <div class="act"><div class="num">✎</div><div class="body">
      <p class="q">Lê o soneto em voz alta duas vezes, a primeira depressa, a segunda devagar, com pausas nas vírgulas e nas reticências. Qual das leituras respeita melhor o poema? Porquê? <span class="pill oral">Oralidade</span></p>
      <div class="lines l2"></div>
    </div></div>'''))

P.append(page('u3-p9', '', 'Poema 9 · Fanatismo', f'''
    <div class="kicker"><b>Poema 9</b> <span class="skill sk-lei">Leitura</span> Poema integral · comparar</div>
    <div class="fan-h"><div><h1 class="title"><em>Fanatismo</em></h1>
      <p class="byline">Florbela Espanca · <i>Livro de Sóror Saudade</i> (1923)</p></div>
      <div class="qr-inline"><div class="qr" style="width:25mm;height:25mm">{{{{QR:https://commons.wikimedia.org/?curid=27859388}}}}</div><span><b>Ouve outro soneto de Florbela, «Amar!»</b> (Wikimedia Commons). Que palavras e sentimentos tem em comum com «Fanatismo»?</span></div></div>
    <div class="fan-p">{poem(fan).replace('class="vpoem"', 'class="vpoem two"')}</div>
    <p class="src">Florbela Espanca, «Fanatismo», <i>Livro de Sóror Saudade</i> (1923). Domínio público.</p>
    <div class="fan-q">
      <h3>Os dois sonetos</h3>
      <ol class="qs two">
        <li>Confirma que «Fanatismo» é um soneto: número de versos, tipo de estrofes, esquema rimático.<div class="lines l2"></div></li>
        <li>Faz a escansão do verso 2: <i>Meus olhos andam cegos de te ver.</i><div class="scan-blank ten"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></li>
        <li>Em «Ser Poeta», «É ser…», «É ter…» repetem-se no início dos versos. Como se chama este recurso?<div class="lines l1"></div></li>
        <li>«Meus olhos andam cegos de te ver» parece uma contradição. Explica o sentido deste <b>paradoxo</b>.<div class="lines l3"></div></li>
        <li>Os dois sonetos terminam com uma declaração de amor. Qual das «chaves de ouro» te parece mais forte? Porquê?<div class="lines l4"></div></li>
        <li>O que é, para Florbela, «ser poeta»? Escolhe dois versos que o mostrem.<div class="lines l4"></div></li>
        <li>Qual dos dois sonetos preferes ler em voz alta? Porquê?<div class="lines l3"></div></li>
      </ol>
    </div>'''))

# ------------------------------------------------------------------ RECURSOS
rec = [('Anáfora', 'Repetição de palavras no início de versos ou frases.', '«E por vezes… / E por vezes…» (Mourão-Ferreira)'),
       ('Enumeração', 'Sequência de elementos da mesma natureza.', '«pernas / ambulâncias / e o luxo blindado» (O\'Neill)'),
       ('Metáfora', 'Comparação implícita, sem «como».', '«o sonho comanda a vida» (Gedeão)'),
       ('Comparação', 'Aproximação de duas realidades com «como», «tal como»…', '«tu és como Deus: princípio e fim» (Florbela)'),
       ('Personificação', 'Dar qualidades humanas a seres não humanos.', '«o vento cala a desgraça» (Alegre)'),
       ('Apóstrofe', 'Chamamento ou interpelação de alguém ou de algo.', '«Tejo que levas as águas» (Fonseca)'),
       ('Hipérbole', 'Exagero intencional.', '«os meses oceanos» (Mourão-Ferreira)'),
       ('Antítese', 'Aproximação de ideias opostas.', '«Morder como quem beija» (Florbela)'),
       ('Paradoxo', 'Ideias que parecem contraditórias mas fazem sentido.', '«Meus olhos andam cegos de te ver» (Florbela)'),
       ('Pleonasmo', 'Repetição de uma ideia para a reforçar.', '«Vi com os meus próprios olhos»'),
       ('Aliteração', 'Repetição de sons consonânticos.', '«Rei do Reino de Aquém e de Além Dor» (Florbela)'),
       ('Imperativo', 'Forma verbal de ordem, pedido ou conselho.', '«Recomeça…» (Torga)')]
rh = "".join(f'<div class="rc"><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in rec)
P.append(page('u3-rec', 'v-oficina-p', 'Recursos expressivos', f'''
    <div class="kicker"><b>Unidade 3</b> <span class="skill sk-lit">Ed. literária</span> Referência</div>
    <h1 class="title">O guia <em>dos recursos</em></h1>
    <p class="lede sm">Os recursos expressivos são as ferramentas do poeta. Reconhecê-los é o primeiro passo; o segundo — o mais importante — é explicar o <b>efeito</b> que produzem.</p>
    <div class="recs">{rh}</div>
    <div class="formula"><b>Fórmula para o comentário</b> «No verso <u>__</u>, o poeta recorre a <u>(recurso)</u> — <u>(citação)</u> — para <u>(efeito: sublinhar, intensificar, sugerir, contrastar…)</u>.»</div>'''))

# ------------------------------------------------------------------ COMENTÁRIO
P.append(page('u3-com', 'v-oficina-p', 'Escrita · Comentário', '''
    <div class="kicker"><b>Unidade 3</b> <span class="skill sk-esc">Escrita</span> Comentário a um poema</div>
    <h1 class="title">Comentar <em>um poema</em></h1>
    <p class="lede sm">Um comentário de poema responde a duas perguntas: <b>de que fala</b> o poema (tema) e <b>como o diz</b> (recursos, forma, ritmo). Tudo com provas — versos citados entre aspas.</p>
    <div class="cm">
      <div class="cm-h">Estrutura em quatro parágrafos</div>
      <div class="cm-r"><span>1</span><b>Apresentação</b><p>Título, autor, e o tema numa frase. <i>«Em "Sísifo", Miguel Torga reflete sobre a necessidade de recomeçar.»</i></p></div>
      <div class="cm-r"><span>2</span><b>O tema desenvolvido</b><p>Como evolui o poema, estrofe a estrofe. Quem fala? A quem?</p></div>
      <div class="cm-r"><span>3</span><b>Um recurso e o seu efeito</b><p>Identifica, cita, explica o efeito (usa a fórmula da p. <span class="ref" data-ref="u3-rec"></span>). Se possível, também a forma: estrofes, métrica, rima.</p></div>
      <div class="cm-r"><span>4</span><b>Apreciação</b><p>O que o poema te fez pensar ou sentir, e porquê. Pode ser atual?</p></div>
    </div>
    <div class="modelc"><b>Exemplo de parágrafo 3</b><p>Logo no primeiro verso, o poeta usa o imperativo — «Recomeça…» — como se desse um conselho ao leitor e a si próprio. As reticências prolongam a palavra e sugerem que recomeçar é um gesto que se repete, tal como o de Sísifo.</p></div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Escolhe um dos nove poemas e escreve um comentário (180 a 230 palavras) com o tema e, pelo menos, um recurso expressivo explicado.</p>
      <div class="lines l16"></div>
    </div></div>'''))

# ------------------------------------------------------------------ GRAMÁTICA DO VERSO
P.append(page('u3-g', 'v-oficina-p', 'Gramática do verso', '''
    <div class="kicker"><b>Unidade 3</b> <span class="skill sk-gra">Gramática</span> Classes de palavras no verso · pontuação e ritmo</div>
    <h1 class="title">As palavras <em>que o verso escolhe</em></h1>
    <p class="lede sm">Num poema, cada palavra conta. Observar as <b>classes de palavras</b> ajuda a perceber o estilo: um poema cheio de verbos tem movimento; um poema cheio de nomes e adjetivos é mais descritivo, mais parado.</p>
    <div class="cls">
      <div class="cl-row"><span class="w n">Tejo</span><span class="w p">que</span><span class="w v">levas</span><span class="w d">as</span><span class="w n">águas</span></div>
      <div class="cl-key"><span class="n">nome</span><span class="p">pronome relativo</span><span class="vl">verbo</span><span class="d">determinante</span><span class="a">adjetivo</span><span class="av">advérbio</span></div>
    </div>
    <div class="act"><div class="num">1</div><div class="body">
      <p class="q">Classifica as palavras do verso de Florbela: <i>«É ter cá dentro um astro que flameja»</i>.</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">2</div><div class="body">
      <p class="q">Em «Ser Poeta», predominam os verbos no infinitivo (<i>ser, morder, dar, ter…</i>). Que efeito tem essa escolha?</p>
      <div class="lines l2"></div>
    </div></div>
    <h2 class="sub">Pontuação e ritmo</h2>
    <div class="pr3">
      <div><b>. ! ?</b><span>pausa longa; entoação de afirmação, emoção ou pergunta</span></div>
      <div><b>, ;</b><span>pausa breve; separa elementos de uma enumeração</span></div>
      <div><b>…</b><span>suspensão; algo fica por dizer, prolonga-se</span></div>
      <div><b>sem pontuação</b><span>o leitor decide as pausas; o ritmo nasce do verso (O'Neill, Alegre)</span></div>
    </div>
    <div class="act"><div class="num">3</div><div class="body">
      <p class="q">Lê em voz alta a primeira quadra de «Fanatismo» duas vezes: primeiro, parando no fim de cada verso; depois, respeitando só a pontuação. Qual das leituras preferes? Porquê?</p>
      <div class="lines l2"></div>
    </div></div>
    <div class="act"><div class="num">4</div><div class="body">
      <p class="q">Pontua a estrofe citada de «Tejo que levas as águas» como achares que deve ser lida e justifica uma das tuas escolhas.</p>
      <div class="lines l4"></div>
    </div></div>'''))

# ------------------------------------------------------------------ PROJETO
P.append(page('u3-proj', '', 'Sarau de poesia', '''
    <div class="kicker"><b>Projeto</b> <span class="skill sk-ora">Oralidade</span> Em grupo · 2 semanas</div>
    <h1 class="title">Sarau <em>no farol</em></h1>
    <p class="lede sm">A turma organiza um <b>sarau de poesia</b> — uma noite (ou uma aula) em que os poemas são ditos, cantados e mostrados. Cada grupo prepara um momento de 4 a 6 minutos.</p>
    <div class="ep">
      <div><span>01</span><b>Escolher</b><p>Um dos nove poemas e um poema de um poeta à vossa escolha.</p></div>
      <div><span>02</span><b>Apresentar</b><p>30 segundos sobre o poeta e o tempo em que escreveu.</p></div>
      <div><span>03</span><b>Dizer</b><p>O poema dito de cor, com pausas, volume e intenção.</p></div>
      <div><span>04</span><b>Transformar</b><p>Um poema visual, uma quadra vossa, ou a canção.</p></div>
      <div><span>05</span><b>Explicar</b><p>Um recurso expressivo e o seu efeito, em 1 minuto.</p></div>
    </div>
    <div class="roles"><b>Para dizer bem</b><span>olha o público</span><span>respeita a pontuação</span><span>não corras</span><span>faz pausas antes das palavras importantes</span><span>varia o volume</span></div>
    <table class="fill rub">
      <tr><th>Critério</th><th>Em construção</th><th>Consolidado</th><th>Excelente</th></tr>
      <tr><td><b>Dizer o poema</b></td><td>leitura hesitante</td><td>de cor, ritmo adequado</td><td>expressivo, pausas intencionais, contacto visual</td></tr>
      <tr><td><b>Conhecimento</b></td><td>informação vaga</td><td>poeta e contexto corretos</td><td>ligação clara entre contexto e poema</td></tr>
      <tr><td><b>Análise</b></td><td>recurso identificado</td><td>recurso e efeito</td><td>efeito relacionado com o tema</td></tr>
      <tr><td><b>Criatividade</b></td><td>transformação simples</td><td>transformação cuidada</td><td>transformação original que ilumina o poema</td></tr>
      <tr><td><b>Grupo</b></td><td>participação desigual</td><td>todos participam</td><td>momento coeso e bem ensaiado</td></tr>
    </table>
    <table class="fill tall gui"><tr><th style="width:30mm">Momento</th><th>Quem</th><th>O quê</th><th style="width:22mm">Tempo</th></tr>
      <tr><td>Apresentar</td><td></td><td></td><td></td></tr><tr><td>Dizer</td><td></td><td></td><td></td></tr><tr><td>Transformar</td><td></td><td></td><td></td></tr><tr><td>Explicar</td><td></td><td></td><td></td></tr></table>
    <div class="cal">
      <div><b>Semana 1 · dia 1</b><span>Escolher poemas e distribuir tarefas</span></div>
      <div><b>Semana 1 · dia 3</b><span>Guião do momento entregue</span></div>
      <div><b>Semana 2 · dia 2</b><span>Ensaio geral, com cronómetro</span></div>
      <div><b>Semana 2 · dia 4</b><span>Sarau: turma, famílias, convidados</span></div>
    </div>
    <div class="after"><b>Depois do sarau</b> Qual foi o momento de outro grupo que mais te tocou? Porquê?<div class="lines l3"></div></div>'''))

# ------------------------------------------------------------------ BALANÇO
P.append(page('u3-bal', '', 'Balanço', '''
    <div class="kicker"><b>Balanço</b> Unidade 3</div>
    <h1 class="title">Dez perguntas <em>em verso</em></h1>
    <div class="quiz">
      <div><i>1</i>Uma estrofe de quatro versos chama-se <span class="blank w2"></span></div>
      <div><i>2</i>O esquema ABAB corresponde à rima <span class="blank w2"></span></div>
      <div><i>3</i>Um verso de sete sílabas métricas é uma <span class="blank w3"></span></div>
      <div><i>4</i>«Pergunto ao vento que passa» tem <span class="blank w1"></span> sílabas métricas.</div>
      <div><i>5</i>O soneto tem 14 versos: duas <span class="blank w2"></span> e dois <span class="blank w2"></span></div>
      <div><i>6</i>«E por vezes… / E por vezes…» — recurso: <span class="blank w2"></span></div>
      <div><i>7</i>«o vento cala a desgraça» — recurso: <span class="blank w2"></span></div>
      <div><i>8</i>Em «Eles não sabem que o sonho comanda a vida», a oração «que o sonho comanda a vida» é subordinada <span class="blank w2"></span></div>
      <div><i>9</i>«De repente» é uma <span class="blank w3"></span></div>
      <div><i>10</i>«Entrar para dentro» é um pleonasmo <span class="opt">expressivo · vicioso</span></div>
    </div>
    <div class="selfcheck">
      <div class="sc-h"><span>Consigo…</span><span>ainda não</span><span>quase</span><span>sim!</span></div>
      <div class="sc-r"><span>identificar estrofes e desenhar o esquema rimático</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>contar sílabas métricas e reconhecer a redondilha</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>reconhecer um soneto e o decassílabo</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>identificar recursos expressivos e explicar o efeito</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>distinguir o que o poema diz do que deixa entender</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>escrever um comentário a um poema</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>reconhecer completivas, advérbios, sujeito e predicado</span><i></i><i></i><i></i></div>
      <div class="sc-r"><span>dizer um poema em voz alta, com expressividade</span><i></i><i></i><i></i></div>
    </div>
    <div class="act"><div class="num">✎</div><div class="body">
      <p class="q">Que verso desta unidade gostavas de guardar de cor? Porquê?</p>
      <div class="lines l4"></div>
    </div></div>'''))

# ------------------------------------------------------------------ GLOSSÁRIO + SOLUÇÕES
P.append(page('u3-sol', 'backmatter', 'Glossário · soluções', '''
    <div class="bm-cols">
      <div>
        <h2>Glossário</h2>
        <dl class="gl">
          <dt>Chave de ouro</dt><dd>Último verso de um soneto, que fecha a ideia com força.</dd>
          <dt>Decassílabo</dt><dd>Verso de dez sílabas métricas.</dd>
          <dt>Elisão</dt><dd>Junção, numa só sílaba métrica, de uma vogal final com a vogal inicial seguinte.</dd>
          <dt>Escansão</dt><dd>Divisão de um verso em sílabas métricas.</dd>
          <dt>Esquema rimático</dt><dd>Representação, com letras, da disposição das rimas.</dd>
          <dt>Poema em prosa</dt><dd>Texto poético sem divisão em versos.</dd>
          <dt>Poesia visual</dt><dd>Poesia em que a forma gráfica faz parte do sentido.</dd>
          <dt>Redondilha maior / menor</dt><dd>Verso de sete / de cinco sílabas métricas.</dd>
          <dt>Soneto</dt><dd>Poema de catorze versos: duas quadras e dois tercetos.</dd>
          <dt>Sujeito poético</dt><dd>A voz que fala no poema (não é, necessariamente, o autor).</dd>
          <dt>Verso livre</dt><dd>Verso sem medida fixa.</dd>
          <dt>Verso solto</dt><dd>Verso que não rima com nenhum outro.</dd>
          <dt>Hiato</dt><dd>Separação, em duas sílabas métricas, de vogais seguidas.</dd>
          <dt>Trova</dt><dd>Composição de gosto popular, feita para ser cantada.</dd>
        </dl>
      </div>
      <div>
        <h2>Soluções</h2>
        <div class="sol">
          <p><b>p. <span class="ref" data-ref="u3-aq"></span> · Aquecimento.</b> 1. Quadra 1: ABAB (cruzada) · quadra 2: ABAB (cruzada) · quadra 3: ABBA (interpolada). Nenhuma é emparelhada. 2. Ó / ve / lho / Ci / ne / ma_Au / ro(ra) = 7 · que_a / pos / sa_um / di / a_a / pa / gar = 7.</p>
          <p><b>p. <span class="ref" data-ref="u3-p1-g"></span> · Pleonasmo e completivas.</b> 1. a) H · b) E · c) P · d) H. 2. a) que o sonho faz o mundo avançar · b) se Gedeão era mais cientista ou mais poeta · c) que íamos ouvir o poema cantado.</p>
          <p><b>p. <span class="ref" data-ref="u3-p2-g"></span> · Advérbios, sujeito e predicado.</b> 1. De repente (tempo) · baixinho (modo) · às escondidas (modo) · nunca (tempo/negação). 2. a) S: Os vizinhos · P: desconfiavam uns dos outros · b) sujeito inexistente (verbo haver) · P: Nas paredes havia ouvidos · c) S: um homem de chapéu · P: Entrou na sala.</p>
          <p><b>p. <span class="ref" data-ref="u3-p4"></span> · Trova.</b> 1. e_o / ven / to / ca / la_a / des / gra(ça) = 7 · o / ven / to / na / da / me / diz = 7. 2. ABAB, rima cruzada. 3. Apóstrofe (e personificação do vento).</p>
          <p><b>p. <span class="ref" data-ref="u3-p7"></span> · Tejo.</b> 1. Te / jo / que / le / vas / as / á(guas) = 7 · le / va_as / má / goas / pa / ra_o / mar = 7. 2. ABAB.</p>
          <p><b>p. <span class="ref" data-ref="u3-p9"></span> · Florbela.</b> 1. 14 versos, 2 quadras + 2 tercetos; ABBA ABBA CCD EED. 2. Meus / o / lhos / an / dam / ce / gos / de / te / ver = 10. 3. Anáfora.</p>
          <p><b>p. <span class="ref" data-ref="u3-bal"></span> · Balanço.</b> 1 quadra · 2 cruzada · 3 redondilha maior · 4 sete · 5 quadras, tercetos · 6 anáfora · 7 personificação · 8 completiva · 9 locução adverbial · 10 vicioso.</p>
        </div>
      </div>
    </div>
    <div class="memo sm">
      <div class="memo-h">Cartão de memória · a unidade numa página</div>
      <div class="memo-g">
        <div class="m-s"><b>A forma</b><ul><li>Estrofes: dístico, terceto, quadra… soneto (4+4+3+3).</li><li>Rima: emparelhada AABB, cruzada ABAB, interpolada ABBA.</li><li>Métrica: contar até à última tónica; elisões. Redondilha maior 7, menor 5; decassílabo 10.</li></ul></div>
        <div class="m-r"><b>O sentido</b><ul><li>Tema: de que fala o poema.</li><li>Sujeito poético: quem fala.</li><li>Recursos: anáfora, enumeração, metáfora, comparação, personificação, apóstrofe, hipérbole, antítese, paradoxo.</li><li>O que diz e o que deixa entender (ironia).</li></ul></div>
        <div class="m-g"><b>Gramática</b><ul><li>Completiva: completa um verbo (<i>que, se</i>).</li><li>Advérbio e locução adverbial: modo, tempo, lugar…</li><li>Sujeito (quem? o quê?) e predicado.</li><li>Pleonasmo e hipérbole.</li></ul></div>
      </div>
    </div>'''))

(R / 'src' / 'u3.html').write_text("\n".join(P))
print(len(P), 'pages')
