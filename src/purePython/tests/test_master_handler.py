import unittest
from unittest.mock import MagicMock
from io import BytesIO
from pureAPI import MasterHandler

class TestMasterHandler(unittest.TestCase):

    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = BytesIO()
        self.mock_client_address = ('127.0.0.1', 8000)
        self.mock_server = MagicMock()

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.send_response = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.wfile = BytesIO()

    def test_do_trace(self):
        # Mock path and routes
        self.handler.path = "/test"
        self.handler.routes.only_TRACE = {"/test": "do_TRACE"}

        # Trigger the TRACE method
        self.handler.do_TRACE()

        # Check response
        self.handler.send_response.assert_called_with(200)
        self.assertIn(b"TRACE", self.handler.wfile.getvalue())

if __name__ == "__main__":
    unittest.main()
