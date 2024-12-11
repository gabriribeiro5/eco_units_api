from purePython.entities.handler import BaseHandler

class TraceHandler(BaseHandler):
    """
    Handles the TRACE HTTP method.
    Reflects the request back to the client as per the HTTP/1.1 specification.
    """
    def __init__(self):
        pass
        

    def handle_trace(self):
        self.log_request(200)  # Logs the request for debugging
        self.send_response(200)  # Send a success response
        self.send_header("Content-Type", "message/http")  # Specify the content type
        self.end_headers()

        # Reflect the request back to the client
        # Fetch the raw HTTP request
        request_line = f"{self.command} {self.path} {self.protocol_version}\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        # Send the reflected request back
        self.wfile.write(request_line.encode("utf-8"))
        self.wfile.write(headers.encode("utf-8"))
        self.wfile.write(b"\r\n")  # Add a final CRLF as a delimiter



        # self.send_response(200)
        # self.send_header("Content-type", "application/json")
        # self.end_headers()
        # response = {"data": self.data_store}
        # self.wfile.write(json.dumps(response).encode())