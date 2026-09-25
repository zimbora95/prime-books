# Audio for the QR codes of Unit 1 — "O Gabinete das Coisas Verdadeiras".
# Each track is a list of (voice, pitch, rate, text, pause_after_seconds).
# Run with the experiment venv:  python audio_scripts.py  -> writes ./audio/*.mp3
import asyncio, os, subprocess, tempfile
import edge_tts

FFMPEG = "/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
R, D = "pt-PT-RaquelNeural", "pt-PT-DuarteNeural"

TRACKS = {
    "01-artigo-osga": [
        (D, "+0Hz", "-8%", "A osga-comum. Tarentola mauritanica.", 0.8),
        (D, "+0Hz", "-8%", "A osga-comum, também chamada osga-moura, é um pequeno réptil que vive em quase todo o território de Portugal continental. É muitas vezes vista nas paredes das casas, ao fim do dia, à espera de insetos.", 0.9),
        (D, "+0Hz", "-8%", "Aspeto.", 0.5),
        (D, "+0Hz", "-8%", "A osga-comum mede cerca de quinze centímetros, com a cauda incluída; alguns exemplares chegam aos dezanove. Tem o corpo largo e achatado, a cabeça bem destacada e olhos grandes, de íris dourada e pupila vertical. A pele das costas é rugosa, coberta de filas de pequenos tubérculos. A cor varia entre o cinzento, o acastanhado e o esbranquiçado, e pode ficar mais clara ou mais escura, conforme o ambiente. A barriga é clara: bege, amarelada ou branca.", 0.9),
        (D, "+0Hz", "-8%", "Onde vive.", 0.5),
        (D, "+0Hz", "-8%", "Prefere lugares quentes e secos. Encontra-se em muros de pedra, rochas, troncos, ruínas e paredes de edifícios, tanto no campo como na cidade. É mais comum no sul e no interior do país. Também existe na ilha da Madeira, onde foi introduzida pelo ser humano.", 0.9),
        (D, "+0Hz", "-8%", "O que come.", 0.5),
        (D, "+0Hz", "-8%", "É um animal crepuscular e noturno: caça ao anoitecer e durante a noite. Alimenta-se sobretudo de insetos, como moscas, mosquitos e traças, e também de aranhas. Por isso, muitas vezes espera junto às lâmpadas, onde os insetos se juntam.", 0.9),
        (D, "+0Hz", "-8%", "Superpoderes.", 0.5),
        (D, "+0Hz", "-8%", "Patas que colam: por baixo de cada dedo, a osga tem almofadas com lamelas, cobertas de pelos microscópicos. É graças a elas que consegue subir paredes lisas e até andar no teto.", 0.6),
        (D, "+0Hz", "-8%", "Cauda de reserva: quando é atacada, a osga pode soltar a cauda, que continua a mexer-se e distrai o predador. Depois, cresce-lhe uma cauda nova, mais lisa e sem tubérculos.", 0.9),
        (D, "+0Hz", "-8%", "Mitos e verdades.", 0.5),
        (D, "+0Hz", "-8%", "Há quem acredite que a osga é venenosa ou que faz mal a quem lhe toca. Não é verdade: a osga-comum é inofensiva para as pessoas. Pelo contrário, é útil, porque come muitos dos insetos que nos incomodam.", 0.5),
    ],
    "02-facto-ou-opiniao": [
        (R, "+0Hz", "-5%", "Facto ou opinião? Vais ouvir oito frases. Depois de cada uma, escreve F, se for um facto, ou O, se for uma opinião.", 1.5),
        (D, "+0Hz", "-10%", "Frase um. Lisboa é a capital de Portugal.", 4),
        (D, "+0Hz", "-10%", "Frase dois. Lisboa é a cidade mais bonita do mundo.", 4),
        (D, "+0Hz", "-10%", "Frase três. Os dicionários são muito aborrecidos.", 4),
        (D, "+0Hz", "-10%", "Frase quatro. O dicionário do Gabinete tem mais de cem anos.", 4),
        (D, "+0Hz", "-10%", "Frase cinco. Na minha opinião, os lobos são assustadores.", 4),
        (D, "+0Hz", "-10%", "Frase seis. Uma alcateia é um grupo de lobos.", 4),
        (D, "+0Hz", "-10%", "Frase sete. Ao nível do mar, a água ferve a cem graus.", 4),
        (D, "+0Hz", "-10%", "Frase oito. O verão é a melhor estação do ano.", 2),
        (R, "+0Hz", "-5%", "Muito bem! Agora compara as tuas respostas com as de um colega. Qual foi a frase mais difícil de decidir?", 0.5),
    ],
    "03-retratos": [
        (R, "+0Hz", "-6%", "Retrato da Dona Guilhermina.", 0.8),
        (R, "+0Hz", "-6%", "A Dona Guilhermina é a guardiã do Gabinete das Coisas Verdadeiras. É uma senhora pequena e magra, com setenta anos bem vividos.", 0.6),
        (R, "+0Hz", "-6%", "Tem o cabelo branco e fofo, apanhado num carrapito onde espeta sempre um lápis amarelo — diz que é para nunca o perder. Os olhos são escuros e vivos, rodeados de ruguinhas de quem se ri muito. Uns óculos redondos, presos a um fio, balançam-lhe no peito e só sobem ao nariz quando é preciso ler letras miudinhas. Usa quase sempre um casaco de malha verde-garrafa, com um botão vermelho que não condiz com os outros.", 0.6),
        (R, "+0Hz", "-6%", "Mas o mais bonito da Dona Guilhermina não se vê logo. É muito paciente: responde à mesma pergunta dez vezes sem se zangar. É curiosíssima: examina uma concha com a lupa como se fosse a primeira que via. E é um bocadinho teimosa, porque se recusa a pôr a osga Mourinha fora do Gabinete.", 0.6),
        (R, "+0Hz", "-6%", "Quando fala dos seus objetos, a voz dela fica mais alta e mais rápida do que o costume. Nesse momento, percebe-se que a Dona Guilhermina não guarda apenas coisas: guarda histórias.", 1.6),
        (D, "+0Hz", "-6%", "O sótão do Gabinete.", 0.8),
        (D, "+0Hz", "-6%", "Subo a escada estreita, que range a cada degrau, e abro a porta do sótão.", 0.5),
        (D, "+0Hz", "-6%", "Lá dentro, o ar é morno e cheira a pó, a papel velho e a madeira. Do teto inclinado, feito de traves escuras, desce um raio de sol que entra pela claraboia. Dentro dele, dançam milhares de grãos de pó dourados.", 0.5),
        (D, "+0Hz", "-6%", "À esquerda, amontoam-se baús de couro, com fechos de latão já gastos. Ao centro, um cavalo de baloiço branco, com a tinta a descascar, parece esperar por uma criança que nunca mais voltou. Atrás dele, uma gaiola vazia descansa em cima de uma pilha de baús. À direita, um manequim de costura usa um chapéu de palha.", 0.5),
        (D, "+0Hz", "-6%", "Ao fundo, a janela redonda é o sítio mais luminoso de todos. Por ela veem-se os telhados cor de laranja de Lisboa e, no parapeito, um pombo que me observa, desconfiado.", 0.5),
        (D, "+0Hz", "-6%", "Aqui, o silêncio é enorme: ouve-se o tique-taque do relógio da parede. O sótão é o lugar mais misterioso do Gabinete — e o meu preferido.", 0.5),
    ],
    "04-visita-guiada-leonor": [
        (R, "+18Hz", "-4%", "Olá a todos! Sabiam que dentro desta vitrine está um animal que é parente dos polvos e que traz a casa às costas? Hoje vou apresentar-vos a concha do náutilo.", 0.8),
        (R, "+18Hz", "-4%", "Primeiro, vou falar-vos do seu aspeto. A concha é enrolada em espiral e tem riscas cor de laranja sobre um fundo branco. Por dentro, está dividida em muitas câmaras, como se fosse uma casa com vários quartos. O animal vive só na última câmara, a maior.", 0.6),
        (R, "+18Hz", "-4%", "Em segundo lugar, vou dizer-vos onde vive. O náutilo vive nos oceanos Índico e Pacífico, normalmente entre os cem e os quinhentos metros de profundidade.", 0.6),
        (R, "+18Hz", "-4%", "Por fim, uma curiosidade: o náutilo sobe e desce na água enchendo as câmaras da concha com gás ou com líquido, um pouco como um submarino.", 0.8),
        (R, "+18Hz", "-4%", "Em resumo, o náutilo é um animal com uma concha em espiral, que vive no fundo do mar e funciona como um submarino. Na minha opinião, é o objeto mais extraordinário do Gabinete. Obrigada pela vossa atenção! Alguém tem alguma pergunta?", 0.5),
    ],
}


async def seg(voice, pitch, rate, text, path):
    await edge_tts.Communicate(text, voice, pitch=pitch, rate=rate).save(path)


async def main():
    os.makedirs(OUT, exist_ok=True)
    for name, parts in TRACKS.items():
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


asyncio.run(main())
