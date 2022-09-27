"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(10, 10), window_size=(2000, 2000))


def update():
    rb.Draw.queue_point((5, 5))
    rb.Draw.queue_line((0, 0), (2, 2))
    # rb.Draw.queue_rect((7, 7), 3, 3)
    # rb.Draw.queue_circle((5, 5), 3)
    # rb.Draw.queue_poly([v + rb.Display.center for v in rb.Vector.poly(5, 3)])


rb.Game.update = update

rb.begin()
