# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include
# distutils: language = c++

# To build: cythonize -3 -i test.py
# import test_surfaces.py

import rubato as rb
import cython
from cython.cimports.cPixelEditor import setPixelRGB
from sdl2 import SDL_MapRGB

rb.init()

main = rb.Scene()

gameobj = rb.GameObject()

raster = rb.Raster(
    width=32,
    height=32,
)

# raster._raster.pixels is an int


@cython.cfunc
def test():
    temp = SDL_MapRGB(raster._raster.format, 20, 20, 20)
    setPixelRGB(raster._raster.pixels, raster._raster.w, 10, 10, temp)
    # setPixelRGB(100, 20, 10, 10, 0, 0, 0)


test()

gameobj.add(raster)
main.add(gameobj)

rb.begin()
