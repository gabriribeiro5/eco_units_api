from utils.config import Definitions
from utils.logger import log_running_and_done
import logging

class I_AsyncDBConnector():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.definitions = Definitions()
        self.DB_HOST = self.definitions.DB_HOST,
        self.DB_USER = self.definitions.DB_USER,
        self.DB_SECRET = self.definitions.DB_SECRET,
        self.DB_NAME = self.definitions.DB_NAME,
        
        self.script_schema_ecosystem_db = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_0_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_1_insert_into_index_tables.sql")
        self.script_insert_into_agent_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_2_insert_into_agent_tables.sql")
        self.script_insert_into_agent_input_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_3_insert_into_agent_input_tables.sql")

    @async_log_running_and_done
    async def _load_sql(self, filename):
        '''
        Open and read the file as a single buffer
        '''
        fd = open(filename, 'r')
        sqlScript = fd.read()
        fd.close()

        return sqlScript

    @async_log_running_and_done
    async def _executeScript(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    @async_log_running_and_done
    async def _connect():
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    @async_log_running_and_done
    async def create_schema(self):
        try:
            self._executeScript(self.script_schema_ecosystem_db)
        except Exception as e:
            logging.error(e)
            raise e

    @async_log_running_and_done
    async def insert_into_index_tables(self):
        try:
            self._executeScript(self.script_insert_into_index_tables)
        except Exception as e:
            logging.error(e)
            raise e