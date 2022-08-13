"""A place to test new WIP features"""  # pylint: disable=all
import ctypes
import rubato as rb
import sdl2, sdl2.ext

rb.init(res=rb.Vector(32, 32), window_size=rb.Vector(32, 32) * 20)
s = rb.Scene()

img = rb.Surface(32, 32)

sdl2.ext.fill(img.surf, sdl2.ext.Color(0, 0, 0))

img.clear()
img.draw_line(rb.Vector(4, 4), rb.Vector(28, 28), rb.Color.blue, width=3)
img.draw_line(rb.Vector(4, 4), rb.Vector(28, 28), rb.Color.red, width=1)
img.draw_rect(rb.Vector(0, 0), rb.Vector(32, 32), rb.Color.purple, width=3)
img.draw_rect(rb.Vector(0, 0), rb.Vector(32, 32), rb.Color.red, width=1)

print(img.get_pixel(rb.Vector(4, 4)))
print(img.get_pixel_tuple(rb.Vector(0, 0)))
print(rb.Color.red)


def update():
    if rb.Input.mouse_pressed():
        x, y = rb.Input.get_mouse_pos().tuple_int()
        img.draw_point(rb.Vector(x, y), rb.Color.yellow)


def draw():
    rb.Draw.surf(img, rb.Vector(0, 0))


rb.Game.draw = draw
rb.Game.update = update

rb.begin()