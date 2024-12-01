import os
from pathlib import PurePath

ROOT_DIR = os.path.dirname(PurePath(os.path.abspath(__file__)).parent) # This is your Project Root
ROUTES_PATH = os.path.join(ROOT_DIR, 'routes.json')  # requires `import os`