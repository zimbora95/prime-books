"""Replace the book's self-hosted audio QR codes with links to external public resources.

The old codes pointed at the temporary development site; every new code points at a
public-broadcaster or institutional page (RTP / Ministry of Education / CPLP).
"""
import pathlib, re
import segno

B = pathlib.Path('/root/prime-books/experiments/y04-pt-u1/build')
P = B / 'pages'
LINKS = {
    'qr-ext-carta': 'https://www.rtp.pt/play/estudoemcasa/p7126/e471900/portugues-3-e-4-anos',
    'qr-ext-noticia': 'https://www.rtp.pt/play/estudoemcasa/p7126/e470561/portugues-3-e-4-anos',
    'qr-ext-cplp-lobo': 'https://cultura.cplp.org/media/wprdx0j2/contos-cplp-18-anos.pdf#page=22',
    'qr-ext-mar': 'https://arquivos.rtp.pt/conteudos/criancas-e-livros-14/',
    'qr-ext-teatro': 'https://www.rtp.pt/play/estudoemcasa/p7790/e542055/portugues-3-e-4-anos',
}
for name, url in LINKS.items():
    segno.make(url, error='m').save(str(B / 'img' / f'{name}.svg'), scale=4, border=0, dark='#1f2a44')

def ed(n, pairs):
    f = P / f'{n:02d}.html'; t = f.read_text()
    for a, b in pairs:
        assert a in t, (n, a[:60]); t = t.replace(a, b)
    f.write_text(t)

ed(9, [('<div class="qr"><img src="img/qr-a-carta-sem-selo.svg" alt=""><div><b>Ouve a história</b>Aponta o tablet para o código.</div></div>',
        '<div class="qr"><img src="img/qr-ext-carta.svg" alt=""><div><b>Vê a aula «A carta»</b>RTP · Estudo em Casa, 3.º e 4.º anos.</div></div>')])
ed(14, [('<div class="qr"><img src="img/qr-radio-limoeiro.svg" alt=""><div><b>Ouve a notícia</b>Aponta o tablet para o código ou pede ao professor para a ler.</div></div>',
         '<div class="qr"><img src="img/qr-ext-noticia.svg" alt=""><div><b>O professor é o locutor!</b>Ouve a notícia lida em voz alta. Depois, vê a aula «A notícia» (RTP · Estudo em Casa).</div></div>')])
ed(54, [('<div class="qr"><img src="img/qr-o-lobo-o-chibinho.svg" alt=""><div><b>Ouve a história</b>Aponta o tablet para o código ou pede ao professor que a leia.</div></div>',
         '<div class="qr"><img src="img/qr-ext-cplp-lobo.svg" alt=""><div><b>O professor conta a história.</b>Depois, lê a versão original nos «Contos Tradicionais da CPLP».</div></div>')])
ed(92, [('<div class="qr"><img src="img/qr-o-mar-tem.svg" alt=""><div><b>Ouve o poema</b>Aponta o tablet para o código ou pede ao professor para o ler.</div></div>',
         '<div class="qr"><img src="img/qr-ext-mar.svg" alt=""><div><b>O professor diz o poema.</b>Depois, ouve atores a dizer poemas do mar (RTP Arquivos).</div></div>')])
ed(93, [('<div class="qr"><img src="img/qr-o-mar-tem.svg" alt=""><div><b>Ouve o poema</b>e segue a partitura.</div></div>',
         '<div class="qr"><img src="img/qr-ext-mar.svg" alt=""><div><b>Poemas do mar</b>ditos por atores (RTP Arquivos).</div></div>')])
ed(104, [('<div class="qr"><img src="img/qr-a-lua-no-chafariz.svg" alt=""><div><b>Ouve a cena</b>e segue o texto com o dedo.</div></div>',
          '<div class="qr"><img src="img/qr-ext-teatro.svg" alt=""><div><b>Vê a aula «O texto dramático»</b>RTP · Estudo em Casa.</div></div>')])
# welcome-page icon legend: the QR icon no longer means "listen"
ed(3, [('<span><b>Aponta o tablet</b> para ouvir</span>', '<span><b>Aponta o tablet</b> e descobre mais</span>')])
# imprint
ed(2, [('<li>Oficinas de escrita guiadas e leituras com áudio</li>', '<li>Oficinas de escrita guiadas e recursos digitais</li>'),
       (' Audio readings use synthetic voices.', ' QR codes link to public educational resources (RTP, Estudo em Casa, CPLP), checked at the date of this edition.')])
print('ok')
