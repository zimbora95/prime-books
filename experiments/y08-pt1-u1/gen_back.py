"""Generate src/back.html — general glossary/index (2 pp.) + sources & credits (1 p.)."""
import pathlib
R = pathlib.Path(__file__).parent


def ref(i): return f'<span class="ref" data-ref="{i}"></span>'


TERMS = [
    ("Advérbio e locução adverbial", "Palavra ou grupo de palavras que modifica o verbo: modo, tempo, lugar…", ["u3-p2-g"]),
    ("Alcance da crítica · classificação", "Juízo final expresso em estrelas, notas ou recomendação.", ["s18"]),
    ("Anáfora", "Repetição de palavras no início de versos ou frases.", ["u3-rec"]),
    ("Anúncio comercial / não comercial", "Vende um produto / defende uma causa ou um comportamento.", ["s6", "s7"]),
    ("Antítese", "Aproximação de ideias opostas.", ["u3-rec"]),
    ("Apelo à ação", "Parte do anúncio que diz o que fazer a seguir.", ["s8"]),
    ("Aparte", "Fala que só o público ouve.", ["u4-map"]),
    ("Apóstrofe", "Interpelação de alguém ou de algo.", ["u3-rec"]),
    ("Argumento · tese", "Razão que sustenta uma opinião · opinião principal.", ["s18", "u6-esc"]),
    ("Artigo de opinião", "Texto que defende uma tese com argumentos.", ["u3-p1-e", "u6-esc"]),
    ("Ato · cena · quadro", "Divisões da peça de teatro.", ["u4-map"]),
    ("Comentário de poema", "Tema + recursos + efeito, com citações.", ["u3-com"]),
    ("Comparação", "Aproximação de duas realidades com «como».", ["u3-rec"]),
    ("Complemento direto / indireto", "Completa o verbo sem preposição (o, a) / destinatário (lhe).", ["u4-l2-g"]),
    ("Conjuntivo", "Modo do desejo, da dúvida, da hipótese.", ["u2-n4-g", "u2-n7-g"]),
    ("Crítica", "Texto que avalia, de forma fundamentada, uma obra.", ["s15", "s18"]),
    ("Decassílabo", "Verso de dez sílabas métricas.", ["u3-v2"]),
    ("Didascália", "Indicação cénica: espaço, luz, som, movimento, tom.", ["u4-map", "u4-l1-gr"]),
    ("Discurso direto / indireto", "Falas reproduzidas tal e qual / contadas pelo narrador.", ["u2-map"]),
    ("Elisão · hiato", "Junção / separação de vogais na contagem métrica.", ["u3-v2"]),
    ("Enumeração", "Sequência de elementos da mesma natureza.", ["s9"]),
    ("Escansão", "Divisão do verso em sílabas métricas.", ["u3-v2"]),
    ("Esquema rimático", "Letras que mostram como rimam os versos.", ["u3-v1"]),
    ("Estrofe", "Grupo de versos: dístico, terceto, quadra…", ["u3-v1"]),
    ("Estrutura da narrativa", "Situação inicial, desenvolvimento, desenlace.", ["u2-map"]),
    ("Exposição · conflito · desenlace", "Estrutura interna do texto dramático.", ["u4-map"]),
    ("Facto / opinião", "Informação verificável / juízo de valor.", ["s18"]),
    ("Formação de palavras", "Derivação, composição, parassíntese.", ["u2-n5-g"]),
    ("Frase ativa / passiva", "O sujeito pratica / sofre a ação (ser + particípio).", ["s21"]),
    ("Frase simples / complexa", "Uma forma verbal / mais do que uma.", ["u2-n1-g"]),
    ("Hipérbole", "Exagero intencional.", ["s9", "u3-p1-g"]),
    ("Imperativo", "Modo da ordem e do conselho; forte na publicidade.", ["s8"]),
    ("Leitura em papéis", "Leitura em voz alta de uma peça, com personagens distribuídas.", ["u4-l1-t"]),
    ("Metáfora", "Comparação implícita.", ["u3-rec"]),
    ("Modificador do grupo verbal", "Informação acessória: tempo, lugar, modo.", ["u2-n6-g", "u4-l2-g"]),
    ("Modificador do nome", "Acrescenta informação ao nome (adjetivo, grupo preposicional).", ["u2-n5-g"]),
    ("Monólogo", "Fala de uma personagem sozinha.", ["u4-map"]),
    ("Narrador", "Quem conta: participante ou não participante.", ["u2-map"]),
    ("Oração completiva", "Completa o sentido de um verbo (que, se).", ["u3-p1-g"]),
    ("Oração condicional / final", "Exprime condição (se) / finalidade (para).", ["u2-n3-g"]),
    ("Oração relativa", "Introduzida por pronome relativo; modifica um nome.", ["u2-n2-g"]),
    ("Paradoxo", "Ideias que parecem contraditórias mas fazem sentido.", ["u3-rec"]),
    ("Personagens · espaço · tempo", "Categorias da narrativa.", ["u2-map"]),
    ("Personificação", "Qualidades humanas dadas a seres não humanos.", ["u3-rec"]),
    ("Pleonasmo", "Repetição de uma ideia, expressiva ou viciosa.", ["u3-p1-g"]),
    ("Poesia visual · poema em prosa", "A forma faz parte do sentido · poema sem versos.", ["u3-p5"]),
    ("Pronome pessoal átono", "Me, te, o, a, lhe…, junto do verbo.", ["u2-n6-g"]),
    ("Pronome relativo", "Que, quem, o qual, onde, cujo.", ["u2-n2-g"]),
    ("Recriação em prosa", "Contar o sentido de um poema por outras palavras.", ["u3-p2-e"]),
    ("Redondilha maior / menor", "Verso de sete / cinco sílabas métricas.", ["u3-v2"]),
    ("Rima cruzada · emparelhada · interpolada", "ABAB · AABB · ABBA.", ["u3-v1"]),
    ("Slogan", "Frase curta e memorável de um anúncio.", ["s13"]),
    ("Soneto", "Duas quadras e dois tercetos.", ["u3-p8"]),
    ("Sujeito · predicado", "De quem se fala · o que se diz dele.", ["u3-p2-g"]),
    ("Sujeito poético", "A voz que fala no poema.", ["u3-v1"]),
    ("Tempos do indicativo", "Presente, pretéritos, futuro.", ["u2-n7-g"]),
    ("Texto principal / secundário", "Falas / didascálias.", ["u4-map"]),
    ("Trocadilho · duplo sentido", "Jogo com os sentidos de uma palavra.", ["s13", "u5-e1"]),
    ("Verso livre", "Verso sem medida fixa.", ["u3-v2"]),
    ("Vilancete", "Mote seguido de voltas, com refrão.", ["u6-t2"]),
]
T2 = sorted(TERMS, key=lambda t: t[0].lower().replace("á", "a").replace("é", "e"))
half = (len(T2) + 1) // 2


def dl(items):
    return "".join(f'<div class="gi"><b>{a}</b><span>{b}</span><em>p. {", ".join(ref(r) for r in rs)}</em></div>' for a, b, rs in items)


P = []
P.append(f'''
<section id="z-glos" class="page v-neutro backmatter z-glos">
  <div class="rail"><span>Glossário geral</span></div>
  <div class="inner">
    <div class="kicker"><b>Glossário geral</b> Os conceitos do ano · onde os aprendeste</div>
    <h1 class="title">Da A <em>à Z</em></h1>
    <div class="gi-cols">{dl(T2[:half])}</div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Glossário geral</span></div>
</section>''')
P.append(f'''
<section id="z-glos2" class="page v-neutro backmatter z-glos">
  <div class="rail"><span>Glossário geral</span></div>
  <div class="inner">
    <div class="kicker"><b>Glossário geral</b> Continuação</div>
    <div class="gi-cols">{dl(T2[half:])}</div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Glossário geral</span></div>
</section>''')

TX = [
    ("Luís de Camões", "«Pastora da serra» · «Amor é um fogo…» · «Descalça vai para a fonte»", "Rimas (séc. XVI)", "domínio público · Wikisource"),
    ("Alexandre Herculano", "«O Castelo de Faria»", "Lendas e Narrativas (1851)", "domínio público"),
    ("Trindade Coelho", "«Parábola dos sete vimes»", "Os Meus Amores (1891)", "domínio público"),
    ("Eça de Queirós", "«O Tesouro» · «O Suave Milagre» (final)", "Contos (1902)", "domínio público · Wikisource"),
    ("Lima Barreto", "«O homem que sabia javanês»", "1911", "domínio público"),
    ("Florbela Espanca", "«Ser Poeta» · «Fanatismo»", "1923 · 1931", "domínio público"),
    ("Fernando Pessoa", "«Mar Português»", "Mensagem (1934)", "domínio público"),
    ("Júlio Verne · Oscar Wilde", "excertos traduzidos para este manual", "1872 · 1887", "originais em domínio público"),
    ("Gedeão, O'Neill, Mourão-Ferreira, Alegre, Hatherly, Torga, M. da Fonseca, Ondjaki, Alice Vieira", "versos e frases breves, com fonte", "—", "obras protegidas: citação para fins de ensino"),
]
AU = [
    ("«Mar Português»", "recitado por NMaia", "CC BY-SA 4.0", "Mar_Portuguez_recitado.ogg", "s10"),
    ("«Ser Poeta»", "Florbela Espanca · leitura de Daniel Barbosa", "domínio público", "Florbela_Espanca_-_Ser_poeta.ogg", "u3-p8"),
    ("«Amar!»", "Florbela Espanca · leitura de Daniel Barbosa", "domínio público", "Florbela_Espanca_-_Amar.ogg", "u3-p9"),
    ("«Amor é fogo que arde sem se ver»", "Camões · leitura de Daniel Barbosa", "domínio público", "Amorefogoqueardesemsever_08_camoes.ogg", "u5-e4"),
    ("«O Suave Milagre»", "Eça de Queirós · LibriVox, leitura de Lena", "domínio público", "Eça_de_Queirós_-_O_Suave_Milagre.ogg", "u6-t1"),
    ("«Descalça vai para a fonte»", "Camões · leitura de Carlos Gomes", "domínio público", "Spc109_descalcavaiparaafonte_camoes_ccg.ogg", "u6-t2"),
]
tx = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in TX)
au = "".join(f'<tr><td><b>{a}</b><small>{b}</small></td><td>{c}</td><td class="url">commons.wikimedia.org/wiki/File:{f}</td><td>p. {ref(r)}</td></tr>' for a, b, c, f, r in AU)
P.append(f'''
<section id="z-cred" class="page v-neutro backmatter z-cred">
  <div class="rail"><span>Fontes e créditos</span></div>
  <div class="inner">
    <div class="kicker"><b>Fontes e créditos</b> Tudo o que está neste livro, e de onde vem</div>
    <h1 class="title">Fontes <em>e créditos</em></h1>
    <h3 class="zh">Textos</h3>
    <table class="fill z-t"><tr><th>Autor</th><th>Texto</th><th>Obra · data</th><th>Estatuto</th></tr>{tx}</table>
    <h3 class="zh">Gravações (códigos QR)</h3>
    <table class="fill z-t"><tr><th>Gravação</th><th>Licença</th><th>Endereço permanente</th><th>No livro</th></tr>{au}</table>
    <p class="z-n">Todos os códigos QR deste livro apontam para arquivos públicos e permanentes (Wikimedia Commons) ou para o sítio da escola (primeschool.pt). Nenhum depende de um endereço temporário.</p>
    <div class="z-g">
      <div><h3 class="zh">Conteúdos criados para este manual</h3><p>Vila Nova do Farol, o Cinema Aurora, os filmes <i>O Farol das Baleias</i> e <i>A Última Sessão</i>, a revista <i>A Lupa</i>, as marcas, os anúncios, as críticas, as cenas «O ensaio geral», «A última bobina» e a adaptação de «O Castelo de Faria», as quadras de aquecimento e as respostas-modelo.</p></div>
      <div><h3 class="zh">Imagem e tipografia</h3><p>Ilustrações criadas com IA generativa sob direção de arte editorial, em estilo de risografia de três tintas; as capas seguem o padrão da coleção Prime School (natureza-morta em 3D na frente, lápis e aguarela no verso). Composição em Fraunces, Bricolage Grotesque e DM Mono; capas em Poppins e Andika (SIL Open Font License).</p></div>
    </div>
  </div>
  <div class="folio"><span class="n"></span><span class="t">Fontes e créditos</span></div>
</section>''')

(R / 'src' / 'back.html').write_text("\n".join(P))
print(len(P), 'pages', len(TERMS), 'terms')
