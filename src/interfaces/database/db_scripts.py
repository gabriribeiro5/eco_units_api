from config import Definitions
import logging

class I_DBScriptSource():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Definitions()
        
        logging.info("loading db scripts")
        ################
        # 0 - DB SETUP #
        ################
        self.script_schema_ecosystem_db = self._load_sql(self.config._DB_SCRIPTS_DIR / "_0_00_schema_ecosystem_db.sql")
        self.script_insert_into_index_tables = self._load_sql(self.config._DB_SCRIPTS_DIR / "_0_10_insert_into_index_tables.sql")
        
        
        ##################
        # 1 - NEW AGENTS #
        ##################
        
        # GENERIC AGENT
        self.script_insert_disabled_agent = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_00_insert_disabled_agent.sql")
        
        # CREATE ADMIN
        self.script_insert_backuser_admin = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_10_insert_backuser_admin.sql")
        self.script_set_backuser_admin_id = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_11_set_backuser_admin_id.sql")

        # CREATE BACKUSER
        self.script_insert_backuser = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_20_insert_backuser.sql")
        self.script_set_backuser_id = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_21_set_backuser_id.sql")

        # CREATE CUSTOMER
        self.script_insert_customer = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_30_insert_customer.sql")
        self.script_set_customer_id = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_31_set_customer_id.sql")

        # CREATE DEVICE
        self.script_insert_device = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_40_insert_device.sql")
        self.script_set_device_id = self._load_sql(self.config._DB_SCRIPTS_DIR / "_1_41_set_device_id.sql")

        #######################
        # 2 - AUTH MANAGEMENT #
        #######################

        # FIRST AUTHENTICATION
        self.script_insert_first_auth_agent = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_10_insert_first_auth_agent.sql")
        self.script_select_first_auth_agent__token = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_11_select_first_auth_agent__token.sql")
        self.script_set_agent__is_enabled = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_12_enable_agent.sql")
        self.script_select_agent__is_enabled = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_13_select_agent__is_enabled.sql")
        self.script_delete_first_auth_agent = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_14_delete_first_auth_agent.sql")

        # SESSIONS
        # use email to find AGENT_ID and validate AGENT_SECRET
        self.script_select_backuser_admin_by_email = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_20_select_backuser_admin_by_email.sql")
        self.script_select_backuser_by_email = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_21_select_backuser_by_email.sql")
        self.script_select_customer_by_email = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_22_select_customer_by_email.sql")
        
        self.script_insert_session = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_23_insert_session.sql")
        self.script_select_session = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_24_select_session__token.sql")
        self.script_delete_session = self._load_sql(self.config._DB_SCRIPTS_DIR / "_2_25_delete_session.sql")

        ####################
        # 3 - AGENT INPUTS #
        ####################
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
    