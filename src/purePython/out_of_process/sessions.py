import uuid
from datetime import datetime, timedelta
import threading
import time
from utils.definitions import SESSION_GROUPS_AND_TIMEOUTS

AUTH_TOKENS = {"client_address": "my_secret_token", "other_client_address": "not_my_token"}
class SessionManager():
    def __init__(self) -> None:
        '''
            Controla todas as sessões ativas
        '''
        # create class variables to represent sessions
        for g, t in SESSION_GROUPS_AND_TIMEOUTS.items():
            setattr(self, g, {})
            setattr(self, f"{g}_timeout", timedelta(minutes=t))
        
        # Deamon threads: If the main program exits while daemon threads are running,
        #   they are abruptly stopped without completing their execution
        # Non-daemon threads, on the other hand, keep the program running until they finish
        cleanup_thread = threading.Thread(target=self.session_cleanup_task, daemon=True)
        cleanup_thread.start()
    
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
        try:
            getattr(self, session_group_name).update(session_id = session_id,
                                                created_at = datetime.now(),
                                                last_access = datetime.now())
        except:
            print(f"nao foi possivel encontrar o grupo de sessões {session_group_name}")

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
        now = datetime.now()
        
        # Access each session group
        for session_group, session_timeout in SESSION_GROUPS_AND_TIMEOUTS.items():
            sessions = getattr(self, session_group, [])
            expired_sessions = [
                session_id
                for session_id, created_at, last_access in sessions
                if (now - last_access > session_timeout) or (now - created_at > session_timeout * 5)
            ]

            for session_id in expired_sessions:
                self.delete_session(session_id)


    def session_cleanup_task(self):
        while True:
            time.sleep(60)  # Run cleanup every minute
            SessionManager.cleanup_sessions()


def test_session_manager():
    sm = SessionManager()
    agent_label = "back_user"
    sid = sm.new_session_id(agent_label)
    print(f"test session_id {sid}")
    sm.delete_session(sid)
    print(f"session_id removed")

if __name__ == "__main__":
    test_session_manager()
