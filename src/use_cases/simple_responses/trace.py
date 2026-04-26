from use_cases.shared.auth.auth import AuthHandler
from utils.logger import log_running_and_done
import logging
import functools

def require_authentication(func):
    """
    Decorator function that checks authentication before allowing the request.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_authenticated():
            self.send_error(401, "Unauthorized")
            return (401, {"Content-Type": "application/json"}, '{"error": "Unauthorized"}\r\n')
        return func(self, *args, **kwargs)
    return wrapper

class TraceHandler(AuthHandler):
    """
    Handles the TRACE HTTP method.
    TRACE is used for diagnostics.
    It simply returns a diagnostic trace that logs data from the request-response cycle
    Reflects the request back to the client as per the HTTP/1.1 specification.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def development_test(self):
        pass
    
    @require_authentication
    @log_running_and_done
    def handle_trace(self):
        """
        Returns the request back to the client. Useful for API health check.
        """        
        # try: # Call external microsservice, if exists
        #     expected_data = self.client.external_call(self.command,
        #                                         self.path,
        #                                         self.request_version,
        #                                         self.headers.items(),
        #                                         data_type = "dict")
        #     if expected_data:
        #         response_line = expected_data["request_line"]
        #         header_lines = expected_data["header_lines"]
        #     else:
        #         raise ValueError("External call incomplete.")
        # except ValueError as e: # Apply business rules
        #     # Log message
        #     logging.info(f'''{e} Running internal Business Logic.''')
        #     # Construct response components
        #     response_line = f'''{self.requestline}'''
        #     header_lines = self.headers
        header_lines = self.headers

        # Generate response variables
        status = 200
        headers = header_lines
        body = f'''~{self.requestline}\r\n'''
    
        return status, headers, body
    