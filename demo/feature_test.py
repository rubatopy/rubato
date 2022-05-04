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
rb.Game.scenes.add(main, "main")

test = rb.GameObject({
    "pos": rb.Vector(100, 100)
}).add(rb.RigidBody()).add(rb.Circle({
    "radius": 40,
    "color": rb.Color.red
}))

test2 = rb.GameObject({
    "pos": rb.Vector(200, 100)
}).add(rb.RigidBody()).add(rb.Rectangle({
    "width": 40,
    "height": 40,
    "color": rb.Color.red
}))

test3 = rb.GameObject({
    "pos": rb.Vector(300, 100)
}).add(rb.RigidBody()).add(rb.Polygon.generate_polygon(5, 40, {"color": rb.Color.red}))

main.add(test, test2, test3)
rb.begin()
