import pymysql
from database import I_BaseDB
from utils.config import Definitions

class I_SyncronousPyMySQL(I_BaseDB):
    def __init__(self, *args, **kwargs) -> None:
        self.definitions = Definitions()
        self.DB_HOST = self.definitions.DB_HOST,
        self.DB_USER = self.definitions.DB_USER,
        self.DB_SECRET = self.definitions.DB_SECRET,
        self.DB_NAME = self.definitions.DB_NAME,
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
        sqlCommands = sqlScript.split(';')
        connection, cursor = self._connect()

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                cursor.execute(command)
            except pymysql.err.OperationalError as msg:
                print("Command skipped: ", msg)
    
