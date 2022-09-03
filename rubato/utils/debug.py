"""
A set of utility functions to help with debugging.
"""
import sys, traceback

from . import PrintError, Display, Time, Draw, Vector, Font, InitError, Color


# THIS IS A STATIC CLASS
class Debug:
    """
    Useful static methods for debugging rubato projects.
    """

    def __init__(self) -> None:
        raise InitError(self)

    @staticmethod
    def draw_fps(font: Font):
        """
        Draws the current FPS to the screen.
        Called automatically if `Game.show_fps` is True.

        Args:
            font: The font to use.
        """
        fps = str(Time.smooth_fps)
        h = int(Display.res.y) >> 5  # 1/32 of the screen height
        p = h // 2  # distance from edge to start of text and half font size (scaled)
        scale = h / font.size  # scale to get the text to the right size
        center = Vector(p + (len(fps) * p), 2 * p)
        Draw.rect(center, (len(fps) * h) + p, h + p, fill=Color(a=200))
        Draw.text(
            fps,
            font=font,
            pos=center,
            align=Vector(0, 0),
            justify="center",
            scale=(scale, scale),
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
