"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init()

main = rb.Scene()

gameobj = rb.GameObject()

raster = rb.Raster(
    width=32,
    height=32,
)
print(raster.get_pixel(0, 0))

gameobj.add(raster)
main.add(gameobj)

rb.begin()