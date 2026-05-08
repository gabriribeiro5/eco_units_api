from config import Definitions
import logging

class I_DBScriptSource():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Definitions()
        
        logging.info("loading db scripts")
        # DB SETUP
        self.script_schema_ecosystem_db = self._load_sql(self.config._DB_SCRIPTS_DIR / "_0_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_insert_into_index_tables.sql")
        
        # NEW AGENTS
        self.script_insert_disabled_agent = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_00_insert_disabled_agent.sql")
        
        self.script_insert_backuser_admin = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_10_insert_backuser_admin.sql")
        self.script_insert_backuser = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_20_insert_backuser.sql")
        self.script_insert_customer = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_30_insert_customer.sql")
        self.script_insert_device = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_40_insert_device.sql")

        self.script_enable_agent = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_99_enable_agent.sql")
        
        # AGENT INPUTS
        # device
        self.script_insert_agent_input = self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_00_insert_agent_input.sql")

        self.script_insert_diagnostic = self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_10_insert_diagnostic.sql")
        self.script_insert_configuration = self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_20_insert_configuration.sql")
        self.script_insert_ecosystem_state = self._load_sql(self.config._DB_SCRIPTS_DIR / "_3_30_insert_ecosystem_state.sql")

    def _load_sql(self, filename):
        '''
        Open and read the file as a single buffer
        '''
        sqlScript = ""
        try:
            fd = open(filename, 'r')
            sqlScript = fd.read()
            fd.close()
        except Exception as e:
            logging.error(f"failed loading {filename}:\n {e}")

        return sqlScript
    