"""
Custom errors for rubato.
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


class RemovalWarning(DeprecationWarning):
    """
    A warning that is raised when you try to use a removed function.
    """
    pass


def deprecated(other_func):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """

    def wrapper(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                f"{func.__name__} has been deprecated. " + f"Please use {other_func.__name__} instead.",
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return new_func

    wrapper.__doc__ = """Warning:\n\tDeprecated.\n""" + other_func.__doc__
    wrapper.__dict__.update(other_func.__dict__)
    return wrapper


def deprecated_no_replacement(func):
    """
    This is a decorator which can be used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            f"{func.__name__} has been deprecated. No replacement.", category=DeprecationWarning, stacklevel=2
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    new_func.__doc__ = """Warning:\n\tDeprecated.\n""" + func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


def removed(other_func=None):
    """
    This is a decorator which can be used to mark functions as removed, they will no longer work.
    """

    def wrapper(func):

        def new_func(*_, **__):
            warnings.simplefilter("always", RemovalWarning)
            warnings.warn(
                f"{func.__name__} has been removed. " +
                (f"Please use {other_func.__name__} instead." if other_func else "There is no replacement."),
                category=RemovalWarning,
                stacklevel=2
            )
            sys.exit()

        return new_func

    wrapper.__name__ = other_func.__name__ if other_func else "[removed function]"
    wrapper.__doc__ = other_func.__doc__
    wrapper.__dict__.update(other_func.__dict__)
    return wrapper
