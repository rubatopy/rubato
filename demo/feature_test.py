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

rb.Game.debug = True

allow = 1


def handle(info: rb.Manifold):
    global allow
    print(info)
    allow -= 1
    if allow == 0:
        rb.Game.state = rb.Game.PAUSED


a = rb.GameObject({
    "pos": rb.Display.res / 2 - rb.Vector(100, 0),
    "rotation": 30
}).add(rb.Polygon({
    "verts": rb.Polygon.generate_polygon(6, rb.Display.res.x / 20),
    "color": rb.Color.red,
})).add(rb.RigidBody({
    "bounciness": 1,
    "velocity": rb.Vector(10, 0),
    "moment": 100
}))

b = rb.GameObject({
    "pos": rb.Display.res / 2 + rb.Vector(100, -50)
}).add(rb.Circle({
    "radius": rb.Display.res.x / 30,
    "color": rb.Color.blue,
    "on_collide": handle
})).add(rb.RigidBody({
    "bounciness": 1,
    "velocity": rb.Vector(-20, 0),
    "ang_vel": 120,
    "moment": 100
}))

main.add(a, b)

rb.Radio.listen("KEYDOWN", lambda e: print(rb.Input.get_mouse_pos()))

rb.begin()
