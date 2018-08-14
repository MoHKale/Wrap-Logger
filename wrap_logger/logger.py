import logging
from functools import wraps
from types import MethodType
from ._decorators import WrapLoggerDecorators

class Logger(logging.Logger):
    """Logger Class Supporting Logging During Function Decoration. Basically Syntactic Sugar.
    
    Notes
    ----
        For each log level in the current logger scope, a wrapper method will be defined at construction.
    
        IMPORTANT: Before you can do anything, you must assign the logger class. logging.setLoggerClass(Logger).
    
    Example
    -------
    Note, for examples to work. The logging.basicConfig method should be called with level=logging.DEBUG.
    
    Log a message at debug level
        
            logger = logging.getLogger(__name__)
            logger.info('Hello World!')
            
    Decorate a function to log upon call
            
            logger = logging.getLogger(__name__)
            
            @logger.wrap_info('Hello World!')
            def foo(): 
                pass
            
            foo() # Will now log hello world
            foo() # Will log hello world again
    
    Updating a loggers name upon the execution of a method
    
        logger = logging.getLogger(__name__)
        
        @logger.wrap__name('Foo')
        @logger.wrap_debug('I\'m Outputting From Foo')
        def foo():
            pass
            
        @logger.wrap__name('Bar')
        @logger.wrap_info('I\'m Outputting From Bar')
        def bar():
            pass

        foo()
        bar()
        foo()
        
        >>> DEBUG:Foo:I'm Outputting From Foo
        >>> INFO:Bar:I'm Outputting From Bar
        >>> DEBUG:Foo:I'm Outputting From Foo
        
    Logging Upon The Entry Of a Function
    
        logger = logging.getLogger(__name__)
    
        class FooBar(object):
            @logger.wrap__entry(new_name='foo')
            def foo(self, arg1, arg2):
                return self.bar(arg2, arg1)
                
            @logger.wrap__entry(new_name='bar')
            def bar(self, arg1, arg2):
                return arg1 + arg2
        
        logger.debug('Program Started')
        
        foobar = FooBar() # Create Instance
        foobar.foo(1, 2) # Call method foo
        
        logger.debug('Program Ending')
        
        >>> DEBUG:__main__:Program Started
        >>> DEBUG:foo:Entered Method foo With (<__main__.FooBar object at 0x000000555CAA1710>, 1, 2, )
        >>> DEBUG:bar:Entered Method bar With (<__main__.FooBar object at 0x000000555CAA1710>, 2, 1, )
        >>> DEBUG:bar:Exited Method bar With 3
        >>> DEBUG:foo:Exited Method foo With 3
        >>> DEBUG:__main__:Program Ending
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call parent constructor to initialise generic logger attributes
        levels = list(map(lambda X: X.lower(), filter(lambda X: X != 'NOTSET', logging._levelToName.values())))
        
        for level_key in levels:
            def decorator_method(self, *args, **kwargs):
                pass # Define Empty Decorator Method
            
            decorator_method = WrapLoggerDecorators.bind_level_key(level_key)(decorator_method)
            setattr(self, f'wrap_{level_key}', MethodType(decorator_method, self)) # as method
            
    def wrap__name(self, new_name: str):
        """Updates Logger Name Before Running A Given Function
        
        Parameters
        ----------
        new_name : str
            Name That Logger Should Be Changed To.
        
        Returns
        -------
        func
            Decorator Method Which Performs The Desired Function After Changing Name"""
        return WrapLoggerDecorators.do_before_func(lambda: self.set_name(new_name))
        
    def wrap__entry(self, log_level_key='DEBUG', new_name=None):
        previous_name = self.name # store before updating if new_name is not None
        
        Parameters
        ----------
        log_level_key : str
            Level at which to log when entering and exiting the given function.
        new_name : str
            Optional parameter, which when None, will change the name of the logger
            during execution of the given method before returning to its value prior
            to the execution of the function."""    
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
        """Logs at a given log level (represented as a string)"""
        return getattr(self, level_key.lower())(*args, **kwargs)
