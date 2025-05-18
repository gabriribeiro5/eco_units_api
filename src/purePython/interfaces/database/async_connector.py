from utils.config import Definitions
import logging

class I_AsyncDBConnector():
    async def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.definitions = Definitions()
        self.DB_HOST = self.definitions.DB_HOST,
        self.DB_USER = self.definitions.DB_USER,
        self.DB_SECRET = self.definitions.DB_SECRET,
        self.DB_NAME = self.definitions.DB_NAME,
        
        logging.info("loading db scripts")
        self.script_schema_ecosystem_db = await self._load_sql(self.config._DB_SCRIPTS_DIR / "_0_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = await self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_insert_into_index_tables.sql")
        self.script_insert_into_agent_tables = await self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_insert_into_agent_tables.sql")
        self.script_insert_into_agent_input_tables = await self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_insert_into_agent_input_tables.sql")

    async def _load_sql(self, filename):
        '''
        Open and read the file as a single buffer
        '''
        try:
            fd = open(filename, 'r')
            sqlScript = fd.read()
            fd.close()
        except Exception as e:
            logging.error(f"failed loading {filename}:\n {e}")

        return sqlScript

    async def _executeScript(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    async def _connect():
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    async def create_schema(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    async def insert_into_index_tables(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()