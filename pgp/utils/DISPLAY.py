from pygame import Surface
import os
import pygame.display as display


class DISPLAY:
    """Global display class that allows any file to access the displayed screen."""
    global_display = Surface((0, 0))

    @staticmethod
    def set(new_surface: Surface):
        """
        Set the global display.

        :param new_surface: The new surface to set.
        """
        DISPLAY.global_display = new_surface

    @staticmethod
    def display() -> Surface:
        return DISPLAY.global_display

    @staticmethod
    def update(surface: Surface, pos: (int, int)):
        DISPLAY.global_display.blit(surface, pos)

    @staticmethod
    def set_window_position(x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

    @staticmethod
    def set_window_name(name):
        display.set_caption(name)
