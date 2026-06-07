import datetime

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

    def create_new_agent(self):
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_disabled_agent)
            connection.commit()
            agent_id = cursor.lastrowid
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

    def create_backoffice_admin(self, agent_id, email, name, surname, secret):
        '''
        Create a device_operation_supervisor admin
        Expected request data:
        `agent_id`,
        `backoffice_admin_email`
        `name`,
        `backoffice_admin_surname`,
        `backoffice_admin_secret`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_backoffice_admin, (agent_id, email, name, surname, secret))
            backoffice_admin_id = cursor.lastrowid
            connection.commit()
            connection.close()
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query script_insert_backoffice_admin\n {msg}")
            connection.close()
            raise msg
                
        return backoffice_admin_id

    def create_device_operation_supervisor(self, agent_id, email, name, surname, secret):
        '''
        Create a device_operation_supervisor
        Expected request data:
        `agent_id`,
        `device_operation_supervisor_email`,
        `device_operation_supervisor_name`,
        `device_operation_supervisor_surname`,
        `device_operation_supervisor_secret`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_device_operation_supervisor, (agent_id, email, name, surname, secret))
            device_operation_supervisor_id = cursor.lastrowid
            logging.debug(f"Created device_operation_supervisor with ID: {device_operation_supervisor_id} for agent ID: {agent_id}")
            connection.commit()
            connection.close()
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query script_insert_device_operation_supervisor\n {msg}")
            connection.close()
            raise msg
        
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_update_agent_set_device_operation_supervisor_id, (device_operation_supervisor_id, agent_id))
            connection.commit()
            connection.close()
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query script_update_agent_set_device_operation_supervisor_id\n {msg}")
            connection.close()
            raise msg
        
        return device_operation_supervisor_id

    def create_customer(self, agent_id, customer_name, customer_surname, customer_email, customer_secret):
        '''
        Create a customer
        Expected request data:
        `agent_id`,
        `customer_name`,
        `customer_surname`,
        `customer_email`,
        `customer_secret`
        '''
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_customer, (agent_id, customer_email, customer_name, customer_surname, customer_secret))
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_customer}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        customer_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return customer_id

    def generate_random_encrypted_secret(self):
        '''
        Generate a random encrypted secret for device authentication.
        The actual device secret is not stored in the database, only its encrypted version.
        '''
        import os
        import hashlib

        # Generate a random 32-byte secret
        random_secret = os.urandom(32)

        # Encrypt the secret using SHA-256 (or any other hashing algorithm)
        encrypted_secret = hashlib.sha256(random_secret).hexdigest()

        return encrypted_secret

    def create_device(self, agent_id, request_data: dict):
        '''
        Create a device
        Expected request data:
        # REQUIRED FIELDS
        `device_strategy_id`

        # OPTIONAL FIELDS
        `require_update`
        `device_secret`
        `device_name`
        `customer_id`
        `location`
        `max_session_length`
        `max_input_hertz`
        `hardware_cost`
        `software_cost`
        `device_operation_supervisor_fee`
        `transport_fee`
        `installation_fee`
        `total_price`
        `monthly_fee`
        `annual_fee`
        '''
        # Extract required fields from request_data
        device_strategy_id = request_data.get("device_strategy_id")
        require_config_update = request_data.get("require_config_update", False)
        require_firmware_update = request_data.get("require_firmware_update", False)

        # Extract optional fields from request_data
        device_secret = self.generate_random_encrypted_secret()
        # use agent_id to find device_operation_supervisor_id
        try:
            result = self.db.run_query(self.script_select_agent__device_operation_supervisor_id, (agent_id,))
            device_operation_supervisor_id = result[0][0] if result and len(result) > 0 else None
        except Exception as msg:
            logging.error(f"Failed running SQL query\n {self.script_select_agent__device_operation_supervisor_id}\n {msg}")
            raise msg

        if not device_operation_supervisor_id:
            logging.error(f"No device_operation_supervisor_id found for agent_id: {agent_id}")
            raise ValueError(f"No device_operation_supervisor_id found for agent_id: {agent_id}")

        created_by_device_operation_supervisor_id = device_operation_supervisor_id
        created_at = datetime.now()
        updated_by_device_operation_supervisor_id = device_operation_supervisor_id
        updated_at = datetime.now()
        device_model_name = request_data.get("device_model_name", None)
        device_name = request_data.get("device_name", None)
        customer_id = request_data.get("customer_id", None)
        location = request_data.get("location", None)
        max_session_length = request_data.get("max_session_length", None)
        max_input_hertz = request_data.get("max_input_hertz", None)
        consulting_services_cost = request_data.get("consulting_services_cost", None)
        regulatory_compliance_cost = request_data.get("regulatory_compliance_cost", None)
        product_design_cost = request_data.get("product_design_cost", None)
        customer_service_cost = request_data.get("customer_service_cost", None)
        advertising_cost = request_data.get("advertising_cost", None)
        sales_cost = request_data.get("sales_cost", None)
        software_cost = request_data.get("software_cost", None)
        electronics_cost = request_data.get("electronics_cost", request_data.get("hardware_cost", None))
        box_cost = request_data.get("box_cost", None)
        landscape_cost = request_data.get("landscape_cost", None)
        operational_cost = request_data.get("operational_cost", None)
        logistics_cost = request_data.get("logistics_cost", request_data.get("transport_fee", None))
        installation_cost = request_data.get("installation_cost", request_data.get("installation_fee", None))
        maintenance_cost = request_data.get("maintenance_cost", None)
        total_price = request_data.get("total_price", None)
        monthly_fee = request_data.get("monthly_fee", None)
        annual_fee = request_data.get("annual_fee", None)
        supply_chain_id = request_data.get("supply_chain_id")

        if supply_chain_id is None:
            logging.error("supply_chain_id is required to create a device")
            raise ValueError("supply_chain_id is required")

        # insert agent and get specific id
        connection, cursor = self.db.connect()
        try:
            cursor.execute(self.script_insert_device, (agent_id,
                                                        supply_chain_id,
                                                        device_strategy_id,
                                                        device_model_name,
                                                        require_config_update,
                                                        require_firmware_update,
                                                        device_secret,
                                                        created_by_device_operation_supervisor_id,
                                                        created_at,
                                                        updated_by_device_operation_supervisor_id,
                                                        updated_at,
                                                        device_name,
                                                        customer_id,
                                                        location,
                                                        max_session_length,
                                                        max_input_hertz,
                                                        consulting_services_cost,
                                                        regulatory_compliance_cost,
                                                        product_design_cost,
                                                        customer_service_cost,
                                                        advertising_cost,
                                                        sales_cost,
                                                        software_cost,
                                                        electronics_cost,
                                                        box_cost,
                                                        landscape_cost,
                                                        operational_cost,
                                                        logistics_cost,
                                                        installation_cost,
                                                        maintenance_cost,
                                                        total_price,
                                                        monthly_fee,
                                                        annual_fee))
        except pymysql.err.OperationalError as msg:
            logging.error(f"Failed running SQL query\n {self.script_insert_device}\n {msg}")
            connection.close()
            raise msg

        # Fetch all results
        device_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return device_id
    
    ####################################################################
    # HANDLERS FOR BACKUSER AND BACKUSER ADMIN CREATION AND ENABLEMENT
    ####################################################################
    @log_running_and_done
    def handle_post_backoffice_admin(self):
        '''
        Validate request data:
         compare secret with second confirmation_secret,
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
        

        agent_id = self.create_new_agent()
        backoffice_admin_id = self.create_backoffice_admin(agent_id,
                                                        request_data.get("agent_email"),
                                                        request_data.get("agent_name"),
                                                        request_data.get("agent_surname"),
                                                        request_data.get("agent_secret")
                                                        )

        first_authentication_token = self.new_hash(agent_id, "admin")

        # add token to first auth agents database
        self.insert_first_auth_agent(agent_id, first_authentication_token)

        # Send verification token via email
        self.email.send_admin_token(first_authentication_token)
     
        # Construct response components
        response = json.dumps(result) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @log_running_and_done
    def handle_patch_backoffice_admin_enable(self):
        '''
        Enable backoffice_admin
        '''
        try:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Invalid auth token"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
        # Find agent_id from token
        try:
            hash_data = self.unhash(token)
            logging.debug(f"Unhashed token data: {hash_data}")
            agent_id = hash_data["id"] if hash_data["agent_type"] == "admin" else None
        except Exception as e:
            message = f"Error unhashing token: {str(e)}"
            logging.error(message)
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not match expected format or type"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

        if agent_id is None:
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not correspond to an admin"}
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Validate token
        if not self.first_auth_token_is_valid(agent_id, token):
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token is not among first auth list"}
                             
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Enable agent
        try:
            self.db.run_script(self.script_update_agent__is_enabled, (agent_id,))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Delete first auth agent to prevent reuse of token
        if self.agent_is_enabled(agent_id):
            self.delete_first_auth_agent(agent_id)

        # Construct response components based on agent_type
        response_dict = {"agent_is_enabled": True}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    ##################################################
    # BACKUSER CREATION AND ENABLEMENT    
    ##################################################
    @log_running_and_done
    @require_authentication
    def handle_post_device_operation_supervisor(self):
        '''
        Validate request data:
         compare secret with second confirmation_secret,
         validate email pattern
         then check if device_operation_supervisor_name and secret are in env var,
         then create a device_operation_supervisor.
        Returns confirmation message.
        '''
        request_data = self.get_request_data()
        logging.debug(f"Received request data for device_operation_supervisor creation: {request_data}")

        if not request_data.get("agent_name"):
            logging.error("agent_name is required")
            response_dict = {"error": "agent_name is required"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for missing agent_name: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        if not request_data.get("agent_email"):
            logging.error("agent_email is required")
            response_dict = {"error": "agent_email is required"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for missing agent_email: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        if not request_data.get("agent_secret"):
            logging.error("agent_secret is required")
            response_dict = {"error": "agent_secret is required"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for missing agent_secret: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        if not request_data.get("confirmation_secret"):
            logging.error("confirmation_secret is required")
            response_dict = {"error": "confirmation_secret is required"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for missing confirmation_secret: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        if request_data.get("agent_secret") != request_data.get("confirmation_secret"):
            logging.error("agent_secret and confirmation_secret do not match")
            response_dict = {"error": "agent_secret and confirmation_secret do not match"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for mismatched secrets: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        # Validate email pattern
        if "@" not in request_data.get("agent_email") or "." not in request_data.get("agent_email"):
            logging.error("Invalid email format")
            response_dict = {"error": "Invalid email format"}
            # Construct response components
            response = json.dumps(response_dict) # Convert dict to JSON string
            logging.debug(f"Response for invalid email format: {response}")
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body

        agent_id = self.create_new_agent()
        device_operation_supervisor_id = self.create_device_operation_supervisor(agent_id,
                                            request_data.get("agent_email"),
                                            request_data.get("agent_name"),
                                            request_data.get("agent_surname"),
                                            request_data.get("agent_secret")
                                            )

        first_authentication_token = self.new_hash(agent_id, "device_operation_supervisor")

        # add token to first auth agents database
        self.insert_first_auth_agent(agent_id, first_authentication_token)

        # Send verification token via email
        self.email.send_device_operation_supervisor_token(first_authentication_token)

        response_dict = {"message": "Backuser created successfully. Please check your email for the verification token."}
        # Construct response components
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_device_operation_supervisor_enable(self):
        '''
        Enable device_operation_supervisor
        '''
        try:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Invalid token"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
        # Find agent_id from token
        try:
            hash_data = self.unhash(token)
            agent_id = hash_data["id"] if hash_data["agent_type"] == "device_operation_supervisor" else None
        except Exception as e:
            message = f"Error unhashing token: {str(e)}"
            logging.error(message)
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not match expected format or type"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

        if agent_id is None:
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not correspond to a device_operation_supervisor"}
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Validate token
        if not self.first_auth_token_is_valid(agent_id, token):
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token is not among first auth list"}
                             
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Enable agent
        try:
            self.db.run_script(self.script_update_agent__is_enabled, (agent_id,))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Delete first auth agent to prevent reuse of token
        if self.agent_is_enabled(agent_id):
            self.delete_first_auth_agent(agent_id)

        # Construct response components based on agent_type
        response_dict = {"agent_is_enabled": True}
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
        Validate request data:
         compare secret with second confirmation_secret,
         validate email pattern
         then check if customer_name and secret are in env var,
         then create a customer.
        Returns confirmation message.
        '''
        result = {}
        request_data = self.get_request_data()

        if not request_data.get("customer_name"):
            raise ValueError("customer_name is required")
        if not request_data.get("customer_email"):
            raise ValueError("customer_email is required")
        if not request_data.get("agent_secret"):
            raise ValueError("agent_secret is required")
        if not request_data.get("confirmation_secret"):
            raise ValueError("confirmation_secret is required")
        if request_data.get("agent_secret") != request_data.get("confirmation_secret"):
            raise ValueError("agent_secret and confirmation_secret do not match")
        # Validate email pattern
        if "@" not in request_data.get("customer_email") or "." not in request_data.get("customer_email"):
            raise ValueError("Invalid email format")       

        agent_id = self.create_new_agent()
        customer_id = self.create_customer(agent_id,
                                            request_data.get("customer_email"),
                                            request_data.get("customer_name"),
                                            request_data.get("customer_surname"),
                                            request_data.get("agent_secret")
                                            )

        first_authentication_token = self.new_hash(agent_id, "customer")

        # add token to first auth agents database
        self.insert_first_auth_agent(agent_id, first_authentication_token)

        # Send verification token via email
        self.email.send_customer_token(first_authentication_token)
     
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
        try:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Invalid token"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
        # Find agent_id from token
        try:
            hash_data = self.unhash(token)
            agent_id = hash_data["id"] if hash_data["agent_type"] == "customer" else None
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not match expected format or type"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

        if agent_id is None:
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not correspond to a customer"}
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Validate token
        if not self.first_auth_token_is_valid(agent_id, token):
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token is not among first auth list"}
                             
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Enable agent
        try:
            self.db.run_script(self.script_update_agent__is_enabled, (agent_id,))
        except Exception as e:
            logging.error(e)
            raise e
     
        # Delete first auth agent to prevent reuse of token
        if self.agent_is_enabled(agent_id):
            self.delete_first_auth_agent(agent_id)

        # Construct response components based on agent_type
        response_dict = {"agent_is_enabled": True}
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

        # REQUIRED FIELDS
        `device_strategy_id`

        # OPTIONAL FIELDS
        `supply_chain_id`
        `device_model_name`
        `require_config_update`
        `require_firmware_update`
        `device_name`
        `customer_id`
        `location`
        `max_session_length`
        `max_input_hertz`
        `consulting_services_cost`
        `regulatory_compliance_cost`
        `product_design_cost`
        `customer_service_cost`
        `advertising_cost`
        `sales_cost`
        `software_cost`
        `electronics_cost`
        `box_cost`
        `landscape_cost`
        `operational_cost`
        `logistics_cost`
        `installation_cost`
        `maintenance_cost`
        `total_price`
        `monthly_fee`
        `annual_fee`
        '''
        request_data = self.get_request_data()

        # required fields validation
        if not request_data.get("device_strategy_id"):
            response_dict = {"device_is_created": False,
                             "error": "device_strategy_id is required"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body

        if not request_data.get("supply_chain_id"):
            response_dict = {"device_is_created": False,
                             "error": "supply_chain_id is required"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 400
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

            return status, headers, body
        
        # optional fields warnings
        if not request_data.get("require_config_update") and not request_data.get("require_update"):
            logging.warning("require_config_update not provided")
        if not request_data.get("device_name"):
            logging.warning("device_name not provided")
        if not request_data.get("customer_id"):
            logging.warning("customer_id not provided")
        if not request_data.get("location"):
            logging.warning("location not provided")
        if not request_data.get("max_session_length"):
            logging.warning("max_session_length not provided")
        if not request_data.get("max_input_hertz"):
            logging.warning("max_input_hertz not provided")
        if not request_data.get("hardware_cost"):
            logging.warning("hardware_cost not provided")
        if not request_data.get("software_cost"):
            logging.warning("software_cost not provided")
        if not request_data.get("device_operation_supervisor_fee"):
            logging.warning("device_operation_supervisor_fee not provided")
        if not request_data.get("transport_fee"):
            logging.warning("transport_fee not provided")
        if not request_data.get("installation_fee"):
            logging.warning("installation_fee not provided")
        if not request_data.get("total_price"):
            logging.warning("total_price not provided")
        if not request_data.get("monthly_fee"):
            logging.warning("monthly_fee not provided")
        if not request_data.get("annual_fee"):
            logging.warning("annual_fee not provided")

        agent_id = self.create_new_agent()
        device_id = self.create_device(agent_id, request_data)

        first_authentication_token = self.new_hash(agent_id, "device")

        # add token to first auth agents database
        self.insert_first_auth_agent(agent_id, first_authentication_token)
     
        # Construct response components
        response_dict = {"device_is_created": True,
                         "device_id": device_id,
                         "first_authentication_token": first_authentication_token
                        }
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body

    @require_authentication
    @log_running_and_done
    def handle_patch_device_enable(self):
        '''
        Enable device
        '''
        try:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Invalid token"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
        # Find agent_id from token
        try:
            hash_data = self.unhash(token)
            agent_id = hash_data["id"] if hash_data["agent_type"] == "device" else None
        except Exception as e:
            logging.error(e)
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not match expected format or type"}
            response = json.dumps(response_dict) # Convert dict to JSON string
            
            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"

        if agent_id is None:
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token does not correspond to a device"}
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Validate token
        if not self.first_auth_token_is_valid(agent_id, token):
            # Construct response components based on agent_type
            response_dict = {"agent_is_enabled": False,
                             "error": "Token is not among first auth list"}
                             
            response = json.dumps(response_dict) # Convert dict to JSON string

            # Expected response variables
            status = 401
            headers = {"Content-Type": "application/json"}
            body = response + "\r\n"
        
            return status, headers, body

        # Enable agent
        try:
            self.db.run_script(self.script_update_agent__is_enabled, (agent_id,))
        except Exception as e:
            logging.error(e)
            raise e

        
        # Delete first auth agent to prevent reuse of token
        if self.agent_is_enabled(agent_id):
            # select device_secret
            try:
                result = self.db.run_query(self.script_select_device__device_secret, (agent_id,))
                device_secret = result[0]["device_secret"] if result else None
            except Exception as e:
                logging.error(e)
                raise e
            self.delete_first_auth_agent(agent_id)

        # Construct response components based on agent_type
        response_dict = {"agent_is_enabled": True,
                         "device_secret": device_secret}
        response = json.dumps(response_dict) # Convert dict to JSON string
    
        # Expected response variables
        status = 200
        headers = {"Content-Type": "application/json"}
        body = response + "\r\n"
    
        return status, headers, body