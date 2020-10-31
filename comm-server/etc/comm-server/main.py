#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server
import ssl
import json
import socket
import logging
from systemd.journal import JournalHandler

log = logging.getLogger("comm-server")
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

with open('settings.json', 'r') as json_file:
    config = json.load(json_file)

log.info("settings read")

class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6

if __name__ == '__main__':
    httpd = HTTPServer((config["HOST_NAME"], config["PORT_NUMBER"]), Server)
    #httpd.socket = ssl.wrap_socket (httpd.socket, 
    #    keyfile=f"/etc/letsencrypt/live/{config['domain']}/privkey.pem", 
    #    certfile=f"/etc/letsencrypt/live/{config['domain']}/fullchain.pem", server_side=True)
    log.info('Server Starts - %s:%s' % (config["HOST_NAME"], config["PORT_NUMBER"]))
    httpd.serve_forever()
