"""
This Debug module provides a set of functions to help with debugging.
"""
from typing import List, Optional

from . import Draw, Vector, Color, Font


class Debug:
    """
    This class is a Draw copy that will queue all commands to the end of the current frame.
    """
    message_draw = "Debug draws last in the draw loop"
    _queue = []

    # -------------------------------------------------------------------------------------------------------------/Draw
    @staticmethod
    def point(pos: Vector, color: Color = Color.green):
        Debug.point.__doc__ = Debug.message_draw + Draw.point.__doc__
        Debug._queue.append(lambda: Draw.point(pos, color))

    @staticmethod
    def line(p1: Vector, p2: Vector, color: Color = Color.green, width: int = 1):
        Debug.line.__doc__ = Debug.message_draw + Draw.line.__doc__
        Debug._queue.append(lambda: Draw.line(p1, p2, color, width))

    @staticmethod
    def rect(
        center: Vector,
        width: int,
        height: int,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        angle: float = 0
    ):
        Debug.rect.__doc__ = Debug.message_draw + Draw.rect.__doc__
        Debug._queue.append(lambda: Draw.rect(center, width, height, border, border_thickness, fill, angle))

    @staticmethod
    def circle(
        center: Vector,
        radius: int = 4,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None
    ):
        Debug.circle.__doc__ = Debug.message_draw + Draw.circle.__doc__
        Debug._queue.append(lambda: Draw.circle(center, radius, border, border_thickness, fill))

    @staticmethod
    def poly(
        points: List[Vector], border: Color = Color.green, border_thickness: int = 1, fill: Optional[Color] = None
    ):
        Debug.poly.__doc__ = Debug.message_draw + Draw.poly.__doc__
        Debug._queue.append(lambda: Draw.poly(points, border, border_thickness, fill))

    @staticmethod
    def text(
        text: str, font: Font, pos: Vector = Vector(), justify: str = "left", align: Vector = Vector(), width: int = 0
    ):
        Debug.text.__doc__ = Debug.message_draw + Draw.text.__doc__
        Debug._queue.append(lambda: Draw.text(text, font, pos, justify, align, width))

    # -------------------------------------------------------------------------------------------------------------Draw\

    # ------------------------------------------------------------------------------------------------------------/Queue
    @staticmethod
    def clear_queue():
        """
        Runs and clears the queue of all commands.
        """
        for command in Debug._queue:
            command()
        Debug._queue.clear()

    # ------------------------------------------------------------------------------------------------------------Queue\
