from utils.config import Definitions
from utils.logger import log_running_and_done
import logging

class I_SyncDBConnector():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Definitions()
        self.DB_HOST = self.config.DB_HOST
        self.DB_PORT = self.config.DB_PORT
        self.DB_USER = self.config.DB_USER
        self.DB_SECRET = self.config.DB_SECRET
        self.DB_NAME = self.config.DB_NAME
        
        logging.info("loading db scripts")
        self.script_schema_ecosystem_db = self._load_sql(self.config._DB_SCRIPTS_DIR / "_0_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_insert_into_index_tables.sql")
        self.script_insert_into_agent_tables = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_insert_into_agent_tables.sql")
        self.script_insert_into_agent_input_tables = self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_insert_into_agent_input_tables.sql")

    def _load_sql(self, filename):
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

    def _executeScript(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    def _connect():
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    def create_schema(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    def insert_into_index_tables(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()