"""
Some custom errors
"""


class Error(Exception):
    """A basic rubato Error."""
    pass


class IdError(Exception):
    """An error that is raised when an invalid ID is used."""
    pass


class SideError(Exception):
    """An error that is raised when the number of sides is invalid"""
    pass
