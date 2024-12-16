from entities.handler import BaseHandler

class OptionsHandler(BaseHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        

    def handle_options(self):
        pass
        # self.send_response(200)
        # self.send_header("Content-type", "application/json")
        # self.end_headers()
        # response = {"data": self.data_store}
        # self.wfile.write(json.dumps(response).encode())
    