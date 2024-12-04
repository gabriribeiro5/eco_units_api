from http.server import BaseHTTPRequestHandler, HTTPServer
from routes import RoutesManager as Routes
from out_of_process.auth import AuthManager as Auth
from utils.definitions import LOG_DIR
from utils.logSetUp import enableLog

class MasterHandler(BaseHTTPRequestHandler):
    def __init__(self):
        self.routes = Routes()
        self.auth = Auth()
        self.data_store = []

    def test(self):
        pass
    
    def require_authentication(self):
        if not self.auth.is_authenticated(self):
            self.send_error(401, "Unauthorized")
            return
    
    def run_handler(self, handler_name):
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler()
        else:
            self.send_error(404, "Not Found")
    
    def do_TRACE(self):
        handler_name = self.routes.only_TRACE.get(self.path)
        self.run_handler(handler_name)

    def do_OPTIONS(self):
        handler_name = self.routes.only_OPTIONS.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_POST(self):
        '''
        Query exemple:
            INSERT INTO users (name, email, created_at, last_updated)
            VALUES ('Jane Doe', 'jane.doe@example.com', NOW(), NOW());
        '''
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_GET(self):
        handler_name = self.routes.only_GET.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_PUT(self):
        '''
        Query exemple:
            INSERT INTO users (user_id, name, email, created_at, last_updated)
            VALUES (42, 'John Doe', 'john.doe@example.com', NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email),
                last_updated = NOW();

        '''
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_PATCH(self):
        '''
        Query exemple:
            UPDATE users
            SET email = 'new_email@example.com',
                last_updated = NOW()
            WHERE user_id = 42;
        '''
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)
        # # Parse request body (JSON payload)
        # content_length = int(self.headers['Content-Length'])
        # patch_data = json.loads(self.rfile.read(content_length))

        # # Extract fields to update (e.g., "email")
        # email = patch_data.get("email")
        # user_id = self.get_user_id_from_url()  # Example function to parse user_id from URL

        # # Build and execute SQL query
        # if email:
        #     sql_query = "UPDATE users SET email = %s, last_updated = NOW() WHERE user_id = %s"
        #     params = (email, user_id)
        #     self.execute_sql(sql_query, params)  # Example function to execute SQL

        # # Send response
        # self.send_response(204)  # No content response for successful PATCH
        # self.end_headers()

    # @require_authentication
    def do_DELETE(self):
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)


# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=MasterHandler, port=8000):
    enableLog(LOG_DIR, "purePython")
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
