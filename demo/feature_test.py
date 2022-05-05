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

from rubato import Vector
import math
v = Vector.from_radial(32, math.radians(180+45))
v2 = Vector.from_radial(342, math.pi).to_int()
v3 = v + v2
print(Vector(8, 8).rationalized_mag_vector)
# print(v3.rationalized_unit) This line should raise our error.
# print(v3.rationalized_unit)


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
