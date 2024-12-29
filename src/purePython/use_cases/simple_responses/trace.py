from entities.handler import I_BaseHandler
import logging

class TraceHandler(I_BaseHandler):
    """
    Handles the TRACE HTTP method.
    Reflects the request back to the client as per the HTTP/1.1 specification.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    
    def handle_trace(self):
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