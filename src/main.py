from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Define the handler for HTTP requests
class SimpleHandler(BaseHTTPRequestHandler):
    # Data storage for demonstration purposes
    data_store = []

    # Handle GET requests
    def do_GET(self):
        if self.path == "/api/data":
            # Set response code and headers
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Send response data
            response = {"data": self.data_store}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Not Found")

    # Handle POST requests
    def do_POST(self):
        if self.path == "/api/data":
            # Read the content length
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            # Parse the JSON and store it
            try:
                data = json.loads(post_data)
                self.data_store.append(data)
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b"Data added successfully")
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
        else:
            self.send_error(404, "Not Found")

# Define and run the server
def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
