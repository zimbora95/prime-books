# Audio for the QR codes of Unit 6 — «Avaliação» (compreensão do oral, parte D de cada teste).
# All texts are ORIGINAL (written for this unit). Each track: list of (voice, pitch, rate, text, pause_after_s).
# Run with the experiment venv:  python audio_scripts.py [name ...]  -> writes ./audio/u6-*.mp3
import asyncio, os, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"

INTRO = "Vais ouvir o texto duas vezes. Na primeira vez, ouve com atenção. Na segunda, responde às perguntas."

TRACKS = {
    # Teste 1 · D — reportagem de rádio (texto informativo; factos e opiniões)
    "u6-01-radio-escola": [
        (R, "+0Hz", "-6%", "Teste um. Compreensão do oral. " + INTRO, 1.6),
        (R, "+0Hz", "-4%", "Rádio Escola. Boletim da manhã.", 0.8),
        (R, "+0Hz", "-4%", "Bom dia a todos! Eu sou a Carolina Mendes e estou no recreio da nossa escola, onde hoje, sexta-feira, vinte e um de março, Dia da Árvore, aconteceu uma coisa diferente.", 0.6),
        (R, "+0Hz", "-4%", "Esta manhã, os alunos do Year 5 plantaram vinte sobreiros junto ao muro do campo de jogos. As pequenas árvores foram oferecidas pelo viveiro municipal e medem, cada uma, cerca de quarenta centímetros.", 0.6),
        (R, "+0Hz", "-4%", "Cada turma adotou quatro árvores e deu-lhes um nome. No verão, os alunos vão regá-las duas vezes por semana.", 0.8),
        (R, "+0Hz", "-4%", "Tiago, o que achaste desta manhã?", 0.5),
        (D, "+22Hz", "+2%", "Acho que foi a melhor manhã do ano! E o nosso sobreiro, o Bolota, é o mais bonito de todos.", 0.8),
        (R, "+0Hz", "-4%", "E a professora Ana Lopes, que organizou a plantação, explicou-nos porquê o sobreiro.", 0.5),
        (R, "-8Hz", "-6%", "O sobreiro é a Árvore Nacional de Portugal e aguenta bem o calor e a secura. Estas árvores só vão dar a primeira cortiça daqui a cerca de vinte e cinco anos. Na minha opinião, é o melhor presente que podíamos deixar a quem vier depois de nós.", 0.8),
        (R, "+0Hz", "-4%", "Para a Rádio Escola, no recreio, Carolina Mendes.", 1.4),
        (R, "+0Hz", "-6%", "Vais ouvir outra vez.", 1.0),
    ],
    # Teste 2 · D — conto (texto narrativo)
    "u6-02-bicicleta-amarela": [
        (D, "+0Hz", "-6%", "Teste dois. Compreensão do oral. " + INTRO, 1.6),
        (D, "+0Hz", "-6%", "A bicicleta amarela.", 0.9),
        (D, "+0Hz", "-6%", "Naquele verão, o Martim foi passar as férias a casa da tia Natércia, em Tavira.", 0.5),
        (D, "+0Hz", "-6%", "Um dia, na garagem, debaixo de uma lona, encontrou uma bicicleta amarela, velha e cheia de ferrugem.", 0.4),
        (R, "-4Hz", "-4%", "Era da tua mãe, quando tinha a tua idade.", 0.4),
        (D, "+0Hz", "-6%", "disse a tia.", 0.6),
        (D, "+0Hz", "-6%", "O Martim ainda não sabia andar de bicicleta sem rodinhas. Por isso, todas as tardes, a tia segurava no selim e corria atrás dele pela rua da praia.", 0.5),
        (D, "+0Hz", "-6%", "Ao princípio, o Martim caía muitas vezes. Depois, começou a dar três pedaladas, cinco, dez...", 0.5),
        (D, "+0Hz", "-6%", "Uma tarde, no fim de agosto, gritou:", 0.3),
        (D, "+26Hz", "+4%", "Tia, não me largues!", 0.5),
        (D, "+0Hz", "-6%", "Mas a tia já o tinha largado há muito tempo: estava lá atrás, parada no meio da rua, a bater palmas.", 0.6),
        (D, "+0Hz", "-6%", "Quando voltou para Lisboa, o Martim levou a bicicleta amarela no carro. Agora, é ele quem a limpa, lhe enche os pneus e lhe dá voltas no bairro.", 1.4),
        (D, "+0Hz", "-6%", "Vais ouvir outra vez.", 1.0),
    ],
    # Teste 3 · D — poema dito em voz alta (texto poético)
    "u6-03-chuva-miudinha": [
        (R, "+0Hz", "-6%", "Teste três. Compreensão do oral. " + INTRO, 1.6),
        (R, "+0Hz", "-12%", "A chuva miudinha.", 1.0),
        (R, "+0Hz", "-14%", "Plic, ploc, na vidraça, a chuva chegou de mansinho; bate à porta como quem anda perdida no caminho.", 1.1),
        (R, "+0Hz", "-14%", "Lava as ruas, lava os carros, lava as árvores do jardim, e dá de beber aos canteiros de rosas e de alecrim.", 1.1),
        (R, "+0Hz", "-14%", "Depois, cansada, adormece numa nuvem de algodão, e o arco-íris é a ponte que o sol estende até ao chão.", 1.6),
        (R, "+0Hz", "-6%", "Vais ouvir outra vez.", 1.0),
    ],
    # Teste 4 · D — cena dramática a várias vozes (texto dramático)
    "u6-04-coroa-do-rei": [
        (D, "+0Hz", "-6%", "Teste quatro. Compreensão do oral. " + INTRO, 1.6),
        (D, "+0Hz", "-6%", "A coroa do rei. Cena única. O palco da escola, na véspera da festa de Natal.", 0.9),
        (R, "-6Hz", "-2%", "Atenção, meninos! É o último ensaio. Luzes, por favor!", 0.6),
        (R, "+28Hz", "+6%", "Professora Helena! A coroa do rei desapareceu!", 0.5),
        (R, "-6Hz", "-2%", "Oh, não! Outra vez? Quem estava com ela?", 0.5),
        (D, "+24Hz", "+2%", "Fui eu... quer dizer, estava comigo até ao lanche. Depois, pousei-a numa cadeira...", 0.6),
        (R, "+28Hz", "+6%", "Ali! Olhem! Está na cabeça do boneco de neve!", 0.6),
        (D, "+24Hz", "+2%", "Ufa! Que alívio!", 0.6),
        (R, "-6Hz", "-2%", "Muito bem. Diogo, põe a coroa. Sofia, vai para o teu lugar. E agora, silêncio: vamos começar!", 0.8),
        (D, "+0Hz", "-6%", "E o ensaio começou, com o rei mais aliviado do mundo.", 1.4),
        (D, "+0Hz", "-6%", "Vais ouvir outra vez.", 1.0),
    ],
}


async def seg(voice, pitch, rate, text, path):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)
            return
        except Exception:
            if attempt == 3:
                raise
            await asyncio.sleep(2 + attempt * 3)


def silence(td, i, pause):
    s = os.path.join(td, f"{i:02d}s.mp3")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(pause), "-q:a", "9", s], check=True)
    return s


async def render(name, parts, td):
    files = []
    for i, (v, p, r, t, pause) in enumerate(parts):
        f = os.path.join(td, f"{i:02d}.mp3")
        await seg(v, p, r, t, f)
        files += [f, silence(td, i, pause)]
    return files


async def main(only):
    os.makedirs(OUT, exist_ok=True)
    for name, parts in TRACKS.items():
        if only and name not in only:
            continue
        with tempfile.TemporaryDirectory() as td:
            intro, body = parts[:1], parts[1:-1]
            outro = parts[-1:]
            # text is played twice: intro · body · "vais ouvir outra vez" · body
            files = await render(name, intro + body + outro, td)
            n_intro = 2
            body_files = files[n_intro:n_intro + 2 * len(body)]
            files = files + body_files
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{f}'\n" for f in files)
            out = os.path.join(OUT, name + ".mp3")
            subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                            "-ar", "24000", "-ac", "1", "-b:a", "64k", out], check=True)
            print(name, os.path.getsize(out))


asyncio.run(main(set(sys.argv[1:])))
