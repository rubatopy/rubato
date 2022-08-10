# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include/
# distutils: language = c++

# To build: cythonize -i test.py -3

import rubato as rb
import sdl2, cython
from cython.cimports.cPixelEditor import setPixelRGB

rb.init()

main = rb.Scene()

gameobj = rb.GameObject()

raster = rb.Raster(
    width=32,
    height=32,
)

# raster._raster.pixels is an int


setPixelRGB(raster._raster.pixels, raster._raster.w, 0, 0, 0, 0, 0)

gameobj.add(raster)
main.add(gameobj)

rb.begin()
