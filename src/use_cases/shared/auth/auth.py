from gateways.sync_api_client import MicroserviceClient
from interfaces.database.db_scripts import I_DBScriptSource
from gateways.sync_pymysql import SyncronousPyMySQL
from use_cases.shared.auth.sessions import SessionManager as Sessions
import os
import uuid
from datetime import datetime
from urllib.parse import parse_qs
import logging
import json
import functools
def try_external_api_call(func):
    """
    Decorator function that checks authentication before allowing the request.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try: # Call external microsservice, if exists
            response_data = self.api_client.external_call(self.command,
                                                self.path,
                                                self.request_version,
                                                self.headers.items(),
                                                data_type = "dict")
            if response_data:
                return response_data
            else:
                raise ValueError("Incompatible response format from external API. Expected a tuple with (status, headers, body).")
        except Exception as e: # Apply business rules
            logging.info(f'''{e} Running internal Business Logic.''')
            return func(self, *args, **kwargs)
    return wrapper

class AuthHandler(Sessions, I_DBScriptSource):
    '''
    - Quem és tú, Jaburu?
    - Atribuir label (Customer, Unit, etc)
    - Solicitar criação de token
    - Retorna o token
    '''
    def __init__(self, *args, **kwargs) -> None:
        self.FIRST_AUTH_AGENTS = {}
        self.db = SyncronousPyMySQL()
        self.api_client = MicroserviceClient(host="localhost", port=8000)  # Example host and port for microservice
        I_DBScriptSource.__init__(self)  # make sure scripts are loaded for classes that inherit from this one
        super().__init__(*args, **kwargs)

    def check_admin_credentials(self, admin_name, admin_secret):
        '''
        Check against environment variables
        '''
        # This is a placeholder check. Replace with actual environment variable checks in production.
        admin_names_and_secrets = os.getenv("API_ADMIN_SECRETS").split(",")
        agent_credential = f"{admin_name}:{admin_secret}"

        if agent_credential not in list(admin_names_and_secrets):
            logging.warning(f"Invalid admin credentials provided: {agent_credential}")
            raise ValueError("Invalid admin credentials")

    # database INSERTS to update in-memory auth data
    def insert_first_auth_agent(self, agent_id, token):
        '''
        Adds a new agent to the FIRST_AUTH_AGENTS list with the provided agent_id and token.
        This is a placeholder implementation and should be replaced with actual database logic in production.
        '''
        try:
            self.db.run_script(self.script_insert_first_auth_agent, agent_id, token)
        except Exception as e:
            logging.error(e)
            return e

    def insert_session(self, agent_id, token):
        '''
        Adds a new session token to the session table with the provided agent_id and token.
        This is a placeholder implementation and should be replaced with actual database logic in production.
        '''
        try:
            self.db.run_script(self.script_insert_session, agent_id, token)
        except Exception as e:
            logging.error(e)
            return e

    # database SELECTS to update in-memory auth data
    def first_auth_token_is_valid(self, agent_id, received_token):
        '''
        Fetch the latest data from the database.
        '''
        try:
            selected_rows = self.db.run_query(self.script_select_first_auth_agent__token, agent_id)
            if not selected_rows or len(selected_rows) == 0:
                logging.warning(f"Agent {agent_id} not found in first_auth_agent")
                return False
            # Expect the first row to be a dict with a 'token' column; fall back to first value if needed
            first_row = selected_rows[0]
            token_value = None
            if isinstance(first_row, dict):
                token_value = first_row.get('token') if 'token' in first_row else (list(first_row.values())[0] if first_row else None)
            else:
                token_value = first_row[0] if first_row else None

            if token_value != received_token:
                logging.warning(f"Unauthorized token: {received_token}")
                logging.warning(f"Expected token: {token_value}")
                return False
            return True
        except Exception as e:
            logging.error(e)
            return e
        

    def agent_is_enabled(self, agent_id):
        '''
        Fetch the latest data from the database.
        '''
        try:
            agent_rows = self.db.run_query(self.script_select_agent__is_enabled, (agent_id,))
            if not agent_rows or len(agent_rows) == 0:
                return False
            first_row = agent_rows[0]
            if isinstance(first_row, dict):
                # try common column name first
                is_enabled = first_row.get('is_enabled') if 'is_enabled' in first_row else list(first_row.values())[0]
            else:
                is_enabled = first_row[0]
            return is_enabled
        except Exception as e:
            logging.error(e)
            raise e

    def delete_first_auth_agent(self, agent_id):
        '''
        Deletes the first auth agent from the database to prevent reuse of the token.
        This is a placeholder implementation and should be replaced with actual database logic in production.
        '''
        try:
            self.db.run_script(self.script_delete_first_auth_agent, agent_id)
            logging.info(f"First auth agent {agent_id} deleted successfully.")
        except Exception as e:
            logging.error(e)
            return e

    def session_token_is_valid(self, agent_id, session_token):
        '''
        Fetch the latest data from the database.
        '''
        try:
            selected_rows = self.db.run_query(self.script_select_session, agent_id)
            if not selected_rows or len(selected_rows) == 0:
                logging.warning(f"Agent {agent_id} not found in session tokens")
                return False
            first_row = selected_rows[0]
            token_value = None
            if isinstance(first_row, dict):
                token_value = first_row.get('token') if 'token' in first_row else list(first_row.values())[0]
            else:
                token_value = first_row[0]

            if token_value != session_token:
                logging.warning(f"Unauthorized access attempt: {session_token}")
                return False
            return True
        except Exception as e:
            logging.error(e)
            return e


    # Hash generation and validation
    def new_hash(self, id, agent_type):
        '''
        Generates a hash token based on specific id (device_operation_supervisor, customer, etc.) and agent type.
        This is a placeholder implementation and should be replaced with a secure hashing algorithm in production.
        '''
        return f"hash_type!{agent_type}_id!{id}"
    
    def unhash(self, hash_string):
        '''
        Placeholder function to reverse the hashing process.
        In a real implementation, this would not be possible with a secure hash, so this is just for demonstration purposes.
        '''
        
        hash_data = {}
        if hash_string.startswith("hash_"): # uses the simplest hashing algorithm
            hash_components = hash_string.split("_") # find basic hash components

            for i in range(len(hash_components)):
                if hash_components[i].startswith("type!"):
                    hash_data["agent_type"] = hash_components[i].split("!")[1] # extract agent type
                if hash_components[i].startswith("id!"):
                    hash_data["id"] = hash_components[i].split("!")[1] # extract id
        else:
            logging.warning(f"Invalid hash format: {hash_string}")

        return hash_data
    
    def select_agent_id_from_database(self, id, agent_type):
        '''
        Placeholder function to select agent_id from database based on id and agent_type.
        In a real implementation, this would involve querying the database to retrieve the corresponding agent_id.
        '''
        # Retrieve agent_id based on the hash
        # TODO: look up the hash in a database
        agent_id_mapping = {
            "admin_id_hash": "new_client_id",
            "device_operation_supervisor_id_hash": "existing_client_id",
            "customer_id_hash": "other_existing_client_id",
            "device_id_hash": "another_existing_client_id"
        }
        if agent_type == "backoffice_admin":
            # Search for agent_id in backoffice_admin database table using the id extracted from the hash
            agent_id = agent_id_mapping.get(id, None)
        if agent_type == "device_operation_supervisor":
            # Search for agent_id in device_operation_supervisors database table using the id extracted from the hash
            agent_id = agent_id_mapping.get(id, None)
        if agent_type == "customer":
            # Search for agent_id in customers database table using the id extracted from the hash
            agent_id = agent_id_mapping.get(id, None)
        if agent_type == "device":
            # Search for agent_id in devices database table using the id extracted from the hash
            agent_id = agent_id_mapping.get(id, None)
        return "agent_id_from_database"
    
    def find_agent_id(self, id_hash):
        '''
        Retrieves the agent_id corresponding to the provided agent_id_hash
        '''
        # Find agent type based on the hash
        hash_data = self.unhash(id_hash)
        id = hash_data.get("id") if hash_data else None
        agent_type = hash_data.get("agent_type") if hash_data else None

        if agent_type:
            logging.debug(f"Agent type {agent_type} identified for hash {id_hash}.")
            agent_id = self.select_agent_id_from_database(id, agent_type) # placeholder function to select agent_id from database based on id and agent_type
        else:
            logging.warning(f"No agent type identified for hash {id_hash}.")
            agent_id = None

        return agent_id

    @try_external_api_call
    def handle_backoffice_admin_first_auth(self):
        '''
        Handles the first authentication step for a client (agent).
        1. Validates the provided agent_id against FIRST_AUTH_AGENTS.
        2. If agent_id is valid, returns its token and moves it to ALLOWED_AGENTS.
        3. If agent_id is not valid, returns None.
        '''
        backoffice_admin_id_hash = self.get_request_data().get("backoffice_admin_id_hash", None).lower()
        backoffice_admin_token = self.get_request_data().get("backoffice_admin_token", None).lower()
        agent_id = self.find_agent_id(backoffice_admin_id_hash) if backoffice_admin_id_hash else None
        
        # Validate agent_id
        try:
            if agent_id in self.FIRST_AUTH_AGENTS and self.FIRST_AUTH_AGENTS[agent_id] == backoffice_admin_token:
                # Move item to allowed agents
                # TODO: this item must be saved to a database
                self.ALLOWED_AGENTS[agent_id] = self.FIRST_AUTH_AGENTS[agent_id]
                logging.info(f"Agent {agent_id} added to allowed agents.")
                
                del self.FIRST_AUTH_AGENTS[agent_id]
                logging.info(f"Agent {agent_id} removed from first auth agents.")
                
                authorized = True
            else:
                logging.warning(f"Agent ID {agent_id} not found in first auth agents.")
                authorized = False
            
        except Exception as e:
            logging.error(f"Error during first authentication for {agent_id}: {str(e)}")
            authorized = False
        
        # expected output: agent_id
        status = 200 if authorized else 401
        response_data = (status, {}, {})
        return response_data
        
    @try_external_api_call
    def handle_agent_login(self):
        '''
        Handles the login process for a client (agent).
        1. Validates the provided id and token against ALLOWED_AGENTS
        2. Get and return a new session ID to the client for future authenticated requests
        '''       
        request_data = self.get_request_data()
        agent_id_hash = request_data.get("agent_id_hash", None).lower()
        
        agent_id = self.find_agent_id(agent_id_hash) if agent_id_hash else "all"
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1].lower()

        # check if agent is enabled in the database, if not, return None
        if not self.agent_is_enabled(agent_id):
            logging.warning(f"Agent {agent_id} is not enabled.")
            return None
        
        # Validate agent_id and token, then get sessoin ID
        try:
            if agent_id in self.ALLOWED_AGENTS and self.ALLOWED_AGENTS[agent_id] == token:
                # Get and return a new session ID.
                # TODO: this item must be saved to a database
                logging.info(f"Agent {agent_id} authenticated successfully.")                
                session_id = self.new_session_id(client_label="device")
            else:
                logging.warning(f"Agent ID {agent_id} not found in first auth agents.")
                return None
            
        except Exception as e:
            logging.error(f"Error during first authentication for {agent_id}: {str(e)}")
            return None
        
        # expected output: session_id
        status = 200 if session_id else 401
        response_data = (status, {}, json.dumps({"session_id": session_id}) if session_id else json.dumps({"error": "Unauthorized"}))
        return response_data
    

    def is_authenticated(self):
        '''
        Validates the session token provided in the Authorization header of the request.
        Returns True if the token is valid and corresponds to an active session, otherwise returns False.
        '''
        request_data = self.get_request_data()
        try:
            agent_id = request_data.get("agent_id")
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                logging.debug(f"Received authentication attempt for agent_id: {agent_id} with token: {token}")
                return self.session_token_is_valid(agent_id, token)
            logging.warning("Unauthorized access attempt without valid Authorization header.")
            return False
        except Exception as e:
            logging.error(f"Error during authentication: {str(e)}")
            return False
