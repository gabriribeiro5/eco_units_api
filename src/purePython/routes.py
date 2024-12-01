import json
from definitions import ROUTES_PATH, ROOT_DIR

class RoutesManager():
    # Inicializa as rotas de forma dinâmica
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"root dir: {ROOT_DIR}")
        self.routes = self.load_routes(ROUTES_PATH)
        

    # Carrega rotas de um arquivo JSON
    @staticmethod
    def load_routes(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar rotas: {e}")
            return {}
        
    def only_get_routes(self):
        routess = self.routes
        print(routess)

if __name__ == "__main__":
    rm = RoutesManager()
    rm.only_get_routes()