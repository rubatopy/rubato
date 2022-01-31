"""
Global display class that allows any file to access the
displayed screen.
"""
from pygame import Surface, display
import os

global_display = Surface((0, 0))


def set_display(new_surface: Surface):
    """
    Set the global display.

    Args:
        new_surface: The new surface to set.
    """
    global global_display
    global_display = new_surface


def update(surface: Surface, pos: tuple):
    """
    Update the current display.

    Args:
        surface: The surface to draw on the display.
        pos: The position to draw the surface on.
    """
    global_display.blit(surface, pos)


def set_window_position(x: int, y: int):
    """
    Set the position of the Pygame window.

    Args:
        x: The x position.
        y: The y position.
    """
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x}, {y}"


def set_window_name(name: str):
    """
    Set the title of the PyGame window.

    Args:
        name: The name of the PyGame window.
    """
    display.set_caption(name)
