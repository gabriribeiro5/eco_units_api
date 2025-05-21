import aiomysql #type: ignore
from interfaces.database.async_connector import I_AsyncDBConnector
from utils.logger import async_log_running_and_done
import logging

class AsyncronousAIOMySQL(I_AsyncDBConnector):
    def __init__(self, *args, **kwargs) -> None:
        self.pool = None
        super().__init__(*args, **kwargs)

    async def initialize(self):
        '''
        This method resolves ``TypeError: __init__() should return None, not 'coroutine'``
        when async class is instantiated
        '''
        self.pool = await self._connect()
        await self.initialize_async_db_connector()

    @async_log_running_and_done
    async def _connect(self):
        connection_pool = await aiomysql.create_pool(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_SECRET,
            db=self.DB_NAME,
            minsize=1,
            maxsize=self.NUM_BATCHES,
            echo=True
        )

        return connection_pool

    @async_log_running_and_done
    async def _executeScript(self, pool:isinstance, sqlScript, allowMultipleConnections=True):
        # all SQL commands (split on ';')
        sqlCommands = sqlScript.split(';\n')

        if allowMultipleConnections:
            # Execute every command from the input file creating a connection for each
            for command in sqlCommands:
                try:
                    async with pool.acquire() as connection:
                        async with connection.cursor() as cursor:
                            await cursor.execute(command)
                            await connection.commit()
                except aiomysql.Error as msg:
                    logging.error(f"Failed running SQL command:\n {command} \n=====\n {msg}")
                    raise msg
        else:
            # Create one connection to run the entire script
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    for command in sqlCommands:
                        try:
                            await cursor.execute(command)
                            await connection.commit()
                        except aiomysql.Error as msg:
                            logging.error(f"Failed running SQL command:\n {command} \n=====\n {msg}")
                            raise msg
    
    @async_log_running_and_done
    async def create_schema(self):
        try:
            await self._executeScript(self.pool, self.script_schema_ecosystem_db)
        except Exception as e:
            logging.error(e)
            raise e

    @async_log_running_and_done
    async def insert_into_index_tables(self):
        try:
            await self._executeScript(self.pool, self.script_insert_into_index_tables)
        except Exception as e:
            logging.error(e)
            raise e