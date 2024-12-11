from purePython.entities.handler import BaseHandler
import json

class DeleteHandler(BaseHandler):

    # Handlers para as rotas
    def handle_delete_some_data(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"data": self.data_store}
        self.wfile.write(json.dumps(response).encode())
    