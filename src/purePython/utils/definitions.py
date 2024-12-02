import os
from pathlib import PurePath

SRC_DIR = os.path.dirname(PurePath(os.path.abspath(__file__)).parent.parent) # This is your Project Root
ROUTES_PATH = os.path.join(SRC_DIR, 'routes.json')  # requires `import os`
AGENT_INPUT_TABLES = ("agent_input", "diagnostic", "configuration", "environment_state")
ALLOWED_INPUT_TABLES = {
    "eco_unit": (AGENT_INPUT_TABLES),
    "customer": (AGENT_INPUT_TABLES),
    "back_user": (AGENT_INPUT_TABLES, "agent", "eco_unit", "customer"),
    "back_user_admin": (AGENT_INPUT_TABLES, "agent", "eco_unit", "customer", "back_user")
}