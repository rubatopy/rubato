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


def update():
    if rb.Display.window_size.x < rb.Display.window_size.y:
        res_amount = rb.Display.res.x
        scale = rb.Display.res.x / rb.Display.window_size.x
    else:
        res_amount = rb.Display.res.y
        scale = rb.Display.res.y / rb.Display.window_size.y

    start = (rb.Display.window_size.x / 2) - (res_amount / scale / 2)

    print(f"size1: {rb.Display.res}   size2: {rb.Display.window_size}     start: {start}")


main.update = update

rb.begin()
