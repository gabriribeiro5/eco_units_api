from http.server import HTTPServer
from routes import RoutesManager as Routes
from out_of_process.auth import AuthManager as Auth
from use_cases.simple_responses.trace import TraceHandler as Trace
from use_cases.simple_responses.options import OptionsHandler as Options
from utils.definitions import LOG_DIR
from utils.logSetUp import LogSetUp
import logging

class MasterHandler(Auth, Routes, Trace, Options):
    def __init__(self, request, client_address, server):
        self.routes = Routes()
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
            handler()
        else:
            logging.error(f"handler {handler_name} not found")
            self.send_error(404, "Not Found")
    
    def do_TRACE(self):
        logging.info(f"(do_TRACE): activated by {self.client_address}")
        handler_name = self.routes.only_TRACE.get(self.path)
        self.run_handler(handler_name)

    def do_OPTIONS(self):
        logging.info(f"(do_OPTIONS): activated by {self.client_address}")
        handler_name = self.routes.only_OPTIONS.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_POST(self):
        '''
        Query exemple:
            INSERT INTO users (name, email, created_at, last_updated)
            VALUES ('Jane Doe', 'jane.doe@example.com', NOW(), NOW());
        '''
        logging.info(f"(do_POST): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_GET(self):
        logging.info(f"(do_GET): activated by {self.client_address}")
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
        logging.info(f"(do_PUT): activated by {self.client_address}")
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
        logging.info(f"(do_PATCH): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)

    # @require_authentication
    def do_DELETE(self):
        logging.info(f"(do_DELETE): activated by {self.client_address}")
        handler_name = self.routes.only_POST.get(self.path)
        self.run_handler(handler_name)

def test():
    logging.debug(f"Running MasterHandler tailored test...")
    mh = MasterHandler()
    mh.test()
    logging.debug(f"Ended MasterHandler tailored test...")
    


# Define e executa o servidor
def run(server_class=HTTPServer, handler_class=MasterHandler, port=8000):
    logger = LogSetUp()
    logger.enableLog(LOG_DIR, "purePython")
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info(f"Starting server on port {port}...")
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()