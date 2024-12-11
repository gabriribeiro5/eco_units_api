from http.server import BaseHTTPRequestHandler

class BaseHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)