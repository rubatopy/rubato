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


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(f"Call to deprecated function {func.__name__}.",
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def removed(func, other_func=None):
    """This is a decorator which can be used to mark functions
    as removed, they will no longer work."""
    def new_func(*args, **kwargs):
        warnings.warn(f"{func.__name__} has been removed. "
                      f"{'use ' + other_func.__name__ + ' instead.' if other_func else 'There is no replacement.'}",
                      category=DeprecationWarning,
                      stacklevel=2)
        sys.exit()
    return new_func
