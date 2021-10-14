from pygame import Surface
import os
import pygame.display as display
from pgp.utils import classproperty, check_types


class Display:
    """Global display class that allows any file to access the displayed screen."""
    global_display = Surface((0, 0))

    @staticmethod
    def set(new_surface: Surface):
        """
        Set the global display.

        :param new_surface: The new surface to set.
        """
        check_types(Display.set, locals())
        Display.global_display = new_surface

    @classproperty
    def display(self) -> Surface:
        """The current display"""
        return Display.global_display

    @staticmethod
    def update(surface: Surface, pos: tuple):
        """
        Update the current display.

        :param surface: The surface to draw on the display.
        :param pos: The position to draw the surface on.
        """
        check_types(Display.update, locals())
        Display.global_display.blit(surface, pos)

    @staticmethod
    def set_window_position(x: int, y: int):
        """
        Set the position of the Pygame window.

        :param x: The x position
        :param y: The y position
        """
        check_types(Display.set_window_position, locals())
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

    @staticmethod
    def set_window_name(name: str):
        """
        Set the title of the PyGame window.

        :param name: The name of the PyGame window.
        """
        check_types(Display.set_window_name, locals())
        display.set_caption(name)
