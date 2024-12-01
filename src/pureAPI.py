import json
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTH_TOKEN = "my_secret_token"

class SimpleHandler(BaseHTTPRequestHandler):
    data_store = []

    # Inicializa as rotas de forma dinâmica
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.routes_get = self.load_routes("routes.json")

    # Carrega rotas de um arquivo JSON
    @staticmethod
    def load_routes(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar rotas: {e}")
            return {}

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

    # Handlers para as rotas
    def handle_get_data(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"data": self.data_store}
        self.wfile.write(json.dumps(response).encode())

    def handle_get_status(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": "API is running"}
        self.wfile.write(json.dumps(response).encode())

    def handle_get_version(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"version": "1.0.0"}
        self.wfile.write(json.dumps(response).encode())

# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
