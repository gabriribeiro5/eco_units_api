from interfaces.handler import I_BaseHandler
from interfaces.client import I_BaseClient
from utils.logSetup import log_running_and_done
import logging

class TraceHandler(I_BaseHandler, I_BaseClient):
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
    
    @log_running_and_done
    def handle_trace(self):
        """
        Returns the request back to the client. Useful for API health check.
        """        
        try: # Call external microsservice, if exists
            expected_data = self.external_call(self.command,
                                                self.path,
                                                self.protocol_version,
                                                self.headers.items(),
                                                data_type = "dict")
            if expected_data:
                request_line = expected_data["request_line"]
                header_lines = expected_data["header_lines"]
            else:
                raise ValueError("External call incomplete.")
        except ValueError as e: # Apply business rules
            # Log message
            logging.info(f'''({e} Running internal Business Logic.''')
            # Construct response components
            request_line = f'''{self.command} {self.path} {self.protocol_version}'''
            header_lines = self.headers

        # Generate response variables
        status = 200
        headers = header_lines
        body = request_line + "\r\n"
    
        return status, headers, body
    