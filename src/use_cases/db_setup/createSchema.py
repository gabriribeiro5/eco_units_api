from interfaces.database.db_scripts import I_DBScriptSource
from gateways.sync_pymysql import SyncronousPyMySQL
from utils.logger import log_running_and_done
import logging

class SchemaSetupHandler(I_DBScriptSource):
    def __init__(self, *args, **kwargs) -> None:
        self.db_conn = SyncronousPyMySQL()
        super().__init__(*args, **kwargs)

    @log_running_and_done
    def create_schema(self):
        try:
            self.db_conn.run_script(self.script_schema_ecosystem_db)
        except Exception as e:
            logging.error(e)
            raise e
    @log_running_and_done
    def insert_into_index_tables(self):
        try:
            self.db_conn.run_script(self.script_insert_into_index_tables)
        except Exception as e:
            logging.error(e)
            raise e
        
    @log_running_and_done
    def schema_setup(self):
        lock_acquired = self.db_conn.acquire_lock('cyclobot_db_setup', 10)
        if lock_acquired:
            try:
                self.create_schema()
                self.insert_into_index_tables()
            finally:
                self.db_conn.release_lock('cyclobot_db_setup')
        else:
            logging.info("DB setup lock not acquired; assuming setup is in progress or completed by another instance")

        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = "\r\n"
    
        return status, headers, body
    