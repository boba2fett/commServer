from response.requestHandler import RequestHandler
import subprocess
import os

class CommHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'text/html'

    def find(self, routeData):
        try:
            self.setStatus(200)
            self.contents = str(os.popen(f'routes{routeData}').read().replace("\n","  "))
            return True
        except:
            self.setStatus(404)
            return False

