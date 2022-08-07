"""
This Debug module provides a set of functions to help with debugging.
"""
import sys, traceback

from . import PrintError, Display, Time, Draw, Vector, Color, Font


class Debug:
    """
    Debug comes with useful functions to help with debugging.
    """

    @staticmethod
    def draw_fps(font: Font):
        fs = str(Time.smooth_fps)
        h = int(Display.res.y) >> 5
        p = h // 2
        Draw.rect(
            Vector(p + (h * len(fs)) / 2, p + h / 2),
            h * len(fs) + p,
            h + p,
            Color(a=200),
            fill=Color(a=200)
        )
        Draw.text(fs, font=font, pos=Vector(p + 4, p + 3), align=Vector(1, 1))

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
