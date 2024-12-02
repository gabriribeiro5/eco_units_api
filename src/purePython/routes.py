import json
from utils.definitions import ROUTES_PATH, SRC_DIR

class RoutesManager():
    # Inicializa as rotas de forma dinâmica
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"root dir: {SRC_DIR}")
        self.routes = self.load_routes(ROUTES_PATH)
        self.routes_GET = self.routes["GET"]
        self.routes_POST = self.routes["POST"]
        self.routes_PUT = self.routes["PUT"]
        self.routes_DELETE = self.routes["DELETE"]
        

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