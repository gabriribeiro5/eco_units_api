from http.server import BaseHTTPRequestHandler, HTTPServer
from routes import RoutesManager as Routes
from sessions import SessionManager as Sessions
from auth import AuthManager as Auth

class MasterHandler(BaseHTTPRequestHandler, Routes, Sessions, Auth):
    def __init__(self, *args, **kwargs):
        Routes.__init__(self, *args, **kwargs)
        Sessions.__init__(self, *args, **kwargs)
        Auth.__init__(self, *args, **kwargs)
        self.data_store = []

    # Lida com requisições GET
    @Auth.require_authentication()
    def do_GET(self):
        handler_name = self.routes_get.get(self.path)
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler()
        else:
            self.send_error(404, "Not Found")

# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=MasterHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
