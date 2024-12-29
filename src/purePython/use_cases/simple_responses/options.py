from entities.handler import I_BaseHandler
import logging
import inspect

class OptionsHandler(I_BaseHandler):
    """/
    Handles the OPTIONS HTTP method.
    OPTIONS is used to describe the communication options for the target resource.
        It helps the client understand what methods and headers are allowed
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def development_test(self):
        self.method_start()

    def log_running_and_done(self, func):
        def wrapper(*args, **kwargs):
            logging.info(f"({func.__name__}): running")
            status, headers, body = func(*args, **kwargs)  # Call the decorated method
            logging.info(f"({func.__name__}): done")
            return status, headers, body
        return wrapper
    
    @log_running_and_done
    def handle_options_for_unauthenticated_client(self, agent_type: tuple):
        '''
        agent_type: ecounit, customer, backuser or backuser_admin
        '''
        # Collect options

        # Construct response components
        request_line = f'''
                        Successfull trace.
                        Here is your request:
                        {self.command} {self.path} {self.protocol_version}'''
        header_lines = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "message/http"}
        body = request_line + header_lines + "\r\n"
    
        return status, headers, body

def test():
    handler = OptionsHandler()
    handler.development_test()

if __name__ == "__main__":
    test()