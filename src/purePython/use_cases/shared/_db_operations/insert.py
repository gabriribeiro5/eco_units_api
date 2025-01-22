from interfaces.handler import I_BaseHandler
import json
import warnings
import logging

"""
This module provides internal shared database operations (e.g., insert, select, update).  
It is meant to be used only by use cases within 'use_cases/'.  
External services or modules should NOT directly access this module.  
"""

class IndexTables(I_BaseHandler):
    '''
    index tables are:
    - sensor_status
    - config_status
    - climate_season
    - ecosystem_category
    '''
    # Handlers para as rotas
    def insert_into_sensor_status(self):
        table_name = "sensor_status"
        
        # build response data
        status = 200
        headers = {"Content-Type": "application/json"}
        body = {}
        
        # Stablish DB connection
        try:
            pass
        except Exception as e:
            status = 500
            msg = f"Failed stablishing database connection"
            msg_exception = f"Exception: {str(e)}"
            logging.exception(f"({self.inspector.say_my_name()}): {msg}\n{msg_exception} ")
            self.send_error(500, msg)

        # Run insert
        try:
            pass
        except Exception as e:
            status = 500
            msg = f"Error while inserting data"
            msg_exception = f"Exception: {str(e)}"
            logging.exception(f"({self.inspector.say_my_name()}): {msg}\n{msg_exception} ")
            self.send_error(500, msg)

        return status, headers, body

class AgentTables(I_BaseHandler):

    # Handlers para as rotas
    def handle_delete_some_data(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"data": self.data_store}
        self.wfile.write(json.dumps(response).encode())

class AgentInputTables(I_BaseHandler):

    # Handlers para as rotas
    def handle_post_unit_configurations(self,
                                        unit_ids: list = None,
                                        evironment_category: list = None,
                                        customer_id: list = None,
                                        unit_location: list = None):
        pass

# raise warnings if db_operations is accessed outside of the intended scope
if __name__ != "__main__" and "use_cases" not in __file__:  
    warnings.warn("Direct access to db_operations is not allowed.")