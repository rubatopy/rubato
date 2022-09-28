"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(10, 10), window_size=(2000, 2000))

a = rb.Surface(2, 2)
a.fill(rb.Color(255, 0, 0))


def update():
    rb.Draw.queue_surface(a, (5, 5))


rb.Game.update = update

rb.begin()
