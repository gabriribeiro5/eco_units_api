from use_cases.shared.auth.sessions import SessionManager as Sessions
import uuid
from datetime import datetime
from urllib.parse import parse_qs
import logging
import json

class AuthHandler(Sessions):
    '''
    - Quem és tú, Jaburu?
    - Atribuir label (Customer, Unit, etc)
    - Solicitar criação de token
    - Retorna o token
    '''
    def __init__(self, *args, **kwargs) -> None:
        self.FIRST_AUTH_DEVICES = {}
        self.ALLOWED_DEVICES = {}
        self.SESSION_TOKENS = {}
        super().__init__(*args, **kwargs)

    def update_first_auth_devices(self):
        '''
        This function must update the FIRST_AUTH_DEVICES dictionary by fetching the latest data from the database.
        '''
        db_first_auth_devices = {"new_client_id_hash": "some_secret token"}
        self.FIRST_AUTH_DEVICES = db_first_auth_devices

    def update_allowed_devices(self):
        '''
        This function must update the ALLOWED_DEVICES dictionary by fetching the latest data from the database.
        '''
        db_allowed_devices = {"client_id_hash": "my_secret_token", "other_client_id_hash": "not_my_token"}
        self.ALLOWED_DEVICES = db_allowed_devices

    def update_session_tokens(self):
        '''
        This function must update the SESSION_TOKENS dictionary by fetching the latest data from the database.
        '''
        db_session_tokens = {"client_id_hash": "my_secret_token"}
        self.SESSION_TOKENS = db_session_tokens

    def get_device_id(self, device_id_hash):
        # Retrieve device_id based on the hash
        # TODO: look up the hash in a database
        device_id_mapping = {
            "new_client_id_hash": "new_client_id",
            "client_id_hash": "existing_client_id",
            "other_client_id_hash": "other_existing_client_id"
        }
        
        device_id = device_id_mapping.get(device_id_hash, None)

        if device_id:
            logging.debug(f"Device ID {device_id} found for hash {device_id_hash}.")
        else:
            logging.warning(f"No device ID found for hash {device_id_hash}.")

        return device_id

    def handle_device_first_auth(self):
        '''
        Handles the first authentication step for a client device.
        1. Validates the provided device_id against FIRST_AUTH_DEVICES.
        2. If device_id is valid, returns its token and moves it to ALLOWED_DEVICES.
        '''
        
        device_id_hash = self.get_request_data().get("device_id_hash", None).lower()
        device_id = self.get_device_id(device_id_hash) if device_id_hash else "all"
        
        # Validate device_id
        try:
            if device_id in self.FIRST_AUTH_DEVICES:
                # Move item to allowed devices
                # TODO: this item must be saved to a database
                self.ALLOWED_DEVICES[device_id] = self.FIRST_AUTH_DEVICES[device_id]
                logging.info(f"Device {device_id} added to allowed devices.")
                
                del self.FIRST_AUTH_DEVICES[device_id]
                logging.info(f"Device {device_id} removed from first auth devices.")
                
                return self.ALLOWED_DEVICES[device_id]
            else:
                logging.warning(f"Device ID {device_id} not found in first auth devices.")
                return None
            
        except Exception as e:
            logging.error(f"Error during first authentication for {device_id}: {str(e)}")
            return None
        
    def handle_device_login(self):
        '''
        Handles the login process for a client device.
        1. Validates the provided id and token against ALLOWED_DEVICES..
        2. Get and return a new session ID to the client for future authenticated requests.
        '''
        
        request_data = self.get_request_data()
        device_id_hash = request_data.get("device_id_hash", None).lower()
        
        device_id = self.get_device_id(device_id_hash) if device_id_hash else "all"
        auth_header = self.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1].lower()

        # update ALLOWED_DEVICES by hitting database
        self.update_allowed_devices()
        
        # Validate device_id and token
        try:
            if device_id in self.ALLOWED_DEVICES and self.ALLOWED_DEVICES[device_id] == token:
                # Get and return a new session ID.
                # TODO: this item must be saved to a database
                logging.info(f"Device {device_id} authenticated successfully.")                
                return self.new_session_id(client_label="cyclobot")
            else:
                logging.warning(f"Device ID {device_id} not found in first auth devices.")
                return None
            
        except Exception as e:
            logging.error(f"Error during first authentication for {device_id}: {str(e)}")
            return None
    

    def is_authenticated(self):
        '''
        Validates the session token provided in the Authorization header of the request.
        Returns True if the token is valid and corresponds to an active session, otherwise returns False.
        '''
        try:
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                self.update_session_tokens()
                if token in self.SESSION_TOKENS.values():
                    return True
                logging.warning(f"Unauthorized access attempt with token: {token}")
                return False
            logging.warning("Unauthorized access attempt without valid Authorization header.")
            return False
        except Exception as e:
            logging.error(f"Error during authentication: {str(e)}")
            return False
