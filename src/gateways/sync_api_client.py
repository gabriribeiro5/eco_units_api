from http.client import HTTPSConnection
import inspect

class MicroserviceClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None

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
        try:
            self.conn = HTTPSConnection(self.host, self.port)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port}. Error: {e}")
            
        self.conn.request(method=kwargs.get("method"),
                          url=route,
                          headers=dict(kwargs.get("headers", {})),
                          body=kwargs.get("body")
                          )
        
        response = self.conn.getresponse()
        if response.status != 200:
            raise ValueError(f"External call failed with status {response.status}: {response.reason}")
        return response


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