from http.server import HTTPServer
from route_options import OptionsManager as RouteOptions
from out_of_process.auth import AuthManager as Auth
from use_cases.simple_responses.trace import TraceHandler as Trace
from use_cases.simple_responses.options import OptionsHandler as Options
from utils.definitions import LOG_DIR
from utils.logSetUp import LogSetUp
import logging

class MasterHandler(Auth, RouteOptions, Trace, Options):
    def __init__(self, request, client_address, server):
        self.routes = RouteOptions()
        super().__init__(request, client_address, server)

    def test(self):
        pass
    
    def require_authentication(self):
        if not self.is_authenticated(self):
            self.send_error(401, "Unauthorized")
            return

    def run_handler(self, handler_name):
        logging.info(f"calling handler: {handler_name}")
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            response_data = handler()  # Call handler and get response data
            return response_data
        else:
            logging.error(f"handler {handler_name} not found")
            self.send_error(404, "Not Found")
    
    def format_and_send(self, response_data):
        logging.info(f"formating and sending response")
        status, headers, body = response_data
        self.send_response(status)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
        if body:
            self.wfile.write(body.encode("utf-8"))
    
    def do_TRACE(self):
        logging.info(f"(do_TRACE): activated by {self.client_address}")
        handler_name = self.routes.only_TRACE.get(self.path).get("method")
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

    def do_OPTIONS(self):
        logging.info(f"(do_OPTIONS): activated by {self.client_address}")
        handler_name = self.routes.only_OPTIONS.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

    # @require_authentication
    def do_POST(self):
        '''
        Query exemple:
            INSERT INTO users (name, email, created_at, last_updated)
            VALUES ('Jane Doe', 'jane.doe@example.com', NOW(), NOW());
        '''
        logging.info(f"(do_POST): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

    # @require_authentication
    def do_GET(self):
        logging.info(f"(do_GET): activated by {self.client_address}")
        handler_name = self.routes.only_GET.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

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
        logging.info(f"(do_PUT): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

    # @require_authentication
    def do_PATCH(self):
        '''
        Query exemple:
            UPDATE users
            SET email = 'new_email@example.com',
                last_updated = NOW()
            WHERE user_id = 42;
        '''
        logging.info(f"(do_PATCH): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

    # @require_authentication
    def do_DELETE(self):
        logging.info(f"(do_DELETE): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        response_data = self.run_handler(handler_name)
        self.format_and_send(response_data)

def test():
    logging.debug(f"Running MasterHandler tailored test...")
    mh = MasterHandler()
    mh.test()
    logging.debug(f"Ended MasterHandler tailored test...")
    


# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=MasterHandler, port=8080):
    logger = LogSetUp()
    logger.enableLog(LOG_DIR, "purePython")
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()