import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from pureAPI import MasterHandler
from use_cases.shared._db_operations.insert import IndexTables, AgentTables, AgentInputTables

class Test_Insert_into_Index_Tables(unittest.TestCase):
    '''
    Tests the insert methods for Index Tables to ensure they complete the expected tasks

    Index tables:
    - sensor_status
    - config_status
    - climate_season
    - ecosystem_category
    '''
    #######################################
    ### METHODS TO SUPPORT UNIT TESTING ###
    #######################################
    def setUp(self):
        # Mock request, client_address, and server
        self.mock_request = MagicMock()
        self.mock_request.makefile = MagicMock(return_value=BytesIO())
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = MagicMock()

        # Create a MasterHandler instance
        self.handler = MasterHandler(self.mock_request, self.mock_client_address, self.mock_server)
        self.handler.send_error = MagicMock()
        self.handler.wfile = BytesIO()
        self.handler.rfile = BytesIO()

        # Create DB Operation instance
        self.db_operation = IndexTables(self.mock_request, self.mock_client_address, self.mock_server)
        self.db_operation.send_error = MagicMock()
        self.db_operation.wfile = BytesIO()
        
        
    ##############################
    ### ACTUAL TESTING METHODS ###
    ##############################
    def test_Insert_into_Index_Table_should_return_status_200(self):
        # expected values
        expected_headers = {"Content-Type": "application/json"}

        # Trigger method
        status, headers, body = self.db_operation.insert_into_sensor_status(self.sensor_status_data)

        # Assertions
        self.assertEqual(status, 200)
        self.assertEqual(headers, expected_headers)
        self.assertEqual(body, {})

    @patch("utils.logSetup.logging.info")
    def test_Inserts_into_Index_Tables_basic_logging(self, mock_logging):
        func_module = "insert" # define filename name
        handler_name = "insert_into_sensor_status"
        # Trigger method
        status, headers, body = self.db_operation.insert_into_sensor_status(self.sensor_status_data)
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): running")
        mock_logging.assert_any_call(f"{func_module} - ({handler_name}): done")

    @patch("utils.logSetup.logging.error")
    def test_Inserts_into_Index_Tables_returns_422_invalid_data(self, mock_logging):
        """
        Ensures ValueError is raised for invalid data.
        Ensures error is logged for invalid data.
        """
        with self.assertRaises(ValueError):
            # define error condition
            self.sensor_status_data = {"test_unexistent_field": "unexistent_value"}
            err_msg = f"Invalid data"
            # self.mock_routes("POST", "insert_into_sensor_status")

            # Trigger method
            status, headers, body = self.db_operation.insert_into_sensor_status(self.sensor_status_data)

            # Verify the expected error parameters were sent
            mock_logging.assert_any_call(err_msg)
            send_error_calls = [call.args for call in self.handler.send_error.call_args_list]
            self.assertIn(422, send_error_calls)
            self.assertIn(err_msg, send_error_calls)


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
        self.handler.wfile.close()  # Close BytesIO to release resources

if __name__ == "__main__":
    unittest.main()
