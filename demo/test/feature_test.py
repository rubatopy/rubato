"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb

rb.init(res=(100, 100), window_size=(2000, 2000))

rb.Scene()

a = rb.Surface.from_file("../files/dino/idle.png")
print(a.width, a.height)

a.set_colorkey(rb.Color(77, 146, 188))

b = rb.Surface(24, 24)
b.blit(a, (0, 0, 24, 24), (0, 0, 12, 12))


def draw():
    rb.Draw.queue_surface(a, rb.Display.center)
    rb.Draw.queue_line((0, 0), rb.world_mouse(), rb.Color.red, 3)
    rb.Draw.queue_circle(rb.world_mouse(), 10, rb.Color.green, 4)
    rb.Draw.queue_rect(rb.world_mouse(), 30, 30, rb.Color.blue, 2)
    rb.Draw.queue_poly(rb.Vector.poly(5, 10), rb.world_mouse(), rb.Color.yellow, 2)


rb.Game.draw = draw

rb.begin()
