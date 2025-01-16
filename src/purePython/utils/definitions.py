from pathlib import Path

class Definitions():
    def __init__(self):
        ### DIRECTORIES ###
        self.SRC_DIR = Path(__file__).resolve().parent.parent
        self.LOG_DIR = "/var/log/eco_units_api"
        self.LOG_FILE_NAME = "purePython"
        self.OPTIONS_DIR = self.SRC_DIR / "options.json"


        ### CONFIGURATION ###
        self.AGENTS_LIST = ("ecounit", "customer", "backuser", "backuser_admin")
        self.AGENT_INPUT_TABLES = ("agent_input", "diagnostic", "configuration", "environment_state")
        self.ALLOWED_INPUT_TABLES = {
            "eco_unit": (self.AGENT_INPUT_TABLES),
            "customer": (self.AGENT_INPUT_TABLES),
            "back_user": (self.AGENT_INPUT_TABLES, "agent", "eco_unit", "customer"),
            "back_user_admin": (self.AGENT_INPUT_TABLES, "agent", "eco_unit", "customer", "back_user")
        }
        self.SESSION_GROUPS_AND_TIMEOUTS = {
            "eco_unit_sessions": 5, # group_name: minutes
            "customer_sessions": 30, # group_name: minutes
            "backoffice_sessions": 30 # group_name: minutes
        }
