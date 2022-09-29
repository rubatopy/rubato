"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(100, 100), window_size=(2000, 2000))

a = rb.Surface.from_file("../files/dino/idle.png")
print(a.width, a.height)

a.set_colorkey(rb.Color(77, 146, 188))

b = rb.Surface(24, 24)
b.merge(a, (0, 0, 24, 24), (0, 0, 12, 12))


def update():
    rb.Draw.queue_surface(a, rb.Display.center)


rb.Game.update = update

rb.begin()
