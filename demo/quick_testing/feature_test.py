"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V
import sdl2, sdl2.ext

width, height = 256, 256

rb.init(res=V(width, height), window_size=V(width, height) * 2)
s = rb.Scene()

raster = rb.Raster(width, height, offset=V(width / 2, height / 2))
img = raster.surf

img.clear()

img.draw_line(V(4, 3), V(28, 27), rb.Color.blue, aa=True, thickness=3, blending=True)


def update():
    if rb.Input.mouse_pressed():
        img.draw_point(rb.Input.get_mouse_pos(), rb.Color(32, 32, 32))


s.add(rb.wrap(raster))
rb.Game.update = update

rb.begin()