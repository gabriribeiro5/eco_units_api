import json
from utils.definitions import Definitions

class OptionsManager():
    # Inicializa as rotas de forma dinâmica
    def __init__(self, *args, **kwargs) -> None:
        self.definitions = Definitions()
        self.all = self.load_options(self.definitions.ROUTES_DIR)
        self.only_TRACE = self.all["TRACE"]
        self.only_OPTIONS = self.all["OPTIONS"]
        self.only_POST = self.all["POST"]
        self.only_GET = self.all["GET"]
        self.only_PUT = self.all["PUT"]
        self.only_PATCH = self.all["PATCH"]
        self.only_DELETE = self.all["DELETE"]
        super().__init__(*args, **kwargs)
        

    # Carrega rotas de um arquivo JSON
    @staticmethod
    def load_options(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar rotas: {e}")
            return {}

if __name__ == "__main__":
    rm = OptionsManager()