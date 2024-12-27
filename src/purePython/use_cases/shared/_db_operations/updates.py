from purePython.entities.handler import I_BaseHandler
import json
import warnings

"""
This module provides internal shared database operations (e.g., insert, select, update).  
It is meant to be used only by use cases within 'use_cases/'.  
External services or modules should NOT directly access this module.  
"""

class DeleteHandler(I_BaseHandler):

    # Handlers para as rotas
    def handle_delete_some_data(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"data": self.data_store}
        self.wfile.write(json.dumps(response).encode())
    
# raise warnings if db_operations is accessed outside of the intended scope
if __name__ != "__main__" and "use_cases" not in __file__:  
    warnings.warn("Direct access to db_operations is not allowed.")