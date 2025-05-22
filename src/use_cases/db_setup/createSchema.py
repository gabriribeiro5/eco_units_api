from interfaces.handler import I_BaseHandler
from connectors.sync_pymysql import SyncronousPyMySQL
from utils.logger import log_running_and_done

class SchemaSetupHandler(I_BaseHandler):
    def __init__(self):
        self.db_conn = SyncronousPyMySQL()

    @log_running_and_done
    def schema_setup(self):
        self.db_conn.create_schema()
        self.db_conn.insert_into_index_tables()

        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = "\r\n"
    
        return status, headers, body
    