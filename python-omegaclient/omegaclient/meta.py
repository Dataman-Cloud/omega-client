"""
This files contains all meta-class that will be used in this project.
"""
from types import FunctionType


class MetaAPI(type):
    """Meta class"""

    def __init__(cls, name, bases, dict):
        super(MetaAPI, cls).__init__(name, bases, dict)
        
        try:
            cls._handlers = cls._handlers.copy()
        except AttributeError:
            cls._handlers = {}

        for name, value in cls.__dict__.items():
            if isinstance(value, FunctionType):
                cls._handlers[name] = value
