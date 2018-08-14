# Wrap-Logger

Lightweight python logger extension providing logging capabilities via decorators.

## Examples

Note, for examples to work. The logging.basicConfig method should be called with level=logging.DEBUG. You also need to set the logger class via the logging.setLoggerClass method to wrap_logger.logger.Logger

### Log a message regularly

```python
logger = logging.getLogger(__name__)
logger.info('Hello World!')
```        
    
> INFO:__main__:Hello World!
        
### Decorate a function to log upon call
        
```python
logger = logging.getLogger(__name__)
        
@logger.wrap_info('Hello World!')
def foo(): 
    pass
        
foo() # Will now log hello world
foo() # Will log hello world again
```

> INFO:__main__:Hello World!
> INFO:__main__:Hello World!

### Updating a loggers name upon the execution of a method

```python
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
```

> DEBUG:Foo:I'm Outputting From Foo
> INFO:Bar:I'm Outputting From Bar
> DEBUG:Foo:I'm Outputting From Foo
    
### Logging Upon The Entry Of a Function

```python
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
```
    
> DEBUG:__main__:Program Started
> DEBUG:foo:Entered Method foo With (<__main__.FooBar object at 0x000000555CAA1710>, 1, 2, )
> DEBUG:bar:Entered Method bar With (<__main__.FooBar object at 0x000000555CAA1710>, 2, 1, )
> DEBUG:bar:Exited Method bar With 3
> DEBUG:foo:Exited Method foo With 3
> DEBUG:__main__:Program Ending