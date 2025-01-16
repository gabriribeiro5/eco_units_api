from http.client import HTTPSConnection
import inspect

class I_BaseClient(HTTPSConnection):
    '''
    HTTPSConnection accepts the following parameters
        host: str,
        port: int | None = None,
        *,
        timeout: float | None = ...,
        source_address: tuple[str, int] | None = None,
        context: ssl.SSLContext | None = None,
        blocksize: int = 8192
    '''
    def __init__(self, request, host, port):
        super().__init__(request, host, port)

    ####               HTTP CALL METHODS                ####
    #### Those method will support future improvements. ####
    #### As the system evolves to microservices, those  ####
    #### methods will allow decoupling Business Rules   ####
    def match_method_with_route(self, calling_method):
        '''
        This method will support future improvements.
        As the system evolves to microservices, the method will allow:
            - Decoupling Business Rules
            - Finding and return the corresponding route for each calling method
        '''
        pass

    def call_route(self, route, *args, **kwargs):
        '''
        This method will support future improvements.
        As the system evolves to microservices, the method will:
        - Encode {data}
        - Send {encoded_data} to {route}
        - Await for response
        - Handle error responses
        - Return {encoded_data}
        '''
        pass

    def data_decoder(self, data, format):
        '''
        This method will support future improvements.
        As the system evolves to microservices, the method will:
        - decode {data} into {format}
        - return expected data
        '''
        pass
    
    def external_call(self, *args, **kwargs):
        # Find out calling method
        calling_method = None # TO DO
        route = self.match_method_with_route(calling_method)
        
        # Collect data from route
        if route:
            encoded_data = self.call_route(route, *args, **kwargs)
            data = self.data_decoder(encoded_data, **kwargs["data_type"])
        else:
            return None

        return data