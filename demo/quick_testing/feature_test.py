"""A place to test new WIP features"""  # pylint: disable=all
import ctypes
import rubato as rb
import sdl2, sdl2.ext

rb.init(res=rb.Vector(32, 32), window_size=rb.Vector(32, 32) * 10)

s = rb.Scene()

img = rb.Sprite("../sprites/spaceship/spaceship.png")


def draw():
    rb.Draw.surf(img, rb.Vector(16, 16))


rb.Game.draw = draw

rb.begin()