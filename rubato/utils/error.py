"""
Some custom errors
"""

import warnings
import functools
import sys


class Error(Exception):
    """A basic rubato Error."""
    pass


class IdError(Exception):
    """An error that is raised when an invalid ID is used."""
    pass


class SideError(Exception):
    """An error that is raised when the number of sides is invalid"""
    pass


class DuplicateComponentError(Exception):
    """
    An error that is raised when you try to add a component to a game object
    that already has a component of the same type
    """
    pass


class ComponentNotAllowed(Exception):
    """
    An error that is raised when you try to add a component on a game object that
    is not allowed by another component on that game object.
    """
    pass


class RemovalWarning(DeprecationWarning):
    """
    A warning that is raised when you try to use a removed function.
    """
    pass


def deprecated(other_func=None):
    """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used."""

    def wrapper(func):
        @functools.wraps(func)
        def new_func(*_args, **_kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(func.__name__ + " has been deprecated. " + "please use " +
                          other_func.__name__ + " instead." if other_func else "There will be no replacement.",
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*_args, **_kwargs)

        return new_func

    return wrapper


def removed(other_func=None):
    """This is a decorator which can be used to mark functions
        as removed, they will no longer work."""

    def wrapper(func):
        def new_func(*_args, **_kwargs):
            warnings.simplefilter('always', RemovalWarning)
            warnings.warn(func.__name__ + " has been removed. " + "please use " +
                          other_func.__name__ + " instead." if other_func else "There is no replacement.",
                          category=RemovalWarning,
                          stacklevel=2)
            sys.exit()

        return new_func

    return wrapper
