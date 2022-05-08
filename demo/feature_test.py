"""A place to test new WIP features"""  # pylint: disable=all
from random import randint, choice
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({
    "name": "Physics Test",
    "physics_fps": 60,
    "window_size": rb.Vector(600, 600),
    "res": rb.Vector(1200, 1200),
})

main = rb.Scene()

test = rb.GameObject({
    "pos": rb.Vector(100, 100)
}).add(rb.Text({
    "text": "test",
    "align": rb.Vector(-1, -1),
    "justify": "right",
    "font": rb.Font({"size": 64})
})).add(rb.Rectangle({
    "color": rb.Color.red,
    "width": 5,
    "height": 5
}))

main.add(test)

rb.begin()
