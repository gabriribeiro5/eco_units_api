from pathlib import Path
import time

class Definitions():
    def __init__(self):
        ### DIRECTORIES ###
        self.SRC_DIR = Path(__file__).resolve().parent
        self.LOG_DIR = "/var/log/cyclobots_api"
        self.LOG_FILE_NAME = f"{time.strftime("%Y%m%d_%H%M%S")}"
        self.ROUTE_OPTIONS = self.SRC_DIR / "route_options.json"
        self._DB_SCRIPTS_DIR = self.SRC_DIR / "interfaces/database/_db_scripts"

        ### APPLICATION CONFIGURATION ###
        self.AGENTS_LIST = ("device", "customer", "device_operation_supervisor", "backoffice_admin")
        self.AGENT_INPUT_TABLES = ("device_operation_agent", "diagnostic", "configuration", "ecosystem_state")
        self.ALLOWED_INPUT_TABLES = {
            "device": (self.AGENT_INPUT_TABLES),
            "customer": (self.AGENT_INPUT_TABLES),
            "device_operation_supervisor": (self.AGENT_INPUT_TABLES, "device_operation_agent", "device", "customer"),
            "backoffice_admin": (self.AGENT_INPUT_TABLES, "device_operation_agent", "device", "customer", "device_operation_supervisor")
        }
        self.SESSION_GROUPS_AND_TIMEOUTS = {
            "device_sessions": 5, # group_name: minutes
            "customer_sessions": 30, # group_name: minutes
            "device_operation_supervisor_sessions": 30, # group_name: minutes
            "backoffice_admin_sessions": 30 # group_name: minutes
        }
        self.LOGGING_ENABLED = True
        self.ASYNC_MODE = False
        self.DEBUG_MODE = False
        self.SERVER_PORT = 8080
        self.DEBUG_PORT = 5678

        ### DATABASE  ### 
        self.DB_HOST = "mysql" # "127.0.0.1"
        self.DB_USER = "cyclobots_api"
        self.DB_SECRET = "s3cr37@dblab73"
        self.DB_NAME = "ecosystem_db"
        self.DB_PORT = 3306
        self.NUM_BATCHES = 10