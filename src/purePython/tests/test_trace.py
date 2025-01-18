import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from pureAPI import MasterHandler

class Test_MasterHandler_TRACE(unittest.TestCase):
    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = MagicMock()
        self.mock_request.makefile = MagicMock(return_value=BytesIO())
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = MagicMock()
        self.mock_path_root = "/pureAPI"

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.send_error = MagicMock()
        self.handler.wfile = BytesIO()
        self.handler.headers = {"Content-Type": "message/http"}
        self.handler.request_version = "HTTP/1.0"
        self.handler.command = "unit test command"
        self.handler.requestline = "unit test requestline"
        
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
        
    def assert_response_contains(self):
        self.assertIn(f"{self.handler.path}".encode("utf-8"), self.handler.wfile.getvalue())
        self.assertIn(f"{self.handler.command}".encode("utf-8"), self.handler.wfile.getvalue())
        self.assertIn(f"{self.handler.requestline}".encode("utf-8"), self.handler.wfile.getvalue())
        self.assertIn(f"{self.handler.request_version}".encode("utf-8"), self.handler.wfile.getvalue())
        self.assertIn(f"\r\n".encode("utf-8"), self.handler.wfile.getvalue())

    def test_do_TRACE_should_return_requestline_and_content_type_msg(self):
        """
        Tests the TRACE HTTP method to ensure the response body contains
        the expected request line, protocol version, and content type.
        """
        # Mock route
        self.mock_routes("TRACE", "handle_trace")

        # expected values
        expected_header = ("Content-Type", "message/http")
        expected_body = (
            f"{self.handler.command} {self.handler.path} {self.handler.request_version}\n"
            f"{self.handler.requestline}\r\n".encode("utf-8")
        )

        # Trigger method
        self.handler.do_TRACE()

        # Assertions
        self.handler.send_response.assert_called_with(200)
        self.assert_response_contains()
        self.assertEqual(expected_body, self.handler.wfile.getvalue())
        # Verify the expected header was sent
        send_header_calls = [call.args for call in self.handler.send_header.call_args_list]
        self.assertIn(expected_header, send_header_calls)

    @patch("utils.logSetup.logging.info")
    def test_do_TRACE_logging(self, mock_logging):
        func_module = "trace" # define filename name
        handler_name = "handle_trace"
        self.mock_routes("TRACE", handler_name)
        self.handler.do_TRACE()
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): running")
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): done")

    @patch("utils.logSetup.logging.error")
    def test_do_TRACE_invalid_handler(self, mock_logging):
        """
        Ensures ValueError is raised for invalid TRACE handler.
        Ensures error is logged for invalid TRACE handler.
        """
        with self.assertRaises(ValueError):
            # define error condition
            handler_name = "nonexistent_test_handler"
            err_msg = f"Handler '{handler_name}' not found"
            self.mock_routes("TRACE", handler_name)

            # Trigger method
            self.handler.do_TRACE()

            # Verify the expected error parameters were sent
            mock_logging.assert_any_call(err_msg)
            send_error_calls = [call.args for call in self.handler.send_error.call_args_list]
            self.assertIn(404, send_error_calls)
            self.assertIn("Handler Not Found", send_error_calls)


    def tearDown(self):
        '''
        Reset shared mock data.
        The tearDown method is automatically invoked after each test in unittest.
        You don't need to call it explicitly.
        '''
        patch.stopall()  # Stop all patches started in setUp
        self.handler.wfile.close()  # Close BytesIO to release resources

if __name__ == "__main__":
    unittest.main()
