from logging import Logger
from functools import wraps

class WrapLoggerDecorators(object):
    """Class Containing Decorators Useful To"""
    @classmethod
    def bind_level_key(cls, level_key):
        """Makes log to at desired level before a functions executes"""
        #Note Decorator is two fold. Outer Decorator for log-data, Inner for func-data
        def decorator(func):
            @wraps(func)
            def wrapped(logger, *logger_args, **logger_kwargs):
                #Note: First Decorator & Wrapped Methods Store Level Key & Logger Data
                
                #Note Second Decorator & Wrapped Methods Run Actual Func & Log Actual Data
                def decorator2(func2):
                    @wraps(func2)
                    def wrapped2(*args, **kwargs):
                        logger.make_log(level_key, *logger_args, **logger_kwargs)
                        
                        return func2(*args, **kwargs) # Give result of initial function
                    return wrapped2
                return decorator2
                #endregion
            
            return wrapped
        return decorator
    
    #region Do Decorators
    @classmethod
    def do_before_func(cls, executable):
        """Runs a given function with no parameters before returning a function"""
        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                executable() # Execute Here
                return func(*args, **kwargs)
            return wrapped
        return decorator
    
    @classmethod
    def do_after_func(cls, executable):
        """Runs a given function with no parameters after returning a function"""
        def decorator(func):
            @wraps(func)
            def wrapped(*args, **kwargs):
                return_val=func(*args, **kwargs)
                executable() # Execute Func Here
                return return_val # Send to caller
            return wrapped
        return decorator
    #endregion
    
    