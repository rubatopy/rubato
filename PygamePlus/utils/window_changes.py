import os
import pygame.display as display

def set_window_position(x, y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)


def set_window_name(name):
    display.set_caption(name)