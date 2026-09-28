# Audio for the QR codes of Unit 3 — "O Coreto das Palavras".
# ONLY original texts written for this book are recorded (never the José Jorge Letria extract).
# Each track is a list of parts. A part is (voice, pitch, rate, text, pause_after_seconds);
# voice "CORO" = both voices at once (the middle column of the two-voice poem), mixed with ffmpeg amix.
# Run with the experiment venv:  python audio_scripts.py [track-name ...]  -> writes ./audio/u3-*.mp3
import asyncio, os, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"
OSGA = (R, "+14Hz", "-14%")      # voice 1: small, quiet, night
POMBO = (D, "-4Hz", "+0%")       # voice 2: round, lively, day


def poem(voice, pitch, rate, title, stanzas, gap=1.1):
    parts = [(voice, pitch, rate, title, 1.0)]
    for i, st in enumerate(stanzas):
        for j, v in enumerate(st):
            last = j == len(st) - 1
            parts.append((voice, pitch, rate, v, gap if last else 0.35))
    return parts


CORETO = [["No meio do jardim velho", "dorme um coreto sozinho,", "com um chapéu de ferro verde", "e, no chapéu, um passarinho."],
          ["Ninguém lá sobe a cantar,", "só o vento, devagar."],
          ["Mas numa noite de lua", "vieram três da minha rua,", "cada um com um papel na mão."],
          ["Leram versos para o céu,", "leram alto, com cuidado —", "e o coreto, que dormia,", "acordou todo encantado."]]
VENTO = [["O vento é um rapazinho", "que acorda a rua a correr;", "assobia no caminho", "e ninguém o pode ver."],
         ["Põe a roupa a bailar", "como um bando de bailarinas,", "e depois vai espreitar", "pelas frestas das cortinas."],
         ["À noite, muito cansado,", "deita-se em cima do telhado", "e dorme, enroladinho,", "tal e qual um gatinho."]]
CHUVA = [["Plic, ploc, plic, ploc,", "a chuva chegou à cidade!", "Plic, ploc, plic, ploc,", "lava os telhados à vontade."],
         ["Molha os carros, molha os cães,", "molha os bancos do jardim,", "molha as tias e as mães", "e molha — chape! — até a mim!"],
         ["Guarda-chuvas, capas, botas,", "poças grandes e pequenas,", "nuvens carregadas de gotas", "e pombos a sacudir as penas."],
         ["Catrapum! Ronca o trovão.", "Plic… ploc… a chuva abranda.", "Fecham-se os guarda-chuvas", "e o sol vem à varanda."]]
NOITE = [["Quando a cidade se deita", "e as janelas apagam a luz,", "a Mourinha espreita", "e o seu olho de ouro reluz."],
         ["Tique-taque, diz o relógio.", "Zzz, ressona o vizinho.", "E ela sobe, sem ruído,", "devagar, devagarinho."],
         ["Mosquitos, moscas e traças", "dançam à volta do candeeiro;", "a Mourinha, sem pressa,", "escolhe o jantar primeiro."],
         ["Depois, quieta como uma pedra,", "fica a ver a lua passar,", "e a lua, lanterna do céu,", "fica com ela a conversar."]]

SILABAS = [("a", "Leram alto, com cuidado.", "Le, ram, al, to, com, cui, da.", "Sete sílabas. Paramos em «da», a sílaba forte de cuidado."),
           ("b", "E o coreto, que dormia.", "E o, co, re, to, que, dor, mi.", "Sete sílabas. «E» e «o» juntam-se numa só; e paramos em «mi», de dormia."),
           ("c", "Molha os carros, molha os cães.", "Mo, lha os, car, ros, mo, lha os, cães.", "Sete sílabas. «Lha» e «os» juntam-se, duas vezes."),
           ("d", "O mar escreve na areia.", "O, mar, es, cre, ve, na a, rei.", "Sete sílabas. «Na» e «a» juntam-se, e paramos em «rei», de areia.")]


def silabas():
    p = [(R, "+0Hz", "-6%", "Contar sílabas métricas. Vais ouvir quatro versos. Primeiro, o verso inteiro; depois, devagar, sílaba a sílaba, como os poetas contam: de ouvido, até à última sílaba forte.", 1.2)]
    for letra, verso, sil, resp in SILABAS:
        p += [(R, "+0Hz", "-6%", f"Verso {letra}.", 0.5), (D, "+0Hz", "-8%", verso, 0.9),
              (D, "+0Hz", "-45%", sil, 1.0), (R, "+0Hz", "-6%", resp, 1.6)]
    p.append((R, "+0Hz", "-6%", "Os quatro versos têm sete sílabas: são redondilhas maiores, o verso preferido das quadras populares portuguesas.", 0.5))
    return p


def duas_vozes():
    O, P, C = OSGA, POMBO, "CORO"
    rows = [(O, "Eu sou da noite."), (P, "Eu sou do dia."), (C, "Moramos os dois no mesmo telhado."),
            (O, "Acordo com a lua acesa."), (P, "Acordo com o sol nas penas."),
            (O, "Sou leve como uma folha seca."), (P, "Sou redondo como um pão."),
            (O, "Subo paredes sem cair."), (P, "Voo sobre a praça inteira."),
            (O, "Ao jantar: mosquitos."), (P, "Ao almoço: migalhas."), (C, "E ninguém nos convida para a mesa!"),
            (O, "Tu arrulhas: ru-ru, ru-ru."), (P, "E tu passas sem dar um pio."),
            (O, "Se dormes, guardo o telhado."), (P, "Se dormes, guardo o telhado."),
            (C, "De manhã, cruzamo-nos na chaminé."), (O, "Boa noite!"), (P, "Bom dia!"),
            (C, "E o telhado nunca fica sozinho.")]
    parts = [(R, "+0Hz", "-4%", "Noite e Dia. Poema em duas vozes: a osga e o pombo.", 1.2)]
    breaks = {2, 6, 11, 16}
    for i, (v, t) in enumerate(rows):
        pause = 1.0 if i in breaks else 0.5
        parts.append(("CORO", "", "", t, pause) if v == "CORO" else (v[0], v[1], v[2], t, pause))
    return parts


TRACKS = {
    "u3-01-o-coreto-adormecido": poem(D, "+0Hz", "-10%", "O Coreto Adormecido.", CORETO),
    "u3-02-tres-rimas": [
        (R, "+0Hz", "-6%", "Três quadras, três rimas.", 0.9),
        (R, "+0Hz", "-6%", "Rima emparelhada.", 0.6),
        *poem(D, "+0Hz", "-10%", "A osga.", [["A osga sobe à parede,", "não tem medo nem tem sede;", "espera a traça que passa", "e apanha-a com muita graça."]])[1:],
        (R, "+0Hz", "-6%", "Rima cruzada.", 0.6),
        *poem(D, "+0Hz", "-10%", "A lua.", [["A lua é um queijo branco", "pendurado no céu escuro;", "o gato salta do banco", "e mia-lhe de cima do muro."]])[1:],
        (R, "+0Hz", "-6%", "Rima interpolada.", 0.6),
        *poem(D, "+0Hz", "-10%", "O mar.", [["O mar escreve na areia", "uma carta com espuma;", "não tem letra nenhuma,", "mas lê-a a lua cheia."]])[1:],
    ],
    "u3-03-contar-silabas": silabas(),
    "u3-04-o-vento-e-a-chuva": poem(R, "+0Hz", "-8%", "O Vento Brincalhão.", VENTO) + [(R, "+0Hz", "-8%", " ", 0.8)]
                              + poem(D, "+0Hz", "-8%", "Chuva na Cidade.", CHUVA),
    "u3-05-a-noite-da-mourinha": poem(R, "+6Hz", "-12%", "A Noite da Mourinha.", NOITE, gap=1.3),
    "u3-06-noite-e-dia-duas-vozes": duas_vozes(),
}


async def seg(voice, pitch, rate, text, path):
    await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)


def silence(path, secs):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(secs), "-q:a", "9", path], check=True)


async def main(names):
    os.makedirs(OUT, exist_ok=True)
    for name in names:
        parts = TRACKS[name]
        with tempfile.TemporaryDirectory() as td:
            files = []
            for i, (v, p, r, t, pause) in enumerate(parts):
                f = os.path.join(td, f"{i:02d}.mp3")
                if not t.strip():
                    silence(f, 0.1)
                elif v == "CORO":
                    a, b = os.path.join(td, f"{i:02d}a.mp3"), os.path.join(td, f"{i:02d}b.mp3")
                    await seg(OSGA[0], OSGA[1], "-8%", t, a)
                    await seg(POMBO[0], POMBO[1], "-8%", t, b)
                    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", a, "-i", b, "-filter_complex",
                                    "[0:a]volume=1.0[x];[1:a]volume=1.0[y];[x][y]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95",
                                    "-ar", "24000", "-ac", "1", f], check=True)
                else:
                    await seg(v, p, r, t, f)
                s = os.path.join(td, f"{i:02d}s.mp3")
                silence(s, pause)
                files += [f, s]
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{f}'\n" for f in files)
            out = os.path.join(OUT, name + ".mp3")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                            "-ar", "24000", "-ac", "1", "-b:a", "64k", out], check=True)
            print(name, os.path.getsize(out))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or list(TRACKS)))
