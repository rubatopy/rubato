"""
This module houses all the utils
"""
import sys
import traceback
from typing import Any


def raise_error(exc: Exception, msg: str, traceback_remove: int = 2):
    traceback.print_stack(limit=-(len(traceback.extract_stack()) - traceback_remove))
    sys.tracebacklimit = 0
    raise exc(msg)


def raise_operator_error(op: str, obj1: Any, obj2: Any):
    raise_error(
        TypeError, f"unsupported operand type(s) for {op}: '{type(obj1).__name__}' and '{type(obj2).__name__}'", 3
    )


# pylint: disable=wrong-import-position
from .path import *
from .error import *
from .rb_math import Math
from .noise import Noise
from .vector import Vector
from .display import Display
from .color import Color
from .font import Font
from .draw import Draw, DrawTask
from .rb_time import DelayedTask, FramesTask, ScheduledTask, Time
from .rb_input import Input
from .sound import Sound
from .debug import Debug
from .radio import Radio, Events
from .camera import Camera
