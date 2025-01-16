
from interfaces.handler import I_BaseHandler
from interfaces.client import I_BaseClient
from route_options import OptionsManager
from utils.logSetup import log_running_and_done
import logging
import json

class OptionsHandler(I_BaseHandler, I_BaseClient, OptionsManager):
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
        agent_type might be "ecounit", "customer", "backuser" or "backuser_admin"
        '''
        # Find out agent_type
        agent_type = "all"

        # Construct response components based on agent_type
        agent_options = self.collect_agent_options(agent_type)
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
    test()