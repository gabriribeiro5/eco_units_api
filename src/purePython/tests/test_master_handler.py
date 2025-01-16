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

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.request_version = "HTTP/1.1"
        self.handler.command = "unit test command"
        self.handler.headers = {"Content-Type": "message/http"}
        self.handler.requestline = ""
        self.handler.send_response = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.wfile = BytesIO()

    @patch("utils.logSetup.logging.info")
    def test_do_TRACE_should_return_request_line(self, mock_logging):
        # Mock path and routes
        self.handler.path = "/pureAPI"
        self.handler.options.only_TRACE = {"/pureAPI": {"method": "handle_trace"}}

        # Trigger the TRACE method
        self.handler.do_TRACE()
        
        # Check response
        request_line = f"{self.handler.command} {self.handler.path}".encode("utf-8") # expected string (encoded to binary format)
        self.handler.send_response.assert_called_with(200) # Was the send_response method called with the correct HTTP status code?
        self.assertIn(request_line, self.handler.wfile.getvalue()) # Does the wfile variable have the expected (binary) value?

    @patch("utils.logSetup.logging.info")
    def test_do_OPTIONS_should_return_api_options(self, mock_logging):
        # Mock path and routes
        self.handler.path = "/pureAPI"
        self.handler.options.only_OPTIONS = {"/pureAPI": {"method": "handle_options_for_unauthenticated_client"}}

        # Trigger the TRACE method
        self.handler.do_OPTIONS()

        # Check response
        request_line = b"OPTIONS" # expected string (encoded to binary format)
        self.handler.send_response.assert_called_with(200) # Was the send_response method called with the correct HTTP status code?
        self.assertIn(request_line, self.handler.wfile.getvalue()) # Does the wfile variable have the expected (binary) value?

if __name__ == "__main__":
    unittest.main()
