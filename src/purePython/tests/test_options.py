import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from pureAPI import MasterHandler

class TestMasterHandler(unittest.TestCase):
    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = MagicMock()
        self.mock_request.makefile = MagicMock(return_value=BytesIO())
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = MagicMock()
        self.mock_headers_content_type_msg = {"Content-Type": "message/http"}
        self.mock_headers_content_type_json = {"Content-Type": "application/json"}
        self.mock_path_root = "/pureAPI"

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.request_version = "HTTP/1.1"
        self.handler.command = "unit test command"
        self.handler.requestline = "unit test requestline"
        self.handler.send_response = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.wfile = BytesIO()

    def mock_routes(self, method: str, handler: str):
        """
        Helper method to mock routes for different HTTP methods.
        
        Args:
            method (str): The HTTP method (e.g., "TRACE", "OPTIONS").
            handler (str): The method name to handle the route (e.g., "handle_trace").
        """
        options_key = f"only_{method.upper()}"
        if hasattr(self.handler.options, options_key):
            getattr(self.handler.options, options_key)[self.handler.path] = {"method": handler}
        else:
            raise ValueError(f"Invalid method: {method}")

    def test_do_OPTIONS_should_return_api_options(self):
        self.handler.path = self.mock_path_root
        self.mock_routes("OPTIONS", f"{self.handler.path}", "handle_options_for_unauthenticated_client")

        self.handler.do_OPTIONS()

        self.handler.send_response.assert_called_with(200)
        self.assertIn(b"OPTIONS", self.handler.wfile.getvalue())

if __name__ == "__main__":
    unittest.main()
