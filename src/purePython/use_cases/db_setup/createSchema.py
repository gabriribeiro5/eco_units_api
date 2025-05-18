from interfaces.handler import I_BaseHandler
from connectors.async_aiomysql import AsyncronousAIOMySQL
from utils.logger import async_log_running_and_done

class SchemaSetupHandler(I_BaseHandler):
    def __init__(self):
        self.async_db_conn = AsyncronousAIOMySQL()

    @async_log_running_and_done
    async def schema_setup(self):
        self.async_db_conn.create_schema()
        self.async_db_conn.insert_into_index_tables()

        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = "\r\n"
    
        return status, headers, body
    