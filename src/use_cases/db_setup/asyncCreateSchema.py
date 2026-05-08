from interfaces.handler import I_BaseHandler
from gateways.async_aiomysql import AsyncronousAIOMySQL
from utils.logger import async_log_running_and_done

class SchemaSetupHandler(I_BaseHandler):
    def __init__(self):
        self.async_db_conn = None

    async def initialize(self):
        '''
        This method resolves ``TypeError: __init__() should return None, not 'coroutine'``
        when async class is instantiated
        '''
        self.async_db_conn = AsyncronousAIOMySQL()
        await self.async_db_conn.initialize()

    @async_log_running_and_done
    async def schema_setup(self):
        await self.async_db_conn.create_schema()
        await self.async_db_conn.insert_into_index_tables()

        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = "\r\n"
    
        return status, headers, body
    