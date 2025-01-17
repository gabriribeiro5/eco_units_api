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
        self.mock_path_root = "/pureAPI"

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.request_version = "HTTP/1.1"
        self.handler.command = "unit test command"
        self.handler.requestline = "unit test requestline"
        self.handler.send_response = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.wfile = BytesIO()

    def mock_routes(self, method: str, handler: str, path: str = None):
        """
        Helper method to mock routes for different HTTP methods.
        
        Args:
            method (str): The HTTP method (e.g., "TRACE", "OPTIONS").
            handler (str): The method name to handle the route (e.g., "handle_trace").
        """
        self.handler.path = path or self.mock_path_root
        options_key = f"only_{method.upper()}"
        if hasattr(self.handler.options, options_key):
            getattr(self.handler.options, options_key)[self.handler.path] = {"method": handler}
        else:
            raise ValueError(f"Invalid method: {method}")

    def test_do_TRACE_should_return_requestline_and_content_type_msg(self):
        """
        Tests the TRACE HTTP method to ensure the response body contains
        the expected request line, protocol version, and content type.
        """
        # method mocks
        self.mock_routes("TRACE", "handle_trace")

        # expected values
        expected_header = {"Content-Type": "message/http"}

        expected_body = (
            f"{self.handler.command} {self.handler.path} {self.handler.protocol_version}\n"
            f"{self.handler.requestline}\r\n".encode("utf-8")
        )

        # run tested method
        self.handler.do_TRACE()
        
        # assertitions
        self.handler.send_header.assert_called_with(expected_header)
        self.handler.send_response.assert_called_with(200)
        self.assertIn(self.handler.command, self.handler.wfile.getvalue())
        self.assertIn(self.handler.path, self.handler.wfile.getvalue())
        self.assertIn(self.handler.protocol_version, self.handler.wfile.getvalue())
        self.assertIn(self.handler.requestline, self.handler.wfile.getvalue())
        self.assertIn(f"\r\n".encode("utf-8"), self.handler.wfile.getvalue())
        self.assertEqual(expected_body, self.handler.wfile.getvalue())

    def test_do_TRACE_invalid_handler(self):
        """
        Ensures ValueError is raised for invalid TRACE handler.
        """
        with self.assertRaises(ValueError):
            # define error condition
            self.mock_routes("TRACE", "handle_nonexistent")
            
            # run tested method
            self.handler.do_TRACE()



if __name__ == "__main__":
    unittest.main()
