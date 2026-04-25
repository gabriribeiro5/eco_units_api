from http.server import BaseHTTPRequestHandler
from utils.heisenberg import WalterWhite
from config import Definitions
from urllib.parse import parse_qs
import logging
import json


class I_BaseHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.inspector = WalterWhite()
        self.definitions = Definitions()
        super().__init__(request, client_address, server)

    def get_request_data(self):
        # Find out device_id from request body, default to "all" if not provided or invalid
        content_length = int(self.headers.get("Content-Length", 0))
        request_body = self.rfile.read(content_length).decode('utf-8') if content_length else ""
        
        try:
            request_body = request_body.strip()  # Remove leading/trailing whitespace            
            # Try parsing as JSON first, then fall back to form data
            if request_body:
                try:
                    request_data = json.loads(request_body)
                except json.JSONDecodeError:
                    # Parse as URL-encoded form data
                    parsed = parse_qs(request_body)
                    request_data = {k: v[0] if v else "" for k, v in parsed.items()}
            else:
                request_data = {}    
        except Exception as e:
            logging.exception(f"Failed to decode request body: {request_body}\nException: {str(e)}")
        
        return request_data