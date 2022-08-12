# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include
# distutils: language = c++

# To build: cythonize -3 -i test.py

import rubato.utils as util
from rubato import *

import sdl2.ext

import cython
from cython.cimports.cPixelEditor import setPixel, getPixel, drawLine, drawCircle, fillCircle, fillRect, clearPixels # pyright: ignore

from sdl2 import SDL_MapRGB

# pylint: disable=all

width, height = 32, 32


init(res=Vector(width, height), window_size=Vector(width, height)*5)
mainS = Scene(background_color=Color(0,0,0))


surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0,
            width,
            height,
            32,
            util.pixel_format,
        ).contents

def update():
    radius = 10
    if Input.mouse_pressed():
        x, y = Input.get_mouse_pos().tuple_int()  #TODO: make sure does not error OOB
        green = SDL_MapRGB(surface.format, 0, 255, 128)
        red = SDL_MapRGB(surface.format, 255, 64, 64)

        clearPixels(surface.pixels, width, height)
        fillRect(surface.pixels, width, height, 0, 0, x, y, green)

        # test draw stuff here

    texture = sdl2.ext.Texture(Display.renderer, surface)
    Draw.queue_texture(texture, Vector(0,0))  #TODO: mention topleft indocs

mainS.update = update
begin()
