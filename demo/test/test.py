# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include
# distutils: language = c++

# To build: cythonize -3 -i test.py

import rubato.utils as util
from rubato import *

import sdl2.ext

import cython
from cython.cimports.cPixelEditor import setPixelRGB, getPixel
from sdl2 import SDL_MapRGB

# pylint: disable=all

width, height = 32, 32


init(res=Vector(width, height))
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
        x,y = Input.get_mouse_pos()  #TODO: make sure does not error OOB
        x,y = int(x), int(y)
        temp = SDL_MapRGB(surface.format, 255, 255, 255)
        # temp = cython.cast(cython.int, temp)

        print(getPixel(surface.pixels, width, x, y), "start")
        setPixelRGB(surface.pixels, width, x, y, temp)
        print(getPixel(surface.pixels, width, x, y), "end")

    texture = sdl2.ext.Texture(Display.renderer, surface)
    Draw.queue_texture(texture, Vector(0,0))  #TODO: mention topleft indocs

mainS.update = update
begin()
