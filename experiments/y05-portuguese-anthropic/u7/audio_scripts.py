# Audio for the QR codes of Unit 7 — «Atividades Extra».
# All texts are ORIGINAL (written for this book). Each track: list of (voice, pitch, rate, text, pause_after_s).
# Run with the experiment venv:  python audio_scripts.py  -> writes ./audio/u7-*.mp3
import asyncio, os, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"

TRAVA = [
    "A osga Mourinha mói milho miúdo no moinho da minha madrinha.",
    "O Pedro pinta pratos pretos e a Paula pinta potes pardos: pratos pretos, potes pardos, que pintura tão pesada!",
    "Sossega o sapo sentado, salta o sapo assustado; se o sapo sossegar, o sapo não vai saltar.",
    "Chove chuva na chaminé do chalé do Chico, e o Chico, chateado, chama pelo chapéu.",
    "Um galo gago gargarejava na garagem do Gaspar; gargarejava tão grave que o Gaspar gargalhava.",
    "Trinta trutas trémulas treparam à trepadeira; a trepadeira tremeu e as trutas trapalhonas tombaram no tanque.",
]

ADIVINHAS = [
    ("Tenho folhas e não sou árvore, tenho lombada e não sou animal; quem me abre viaja longe sem sair do seu quintal.", "o livro"),
    ("Subo paredes sem escada, ando no teto sem cair; se me agarram pela cauda, deixo-a lá e ponho-me a fugir.", "a osga"),
    ("Tenho dentes e não mordo, penteio sem ter mão; passo pelo teu cabelo e desfaço a confusão.", "o pente"),
    ("Quanto mais eu cresço, menos tu consegues ver; chego sempre com a noite e fujo ao amanhecer.", "o escuro"),
    ("Tenho um só olho e não vejo, passo a vida a costurar; levo atrás de mim a linha onde quer que vá parar.", "a agulha"),
    ("Tenho cidades sem casas e rios sem peixe a nadar, tenho montanhas sem pedras e dobro-me para viajar.", "o mapa"),
]

ORD = ["Primeiro", "Segundo", "Terceiro", "Quarto", "Quinto", "Sexto"]
ORDA = ["Primeira", "Segunda", "Terceira", "Quarta", "Quinta", "Sexta"]

TRACKS = {
    "u7-01-trava-linguas": [(R, "+0Hz", "-4%", "Trava-línguas da Mourinha. Primeiro, ouve cada um devagarinho. Depois, ouve-o depressa. Por fim, carrega na pausa e tenta tu: três vezes seguidas, sem tropeçar!", 1.2)]
    + sum([[(R, "+0Hz", "-4%", f"{ORD[i]} trava-línguas.", 0.6),
            (D, "+0Hz", "-18%", t, 1.0),
            (D, "+0Hz", "+18%", t, 2.4)] for i, t in enumerate(TRAVA)], [])
    + [(R, "+0Hz", "-4%", "Qual foi o mais difícil? Agora inventa um trava-línguas teu, com o som que preferires.", 0.5)],
    "u7-02-adivinhas": [(R, "+0Hz", "-4%", "Adivinha, adivinha! Vais ouvir seis adivinhas. Depois de cada uma, tens alguns segundos para pensar. Não espreites as respostas ao fundo da página!", 1.2)]
    + sum([[(R, "+0Hz", "-4%", f"{ORDA[i]} adivinha.", 0.6),
            (D, "+0Hz", "-10%", q, 5.5),
            (R, "+0Hz", "-4%", f"A resposta é: {a}!", 1.4)] for i, (q, a) in enumerate(ADIVINHAS)], [])
    + [(R, "+0Hz", "-4%", "Quantas acertaste? Agora é a tua vez: inventa uma adivinha e desafia a tua família.", 0.5)],
    "u7-03-comeco-de-historia": [
        (R, "+0Hz", "-4%", "Começo de história. Ouve com atenção. No fim, a história é tua.", 1.2),
        (D, "+0Hz", "-8%", "Na pequena vila do Cabo das Gaivotas, toda a gente sabia três coisas: que o pão da Dona Aurora era o melhor da costa, que o farol nunca se apagava e que ninguém, mas mesmo ninguém, podia entrar lá dentro.", 0.8),
        (D, "+0Hz", "-8%", "Até à manhã de nevoeiro em que o velho faroleiro, o senhor Baltazar, apareceu na praça, de boné na mão e bigode a tremer.", 0.6),
        (D, "-6Hz", "-12%", "Perdi a chave do farol! — gritou ele. — E esta noite vem aí a maior tempestade do ano!", 0.9),
        (D, "+0Hz", "-8%", "Foi nesse preciso momento que a Leonor sentiu qualquer coisa a mexer-se no bolso do casaco. Meteu lá a mão, devagarinho, e tirou uma chave antiga, de latão, que nunca tinha visto na vida. Presa à chave, havia uma etiqueta de papel, já amarelada, com uma única palavra escrita.", 1.0),
        (D, "+0Hz", "-12%", "A Leonor leu-a em voz baixa… e arregalou os olhos.", 1.4),
        (R, "+0Hz", "-4%", "Que palavra estaria escrita na etiqueta? Como foi a chave parar ao bolso da Leonor? Para a gravação e continua tu a história. Podes lançar os dados de histórias para decidir quem aparece a seguir.", 0.5),
    ],
}


async def seg(voice, pitch, rate, text, path):
    await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)


async def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    for name, parts in TRACKS.items():
        if only and name not in only:
            continue
        with tempfile.TemporaryDirectory() as td:
            files = []
            for i, (v, p, r, t, pause) in enumerate(parts):
                f = os.path.join(td, f"{i:02d}.mp3")
                for attempt in range(4):
                    try:
                        await seg(v, p, r, t, f)
                        break
                    except Exception as e:  # network hiccups
                        print("retry", name, i, e)
                        await asyncio.sleep(2 + attempt * 3)
                else:
                    raise SystemExit(f"tts failed: {name} {i}")
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


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:] or None))
