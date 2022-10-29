"""
Custom errors for rubato.
"""
import warnings
import functools
from typing import Callable


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


class ImplementationError(Exception):
    """
    An error that is raised when you incorrectly implement something in rubato.
    """
    pass


class PrintError(Exception):
    """
    An error that is raised when you try to print something, and are checking for it with Debug.
    """
    pass


class InitError(Exception):
    """
    An error that is raised when you try to initialize a static class.

    Args:
        classObject: The static class.
    """

    def __init__(self, classObject: object):
        super().__init__(f"{classObject.__class__.__name__} is a static class and cannot be initialized.")


class RemovedError(Exception):
    """
    An error that is raised when you try to use a removed function.
    """
    pass


def deprecated(deprecated_ver: str, removal_ver: str = "", other_func: Callable | None = None):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.

    Args:
        deprecated_ver: The version that the function was deprecated in (without the v, i.e. "1.0.0").
        removal_ver: The version that the function will be removed in (without the v, i.e. "1.0.0"). Use an empty
            string if there are no removal plans yet. Defaults to "".
        other_func: The function that replaces the deprecated function. Defaults to None.
    """
    replacement_msg = f"Please use {other_func.__qualname__}() instead." if other_func else "There is no replacement."
    removal_msg = f"It will be removed in version {removal_ver}. " if removal_ver != "" else ""

    def wrapper(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"{func.__qualname__}() is deprecated since version {deprecated_ver}. {replacement_msg}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)

        new_func.__doc__ = f"Warning:\n\tThis function is depricated since version {deprecated_ver}. {removal_msg}" + \
            f"{replacement_msg}\n{func.__doc__}"
        return new_func

    return wrapper


def removed(removed_ver: str, other_func: Callable | None = None):
    """
    This is a decorator which can be used to mark functions as removed, they will no longer work.

    Args:
        removed_ver: The version that the function was removed in (without the v, i.e. "1.0.0").
        other_func: The function that replaces the removed function. Defaults to None.
    """
    replacement_msg = f"Please use {other_func.__qualname__}() instead." if other_func else "There is no replacement."

    def wrapper(func):

        @functools.wraps(func)
        def new_func(*_, **__):
            raise RemovedError(f"{func.__qualname__}() is removed since version {removed_ver}. {replacement_msg}",)

        new_func.__doc__ = f"This function is removed since version {removed_ver}. {replacement_msg}"
        return new_func

    return wrapper
