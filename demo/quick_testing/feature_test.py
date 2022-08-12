"""A place to test new WIP features"""  # pylint: disable=all
import ctypes
import rubato as rb
import sdl2, sdl2.ext

rb.init(res=rb.Vector(32, 32), window_size=rb.Vector(32, 32) * 10)

s = rb.Scene()

img = rb.Raster()

img.draw_point(rb.Vector(0, 0), rb.Color(255, 0, 0))

s.add(rb.wrap(img, pos=rb.Vector(16, 16)))

rb.begin()