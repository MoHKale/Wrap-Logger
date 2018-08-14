import logging
from functools import wraps
from types import MethodType
from ._decorators import WrapLoggerDecorators

class Logger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call parent constructor to initialise generic logger attributes
        