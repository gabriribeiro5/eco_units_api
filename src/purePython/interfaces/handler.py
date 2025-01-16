from http.server import BaseHTTPRequestHandler
from utils.heisenberg import WalterWhite
from utils.logSetUp import LogSetUp
from utils.definitions import Definitions

class I_BaseHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = LogSetUp()
        self.inspector = WalterWhite()
        self.definitions = Definitions()
        super().__init__(request, client_address, server)