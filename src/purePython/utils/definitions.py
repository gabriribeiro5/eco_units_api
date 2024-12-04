from pathlib import Path

### DIRECTORIES ###
SRC_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = SRC_DIR.parent / "logs"
ROUTES_DIR = SRC_DIR / "routes.json"


### CONFIGURATION ###
AGENT_INPUT_TABLES = ("agent_input", "diagnostic", "configuration", "environment_state")
ALLOWED_INPUT_TABLES = {
    "eco_unit": (AGENT_INPUT_TABLES),
    "customer": (AGENT_INPUT_TABLES),
    "back_user": (AGENT_INPUT_TABLES, "agent", "eco_unit", "customer"),
    "back_user_admin": (AGENT_INPUT_TABLES, "agent", "eco_unit", "customer", "back_user")
}
SESSION_GROUPS_AND_TIMEOUTS = {
    "eco_unit_sessions": 5, # group_name: minutes
    "customer_sessions": 30, # group_name: minutes
    "backoffice_sessions": 30 # group_name: minutes
}