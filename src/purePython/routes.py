import json
from purePython.utils.definitions import ROUTES_DIR, SRC_DIR

class RoutesManager():
    # Inicializa as rotas de forma dinâmica
    def __init__(self):
        self.all = self.load_routes(ROUTES_DIR)
        self.only_POST = self.all["POST"]
        self.only_GET = self.all["GET"]
        self.only_PUT = self.all["PUT"]
        self.only_PATCH = self.all["PATCH"]
        self.only_DELETE = self.all["DELETE"]
        self.only_TRACE = self.all["TRACE"]
        self.only_OPTIONS = self.all["OPTIONS"]
        

    # Carrega rotas de um arquivo JSON
    @staticmethod
    def load_routes(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar rotas: {e}")
            return {}
    

if __name__ == "__main__":
    rm = RoutesManager()