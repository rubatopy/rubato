"""A place to test new WIP features"""  # pylint: disable=all
import rubato as rb
from random import randint, choice
import random, ctypes, sdl2, sdl2.ext
import sys, os

import numpy

sys.path.insert(0, os.path.abspath("../"))

rb.init({
    "name": "Physics Test",
    "physics_fps": 60,
    "window_size": rb.Vector(600, 600),
    "res": rb.Vector(1200, 1200),
})

rb.Game.debug = True

main = rb.Scene()

test = rb.GameObject({
    "pos": rb.Vector(300, 300)
}).add(rb.Rectangle({
    "width": 50,
    "height": 100,
    "color": rb.Color.red
}))


def update():
    if rb.Input.key_pressed("a"):
        test.rotation -= 1
    elif rb.Input.key_pressed("d"):
        test.rotation += 1


main.update = update

main.add(test)
rb.begin()
