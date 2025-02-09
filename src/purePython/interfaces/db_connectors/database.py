from utils.definitions import Definitions

class I_BaseDB():
    def __init__(self, *args, **kwargs) -> None:
        self.definitions = Definitions()
        self.script_schema_ecosystem_db = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_0_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_1_insert_into_index_tables.sql")
        self.script_insert_into_agent_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_2_insert_into_agent_tables.sql")
        self.script_insert_into_agent_input_tables = self._load_sql(self.definitions._DB_SCRIPTS_DIR / "_3_insert_into_agent_input_tables.sql")
        
        self.drop_table_query = "DROP TABLE IF EXISTS (%s)"
        self.insert_query = "INSERT INTO %s (%s) VALUES (%s)"
        self.select_query = "SELECT * FROM %s WHERE id = %s"
        self.delete_query = "DELETE FROM %s WHERE %s LIMIT %s"
        self.update_query = "UPDATE %s SET (%s) = %s WHERE %s = %s"
        
        super().__init__(*args, **kwargs)

    def _load_sql(self, filename):
        '''
        Open and read the file as a single buffer
        '''
        fd = open(filename, 'r')
        sqlScript = fd.read()
        fd.close()

        return sqlScript

    def _executeScriptsFromFile(self, sqlScript):
        raise NotImplementedError()
    
    def _connect():
        raise NotImplementedError()
