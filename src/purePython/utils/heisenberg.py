import inspect

class WalterWhite():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def say_my_module(self):
        # Find the name of the calling module
        frm = inspect.stack()[1]  # The call's frame: filepath, code line, etc.
        mod = inspect.getmodule(frm[0])
        callingModule = inspect.getmodulename(mod.__file__)
        return callingModule

    def say_my_class(self):
        # Find the name of the calling method's class
        frm = inspect.stack()[1]  # The call's frame: filepath, code line, etc.
        cls = frm.frame.f_locals.get('self', None)
        if cls:
            return cls.__class__.__name__
        return None

    def say_my_name(self):
        # Find the calling method's name
        frm = inspect.stack()[1]  # The call's frame
        method_name = frm.function
        return method_name
