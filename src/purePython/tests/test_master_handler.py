import unittest
from unittest.mock import MagicMock
from io import BytesIO
from pureAPI import MasterHandler

class TestMasterHandler(unittest.TestCase):

    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = MagicMock()
        self.mock_request.makefile = MagicMock(return_value=BytesIO())
        self.mock_client_address = ('127.0.0.1', 8000)
        self.mock_server = MagicMock()

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.request_version = "HTTP/1.1"
        self.handler.command = "UNIT TEST"
        self.handler.headers = {"Content-Type": "message/http"}
        self.handler.requestline = ""
        self.handler.send_response = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.wfile = BytesIO()

    def test_do_trace(self):
        # Mock path and routes
        self.handler.path = "/pureAPI"
        self.handler.routes.only_TRACE = {"/pureAPI": "handle_trace"}

        # Trigger the TRACE method
        self.handler.do_TRACE()

        # Check response
        self.handler.send_response.assert_called_with(200)
        self.assertIn(b"UNIT TEST", self.handler.wfile.getvalue())

if __name__ == "__main__":
    unittest.main()
