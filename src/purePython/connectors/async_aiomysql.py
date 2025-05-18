import aiomysql #type: ignore
from interfaces.database.async_connector import I_AsyncDBConnector
from utils.logger import async_log_running_and_done
import logging

class AsyncronousAIOMySQL(I_AsyncDBConnector):
    async def __init__(self, *args, **kwargs) -> None:
        self.pool = await self._connect()
        super().__init__(*args, **kwargs)

    @async_log_running_and_done
    async def _connect(self):
        connection_pool = await aiomysql.create_pool(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            db=self.DB_NAME,
            minsize=1,
            maxsize=self.num_batches,
            echo=True,
        )

        return connection_pool

    @async_log_running_and_done
    async def _executeScript(self, pool:isinstance, sqlScript, allowMultipleConnections=True):
        # all SQL commands (split on ';')
        sqlCommands = sqlScript.split(';')

        if allowMultipleConnections:
            # Execute every command from the input file creating a connection for each
            for command in sqlCommands:
                try:
                    async with pool.acquire() as connection:
                        async with connection.cursor() as cursor:
                            # Drop the table if it exists and create it again
                            await cursor.execute(command)
                            await cursor.execute(command)
                            await connection.commit()
                except aiomysql.err.OperationalError as msg:
                    logging.error(f"Failed running SQL command\n {msg}")
                    raise msg
        else:
            # Create one connection to run the entire script
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    for command in sqlCommands:
                        try:
                            # Drop the table if it exists and create it again
                            await cursor.execute(command)
                            await cursor.execute(command)
                            await connection.commit()
                        except aiomysql.err.OperationalError as msg:
                            logging.error(f"Failed running SQL command\n {msg}")
                            raise msg
    
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