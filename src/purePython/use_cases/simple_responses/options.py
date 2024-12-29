from entities.handler import I_BaseHandler
import logging

class OptionsHandler(I_BaseHandler):
    """/
    Handles the OPTIONS HTTP method.
    OPTIONS is used to describe the communication options for the target resource.
        It helps the client understand what methods and headers are allowed
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        

    def handle_options(self):
        logging.info(f"(handle_trace): running")
    
        # Construct the response components
        status = 200
        headers = {"Content-Type": "message/http"}
        request_line = f'''
                        Successfull trace.
                        Here is your request:
                        {self.command} {self.path} {self.protocol_version}'''
        header_lines = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        body = request_line + header_lines + "\r\n"
    
        logging.info(f"(handle_trace): done")
        return status, headers, body