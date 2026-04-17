import uuid
from datetime import datetime, timedelta
import threading
import time
from out_of_process.sessions import SessionManager as Sessions
import json

AUTH_TOKENS = {"client_address": "my_secret_token", "other_client_address": "not_my_token"}

class AuthManager(Sessions):
    '''
    - Quem és tú, Jaburu?
    - Atribuir label (Customer, Unit, etc)
    - Solicitar criação de token
    - Retorna o token
    '''
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def is_authenticated(self, func):
        def wrapper(*args, **kwargs):
            # Temporary bypass
            return func(*args, **kwargs)
            # Authentication logic
            try:
                auth_header = self.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    if token in AUTH_TOKENS.values():
                        return func(*args, **kwargs)
            except Exception as e:
                print(f"Error during authentication: {e}")
                status = 401
                headers = {"Content-Type": "application/json"}
                body = json.dumps({"error": "Unauthorized"}) + "\r\n"

                return status, headers, body
                
        return wrapper
