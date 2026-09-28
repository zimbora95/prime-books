# Audio for the QR codes of Unit 5 — "O Comboio das Quatro Estações" (Revisões Anuais).
# Only ORIGINAL texts written for this unit are recorded. Each track is a list of
# (voice, pitch, rate, text, pause_after_seconds).
# Run:  /root/.hermes/cache/scratch/exp-venv/bin/python audio_scripts.py [track ...]  -> writes ./audio/u5-*.mp3
import asyncio, os, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"
TOMAS = (D, "+28Hz", "-4%")
INES = (R, "+22Hz", "-2%")
AVO = (D, "-12Hz", "-10%")
ALBANO = (D, "-4Hz", "-6%")
MARIA = (R, "-4Hz", "-4%")
NARR = (R, "+0Hz", "-8%")


def say(v, text, pause=0.6):
    return (v[0], v[1], v[2], text, pause)


RELATO = [
    say(TOMAS, "Diário de viagem. Sábado, doze de abril.", 1.0),
    say(TOMAS, "Olá! Sou o Tomás e hoje fiz a minha primeira viagem na Linha do Douro."),
    say(TOMAS, "Primeiro, apanhámos o comboio na estação de São Bento, no Porto, às oito da manhã. A estação estava cheia de gente, e as paredes estavam cobertas de azulejos azuis e brancos."),
    say(TOMAS, "Depois de uma hora de viagem, o comboio encontrou o rio Douro e, a partir daí, seguiu sempre ao lado dele. Quando parámos na Régua, começaram as vinhas: milhares de socalcos, como degraus gigantes, a descer até à água. Enquanto o comboio atravessava os túneis, a Inês tapava os ouvidos e eu contava até dez."),
    say(TOMAS, "Mais tarde, chegámos ao Pinhão. A estação é pequena, mas tem vinte e quatro painéis de azulejos, colocados em mil novecentos e trinta e sete. Mostram as vindimas, as pessoas a carregar cestos de uvas e os barcos rabelos, que levavam o vinho do Porto pelo rio abaixo. Para mim, é a estação mais bonita de Portugal!"),
    say(TOMAS, "Por fim, antes de regressarmos, demos um passeio num barco rabelo. A água estava verde e calma, e o barqueiro contou-nos histórias do rio."),
    say(TOMAS, "Foi o melhor sábado do ano. Na próxima viagem, quero ir até ao fim da linha, no Pocinho.", 0.5),
]

DIT = (R, "+0Hz", "-22%")
DITADO_PARTS = [
    "No fim da viagem, vírgula, o comboio parou devagar na estação do Pinhão. Ponto final.",
    "Nas paredes, vírgula, os azulejos azuis contavam a história das vindimas. Ponto final.",
    "A Inês desceu a correr e gritou, dois pontos. Parágrafo.",
    "Travessão. Avô, vírgula, olha os barcos no rio! Ponto de exclamação. Parágrafo.",
    "O avô sorriu, vírgula, pegou na mala e respondeu, dois pontos. Parágrafo.",
    "Travessão. Parece que também eles vão de viagem. Ponto final.",
]
DITADO = [say(NARR, "Ditado. Vou ler cada frase duas vezes. Escreve com atenção e não te esqueças das maiúsculas e dos acentos.", 2.0)]
for p in DITADO_PARTS:
    DITADO += [(DIT[0], DIT[1], DIT[2], p, 5.0), (DIT[0], DIT[1], DIT[2], p, 7.0)]
DITADO += [say(NARR, "Agora, vou ler o texto todo, sem parar. Revê o que escreveste.", 1.5),
           say(NARR, "No fim da viagem, o comboio parou devagar na estação do Pinhão. Nas paredes, os azulejos azuis contavam a história das vindimas. A Inês desceu a correr e gritou: Avô, olha os barcos no rio! O avô sorriu, pegou na mala e respondeu: Parece que também eles vão de viagem.", 0.5)]

CONTO = [
    say(NARR, "A mala azul da carruagem três.", 1.0),
    say(NARR, "Naquela manhã de abril, o comboio da Linha do Douro ia quase vazio. A Inês viajava com o avô Artur e com o Tomás, o seu melhor amigo, para visitar a tia, que morava no Pinhão."),
    say(NARR, "Enquanto o avô lia o jornal, a Inês reparou numa coisa estranha: na prateleira das bagagens, estava uma pequena mala azul, de cantos dourados. Ninguém se sentava por baixo dela."),
    say(INES, "De quem será aquela mala?", 0.3), say(NARR, "perguntou ela, em voz baixa.", 0.4),
    say(TOMAS, "De um espião!", 0.3), say(NARR, "sussurrou o Tomás, de olhos arregalados.", 0.4),
    say(NARR, "O avô baixou o jornal e sorriu:", 0.3),
    say(AVO, "Ou de alguém com muita pressa e pouca memória."),
    say(NARR, "Primeiro, os dois amigos percorreram a carruagem e perguntaram a todos os passageiros se tinham perdido uma mala. Ninguém sabia de nada. Depois, procuraram uma etiqueta com um nome, mas só encontraram uma pena branca e comprida, presa na pega."),
    say(INES, "É uma pena de cegonha!", 0.3), say(NARR, "exclamou a Inês, que sabia muito de aves."),
    say(NARR, "Então, lembraram-se do revisor. O senhor Albano ouviu a história com atenção, coçou o bigode e abriu a mala com cuidado. Lá dentro, havia um mapa dobrado e um caderno cheio de desenhos de cegonhas."),
    say(ALBANO, "Já sei!", 0.3), say(NARR, "disse ele.", 0.3),
    say(ALBANO, "Na Régua, uma senhora de chapéu de palha mudou de lugar, porque o sol lhe batia nos olhos. Passou a viagem a desenhar. Deve estar na carruagem cinco!"),
    say(NARR, "Os três correram pelo corredor. Na carruagem cinco, uma senhora remexia, aflita, a sua bolsa."),
    say(NARR, "Quando viu a mala azul, a Maria do Céu, era esse o seu nome, deu um grito de alegria. Era ilustradora e andava a desenhar as cegonhas do Alentejo para um livro. Como agradecimento, desenhou a Inês e o Tomás no caderno, ao lado das cegonhas."),
    say(NARR, "Desde esse dia, sempre que viaja de comboio, a Inês espreita as prateleiras das bagagens. Nunca se sabe que mistério pode estar à espera.", 0.5),
]

POEMA = [
    say(NARR, "Comboio da noite.", 1.2),
    (R, "+0Hz", "-16%", "Pouca-terra, pouca-terra, e o comboio sobe a serra; leva um colar de janelas acesas como as estrelas.", 1.3),
    (R, "+0Hz", "-16%", "O comboio já suspira, a ponte treme de frio, a lua abre um olho e mira, e dorme, calado, o rio.", 1.3),
    (R, "+0Hz", "-16%", "Passam vinhas, passam montes, passam casas, passam gentes, e as estrelas são sementes no campo dos horizontes.", 0.5),
]

CENA = [
    say(NARR, "A mala azul. Cena dois: na carruagem cinco.", 1.2),
    say(MARIA, "Ai, que cabeça a minha! Os desenhos de um ano inteiro... perdidos! Como é que vou explicar isto à editora?", 0.9),
    say(MARIA, "Calma, Maria. Respira. Talvez alguém a tenha encontrado...", 1.0),
    say(INES, "Desculpe! A senhora perdeu uma mala azul?"),
    say(MARIA, "A minha mala! Onde é que a encontraram?"),
    say(TOMAS, "Na carruagem três, na prateleira. Pensámos que era de um espião!"),
    say(MARIA, "De um espião? Não, não... sou só uma ilustradora distraída."),
    say(AVO, "Ufa! Estes dois correm mais do que o comboio."),
    say(INES, "Foi a pena de cegonha que nos deu a pista!"),
    say(MARIA, "Obrigada! Obrigadíssima! Sentem-se aqui, os dois. Vou desenhar-vos ao lado das cegonhas."),
    say(TOMAS, "A sério? Que fixe!", 0.9),
    say(ALBANO, "Então, o mistério ficou resolvido?", 0.4),
    (R, "+10Hz", "+0%", "Ficou!", 0.1),
]

TRACKS = {
    "u5-01-relato-linha-do-douro": RELATO,
    "u5-02-ditado": DITADO,
    "u5-03-conto-a-mala-azul": CONTO,
    "u5-04-poema-comboio-da-noite": POEMA,
    "u5-05-cena-carruagem-5": CENA,
}


async def seg(voice, pitch, rate, text, path):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)
            return
        except Exception as e:  # network hiccups
            if attempt == 3:
                raise
            await asyncio.sleep(2 + attempt * 2)


async def main(only):
    os.makedirs(OUT, exist_ok=True)
    for name, parts in TRACKS.items():
        if only and name not in only:
            continue
        with tempfile.TemporaryDirectory() as td:
            files = []
            for i, (v, p, r, t, pause) in enumerate(parts):
                f = os.path.join(td, f"{i:02d}.mp3")
                await seg(v, p, r, t, f)
                s = os.path.join(td, f"{i:02d}s.mp3")
                subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                                "anullsrc=r=24000:cl=mono", "-t", str(pause), "-q:a", "9", s], check=True)
                files += [f, s]
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{f}'\n" for f in files)
            out = os.path.join(OUT, name + ".mp3")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                            "-ar", "24000", "-ac", "1", "-b:a", "64k", out], check=True)
            print(name, os.path.getsize(out))


asyncio.run(main(set(sys.argv[1:])))
