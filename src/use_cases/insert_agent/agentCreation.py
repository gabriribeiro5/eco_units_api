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

class AgentCreationHandler(AuthHandler):
    """
    Create a backoffice user.
    0. Check for external routes
    1. Collect parameters
    2. Build or get query
    3. Connect to db
    4. Send query
    5. Close db conn
    """
    def __init__(self, *args, **kwargs) -> None:
        self.db = SyncronousPyMySQL()
        self.email = EmailClient()
        super().__init__(*args, **kwargs)
        
    def development_test(self):
        pass
        
    def get_request_data(self):
        # Select request_data
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
            
            return request_data
        except Exception as e:
            logging.exception(f"Failed to decode request body: {request_body}\nException: {str(e)}")
            raise e

    def create_new_agent(self):
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_disabled_agent)
            logging.debug("Executed script to create new disabled agent")
            connection.commit()
            logging.debug("Committed new agent to database")
            agent_id = cursor.lastrowid
            logging.debug(f"Created new agent with ID: {agent_id}")
            connection.close()
            return agent_id
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_disabled_agent}\n {msg}")
            connection.close()
            raise msg
        except AttributeError as attErr:
            logging.error(f"Attribute error while creating agent:\n {attErr}")
            connection.close()
            raise attErr
        except Exception as e:
            logging.error(f"Error while creating agent:\n {e}")
            connection.close()
            raise e

    def create_backuser_admin(self, agent_id, name, surname, email):
        '''
        Create a backuser admin
        Expected request data:
        `agent_id`,
        `name`,
        `backuser_admin_surname`,
        `backuser_admin_email`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_backuser_admin, (agent_id, name, surname, email))
            backuser_admin_id = cursor.lastrowid
            logging.debug(f"Created backuser admin with ID: {backuser_admin_id} for agent ID: {agent_id}")
            connection.commit()
            connection.close()
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query script_insert_backuser_admin\n {msg}")
            connection.close()
            raise msg
        
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_set_backuser_admin_id, (backuser_admin_id, agent_id))
            connection.commit()
            connection.close()
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query script_set_backuser_admin_id\n {msg}")
            connection.close()
            raise msg
        
        return backuser_admin_id

    def create_backuser(self, agent_id, name, surname, email):
        '''
        Create a backuser
        Expected request data:
        `agent_id`,
        `name`,
        `backuser_surname`,
        `backuser_email`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_backuser, (agent_id, name, surname, email))
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_backuser}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        backuser_id = cursor.lastrowid
        connection.close()
        return backuser_id

    def create_customer(self, agent_id, customer_name, customer_surname, customer_email ):
        '''
        Create a customer
        Expected request data:
        `agent_id`,
        `customer_name`,
        `customer_surname`,
        `customer_email`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_customer, (agent_id, customer_name, customer_surname, customer_email))
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_customer}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        customer_id = cursor.lastrowid
        connection.close()
        return customer_id

    def create_device(self, agent_id, device_name, customer_id, ecosystem_category_id):
        '''
        Create a device
        Expected request data:
        `agent_id`,
        `device_name`,
        `customer_id`,
        `ecosystem_category_id`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_device, (agent_id, device_name, customer_id, ecosystem_category_id))
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_device}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        device_id = cursor.lastrowid
        connection.close()
        return device_id
    
    ####################################################################
    # HANDLERS FOR BACKUSER AND BACKUSER ADMIN CREATION AND ENABLEMENT
    ####################################################################
    @require_authentication
    @log_running_and_done
    def handle_post_backuser_admin(self):
        '''
        Compare secret with second confirmation_secret,
         validate email pattern
         then check if admin_name and secret are in env var,
         then create a administrator with admin privileges.
        Returns confirmation message.
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("agent_name"):
            raise ValueError("agent_name is required")
        if not request_data.get("agent_email"):
            raise ValueError("agent_email is required")
        if not request_data.get("agent_secret"):
            raise ValueError("agent_secret is required")
        if not request_data.get("confirmation_secret"):
            raise ValueError("confirmation_secret is required")
        if request_data.get("agent_secret") != request_data.get("confirmation_secret"):
            raise ValueError("agent_secret and confirmation_secret do not match")
        # Validate email pattern
        if "@" not in request_data.get("agent_email") or "." not in request_data.get("agent_email"):
            raise ValueError("Invalid email format")

        # Check if admin_name and secret are in env var
        self.check_admin_credentials(request_data.get("agent_name"), request_data.get("agent_secret"))
        

        backuser_admin_id = self.create_backuser_admin(self.create_new_agent(),
                                                        request_data.get("agent_name"),
                                                        request_data.get("agent_surname"),
                                                        request_data.get("agent_email")
                                                        )

        first_authentication_token = self.new_hash(backuser_admin_id, "backuser_admin")

        # add token to first auth agents database
        self.insert_first_auth_agent(backuser_admin_id, first_authentication_token)

        # Send verification token via email
        self.email.send_admin_token(first_authentication_token)
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_backuser_admin_enable(self):
        '''
        Enable backuser_admin
        '''
        request_data = self.get_request_data()

        # Check if admin_name and secret are in env var
        self.check_admin_credentials(request_data.get("agent_name"), request_data.get("agent_secret"))

        # Validate token
        self.update_first_auth_agents()
        if request_data.get("first_authentication_token") not in self.FIRST_AUTH_AGENTS.values():
            raise ValueError("Invalid first_authentication_token")

        # Use token to find agent_id
        agent_id = None
        for key, value in self.FIRST_AUTH_AGENTS.items():
            if value == request_data.get("first_authentication_token"):
                agent_id = key
                break

        # Enable backoffice user
        try:
            self.db.run_script(self.script_enable_agent, (agent_id))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Construct response components based on agent_type
        response_dict = {}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    ##################################################
    # BACKUSER CREATION AND ENABLEMENT    
    ##################################################
    @require_authentication
    @log_running_and_done
    def handle_post_backuser(self):
        '''
        Compare secret with second confirmation_secret,
         validate email pattern
         then check if admin_name and secret are in env var,
         then create a backuser with admin privileges.
        Returns confirmation message.
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("agent_name"):
            raise ValueError("agent_name is required")
        if not request_data.get("agent_email"):
            raise ValueError("agent_email is required")
        if not request_data.get("agent_secret"):
            raise ValueError("agent_secret is required")
        if not request_data.get("confirmation_secret"):
            raise ValueError("confirmation_secret is required")
        if request_data.get("agent_secret") != request_data.get("confirmation_secret"):
            raise ValueError("agent_secret and confirmation_secret do not match")
        # Validate email pattern
        if "@" not in request_data.get("agent_email") or "." not in request_data.get("agent_email"):
            raise ValueError("Invalid email format")
       
        backuser_id = self.create_backuser(self.create_new_agent(),
                                                request_data.get("agent_name"),
                                                request_data.get("agent_surname"),
                                                request_data.get("agent_email")
                                                )

        logging.debug("backuser created")


        first_authentication_token = self.new_hash(backuser_id, "backuser_admin")

        # add token to first auth agents database
        self.insert_first_auth_agent(backuser_id, first_authentication_token)

        # Send verification token via email
        self.email.send_admin_token(first_authentication_token)
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_backuser_enable(self):
        '''
        Enable backuser
        '''
        result = {}
        request_data = self.get_request_data()
        
        # Validate token
        self.update_first_auth_agents()
        if request_data.get("first_authentication_token") not in self.FIRST_AUTH_AGENTS.values():
            raise ValueError("Invalid first_authentication_token")
        
        # Use token to find agent_id
        agent_id = None
        for key, value in self.FIRST_AUTH_AGENTS.items():
            if value == request_data.get("first_authentication_token"):
                agent_id = key
                break

        # Enable backoffice user
        try:
            self.db.run_script(self.script_enable_agent, (agent_id))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Construct response components based on agent_type
        response_dict = {}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    ##################################################
    # CUSTOMER CREATION AND ENABLEMENT    
    ##################################################
    @require_authentication
    @log_running_and_done
    def handle_post_customer(self):
        '''
        Compare secret with second confirmation_secret,
         validate email pattern
         then create a backuser with admin privileges.
        Returns confirmation message.
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("agent_name"):
            raise ValueError("agent_name is required")
        if not request_data.get("agent_email"):
            raise ValueError("agent_email is required")
        if not request_data.get("agent_secret"):
            raise ValueError("agent_secret is required")
        if not request_data.get("confirmation_secret"):
            raise ValueError("confirmation_secret is required")
        if request_data.get("agent_secret") != request_data.get("confirmation_secret"):
            raise ValueError("agent_secret and confirmation_secret do not match")
        # Validate email pattern
        if "@" not in request_data.get("agent_email") or "." not in request_data.get("agent_email"):
            raise ValueError("Invalid email format")
       
        customer_id = self.create_customer(self.create_new_agent(),
                                                request_data.get("agent_name"),
                                                request_data.get("agent_surname"),
                                                request_data.get("agent_email")
                                                )

        logging.debug("customer created")

        
        first_authentication_token = self.new_hash(customer_id, "backuser_admin")

        # add token to first auth agents database
        self.insert_first_auth_agent(customer_id, first_authentication_token)

        # Send verification token via email
        self.email.send_admin_token(first_authentication_token)
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_customer_enable(self):
        '''
        Enable customer
        '''
        result = {}
        request_data = self.get_request_data()
        
        # Validate token
        self.update_first_auth_agents()
        if request_data.get("first_authentication_token") not in self.FIRST_AUTH_AGENTS.values():
            raise ValueError("Invalid first_authentication_token")
        
        # Use token to find agent_id
        agent_id = None
        for key, value in self.FIRST_AUTH_AGENTS.items():
            if value == request_data.get("first_authentication_token"):
                agent_id = key
                break

        # Enable backoffice user
        try:
            self.db.run_script(self.script_enable_agent, (agent_id))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Construct response components based on agent_type
        response_dict = {}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    ##################################################
    # DEVICE CREATION AND ENABLEMENT    
    ##################################################
    @require_authentication
    @log_running_and_done
    def handle_post_device(self):
        '''
        Compare secret with second confirmation_secret,
         validate email pattern
         then create a device with admin privileges.
        Returns confirmation message.
        Expected request data:
        `agent_id`
        `device_name`
        `customer_id`
        `ecosystem_category_id`
        `location` (optional)
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("agent_id"):
            raise ValueError("agent_id is required")
        if not request_data.get("device_name"):
            raise ValueError("device_name is required")
        if not request_data.get("customer_id"):
            raise ValueError("customer_id is required")
        if not request_data.get("ecosystem_category_id"):
            raise ValueError("ecosystem_category_id is required")
       
        device_id = self.create_device(self.create_new_agent(),
                                        request_data.get("agent_id"),
                                        request_data.get("device_name"),
                                        request_data.get("customer_id"),
                                        request_data.get("ecosystem_category_id"),
                                        )

        logging.debug("device created")

        
        first_authentication_token = self.new_hash(device_id, "backuser_admin")

        # add token to first auth agents database
        self.insert_first_auth_agent(device_id, first_authentication_token)

        # Send verification token via email
        self.email.send_admin_token(first_authentication_token)
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_backuser_enable(self):
        '''
        Enable backuser
        '''
        request_data = self.get_request_data()
        
        # Validate token
        self.update_first_auth_agents()
        if request_data.get("first_authentication_token") not in self.FIRST_AUTH_AGENTS.values():
            raise ValueError("Invalid first_authentication_token")
        
        # Use token to find agent_id
        agent_id = None
        for key, value in self.FIRST_AUTH_AGENTS.items():
            if value == request_data.get("first_authentication_token"):
                agent_id = key
                break

        # Enable backoffice user
        try:
            self.db.run_script(self.script_enable_agent, (agent_id))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Construct response components based on agent_type
        response_dict = {}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body