import os

from http.server import BaseHTTPRequestHandler

from urllib.parse import urlparse, parse_qs
from response.commHandler import CommHandler
from response.badRequestHandler import BadRequestHandler
from response.forbiddenRequestHandler import ForbiddenRequestHandler
import json
import logging
from systemd.journal import JournalHandler

log = logging.getLogger("comm-server")
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

with open('settings.json', 'r') as json_file:
    config = json.load(json_file)

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        parsed_path = urlparse(self.path)
        params=parse_qs(parsed_path.query)
        real_path=parsed_path.path

        if 't' not in params or params['t'][0]!=config["token"]:
            handler=ForbiddenRequestHandler()
            log.warn(f"Unautherised: {self.client_address}")
            print(f"Unautherised: {self.client_address}")
        else:
            if real_path[1::] in os.listdir("routes"): # prefix is still /
                handler = CommHandler()
                handler.find(real_path)
            else:
                handler = BadRequestHandler()
 
        self.respond({
            'handler': handler
        })

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        
        parsed_path = urlparse(self.path)
        real_path=parsed_path.path
        
        if post_body!=bytes(config["token"],"utf8"):
            handler=ForbiddenRequestHandler()
            log.warn(f"Unautherised: {self.client_address}")
            print(f"Unautherised: {self.client_address}")
        else:
            if real_path[1::] in os.listdir("routes"):
                handler = CommHandler()
                handler.find(real_path)
            else:
                handler = BadRequestHandler()
 
        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        content = handler.getContents()
        self.send_header('Content-type', handler.getContentType())
        self.send_header('Access-Control-Allow-Origin', '*') # proxy support

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
