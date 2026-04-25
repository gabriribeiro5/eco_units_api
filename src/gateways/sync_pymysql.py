import pymysql # type: ignore
from interfaces.database.sync_connector import I_SyncDBConnector
from config import Definitions
from utils.logger import log_running_and_done
import logging

class SyncronousPyMySQL(I_SyncDBConnector):
    def __init__(self, *args, **kwargs) -> None:
        self.definitions = Definitions()
        super().__init__(*args, **kwargs)

    def _connect(self):
        connection = pymysql.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_SECRET,
            database=self.DB_NAME,
        )

        cursor = connection.cursor()
        return connection, cursor

    def _executeScript(self, sqlScript):
        # all SQL commands (split on ';')
        sqlCommands = sqlScript.split(';\n')
        connection, cursor = self._connect()

        # Execute every command from the input file
        for command in sqlCommands:
            try:
                cursor.execute(command)
            except pymysql.err.OperationalError as msg:
                logging.error(f"Failed running SQL command\n {command}\n {msg}")
                raise msg
    
    @log_running_and_done
    def create_schema(self):
        try:
            self._executeScript(self.script_schema_ecosystem_db)
        except Exception as e:
            logging.error(e)
            raise e

    @log_running_and_done
    def insert_into_index_tables(self):
        try:
            self._executeScript(self.script_insert_into_index_tables)
        except Exception as e:
            logging.error(e)
            raise e