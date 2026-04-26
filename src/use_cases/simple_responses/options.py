from use_cases.shared.auth.auth import AuthHandler as Auth
from route_options import OptionsManager
from utils.logger import log_running_and_done
from urllib.parse import parse_qs
import logging
import json
import functools

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

class OptionsHandler(Auth, OptionsManager):
    """/
    Handles the OPTIONS HTTP method.
    OPTIONS is used to describe the communication options for the target resource.
        It helps the client understand what methods and headers are allowed
    """
    def __init__(self, *args, **kwargs) -> None:
        self.options = OptionsManager()
        super().__init__(*args, **kwargs)
        
    def development_test(self):
        pass

    def collect_agent_options(self, agent_type = "all"):
        agent_options = {
            "TRACE": {},
            "OPTIONS": {},
            "POST": {},
            "GET": {},
            "PUT": {},
            "PATCH": {},
            "DELETE": {}
        }
        if agent_type not in self.definitions.AGENTS_LIST:
            agent_type = "all"

        # Read all options and apply them to agent_options
        for http_method, method_options in self.options.all.items():
            for route, route_details in method_options.items():
                try:
                    if route == "_comment":
                        pass
                    elif agent_type == "all" or agent_type in route_details.get("target_agents"):
                        agent_options[http_method].update({route: route_details})
                except Exception as e:
                    msg = f"failed to find route's 'target_agents'."
                    msg_detail = f"Route {route} in method {http_method}."
                    msg_exception = f"Exception: {str(e)}"
                    logging.exception(f"({self.inspector.say_my_name()}): {msg}\n{msg_detail}\n{msg_exception} ")

        for http_method in agent_options:
            if http_method == {}:
                del agent_options[http_method]
        
        return agent_options
    
    @log_running_and_done
    def handle_options_for_unauthenticated_client(self):
        '''
        agent_type might be "cyclobot", "customer", "backuser" or "backuser_admin"
        '''
        # Find out agent_type from request body, default to "all" if not provided or invalid
        content_length = int(self.headers.get("Content-Length", 0))
        request_body = self.rfile.read(content_length).decode('utf-8') if content_length else ""

        try:
            request_body = request_body.strip()  # Remove leading/trailing whitespace            
            # Try parsing as JSON first, then fall back to form data
            if request_body:
                try:
                    request_data = json.loads(request_body)
                except json.JSONDecodeError:
                    # Parse as URL-encoded form data
                    parsed = parse_qs(request_body)
                    request_data = {k: v[0] if v else "" for k, v in parsed.items()}
            else:
                request_data = {}
            
            agent_type = request_data.get("agent_type", "all").lower()
        except Exception as e:
            logging.exception(f"Failed to decode request body: {request_body}\nException: {str(e)}")
            agent_type = "all"

        logging.debug(f"Received OPTIONS request with agent_type: {agent_type}")
     
        # Construct response components based on agent_type
        agent_options = self.collect_agent_options(agent_type)
        response = json.dumps(agent_options) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body
    
    @require_authentication
    @log_running_and_done
    def handle_options_for_customer(self):
        '''
        return all routes for "customer"
        '''
        # Construct response components based on agent_type
        agent_options = self.collect_agent_options("customer")
        response = json.dumps(agent_options) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body
    
    @require_authentication
    @log_running_and_done
    def handle_options_for_backuser(self):
        '''
        return all routes for "backuser"
        '''
        # Construct response components based on agent_type
        agent_options = self.collect_agent_options("backuser")
        response = json.dumps(agent_options) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body
    
    
    @require_authentication
    @log_running_and_done
    def handle_options_for_backuser_admin(self):
        '''
        return all routes for "backuser_admin"
        '''
        # Construct response components based on agent_type
        agent_options = self.collect_agent_options("backuser_admin")
        response = json.dumps(agent_options) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

def test():
    handler = OptionsHandler()
    handler.development_test()

if __name__ == "__main__":
    test() # Ugly but efficient