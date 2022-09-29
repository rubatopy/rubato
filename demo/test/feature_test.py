"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(32 * 3, 32 * 2), window_size=(1000, 1000))

c = rb.Camera()


def update():
    rb.Draw.queue_point((16, 16), camera=c)
    rb.Draw.queue_line((32, 0), (64, 31), camera=c)
    rb.Draw.queue_rect((64 + 16, 16), 32, 32, fill=rb.Color.red, camera=c)
    rb.Draw.queue_circle((16, 32 + 16), 16, fill=rb.Color.red, camera=c)
    # rb.Draw.queue_poly([v + rb.Vector(32 + 16, 32 + 16) for v in rb.Vector.poly(5, 16)], fill=rb.Color.red, camera=c)


rb.Game.update = update

rb.begin()
