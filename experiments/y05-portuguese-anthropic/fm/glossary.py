"""Curated glossary of the year (edited by hand; pages are resolved from the built unit PDFs by build.py).

Each entry: (term, unit, definition, [search patterns]) — patterns are matched, case-insensitively, against
the bold lines first (where a term is taught) and then the running text of the unit's pages.
Definitions harvested from a unit's own «glossário» box replace these when the term matches exactly.
"""

G = [
    # ---- Unidade 1 (from Unit 1's own «Glossário da visita», p. 24)
    ("aceção", 1, "cada um dos significados de uma palavra no dicionário.", ["aceç"]),
    ("artigo de enciclopédia", 1, "texto que informa sobre um assunto, organizado por subtítulos.", ["artigo de enciclopédia", "enciclopédia"]),
    ("aviso", 1, "texto curto que informa ou alerta um grupo de pessoas.", ["aviso"]),
    ("exposição oral", 1, "apresentação de um tema a um público, com abertura, desenvolvimento e fecho.", ["exposição oral", "exposição"]),
    ("facto", 1, "informação que se pode verificar.", ["facto"]),
    ("graus do adjetivo", 1, "normal, comparativo e superlativo.", ["graus do adjetivo", "superlativo"]),
    ("modo imperativo", 1, "forma do verbo para ordenar, pedir ou aconselhar.", ["imperativo"]),
    ("nome coletivo", 1, "nome no singular que designa um conjunto.", ["coletivo"]),
    ("opinião", 1, "o que alguém pensa ou sente.", ["opinião"]),
    ("retrato", 1, "descrição de uma pessoa (física e psicológica) ou de um lugar.", ["retrato"]),
    ("verbete", 1, "texto que explica uma palavra no dicionário.", ["verbete"]),
    # ---- Unidade 2 (definitions aligned with the unit's own boxes: «A mala da narrativa», p. 27)
    ("lenda", 2, "narrativa tradicional, contada de geração em geração, que junta acontecimentos reais e maravilhosos.", ["lenda"]),
    ("relato de viagem", 2, "texto em que alguém conta, na primeira pessoa, uma viagem que fez.", ["relato"]),
    ("biografia", 2, "texto que conta a vida de uma pessoa, escrito por outra pessoa.", ["biografia"]),
    ("autobiografia", 2, "texto em que uma pessoa conta a sua própria vida.", ["autobiografia"]),
    ("narrador", 2, "a voz que conta a história; pode participar nela ou não.", ["narrador"]),
    ("personagem", 2, "cada ser (pessoa, animal ou objeto) que participa na ação de uma história.", ["personage"]),
    ("espaço", 2, "o lugar ou os lugares onde a ação acontece.", ["espaço"]),
    ("tempo", 2, "quando a ação acontece e quanto tempo dura.", ["tempo"]),
    ("ação", 2, "o que acontece na história, do princípio ao fim.", ["ação"]),
    ("estrutura da narrativa", 2, "a organização da história: situação inicial, problema, tentativas e resolução.", ["estrutura", "resolução"]),
    ("discurso direto", 2, "reprodução das palavras exatas de uma personagem, introduzidas por travessão.", ["discurso direto"]),
    ("travessão", 2, "sinal (—) que marca o início da fala de uma personagem.", ["travessão"]),
    ("verbo introdutor", 2, "verbo que anuncia uma fala: dizer, perguntar, responder, exclamar…", ["introdutor"]),
    ("pretérito perfeito", 2, "tempo verbal para ações acabadas no passado: «encontrou», «partiram».", ["perfeito"]),
    ("pretérito imperfeito", 2, "tempo verbal para descrever o passado ou falar de ações habituais: «era», «brincavam».", ["imperfeito"]),
    ("conector de tempo", 2, "palavra ou expressão que ordena os acontecimentos: primeiro, depois, entretanto, por fim.", ["conector"]),
    ("sinónimo", 2, "palavra com significado igual ou muito próximo de outra.", ["sinónimo"]),
    ("antónimo", 2, "palavra com significado contrário ao de outra.", ["antónimo"]),
    ("família de palavras", 2, "conjunto de palavras que nascem da mesma palavra: mar, marinheiro, maré.", ["família de palavras", "família"]),
    ("língua portuguesa no mundo", 2, "o português é língua oficial em nove países, em quatro continentes.", ["língua portuguesa", "lusofonia", "língua oficial"]),
    # ---- Unidade 3
    ("poema", 3, "texto escrito em verso, que joga com os sons, o ritmo e as imagens das palavras.", ["poema"]),
    ("verso", 3, "cada linha de um poema.", ["verso"]),
    ("estrofe", 3, "conjunto de versos separado por um espaço: dístico (2), terceto (3), quadra (4).", ["estrofe"]),
    ("rima", 3, "repetição de sons iguais ou parecidos no fim dos versos.", ["rima"]),
    ("rima emparelhada", 3, "rima de versos seguidos: AABB.", ["emparelhada"]),
    ("rima cruzada", 3, "rima alternada entre versos: ABAB.", ["cruzada"]),
    ("rima interpolada", 3, "rima entre o primeiro e o último verso, com outros no meio: ABBA.", ["interpolada"]),
    ("ritmo", 3, "a música de um poema, feita de sílabas fortes e fracas, pausas e repetições.", ["ritmo"]),
    ("sílaba métrica", 3, "cada sílaba contada num verso, só até à última sílaba tónica.", ["métrica"]),
    ("comparação", 3, "relação entre duas coisas com uma palavra como «como» ou «parece».", ["comparação"]),
    ("personificação", 2, "dar ações ou sentimentos humanos a animais, objetos ou ideias.", ["personificação"]),
    ("metáfora", 3, "comparação sem «como»: diz-se que uma coisa É outra.", ["metáfora"]),
    ("repetição", 3, "voltar a usar uma palavra ou um verso para lhe dar força.", ["repetição"]),
    ("onomatopeia", 3, "palavra que imita um som: tique-taque, miau, zum.", ["onomatopeia"]),
    ("enumeração", 3, "lista de palavras ou expressões seguidas.", ["enumeração"]),
    ("poema a duas vozes", 3, "poema escrito para ser dito por duas pessoas, com versos a solo e em coro.", ["duas vozes"]),
    # ---- Unidade 4
    ("texto principal e texto secundário", 4, "as falas são o texto principal; a lista de personagens, as indicações de cena e as didascálias são o texto secundário.", ["texto principal"]),
    ("texto dramático", 4, "texto escrito para ser representado num palco.", ["texto dramático", "dramático"]),
    ("lista de personagens", 4, "lista, no início da peça, de quem entra na história.", ["lista de personagens"]),
    ("ato", 4, "grande parte de uma peça de teatro, dividida em cenas.", ["ato"]),
    ("cena", 4, "parte de um ato; muda quando entra ou sai uma personagem.", ["cena"]),
    ("fala", 4, "o que cada personagem diz, precedido do seu nome.", ["fala"]),
    ("réplica", 4, "fala que responde a outra fala.", ["réplica"]),
    ("didascália", 4, "indicação para os atores e para o encenador, em itálico e entre parênteses.", ["didascália"]),
    ("monólogo", 4, "fala de uma personagem sozinha, ou para si própria.", ["monólogo"]),
    ("diálogo", 4, "conversa entre duas ou mais personagens.", ["diálogo"]),
    ("cenário", 4, "a decoração do palco que mostra onde se passa a ação.", ["cenário"]),
    ("guarda-roupa", 4, "as roupas e acessórios que os atores vestem.", ["guarda-roupa"]),
    ("adereço", 4, "objeto usado em cena pelos atores.", ["adereço"]),
    ("tipos de frase", 4, "declarativa, interrogativa, exclamativa e imperativa.", ["tipos de frase", "interrogativa"]),
    ("interjeição", 4, "palavra que exprime emoção ou chama alguém: ah!, ui!, olá!", ["interjeiç"]),
]


# term -> regex of the heading (h1) of the page where the unit actually TEACHES it (hand-checked against the
# built PDFs, 25 Sep 2026). Headings, not page numbers, so a unit that shifts its pages stays right.
TAUGHT_AT = {
    "narrador": r"A mala da narrativa", "personagem": r"A mala da narrativa", "espaço": r"A mala da narrativa",
    "tempo": r"A mala da narrativa", "ação": r"A mala da narrativa",
    "estrutura da narrativa": r"Três tentativas",
    "poema": r"A forma do poema", "personificação": r"Flores que falam",
    "texto dramático": r"Raio-X de uma peça", "ato": r"Raio-X de uma peça", "cena": r"Raio-X de uma peça",
    "fala": r"Raio-X de uma peça", "réplica": r"Raio-X de uma peça", "didascália": r"Raio-X de uma peça",
    "monólogo": r"Raio-X de uma peça", "diálogo": r"Raio-X de uma peça", "lista de personagens": r"Raio-X de uma peça",
    "texto principal e texto secundário": r"Raio-X de uma peça",
}
