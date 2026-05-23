from use_cases.shared.auth.auth import AuthHandler
from gateways.sync_pymysql import SyncronousPyMySQL
from gateways.sync_email_client import EmailClient
from utils.logger import log_running_and_done
from urllib.parse import parse_qs
import logging
import json
import functools
import pymysql # type: ignore

def require_authentication(func):
    """
    Decorator function that checks authentication before allowing the request.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_authenticated():
            self.send_error(401, "Unauthorized")
            return (401, {"Content-Type": "application/json"}, '{"error": "Unauthorized"}\r\n')
        return func(self, *args, **kwargs)
    return wrapper

class AgentLoginHandler(AuthHandler):
    """
    Handler for agent login and related operations such as creating backusers, customers, and devices.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.db = SyncronousPyMySQL()
        super().__init__(*args, **kwargs)
        
    def development_test(self):
        pass
    
    def authenticate_agent(self, email, secret, agent_type):
        '''
        Authenticate an agent (backuser admin, backuser, or customer) based on email and secret.
        '''
        try:
            if agent_type == "admin":
                query = self.script_select_backuser_admin_by_email
            elif agent_type == "backuser":
                query = self.script_select_backuser_by_email
            elif agent_type == "customer":
                query = self.script_select_customer_by_email
            else:
                raise ValueError("Invalid agent type")

            result = self.db.run_query(query, (email,))
            if result and len(result) > 0:
                stored_secret = result[0]["backuser_admin_secret"] if agent_type == "admin" else result[0]["backuser_secret"] if agent_type == "backuser" else result[0]["customer_secret"]
                if stored_secret == secret:
                    return self.new_hash(result[0]["agent_id"], agent_type)  # Generate and return a session token
                else:
                    logging.warning(f"Authentication failed for {agent_type}: {email} - Incorrect secret")
            else:
                logging.warning(f"Authentication failed for {agent_type}: {email} - No such email found")
        except Exception as e:
            logging.error(f"Error during authentication for {agent_type}: {email} - {str(e)}")
        return None

    ####################################################################
    # HANDLERS FOR AGENT LOGIN AND ENABLEMENT
    ####################################################################
    def handle_get_backuser_admin_login(self):
        '''
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("agent_email"):
            raise ValueError("agent_email is required")
        if not request_data.get("agent_secret"):
            raise ValueError("agent_secret is required")
        # Validate email pattern
        if "@" not in request_data.get("agent_email") or "." not in request_data.get("agent_email"):
            raise ValueError("Invalid email format")

        session_token = self.authenticate_agent(request_data.get("agent_email"), request_data.get("agent_secret"), "admin")
        if session_token:
            result["session_token"] = session_token
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body
