"""The volume plan: «Português · Year 5 — Manual do aluno» (Prime School Press).

Front matter i–viii (8 pp.) + Units 1–7 (pp. 1–144) + back matter pp. 145–151 + back cover = 160 pp.
Unit accents stay inside Unit 1's palette; the book matter uses the Year 5 house magenta.
Titles/sections given here are PROVISIONAL: build.py replaces them with what harvest.py reads
from each unit's built PDF/HTML.
"""

YEAR5 = "#C32480"      # tools/cover_assets/cover_meta.json -> stripes["5"]
YEAR5_DARK = "#7D1A52"  # small type on white (imprint standard)
YEAR5_TINT = "#F6DDEA"

PAL = {  # Unit 1 palette (src/unit.html :root) + its tints
    "verm": ("#DC4A2E", "#F7D9CE"), "verde": ("#2F6E5C", "#D7E6DC"), "ameixa": ("#7B3F6E", "#EBDCE5"),
    "ultra": ("#2D4BA8", "#DCE1F3"), "ocre": ("#D9922A", "#F6E3BF"), "turq": ("#1C7C89", "#D3E9EA"),
    "tinta": ("#1C2536", "#E3DED2"),
}

UNITS = [
    dict(n=1, folder=".", first=1, last=24, pal="verm", vign="v-gabinete",
         title="O Gabinete das Coisas Verdadeiras", genre="Textos para informar e descrever",
         q="Como se diz o que é verdadeiro — e como se descreve o que se vê?",
         kinds=["artigo de enciclopédia", "verbete", "retrato", "aviso", "exposição oral"]),
    dict(n=2, folder="u2", first=25, last=64, pal="verde", vign="v-galo",
         title="Lugar, Tempo e Memória", genre="Texto narrativo",
         q="Porque contamos histórias — e o que faz uma história ficar na memória?",
         kinds=["lenda", "relato de viagem", "biografia", "conto", "discurso direto"]),
    dict(n=3, folder="u3", first=65, last=80, pal="ameixa", vign="v-poesia",
         title="Linguagem Figurada", genre="Texto poético",
         q="O que consegue um poema dizer que as outras palavras não dizem?",
         kinds=["verso e estrofe", "rima", "comparação", "personificação", "poema a duas vozes"]),
    dict(n=4, folder="u4", first=81, last=96, pal="ultra", vign="v-teatro",
         title="Texto Dramático", genre="Texto dramático",
         q="Como se conta uma história só com falas, gestos e didascálias?",
         kinds=["personagens", "cena", "didascálias", "ensaio", "representação"]),
    dict(n=5, folder="u5", first=97, last=112, pal="ocre", vign="v-comboio",
         title="Revisões Anuais", genre="Revisões do ano",
         q="O que já sei fazer — e o que ainda quero treinar?",
         kinds=["informativo", "narrativo", "poético", "dramático", "gramática"]),
    dict(n=6, folder="u6", first=113, last=128, pal="tinta", vign="v-avaliacao",
         title="Avaliação", genre="Testes e autoavaliação",
         q="Como mostro, com calma, tudo o que aprendi?",
         kinds=["quatro testes", "critérios", "autoavaliação", "balanço do ano"]),
    dict(n=7, folder="u7", first=129, last=144, pal="turq", vign="v-jogos",
         title="Atividades Extra", genre="Para ir mais longe",
         q="Que mais posso fazer com as palavras — só pelo gosto de brincar com elas?",
         kinds=["jogos de palavras", "escrita criativa", "oralidade", "clube de leitura"]),
]
for u in UNITS:
    u["c"], u["t"] = PAL[u["pal"]]
    u["pages"] = u["last"] - u["first"] + 1

FRONT_PAGES = 8
BACK_PAGES = 8
TOTAL = FRONT_PAGES + sum(u["pages"] for u in UNITS) + BACK_PAGES  # 160

BACK = [  # back matter, pp. 145–151 (+ unnumbered back cover)
    (145, "Glossário"), (146, "Glossário (continuação)"), (147, "Recursos digitais"),
    (148, "Referências e créditos"), (149, "Planificação anual"), (150, "O meu 5.º ano — antes de fechar o livro"),
    (151, "Colofão"),
]
FRONT = [  # (folio, title) — i and ii are unnumbered
    ("i", "Capa"), ("ii", "Ficha técnica"), ("iii", "Como usar este livro"), ("iv", "Mapa do ano"),
    ("v", "Índice"), ("vi", "Índice (continuação)"), ("vii", "O meu ano de leitura"), ("viii", "Quem sou eu como leitor"),
]
assert TOTAL == 160, TOTAL
