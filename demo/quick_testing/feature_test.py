"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from rubato import Vector as V
import sdl2, sdl2.ext
from rubato.c_src import pixel_editor as pe

width, height = 32, 32

rb.init(res=V(width, height), window_size=V(width, height) * 20)
s = rb.Scene()

img = rb.Surface(width, height)

sdl2.ext.fill(img.surf, sdl2.ext.Color(0, 0, 0))

img.clear()

# img.draw_rect(V(1, 1), V(30, 30), rb.Color.purple, 3, rb.Color.green)
# img.draw_rect(V(0, 0), V(32, 32), rb.Color.red)
# img.draw_circle(V(16, 16), 7, rb.Color.red, rb.Color.yellow)
# img.draw_line(V(4, 3), V(28, 27), rb.Color.blue, 3)
# img.draw_line(V(4, 4), V(28, 28), rb.Color(32, 32, 32, 128), 5)
# img.draw_poly([V(16, 0), V(0, 16), V(32, 16)], rb.Color.gray, 3)
# img.draw_poly([V(16, 0), V(0, 16), V(32, 16)], border=rb.Color.blue, aa=True)
# img.draw_rect(V(2, 2), V(18, 12), fill=rb.Color(0, 0, 255, 128))
# img.draw_line(V(4, 4), V(25, 28), rb.Color(32, 32, 32, 255), aa=True)
# pe.draw_line(
#     img.surf.pixels, img.surf.w, img.surf.h, 4, 24, 15, 0, rb.Color(32, 32, 32, 255).rgba32(), aa=True, bottom=False
# )
# pe.draw_line(img.surf.pixels, img.surf.w, img.surf.h, 4, 24, 15, 0, rb.Color(32, 32, 32, 255).rgba32())
img.draw_poly([V(16, 0), V(0, 16), V(31, 16)], border=rb.Color.black, aa=True)
# print(img.get_pixel(V(4, 4)))
# print(img.get_pixel_tuple(V(0, 0)))
# print(rb.Color.red)

# pe.draw_antialiased_circle(img.surf.pixels, width, 255, 15, 15, 10, rb.Color.blue.rgba32())
# polygon = rb.Polygon([V(0, 16), V(31, 16), V(16, 0)], rb.Color.gray)
# pe.draw_circle(img.surf.pixels, width, height, 15, 15, 10, rb.Color.red.rgba32(), 4)
# pe.draw_circle(img.surf.pixels, width, height, 15, 15, 10, rb.Color.green.rgba32())
# pe.draw_line(img.surf.pixels, width, height, 15, 15, 15 + 10, 15, rb.Color.blue.rgba32())


def update():
    if rb.Input.mouse_pressed():
        img.draw_point(rb.Input.get_mouse_pos(), rb.Color(32, 32, 32))


def draw():
    rb.Draw.surf(img, V(width / 2, height / 2))


rb.Game.draw = draw
rb.Game.update = update

rb.begin()