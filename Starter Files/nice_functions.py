import os
import pygame
from cool_code_library import *

@register
def set_window_position(x, y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

@register
def set_window_name(name):
    pygame.display.set_caption(name)

