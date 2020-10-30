#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server
import ssl
import json
import socket

with open('settings.json', 'r') as json_file:
    config = json.load(json_file)

class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6

if __name__ == '__main__':
    httpd = HTTPServer((config["HOST_NAME"], config["PORT_NUMBER"]), Server)
    httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile=f"/etc/letsencrypt/live/{config['domain']}/privkey.pem", 
        certfile=f"/etc/letsencrypt/live/{config['domain']}/fullchain.pem", server_side=True)
    print(time.asctime(), 'Server Starts - %s:%s' % (config["HOST_NAME"], config["PORT_NUMBER"]))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (config["HOST_NAME"], config["PORT_NUMBER"]))
