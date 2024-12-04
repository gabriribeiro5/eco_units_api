import uuid
from datetime import datetime, timedelta
import threading
import time
from utils.definitions import SESSION_GROUPS_AND_TIMEOUTS
from out_of_process.sessions import SessionManager as Sessions

AUTH_TOKENS = {"client_address": "my_secret_token", "other_client_address": "not_my_token"}

class AuthManager(Sessions):
    '''
    - Quem és tú, Jaburu?
    - Atribuir label (Customer, Unit, etc)
    - Solicitar criação de token
    - Retorna o token
    '''
    def __init__(self, *args, **kwargs) -> None:
        Sessions.__init__(self, *args, **kwargs)

    # Verifica se a requisição está autenticada
    def is_authenticated(self):
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token == AUTH_TOKENS[self.client_address]
        return False