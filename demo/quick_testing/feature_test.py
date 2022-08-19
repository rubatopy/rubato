"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V

width, height = 256, 256
off = int(width / 8)

rb.init(res=V(width, height), window_size=V(width, height) * 20)
s = rb.Scene()

raster = rb.Raster(width, height, offset=V(width / 2, height / 2))
raster2 = rb.Raster(width, height, offset=V(width / 2, height / 2))


def update():
    raster.surf.clear()
    raster.surf.draw_poly(
        [v + rb.world_mouse().floor() for v in rb.Vector.poly(8, off)], rb.Color.blue, aa=True, blending=True
    )
    if rb.Input.mouse_pressed():
        raster2.merge(raster)


s.add(rb.wrap([raster2, raster]))
rb.Game.update = update

rb.begin()