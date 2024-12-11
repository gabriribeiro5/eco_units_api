import uuid
from datetime import datetime, timedelta
import threading
import time
from purePython.utils.definitions import SESSION_GROUPS_AND_TIMEOUTS

class SessionManager:
    def __init__(self) -> None:
        """
        Controls all active sessions.
        """
        # Initialize session groups and timeouts
        for group_name, timeout in SESSION_GROUPS_AND_TIMEOUTS.items():
            setattr(self, group_name, {})  # Each group is a dictionary of session data
            setattr(self, f"{group_name}_timeout", timedelta(minutes=timeout))

        # Start a daemon thread for periodic session cleanup
        cleanup_thread = threading.Thread(target=self.session_cleanup_task, daemon=True)
        cleanup_thread.start()

    def _create_session_id(self, session_group: str) -> str:
        """
        Generates a unique session ID for the specified group.
        """
        return f"{session_group}:{uuid.uuid4()}"

    def _cache_session_id(self, session_group: str, session_id: str):
        """
        Caches a new session ID in the corresponding session group.
        """
        now = datetime.now()
        session_data = {
            "session_id": session_id,
            "created_at": now,
            "last_access": now,
        }
        group_sessions = getattr(self, session_group, None)
        if group_sessions is not None:
            group_sessions[session_id] = session_data
        else:
            raise ValueError(f"Session group '{session_group}' does not exist.")

    def new_session_id(self, client_label: str) -> str:
        """
        Public method for creating a new session ID based on the client label.
        Delegates session group determination and caching to internal methods.
        """
        session_group = self._determine_session_group(client_label)
        session_id = self._create_session_id(session_group)
        self._cache_session_id(session_group, session_id)
        return session_id

    def _determine_session_group(self, client_label: str) -> str:
        """
        Maps client labels to corresponding session groups.
        """
        match client_label:  # Requires Python 3.10 or newer
            case "eco_unit":
                return "eco_unit_sessions"
            case "customer":
                return "customer_sessions"
            case "backoffice":
                return "backoffice_sessions"
            case _:
                raise ValueError(f"Unknown client label '{client_label}'")

    def delete_session(self, session_id: str):
        """
        Deletes a session ID from all session groups.
        """
        for group_name in SESSION_GROUPS_AND_TIMEOUTS:
            group_sessions = getattr(self, group_name, {})
            if session_id in group_sessions:
                del group_sessions[session_id]
                break

    def cleanup_sessions(self):
        """
        Removes expired sessions across all session groups.
        """
        now = datetime.now()
        for group_name, timeout_minutes in SESSION_GROUPS_AND_TIMEOUTS.items():
            group_sessions = getattr(self, group_name, {})
            timeout = timedelta(minutes=timeout_minutes)
            expired_sessions = [
                session_id
                for session_id, data in group_sessions.items()
                if (now - data["last_access"] > timeout)
            ]
            for session_id in expired_sessions:
                self.delete_session(session_id)

    def session_cleanup_task(self):
        """
        Periodic task to clean up expired sessions.
        """
        while True:
            time.sleep(60)  # Run cleanup every minute
            self.cleanup_sessions()




def test_session_manager():
    sm = SessionManager()
    agent_label = "back_user"
    sid = sm.new_session_id(agent_label)
    print(f"test session_id {sid}")
    sm.delete_session(sid)
    print(f"session_id removed")

if __name__ == "__main__":
    test_session_manager()
