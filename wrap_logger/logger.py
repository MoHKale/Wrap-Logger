import logging
from functools import wraps
from types import MethodType
from ._decorators import WrapLoggerDecorators

class Logger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call parent constructor to initialise generic logger attributes
        levels = list(map(lambda X: X.lower(), filter(lambda X: X != 'NOTSET', logging._levelToName.values())))
        
        for level_key in levels:
            def decorator_method(self, *args, **kwargs):
                pass # Define Empty Decorator Method
            
            decorator_method = WrapLoggerDecorators.bind_level_key(level_key)(decorator_method)
            setattr(self, f'wrap_{level_key}', MethodType(decorator_method, self)) # as method
            
    def wrap__name(self, new_name):
        return WrapLoggerDecorators.do_before_func(lambda: self.set_name(new_name))
        
    def wrap__entry(self, log_level_key='DEBUG', new_name=None):
        previous_name = self.name # store before updating if new_name is not None
        
        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                if self.disabled: return func(*args, **kwargs) # When Disabled
                else: # Only bother going through  tasking operations when logging
                    formatted_params = self.format_params(*args, **kwargs) # Format inputted parameters
                    
                    self.make_log(log_level_key, f'Entered Method {func.__name__} With {formatted_params}')
                    if new_name is not None: self.set_name(new_name) # then update name to argument name
                    
                    return_value = func(*args, **kwargs) # Call argument function after logging entry
                    
                    if new_name is not None: self.set_name(previous_name) # Then revert to previous name
                    self.make_log(log_level_key, f'Exited Method {func.__name__}') # State function exit
                    
                    return return_value # Give result of function call after making logs
            return wrapped
        return decorator
    
    def set_name(self, new_name):
        self.name = new_name
        
    @classmethod
    def format_params(*args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0: return '()' # is empty, I.E. No arguments
        else:
            formatted_kwargs = ", ".join(f"{key}={repr(value)}" for key, value in kwargs.items())
            formatted_args   = ', '.join(map(repr, args)) # List of argument/s representations
            return f'({formatted_args}, {formatted_kwargs})' # Format with non-kwargs first

    def make_log(self, level_key:str, *args, **kwargs):
        return getattr(self, level_key.lower())(*args, **kwargs)






