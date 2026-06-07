from interfaces.email.sync_email_sender import I_EmailSender

class EmailClient(I_EmailSender):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def send_admin_token(self, token):
        pass
    
    def send_device_operation_supervisor_token(self, token):
        pass
    
    def send_customer_token(self, token):
        pass
    
    def send_device_token(self, token):
        pass