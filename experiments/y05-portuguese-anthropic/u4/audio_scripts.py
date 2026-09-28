# Audio for the QR codes of Unit 4 — "Texto Dramático".
# Each track is a list of segments: (who, text, pause_after_seconds) or ("SFX", name, pause).
# `who` maps to a (voice, pitch, rate) — one distinct voice per character; a list of voices = chorus.
# A narrator reads the scene headings and the main stage directions; short tone/gesture
# didascálias are acted, not read (as the book teaches on p. 86).
# Run with the experiment venv:  python audio_scripts.py [track ...]  -> writes ./audio/u4-*.mp3
import asyncio, os, subprocess, sys, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"

V = {
    "NARR": (D, "-4Hz", "-8%"),     # narrator: calm, neutral
    "GUI": (R, "-16Hz", "-12%"),    # D. Guilhermina: older, slower
    "ANS": (D, "-20Hz", "-6%"),     # Sr. Anselmo: deep
    "BEA": (R, "+24Hz", "-2%"),     # Beatriz: child, measured
    "LUC": (D, "+32Hz", "+10%"),    # Lucas: child, always in a hurry
    "ROSA": (R, "+2Hz", "+4%"),     # D. Rosa: brisk, warm
    "INTRO": (R, "+0Hz", "-5%"),
    "FRASE": (D, "+0Hz", "-8%"),
}
V["TODOS"] = [V["GUI"], V["BEA"], V["LUC"], V["ANS"]]

TRACKS = {
    "u4-01-o-aviso": [
        ("NARR", "Duas Cenas: O Aviso. Uma peça em duas cenas.", 1.0),
        ("NARR", "Cena um. Sexta-feira, ao fim da tarde. O átrio do Gabinete das Coisas Verdadeiras. Ao lado da porta da Sala Grande, um placard com um aviso. Em cima da parte de baixo do aviso, dorme a Mourinha. Entra o Lucas, a correr.", 0.8),
        ("LUC", "Sábado não há ensaio.", 0.7),
        ("LUC", "Não há ensaio?! Mas a estreia é já daqui a uma semana!", 0.4),
        ("BEA", "Lucas, porque estás a gritar? Ouve-se lá da rua!", 0.4),
        ("LUC", "Lê tu mesma! Acabou-se! Cancelaram tudo!", 0.4),
        ("BEA", "Espera… O aviso continua. Há mais letras aqui em baixo, mas estão escondidas debaixo de…", 0.4),
        ("BEA", "Ui! De uma osga!", 0.4),
        ("LUC", "Uma osga?! Eu não chego perto disso nem por nada!", 0.4),
        ("BEA", "As osgas não fazem mal a ninguém. Aprendemos isso na visita ao Gabinete, lembras-te? Basta esperar que ela saia.", 0.4),
        ("LUC", "Esperar? Não há tempo para esperar! Tenho de avisar o grupo todo.", 0.6),
        ("NARR", "Entra o senhor Anselmo, com um escadote ao ombro e uma lâmpada na mão.", 0.5),
        ("ANS", "Boa tarde, meninos! Que caras são essas? Parece que viram um fantasma!", 0.4),
        ("LUC", "Pior, senhor Anselmo! Sábado não há ensaio. Está ali escrito!", 0.4),
        ("ANS", "Não há ensaio… Ainda bem que me avisas. Amanhã cedo, arrumo as cadeiras todas no armazém.", 0.4),
        ("BEA", "Espere, senhor Anselmo! Ainda não lemos o aviso até ao fim!", 0.4),
        ("ANS", "Não há ensaio, não há cadeiras. É simples!", 0.4),
        ("LUC", "Vês? O senhor Anselmo concorda comigo. Vou para casa.", 0.6),
        ("BEA", "E tu, osga? Sabes o que está escrito aí debaixo, não sabes?", 0.9),
        ("BEA", "Pois… Amanhã venho cá mais cedo.", 0.6),
        ("NARR", "O candeeiro apaga-se. Escuro.", 1.6),
        ("NARR", "Cena dois. Sábado, nove e meia da manhã. A Sala Grande, vazia: não há uma única cadeira. A dona Guilhermina está sozinha, junto a um cabide cheio de fatos.", 0.8),
        ("GUI", "Nove e meia e nem um ator! Os pais chegam às dez… e as cadeiras? Onde estão as cadeiras?", 0.6),
        ("GUI", "Tive de mudar a estreia para hoje, porque o palco vai ser pintado na próxima semana. E escrevi o aviso com tanto cuidado! Sábado não há ensaio: há estreia! Com ponto de exclamação e tudo. Será que ninguém o leu até ao fim?", 0.6),
        ("NARR", "Entra a Beatriz, a correr, a puxar o Lucas por um braço. Traz o aviso na mão.", 0.5),
        ("BEA", "Chegámos, dona Guilhermina! Voltei ao átrio às oito. A osga já se tinha ido embora e o aviso estava inteirinho.", 0.5),
        ("BEA", "Sábado não há ensaio: há estreia! Às dez horas, com público. Tragam os fatos.", 0.5),
        ("LUC", "Eu só li a primeira linha…", 0.4),
        ("GUI", "Ai, Lucas, Lucas! Um aviso lê-se até ao fim. Até à assinatura!", 0.4),
        ("LUC", "E o pior é que eu disse ao senhor Anselmo que não havia ensaio…", 0.6),
        ("NARR", "Entra o senhor Anselmo, muito satisfeito, a sacudir o pó das mãos.", 0.5),
        ("ANS", "Pronto, dona Guilhermina! As cadeiras estão todas no armazém, bem empilhadinhas. Não há ensaio, pois não?", 0.4),
        ("TODOS", "Não há ensaio… Há estreia!", 0.5),
        ("ANS", "Hã?! Estreia? Com público?! Oh, não!", 0.4),
        ("GUI", "Depressa, que faltam vinte minutos! Beatriz, os fatos! Lucas e senhor Anselmo, as cadeiras!", 0.5),
        ("NARR", "Todos correm de um lado para o outro. Ouve-se a campainha da porta.", 0.2),
        ("SFX", "campainha", 0.5),
        ("GUI", "Chegaram os primeiros pais!", 0.4),
        ("LUC", "Pronto… Prometo que, da próxima vez, leio tudo até ao fim!", 0.6),
        ("NARR", "O senhor Anselmo pendura na parede um aviso novo: Ler até ao fim! A Mourinha sobe pela parede e deita-se, satisfeita, mesmo em cima da palavra fim. Todos se riem. Pano.", 0.5),
    ],
    "u4-02-a-chave-desaparecida": [
        ("NARR", "A Chave Desaparecida. Comédia de mistério num ato e três cenas. A ação passa-se no átrio do Gabinete das Coisas Verdadeiras, numa segunda-feira de manhã.", 1.0),
        ("NARR", "Cena um. O alarme. Nove e quarenta e cinco. Ao centro, a Vitrine das Coisas Raras, fechada com um cadeado. Lá dentro, um relógio de bolso antigo. Faz frio. A dona Guilhermina procura qualquer coisa em todos os bolsos.", 0.8),
        ("GUI", "Aqui não está… Aqui também não… Ai, meu Deus!", 0.3),
        ("SFX", "tlim", 0.6),
        ("ANS", "Bom dia, dona Guilhermina! Perdeu alguma coisa?", 0.4),
        ("GUI", "A chave da Vitrine das Coisas Raras! A turma do Year 5 chega às dez, e eu prometi mostrar-lhes o relógio de bolso.", 0.4),
        ("ANS", "A senhora não costumava pendurar a chave no fio dos óculos?", 0.4),
        ("GUI", "Isso era dantes! Agora guardo-a sempre no bolso.", 0.5),
        ("GUI", "Brrr! Que frio está hoje!", 0.6),
        ("NARR", "Entram a Beatriz e o Lucas. Ele traz uma lupa enorme; ela, um caderno.", 0.5),
        ("LUC", "Chegámos cedo para ajudar! O que se passa?", 0.4),
        ("ANS", "Desapareceu a chave da vitrine.", 0.4),
        ("LUC", "Um mistério! Que ninguém saia daqui. São todos suspeitos!", 0.4),
        ("BEA", "Calma, Lucas. Primeiro, as perguntas. Dona Guilhermina, quando viu a chave pela última vez?", 0.4),
        ("GUI", "Às nove em ponto. Abri a vitrine para limpar o relógio e fechei-a logo a seguir.", 0.3),
        ("SFX", "tlim", 0.5),
        ("NARR", "A Beatriz levanta os olhos do caderno, intrigada.", 1.6),
        ("NARR", "Cena dois. Os suspeitos. Entra a dona Rosa, com um tabuleiro de pastéis de nata.", 0.6),
        ("ROSA", "Bom dia a todos! Trouxe os pastéis para a visita. Estão quentinhos!", 0.4),
        ("LUC", "Alto aí! Dona Rosa, onde estava às nove horas?", 0.4),
        ("ROSA", "Às nove? Aqui mesmo, a trazer o café à dona Guilhermina, como todos os dias. Depois, levei o tabuleiro para a pastelaria.", 0.4),
        ("LUC", "Aha! A chave caiu no tabuleiro e foi parar à pastelaria!", 0.4),
        ("ROSA", "Ó menino, eu lavei esse tabuleiro com estas mãos. Só lá havia migalhas!", 0.4),
        ("LUC", "E o senhor? O que fez esta manhã?", 0.4),
        ("ANS", "Pus a brilhar os metais todos do Gabinete: os castiçais, os puxadores, a campainha…", 0.4),
        ("LUC", "Os metais! E as chaves são de metal! Vire os bolsos do avesso!", 0.6),
        ("NARR", "O senhor Anselmo vira os bolsos. Cai um pano aos quadrados… e um pastel de nata.", 0.5),
        ("ROSA", "O meu pastel! Então é o senhor que me tira um pastel todas as manhãs!", 0.4),
        ("ANS", "Era… para o lanche.", 0.5),
        ("LUC", "Um pastel não é uma chave.", 0.4),
        ("GUI", "Faltam dez minutos! Que vergonha, com os meninos à porta!", 0.3),
        ("SFX", "tlim", 1.4),
        ("NARR", "Cena três. As pistas. A Beatriz senta-se no degrau e relê o caderno. Os outros continuam a procurar. Na parede, a Mourinha não tira os olhos da dona Guilhermina.", 0.7),
        ("BEA", "Pista número um: às nove, a chave estava na mão da dona Guilhermina. Pista número dois: estava frio, e ela abotoou o casaco até ao pescoço. Pista número três… um barulhinho: tlim-tlim.", 0.4),
        ("LUC", "Tlim-tlim? Isso lá é pista!", 0.4),
        ("BEA", "É a pista mais importante de todas. E há mais uma: olha para a Mourinha.", 0.4),
        ("LUC", "A osga? Está só a olhar para a dona Guilhermina.", 0.4),
        ("BEA", "Pois está. Há dez minutos que não olha para mais nada.", 0.5),
        ("BEA", "Já sei onde está a chave!", 0.4),
        ("TODOS", "Onde?!", 0.5),
        ("NARR", "Toca a campainha da porta: chegou a turma do Year 5.", 0.2),
        ("SFX", "campainha", 0.5),
        ("NARR", "Escuro. E agora? A cena quatro… és tu que a escreves.", 0.5),
    ],
    "u4-03-ouve-e-decide": [
        ("INTRO", "Ouve e decide. Vais ouvir oito frases. Repara na voz: sobe, desce ou explode? Depois de cada frase, escreve D, se for declarativa, I, se for interrogativa, E, se for exclamativa, ou I M, se for imperativa.", 1.5),
        ("INTRO", "Frase um.", 0.3), ("FRASE", "Há estreia.", 4),
        ("INTRO", "Frase dois.", 0.3), ("FRASE", "Há estreia?", 4),
        ("INTRO", "Frase três.", 0.3), ("FRASE", "Há estreia!", 4),
        ("INTRO", "Frase quatro.", 0.3), ("FRASE", "Tragam os fatos.", 4),
        ("INTRO", "Frase cinco.", 0.3), ("FRASE", "Onde está a chave?", 4),
        ("INTRO", "Frase seis.", 0.3), ("FRASE", "Que frio está hoje!", 4),
        ("INTRO", "Frase sete.", 0.3), ("FRASE", "Não há ensaio.", 4),
        ("INTRO", "Frase oito.", 0.3), ("FRASE", "Sentem-se, por favor.", 3),
        ("INTRO", "Agora, experimenta tu: diz a frase «Há estreia» das três maneiras — como quem informa, como quem pergunta e como quem está muito espantado.", 0.5),
    ],
}

SFX = {
    # little metallic "tlim-tlim": two short bright tones with a fast decay
    "tlim": "sine=f=2637:d=0.16,afade=t=out:st=0:d=0.16[a];sine=f=3136:d=0.22,afade=t=out:st=0:d=0.22,adelay=190[b];[a][b]amix=inputs=2:duration=longest:normalize=0,volume=0.55",
    # door bell "ding-dong"
    "campainha": "sine=f=784:d=0.9,afade=t=out:st=0.05:d=0.85[a];sine=f=622:d=1.1,afade=t=out:st=0.05:d=1.05,adelay=600[b];[a][b]amix=inputs=2:duration=longest:normalize=0,volume=0.5",
}


def ff(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *args], check=True)


async def tts(spec, text, path):
    v, p, r = spec
    for attempt in range(5):
        try:
            await edge_tts.Communicate(text, v, pitch=p, rate=r).save(path)
            return
        except Exception:
            if attempt == 4:
                raise
            await asyncio.sleep(3 * (attempt + 1))


async def segment(who, text, path, td):
    if who == "SFX":
        ff("-filter_complex", SFX[text], "-ar", "24000", "-ac", "1", path)
        return
    spec = V[who]
    if isinstance(spec, list):  # chorus: same line in several voices, slightly staggered
        parts = []
        for j, s in enumerate(spec):
            f = os.path.join(td, f"ch{j}.mp3")
            await tts(s, text, f)
            parts.append(f)
        inputs = sum((["-i", f] for f in parts), [])
        delays = ";".join(f"[{j}]adelay={j * 40}[d{j}]" for j in range(len(parts)))
        mix = "".join(f"[d{j}]" for j in range(len(parts)))
        ff(*inputs, "-filter_complex", f"{delays};{mix}amix=inputs={len(parts)}:normalize=0,volume=0.55",
           "-ar", "24000", "-ac", "1", path)
        return
    await tts(spec, text, path)


async def main(names):
    os.makedirs(OUT, exist_ok=True)
    for name, parts in TRACKS.items():
        if names and name not in names:
            continue
        with tempfile.TemporaryDirectory() as td:
            files = []
            for i, (who, t, pause) in enumerate(parts):
                f = os.path.join(td, f"{i:03d}.mp3")
                await segment(who, t, f, td)
                s = os.path.join(td, f"{i:03d}s.mp3")
                ff("-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(pause), "-q:a", "9", s)
                files += [f, s]
            lst = os.path.join(td, "list.txt")
            with open(lst, "w") as fh:
                fh.writelines(f"file '{f}'\n" for f in files)
            out = os.path.join(OUT, name + ".mp3")
            ff("-f", "concat", "-safe", "0", "-i", lst, "-ar", "24000", "-ac", "1", "-b:a", "64k", out)
            print(name, os.path.getsize(out))


asyncio.run(main(sys.argv[1:]))
