import datetime

class I_AgentInput():
    def __init__(self) -> None:
        self.agent_input_id:int
        self.agent_id:int
        self.eco_unit_id:int
        self.date_time:datetime.datetime
        self.failed_communication:bool
        self.allowed_tables = None # This interface can not be used alone



class I_EcoUnitInput(I_AgentInput):
    def __init__(self, *args, **kwargs) -> None:
        I_AgentInput.__init__(self, *args, **kwargs)

class I_CustomerInput(I_AgentInput):
    def __init__(self, *args, **kwargs) -> None:
        I_AgentInput.__init__(self, *args, **kwargs)

class I_BackUserInput(I_AgentInput):
    def __init__(self, *args, **kwargs) -> None:
        I_AgentInput.__init__(self, *args, **kwargs)

class I_BackUserAdminInput(I_AgentInput):
    def __init__(self, *args, **kwargs) -> None:
        I_AgentInput.__init__(self, *args, **kwargs)

class I_SystemAdminInput(I_AgentInput):
    def __init__(self, *args, **kwargs) -> None:
        I_AgentInput.__init__(self, *args, **kwargs)