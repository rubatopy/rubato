# distutils: sources = PixelEditor.cpp
# distutils: include_dirs = SDL2/include
# distutils: language = c++

# To build: cythonize -3 -i test.py

import rubato as rb
import cython
from cython.cimports.cPixelEditor import setPixelRGB

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
    setPixelRGB(int(raster._raster.pixels), raster._raster.w, 10, 10, *(0, 0, 0))
    # setPixelRGB(100, 20, 10, 10, 0, 0, 0)


test()

gameobj.add(raster)
main.add(gameobj)

rb.begin()
