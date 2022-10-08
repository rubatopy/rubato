"""
A set of utility functions to help with debugging.
"""
import sys, traceback, math

from . import PrintError, Display, Time, Draw, Vector, Font, InitError


# THIS IS A STATIC CLASS
class Debug:
    """
    Useful static methods for debugging rubato projects.
    """

    def __init__(self) -> None:
        raise InitError(self)

    @staticmethod
    def _draw_fps(font: Font):
        """
        Draws the current FPS to the screen.
        Called automatically if `Game.show_fps` is True.

        Args:
            font: The font to use.
        """
        height: int = math.ceil(Display.res.y / 32)
        pad = max(height / 4, 1)

        scale = height / font.size

        Draw.text(
            str(Time.smooth_fps),
            font=font,
            pos=(pad, pad),
            align=Vector(1, 1),
            justify="center",
            scale=(scale, scale),
            shadow=True,
            shadow_pad=(pad, pad),
        )

    @staticmethod
    def find_my_print():
        """
        Will print the stack when it finds a print statement.
        Examples:
            Place this next to your rubato import.
            >>> Debug.find_my_print()
        """

        class TracePrints(object):

            def __init__(self):
                self.stdout = sys.stdout

            def write(self, _):
                traceback.print_stack(file=self.stdout)

            def flush(self):
                self.stdout.flush()

        sys.stdout = TracePrints()

    @staticmethod
    def error_my_print():
        """
        Will break the program if it finds a print statement.

        Examples:
            Place this next to your rubato import.
            >>> Debug.error_my_print()
        """

        class TracePrints(object):

            def __init__(self):
                self.stdout = sys.stdout

            def write(self, s):
                raise PrintError("Print statement found!")

            def flush(self):
                self.stdout.flush()

        sys.stdout = TracePrints()
