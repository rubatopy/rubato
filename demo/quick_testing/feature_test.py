"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V
import sdl2, sdl2.ext

width, height = 32, 32

rb.init(res=V(width, height), window_size=V(width, height) * 20)
s = rb.Scene()

img = rb.Surface(width, height)

sdl2.ext.fill(img.surf, sdl2.ext.Color(0, 0, 0))

img.clear()
# img.draw_rect(V(1, 1), V(30, 30), rb.Color.purple, rb.Color.green)
# img.draw_rect(V(0, 0), V(32, 32), rb.Color.red)
# img.draw_circle(V(16, 16), 7, rb.Color.red, rb.Color.yellow)
# img.draw_line(V(4, 3), V(28, 27), rb.Color.blue)
# img.draw_line(V(4, 4), V(28, 28), rb.Color(32,32,32,128))
# img.draw_poly([V(16, 0), V(0, 16), V(32, 16)], rb.Color.gray)
# img.draw_rect(V(2, 2), V(18, 12), fill=rb.Color(0, 0, 256, 64))

# print(img.get_pixel(V(4, 4)))
# print(img.get_pixel_tuple(V(0, 0)))
# print(rb.Color.red)

polygon = rb.Polygon([V(0, 16), V(31, 16), V(16, 0)], rb.Color.gray)
from rubato.c_src import pixel_editor as pe
pe.fill_poly(img.surf.pixels, width, height, polygon.verts, rb.Color.red.rgba32())


def update():
    if rb.Input.mouse_pressed():
        img.draw_point(rb.Input.get_mouse_pos(), rb.Color(32, 32, 32))


def draw():
    rb.Draw.surf(img, V(16, 16))


rb.Game.draw = draw
rb.Game.update = update

rb.begin()