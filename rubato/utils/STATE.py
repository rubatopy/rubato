# pylint: disable=invalid-name
"""
A state tracker
"""
from enum import Enum


class STATE(Enum):
    """
    An enum to keep track of the state things
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3
