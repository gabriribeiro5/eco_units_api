import uuid
from datetime import datetime, timedelta
import threading
import time
from utils.definitions import SESSION_GROUPS_AND_TIMEOUTS

AUTH_TOKENS = {"client_address": "my_secret_token", "other_client_address": "not_my_token"}
class SessionManager():
    '''
    - Criar token
    - Atribuir horario
    - Adicionar à lista (MemCache)
    - Retornar token
    - Iniciar temporizador
    - Monitorar
    - Remover token
    '''
    def __init__(self) -> None:
        # create class variables to represent sessions
        for g, t in SESSION_GROUPS_AND_TIMEOUTS.items():
            setattr(self, g, {})
            setattr(self, f"{g}_timeout", timedelta(minutes=t))
    
    def create_session_id(self, session_group):
        random_hash = str(uuid.uuid4())
        session_id = f"{session_group}:{random_hash}"
        return session_id
    
    def cache_session_id(self, session_id, session_group_name):
        '''
        This module is basically running
            > dict.update(key = value, ...)
        in a sofisticated way

        An actual exemple migh be
            > self.eco_unit_sessions.update(session_id = session_id,
                                            created_at = datetime.now(),
                                            last_access = datetime.now())            
        Where 
            > getattr(self, session_group_name)
        is equal to
            > self.eco_unit_sessions
            > self.customer_sessions
            > ...
        '''
        getattr(self, session_group_name).update(session_id = session_id,
                                                created_at = datetime.now(),
                                                last_access = datetime.now())

    def new_session_id(self, client_label):
        match client_label:
            case "eco_unit":
                session_group_name = f"{client_label}_sessions"
                session_id = self.create_session_id(session_group_name)
                self.cache_session_id(session_id, session_group_name)
                return session_id
            case "customer":
                session_group_name = f"{client_label}_sessions"
                session_id = self.create_session_id(session_group_name)
                self.cache_session_id(session_id, session_group_name)
                return session_id
            case _:
                session_group_name = f"backoffice_sessions"
                session_id = self.create_session_id(session_group_name)
                self.cache_session_id(session_id, session_group_name)
                return session_id
    
    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def cleanup_sessions(self):
        for session_group, session_timeout in SESSION_GROUPS_AND_TIMEOUTS.items():
            for session_id, created_at, last_access in getattr(self, session_group):
                agent_inactive:bool = (datetime.now() - last_access) > session_timeout
                session_up_for_too_long:bool = (datetime.now() - created_at) > session_timeout*5
                if agent_inactive or session_up_for_too_long:
                    self.delete_session(session_id)

def session_cleanup_task(SessionManager):
    while True:
        time.sleep(60)  # Run cleanup every minute
        SessionManager.cleanup_sessions()

# Start cleanup thread
session_manager = SessionManager()
cleanup_thread = threading.Thread(target=session_cleanup_task, args=(session_manager,), daemon=True)
cleanup_thread.start()

if __name__ == "__main__":
    sm = SessionManager()
    sm.new_session_id("eco_unit")

class AuthManager():
    '''
    - Quem és tú, Jaburu?
    - Atribuir label (Customer, Unit, etc)
    - Solicitar criação de token
    - Retorna o token
    '''
    def __init__(self) -> None:
        pass

    # Verifica se a requisição está autenticada
    def is_authenticated(self):
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token == AUTH_TOKENS[self.client_address]
        return False
    
    def require_authentication(self):
        if not self.is_authenticated():
            self.send_error(401, "Unauthorized")
            return
