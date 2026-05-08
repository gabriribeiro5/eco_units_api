from config import Definitions
import logging

class I_SyncDBConnector():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Definitions()
        self.DB_HOST = self.config.DB_HOST
        self.DB_PORT = self.config.DB_PORT
        self.DB_USER = self.config.DB_USER
        self.DB_SECRET = self.config.DB_SECRET
        self.DB_NAME = self.config.DB_NAME
    
    def connect():
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    def run_script(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()

    def run_query(self):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
