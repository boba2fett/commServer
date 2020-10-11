import os

from http.server import BaseHTTPRequestHandler

from response.commHandler import CommHandler
from response.badRequestHandler import BadRequestHandler
from response.forbiddenRequestHandler import ForbiddenRequestHandler
import json

with open('settings.json', 'r') as json_file:
    config = json.load(json_file)

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        print(split_path)
        if split_path[0][1::] in os.listdir("routes"):
            handler = CommHandler()
            handler.find(self.path)
        else:
            handler = BadRequestHandler()
 
        self.respond({
            'handler': handler
        })

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        split_path = os.path.splitext(self.path)
        print(split_path)
        print(post_body)
        if post_body!=bytes(config["token"],"utf8"):
            handler=ForbiddenRequestHandler()
        else:
            if split_path[0][1::] in os.listdir("routes"):
                handler = CommHandler()
                handler.find(self.path)
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

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
