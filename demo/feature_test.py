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

main.add(
    rb.GameObject({
        "pos": rb.Display.bottom_center + rb.Vector(0, -60),
        "rotation": -50
    }).add(rb.Rectangle({
        "width": rb.Display.res.x / 2,
        "height": rb.Display.res.y / 10,
        "color": rb.Color.gray
    }))
)


def stop(info):
    print("hi")


main.add(
    rb.GameObject({
        "pos": rb.Display.res / 2
    }).add(rb.Circle({
        "radius": rb.Display.res.x / 50,
        "color": rb.Color.red,
        "on_collide": stop
    })).add(rb.RigidBody({
        "bounciness": 1,
        "friction": 0.2,
        "gravity": rb.Vector(0, 100),
        "moment": 10
    }))
)

rb.begin()
