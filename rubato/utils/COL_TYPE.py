# pylint: disable=invalid-name
"""
The collision type
"""
from enum import Enum


class COL_TYPE(Enum):
    ELASTIC = 1
    STATIC = 2
