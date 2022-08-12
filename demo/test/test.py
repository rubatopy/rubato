# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include
# distutils: language = c++

# To build: cythonize -3 -i test.py

import rubato.utils as util
from rubato import *

import sdl2.ext

import cython
from cython.cimports.cPixelEditor import setPixelRGB, getPixel, Bresenham # pyright: ignore
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
    if Input.mouse_pressed():
        x, y = Input.get_mouse_pos().tuple_int()  #TODO: make sure does not error OOB
        temp = SDL_MapRGB(surface.format, 255, 255, 255)
        # temp = cython.cast(cython.int, temp)

        # setPixelRGB(surface.pixels, width, x, y, temp)
        Bresenham(surface.pixels, width, 0, 0, x-1, y-1, temp)

    texture = sdl2.ext.Texture(Display.renderer, surface)
    Draw.queue_texture(texture, Vector(0,0))  #TODO: mention topleft indocs

mainS.update = update
begin()
