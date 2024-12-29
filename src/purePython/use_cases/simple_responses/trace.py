from entities.handler import I_BaseHandler
import logging
import inspect

class TraceHandler(I_BaseHandler):
    """
    Handles the TRACE HTTP method.
    TRACE is used for diagnostics.
    It simply returns a diagnostic trace that logs data from the request-response cycle
    Reflects the request back to the client as per the HTTP/1.1 specification.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    
    def handle_trace(self):
        """
        Returns the request back to the client. Useful for API diagnostics.
        """
        method_name = inspect.currentframe().f_code.co_name
        logging.info(f"({method_name}): running")

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
    
        logging.info(f"({method_name}): done")
        return status, headers, body