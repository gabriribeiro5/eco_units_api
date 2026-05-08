class I_EmailSender():    
    def send_admin_token(self, token):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    def send_backuser_token(self, token):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    def send_customer_token(self, token):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()
    
    def send_device_token(self, token):
        # This method must be implemented where the connection library is called
        raise NotImplementedError()