import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from controllers.sync_controller import MasterHandler
from use_cases.shared._db_operations.insert import IndexTables, AgentTables, AgentInputTables

class Test_Insert_into_Index_Tables(unittest.TestCase):
    '''
    Tests the insert methods for Index Tables to ensure they complete the expected tasks

    Index tables:
    - component_status
    - config_status
    - climate_season
    - device_strategy
    '''
    #######################################
    ### METHODS TO SUPPORT UNIT TESTING ###
    #######################################
    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = MagicMock()
        self.mock_request_file = b"POST / HTTP/1.1\r\n\r\n"
        self.mock_request.makefile = MagicMock(return_value=BytesIO(self.mock_request_file))  # Simulating a valid HTTP request
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = MagicMock()

        # Create DB Operation instance
        self.db_operation = IndexTables(self.mock_request, self.mock_client_address, self.mock_server)
        self.db_operation.rfile = BytesIO(self.mock_request_file)  # Simulating an HTTP request stream
        self.db_operation.wfile = BytesIO()  # Mock writable output stream
        self.db_operation.send_error = MagicMock()
        
        self.component_status_data = {
            "valid_field": "value",
            "valid_field2": "value2"
        }
        
        
    ##############################
    ### ACTUAL TESTING METHODS ###
    ##############################
    def test_Insert_into_Index_Table_should_return_status_200(self):
        # expected values
        expected_headers = {"Content-Type": "application/json"}

        # Trigger method
        status, headers, body = self.db_operation.insert_into_component_status(self.component_status_data)

        # Assertions
        self.assertEqual(status, 200)
        self.assertEqual(headers, expected_headers)
        self.assertEqual(body, {})

    @patch("utils.logger.logging.info")
    def test_Inserts_into_Index_Tables_basic_logging(self, mock_logging):
        func_module = "insert" # define filename name
        handler_name = "insert_into_component_status"
        # Trigger method
        status, headers, body = self.db_operation.insert_into_component_status(self.component_status_data)
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): running")
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): done")

    @patch("utils.logger.logging.error")
    def test_Inserts_into_Index_Tables_returns_422_invalid_data(self, mock_logging):
        """
        Ensures ValueError is raised for invalid data.
        Ensures error is logged for invalid data.
        """
        # logging variables
        func_module = "insert" # define filename name
        handler_name = "create_query"
        
        # define error condition
        self.component_status_data = {"test_unexistent_field": "unexistent_value"}
        msg_err = f"Invalid data"
        with self.assertRaises(KeyError):
            # Trigger method
            status, headers, body = self.db_operation.insert_into_component_status(self.component_status_data)

            # Verify the expected error parameters were sent to send_error
            send_error_calls = [call.args for call in self.db_operation.send_error.call_args_list]
            self.assertIn((422, msg_err), send_error_calls)

            # Verify the expected error parameters were sent to logging
            logging_calls = [call.args for call in mock_logging.call_args_list]
            logging_args = []
            for args in logging_calls:
                logging_args = logging_args + [arg for arg in args]
            self.assertIn(msg_err, logging_args)


    #########################################
    ### UNITTEST AUTOMATIC CLEANUP METHOD ###
    #########################################
    def tearDown(self):
        '''
        Reset shared mock data.
        The tearDown method is automatically invoked after each test in unittest.
        You don't need to call it explicitly.
        '''
        patch.stopall()  # Stop all patches started in setUp
        self.db_operation.wfile.close()  # Close BytesIO to release resources

if __name__ == "__main__":
    unittest.main()
