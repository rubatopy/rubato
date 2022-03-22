"""Helper functions for internal use only"""
from functools import wraps

class classproperty:  # pylint: disable=invalid-name
    """
    A class property that behaves by itself exactly as a normal property.
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        @wraps(self.fget)
        def wrapper(obj):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
        return wrapper

    def __set__(self, obj, value):
        @wraps(self.fset)
        def wrapper(obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(obj, value)
        return wrapper

    def __delete__(self, obj):
        @wraps(self.fdel)
        def wrapper(obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        return wrapper

    def __call__(self, *args, **kwargs):
        @wraps(self.fget)
        def wrapper(*args, **kwargs):
            return self.fget(*args, **kwargs)

        return wrapper

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class StaticClass(type):
    """
    A metaclass that overrides object creation to allow static properties
    """

    def __new__(mcs, name, bases, props):
        class_properties = {}
        for key, value in props.items():
            if isinstance(value, classproperty):
                class_properties[key] = value

        return type(name, (type,), class_properties)(name, bases, props)
