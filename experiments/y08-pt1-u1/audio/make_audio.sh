#!/usr/bin/env bash
# Builds the two radio spots used in Sessão 3 (Ouvir para desmontar).
set -euo pipefail
cd "$(dirname "$0")"
TTS=../.venv/bin/edge-tts
FF=/root/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg
R=pt-PT-RaquelNeural
D=pt-PT-DuarteNeural

# ---- Spot A: comercial (Cinema Aurora) ----
$TTS -v $R --rate=+4% -t "Lembras-te do cheiro das pipocas? Do escuro, mesmo antes de o filme começar?" --write-media a1.mp3
$TTS -v $D --rate=+10% --pitch=+2Hz -t "O Cinema Aurora está de volta! Depois de dez anos de portas fechadas, a sala mais antiga da costa reabre a três de outubro, com a estreia de O Farol das Baleias: a aventura que está a encher salas por todo o país!" --write-media a2.mp3
$TTS -v $R --rate=+8% -t "Bilhetes a quatro euros para estudantes. E, às quartas-feiras, as pipocas Maré são oferecidas pela casa!" --write-media a3.mp3
$TTS -v $D --rate=+2% -t "Cinema Aurora. Quem vem à Aurora nunca vai embora." --write-media a4.mp3

# ---- Spot B: não comercial (Campanha Mar Limpo) ----
$TTS -v $R --rate=-8% -t "Ouve. Este é o som do mar." --write-media b1.mp3
$TTS -v $R --rate=-6% -t "Todos os anos, milhões de toneladas de plástico chegam aos oceanos. Uma única garrafa pode demorar centenas de anos a desaparecer. E, enquanto não desaparece, alguém a come, alguém fica preso nela." --write-media b2.mp3
$TTS -v $D --rate=-4% -t "Tu podes mudar isto. Leva a tua garrafa. Recusa o descartável." --write-media b3.mp3
$TTS -v $R --rate=-10% -t "O mar não cabe numa garrafa. Mas o plástico cabe no mar. Campanha Mar Limpo, uma iniciativa da Associação Amigos da Costa." --write-media b4.mp3

sil() { $FF -y -loglevel error -f lavfi -i anullsrc=r=24000:cl=mono -t "$1" "$2"; }
sil 0.6 s06.mp3; sil 1.2 s12.mp3; sil 2.2 s22.mp3; sil 0.4 s04.mp3

# voice tracks
$FF -y -loglevel error -i s06.mp3 -i a1.mp3 -i s04.mp3 -i a2.mp3 -i s04.mp3 -i a3.mp3 -i s06.mp3 -i a4.mp3 -i s12.mp3 \
  -filter_complex "concat=n=9:v=0:a=1" voiceA.wav
$FF -y -loglevel error -i s12.mp3 -i b1.mp3 -i s22.mp3 -i b2.mp3 -i s12.mp3 -i b3.mp3 -i s12.mp3 -i b4.mp3 -i s22.mp3 \
  -filter_complex "concat=n=9:v=0:a=1" voiceB.wav

durA=$( ($FF -i voiceA.wav 2>&1 || true) | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')
durB=$( ($FF -i voiceB.wav 2>&1 || true) | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')

# Spot A bed: bright pulsing C-major pad (C E G + high C), gently rhythmic
$FF -y -loglevel error -f lavfi -i "aevalsrc='(0.05*sin(2*PI*261.63*t)+0.04*sin(2*PI*329.63*t)+0.04*sin(2*PI*392*t)+0.03*sin(2*PI*523.25*t*(1+0.002*sin(6*t))))*(0.55+0.45*abs(sin(2*PI*1.1*t)))':s=24000:d=${durA}" \
  -af "afade=t=in:d=0.8,afade=t=out:st=$(echo "$durA-1.5" | bc):d=1.5" bedA.wav
# Spot B bed: surf — brown noise, slow swell, low-passed
$FF -y -loglevel error -f lavfi -i "anoisesrc=color=brown:amplitude=0.5:r=24000:d=${durB}" \
  -af "lowpass=f=900,tremolo=f=0.13:d=0.75,volume=0.55,afade=t=in:d=2,afade=t=out:st=$(echo "$durB-2.5" | bc):d=2.5" bedB.wav

mix() { $FF -y -loglevel error -i "$1" -i "$2" -filter_complex "[1:a]volume=$3[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5" -ar 44100 -b:a 128k "$4"; }
mix voiceA.wav bedA.wav 0.9 spot-a-cinema-aurora.mp3
mix voiceB.wav bedB.wav 1.0 spot-b-mar-limpo.mp3
rm -f a?.mp3 b?.mp3 s[0-9]*.mp3 voice?.wav bed?.wav
ls -la *.mp3
