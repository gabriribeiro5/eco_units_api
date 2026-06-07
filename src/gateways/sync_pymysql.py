import time
import pymysql # type: ignore
from interfaces.database.sync_connector import I_SyncDBConnector
from utils.logger import log_running_and_done
import logging

class SyncronousPyMySQL(I_SyncDBConnector):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def connect(self):
        connection = pymysql.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_SECRET,
            database=self.DB_NAME,
        )

        cursor = connection.cursor()
        return connection, cursor

    def run_script(self, sqlScript, *args, **kwargs):
        # All SQL commands (split on ;\n while preserving multiline statements)
        sqlCommands = [command.strip() for command in sqlScript.split(';\n') if command.strip()]
        attempts = 0
        max_attempts = kwargs.pop('max_attempts', 3)

        if len(args) == 1 and not isinstance(args[0], (tuple, list, dict)):
            params = (args[0],)
        else:
            params = args if args else None

        while True:
            connection = None
            try:
                connection, cursor = self.connect()

                # Execute every command from the input file
                for command in sqlCommands:
                    if params is not None:
                        cursor.execute(command, params)
                    else:
                        cursor.execute(command)
                    connection.commit()

                connection.close()
                return
            except pymysql.err.OperationalError as msg:
                if connection is not None:
                    connection.rollback()
                    connection.close()

                error_code = msg.args[0] if isinstance(msg.args, tuple) else None
                if error_code == 1213 and attempts < max_attempts:
                    attempts += 1
                    logging.warning(f"Deadlock detected, retrying script (attempt {attempts}/{max_attempts})")
                    time.sleep(0.5)
                    continue

                logging.error(f"Failed running SQL script after {attempts + 1} attempt(s)\n {msg}")
                raise msg
            

    def run_query(self, sqlQuery, *args, **kwargs):
        connection, cursor = self.connect()

        if len(args) == 1 and not isinstance(args[0], (tuple, list, dict)):
            params = (args[0],)
        else:
            params = args if args else None

        # Execute the query
        try:
            if params is not None:
                cursor.execute(sqlQuery, params)
            else:
                cursor.execute(sqlQuery)
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {sqlQuery}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        results = cursor.fetchall()

        # Normalize results to a list of dictionaries using cursor.description
        try:
            if results and isinstance(results[0], tuple):
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in results]
        except Exception:
            # If any issue occurs during normalization, fall back to raw results
            pass

        connection.commit()
        connection.close()
        return results

    def acquire_lock(self, lock_name, timeout=5):
        """Acquire a named lock. Returns True if acquired, False otherwise."""
        try:
            result = self.run_query(f"SELECT GET_LOCK('{lock_name}', {timeout})")
            if not result:
                return False
            # result[0] is expected to be a dict with a single value (the GET_LOCK result)
            first_row = result[0]
            first_value = list(first_row.values())[0]
            return int(first_value) == 1
        except Exception as e:
            logging.error(f"Failed to acquire lock '{lock_name}': {e}")
            return False

    def release_lock(self, lock_name):
        """Release a named lock."""
        try:
            self.run_query(f"SELECT RELEASE_LOCK('{lock_name}')")
        except Exception as e:
            logging.error(f"Failed to release lock '{lock_name}': {e}")

    