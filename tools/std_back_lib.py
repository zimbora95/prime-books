
import sys, os, json
sys.path.insert(0,'/root/prime-books')
import pymupdf
from PIL import Image, ImageOps
HERE='/root/prime-books'
ASSETS=HERE+'/tools/cover_assets'
FONT_TITLE=ASSETS+'/Poppins-ExtraBold.ttf'
FONT_TITLE_MED=ASSETS+'/Poppins-SemiBold.ttf'
FONT_BODY=ASSETS+'/Andika-Regular.ttf'
META=json.load(open(ASSETS+'/cover_meta.json'))
CREAM=(249/255,245/255,234/255)
SAND=(0xF2/255,0xEB/255,0xDC/255)
INK=(0x1A/255,)*3
GREY=(0x6B/255,0x6B/255,0x5E/255)
BROWN=(0x5A/255,0x24/255,0x09/255)
TERRA=(0x7C/255,0x40/255,0x22/255)
INKISH=(0x2E/255,0x2A/255,0x24/255)
f_title=pymupdf.Font(fontfile=FONT_TITLE)
f_body=pymupdf.Font(fontfile=FONT_BODY)

def tw(font,text,size): return font.text_length(text,fontsize=size)
def wrap(text,font,size,maxw):
    words,lines,cur=text.split(),[],''
    for w in words:
        t=(cur+' '+w).strip()
        if tw(font,t,size)<=maxw or not cur: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def build_back(page, year, subject_title, level, ages, band, copy, art_path, stripe_rgb):
    W,H=page.rect.width,page.rect.height
    im=Image.open(art_path).convert('RGB').resize((714,int(714*H/W)),Image.LANCZOS)
    g=ImageOps.grayscale(im).convert('L')
    r=g.point([min(255,int(p*0.97+16)) for p in range(256)])
    gg=g.point([min(255,int(p*0.97+16)) for p in range(256)])
    b=g.point([min(255,int(p*0.96+15)) for p in range(256)])
    im=Image.merge('RGB',(r,gg,b))
    white=Image.new('RGB',im.size,(250,249,246))
    im=Image.blend(im,white,0.62)
    tmp='/tmp/_backbg.png'; im.save(tmp)
    page.insert_image(pymupdf.Rect(0,0,W,H),filename=tmp,keep_proportion=False)
    stripe_w=34.0
    page.draw_rect(pymupdf.Rect(0,0,stripe_w,H),color=None,fill=tuple(c/255 for c in stripe_rgb))
    x0=85.0
    page.insert_text((x0,78),'P R I M E  B O O K S',fontsize=9.6,fontname='med',fontfile=FONT_TITLE_MED,color=GREY)
    size=33.0; y=96
    lines=wrap(subject_title,f_title,size,460)
    for i,line in enumerate(lines):
        page.insert_text((x0,y+32+i*36),line,fontsize=size,fontname='ttl',fontfile=FONT_TITLE,color=INK)
    ty=y+32+len(lines)*36+2
    page.draw_rect(pymupdf.Rect(x0,ty,x0+22,ty+3),color=None,fill=tuple(c/255 for c in stripe_rgb))
    page.insert_text((x0,ty+22),f'Year {year} · Student Manual',fontsize=11,fontname='body',fontfile=FONT_BODY,color=GREY)
    by=ty+48
    paras=[copy['hook'],copy.get('blurb','')]
    for p in paras:
        for ln in wrap(p,f_body,11.4,438):
            page.insert_text((x0,by),ln,fontsize=11.4,fontname='body',fontfile=FONT_BODY,color=INKISH)
            by+=17.2
        by+=7
    card_x0,card_x1=x0-14,470
    card_y0=max(by+6,0.42*H)
    bullets=copy['bullets']
    card_h=30+9+len(bullets)*19+14
    card_y1=min(card_y0+card_h,H-120)
    card=page.new_shape()
    card.draw_rect(pymupdf.Rect(card_x0,card_y0,card_x1,card_y1),radius=0.06)
    card.finish(color=None,fill=SAND)
    card.commit()
    page.insert_text((card_x0+16,card_y0+24),'INSIDE THIS BOOK',fontsize=9.4,fontname='med',fontfile=FONT_TITLE_MED,color=BROWN)
    yy=card_y0+44
    for bl in bullets:
        page.insert_text((card_x0+16,yy),'•',fontsize=10.6,fontname='body',fontfile=FONT_BODY,color=INKISH)
        first=True
        for ln in wrap(bl,f_body,10.6,card_x1-card_x0-46):
            page.insert_text((card_x0+30,yy),ln,fontsize=10.6,fontname='body',fontfile=FONT_BODY,color=INKISH)
            yy+=19 if first else 15
            first=False
    fy=H-65
    page.insert_text((x0,fy),f'Prime Books · {subject_title}',fontsize=9,fontname='med',fontfile=FONT_TITLE_MED,color=INK)
    page.insert_text((x0,fy+16),f'{ages} · {band}',fontsize=9,fontname='body',fontfile=FONT_BODY,color=GREY)
    page.insert_text((x0,fy+32),'primeschool.pt',fontsize=9,fontname='med',fontfile=FONT_TITLE_MED,color=TERRA)
