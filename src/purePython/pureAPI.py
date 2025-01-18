from http.server import HTTPServer
from out_of_process.auth import AuthManager as Auth
from use_cases.simple_responses.trace import TraceHandler as Trace
from use_cases.simple_responses.options import OptionsHandler as Options
from utils.definitions import Definitions
from utils.logSetup import LogSetup
import logging

class MasterHandler(Auth, Trace, Options):
    def __init__(self, request, client_address, server):
        # set protocol_version to HTTP/1.1 to enable automatic keepalive
        self.protocol_version = "HTTP/1.1"
        super().__init__(request, client_address, server)

    def test(self):
        pass
    
    def require_authentication(self):
        if not self.is_authenticated(self):
            self.send_error(401, "Unauthorized")
            return

    def run_handler(self, handler_name, *args, **kwargs):
        logging.info(f"calling handler: {handler_name}")
        if handler_name and hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            response_data = handler(*args, **kwargs)  # Call handler and get response data
            return response_data
        else:
            err_msg = f"Handler '{handler_name}' not found"
            logging.error(err_msg)
            self.send_error(404, "Handler Not Found")
            raise ValueError(err_msg)
    
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
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_TRACE.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

    def do_OPTIONS(self):
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_OPTIONS.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

    # @require_authentication
    def do_POST(self):
        '''
        Query exemple:
            INSERT INTO users (name, email, created_at, last_updated)
            VALUES ('Jane Doe', 'jane.doe@example.com', NOW(), NOW());
        '''
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_POST.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

    # @require_authentication
    def do_GET(self):
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_GET.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

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
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_POST.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

    # @require_authentication
    def do_PATCH(self):
        '''
        Query exemple:
            UPDATE users
            SET email = 'new_email@example.com',
                last_updated = NOW()
            WHERE user_id = 42;
        '''
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_POST.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

    # @require_authentication
    def do_DELETE(self):
        logging.info(f"method activated by {self.client_address}")
        handler_name = self.options.only_POST.get(self.path).get("method")
        if isinstance(handler_name, str):  # Ensure it is a string
            response_data = self.run_handler(handler_name)
            self.format_and_send(response_data)
        else:
            logging.error(f"Invalid handler name: {handler_name}")
            self.send_error(500, "Internal Server Error")

def test():
    logging.debug(f"Running MasterHandler tailored test...")
    mh = MasterHandler()
    mh.test()
    logging.debug(f"Ended MasterHandler tailored test...")
    


# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=MasterHandler, port=8080):
    logger = LogSetup()
    definitions = Definitions()
    logger.enableLog(definitions.LOG_DIR, definitions.LOG_FILE_NAME)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()