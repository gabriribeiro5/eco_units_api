import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from routes import RoutesManager

AUTH_TOKEN = "my_secret_token"

class EcoUnitHandler(BaseHTTPRequestHandler, RoutesManager):
    def __init__(self, *args, **kwargs):
        RoutesManager.__init__(self, *args, **kwargs)
        self.data_store = []

    def test(self): 
        b = self.routes_POST
        print(f"<<< POST >>> {b}")

    # Verifica se a requisição está autenticada
    def is_authenticated(self):
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token == AUTH_TOKEN
        return False

    # Lida com requisições GET
    def do_GET(self):
        if not self.is_authenticated():
            self.send_error(401, "Unauthorized")
            return

        handler_name = self.routes_get.get(self.path)
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler()
        else:
            self.send_error(404, "Not Found")

    

# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=EcoUnitHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    # run()
    e = EcoUnitHandler()
    e.test()
