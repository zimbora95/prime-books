
import json, os
import pymupdf
from PIL import Image

HERE='/root/prime-books'
ASSETS=HERE+'/tools/cover_assets'
FONT_TITLE=ASSETS+'/Poppins-ExtraBold.ttf'
FONT_TITLE_MED=ASSETS+'/Poppins-SemiBold.ttf'
FONT_BODY=ASSETS+'/Andika-Regular.ttf'
LOGO=ASSETS+'/logo_prime_school.png'
META=json.load(open(ASSETS+'/cover_meta.json'))
CREAM=(249/255,245/255,234/255)
INK=(0x1A/255,)*3
GREY=(0x6B/255,0x6B/255,0x5E/255)
f_title=pymupdf.Font(fontfile=FONT_TITLE)

def tw(font,text,size): return font.text_length(text,fontsize=size)

def wrap(text,font,size,maxw):
    words,lines,cur=text.split(),[],''
    for w in words:
        t=(cur+' '+w).strip()
        if tw(font,t,size)<=maxw or not cur: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_logo(page,x,y,height=64.0):
    im=Image.open(LOGO); ratio=im.width/im.height; w=height*ratio
    page.insert_image(pymupdf.Rect(x,y,x+w,y+height),filename=LOGO)

def build_front(page, year, subject_title, level, art_path, stripe_rgb, art_top=315.0):
    W,H=page.rect.width,page.rect.height
    stripe_w=34.0
    page.draw_rect(pymupdf.Rect(0,0,W,H),color=None,fill=CREAM)
    page.draw_rect(pymupdf.Rect(0,0,stripe_w,H),color=None,fill=tuple(c/255 for c in stripe_rgb))
    draw_logo(page,85,42,height=64.0)
    x0=85.0; size=33.0
    lines=wrap(subject_title,f_title,size,W-125)
    for i,line in enumerate(lines):
        page.insert_text((x0,140+i*38),line,fontsize=size,fontname='ttl',fontfile=FONT_TITLE,color=INK)
    ymeta=140+len(lines)*38+26
    page.insert_text((x0,ymeta),f'Year {year}',fontsize=17,fontname='med',fontfile=FONT_TITLE_MED,color=INK)
    page.insert_text((x0,ymeta+24),level,fontsize=11,fontname='body',fontfile=FONT_BODY,color=GREY)
    page.insert_text((x0,ymeta+40),'Student Manual',fontsize=11,fontname='body',fontfile=FONT_BODY,color=GREY)
    ry=ymeta+52
    page.draw_rect(pymupdf.Rect(x0,ry,x0+46,ry+2.6),color=None,fill=tuple(c/255 for c in stripe_rgb))
    page.insert_image(pymupdf.Rect(stripe_w,art_top,W,H),filename=art_path,keep_proportion=False)

def find_front_art(page):
    """Largest image occupying the lower art zone -> (xref, rect) or None."""
    W,H=page.rect.width,page.rect.height
    best=None
    for im in page.get_images(full=True):
        xref=im[0]
        try:
            for rc in page.get_image_rects(xref):
                if rc.width>W*0.55 and rc.y0>180:
                    if best is None or rc.width*rc.height>best[1].width*best[1].height:
                        best=(xref,rc)
        except Exception: pass
    return best

def std_title(slug):
    return META['subjects'][slug]['title']
