import aiomysql
from interfaces.database.async_connector import I_AsyncDBConnector
from utils.config import Definitions
import logging

class AsyncronousAIOMySQL(I_AsyncDBConnectorr):
    def __init__(self, *args, **kwargs) -> None:
        self.definitions = Definitions()
        super().__init__(*args, **kwargs)

    @async_log_running_and_done
    async def _connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            db=self.DB_NAME,
            minsize=1,
            maxsize=self.num_batches,
            echo=True,
        )

        cursor = connection.cursor()
        return connection, cursor

    @async_log_running_and_done
    async def _executeScript(self, sqlScript):
        # all SQL commands (split on ';')
        sqlCommands = sqlScript.split(';')
        connection, cursor = self._connect()

        # Execute every command from the input file
        for command in sqlCommands:
            try:
                cursor.execute(command)
            except pymysql.err.OperationalError as msg:
                logging.error(f"Failed running SQL command\n {msg}")
                raise msg
    
