from purePython.entities.handler import BaseHandler

class View(BaseHandler):
    def __init__(self):
        pass
        

    def diagnostic(self):
        pass
        # self.send_response(200)
        # self.send_header("Content-type", "application/json")
        # self.end_headers()
        # response = {"data": self.data_store}
        # self.wfile.write(json.dumps(response).encode())
    
    def configuration(self):
        pass
        # self.send_response(200)
        # self.send_header("Content-type", "application/json")
        # self.end_headers()
        # response = {"data": self.data_store}
        # self.wfile.write(json.dumps(response).encode())
    
    def environment_state(self):
        pass
        # self.send_response(200)
        # self.send_header("Content-type", "application/json")
        # self.end_headers()
        # response = {"data": self.data_store}
        # self.wfile.write(json.dumps(response).encode())
    