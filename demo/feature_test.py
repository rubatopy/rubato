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

top = rb.GameObject({
    "pos": rb.Display.top_center + rb.Vector(0, -30)
}).add(rb.Rectangle({
    "width": rb.Display.res.x + 175,
    "height": rb.Display.res.y / 10,
    "color": rb.Color.gray,
}))

bottom = rb.GameObject({
    "pos": rb.Display.bottom_center + rb.Vector(0, 30)
}).add(rb.Rectangle({
    "width": rb.Display.res.x + 175,
    "height": rb.Display.res.y / 10,
    "color": rb.Color.gray,
}))

left = rb.GameObject({
    "pos": rb.Display.center_left + rb.Vector(-30, 0)
}).add(rb.Rectangle({
    "width": rb.Display.res.x / 10,
    "height": rb.Display.res.y + 175,
    "color": rb.Color.gray,
}))

right = rb.GameObject({
    "pos": rb.Display.center_right + rb.Vector(30, 0)
}).add(rb.Rectangle({
    "width": rb.Display.res.x / 10,
    "height": rb.Display.res.y + 175,
    "color": rb.Color.gray,
}))

main.add(top, left, bottom, right)

allow = 100


def handle(info):
    global allow
    print(info)
    allow -= 1
    if allow == 0:
        rb.Game.state = rb.Game.PAUSED


main.add(
    rb.GameObject({
        "pos": rb.Display.res / 2 + rb.Vector(100, 0),
        "rotation": 30
    }).add(rb.Circle({
        "radius": rb.Display.res.x / 20,
        "color": rb.Color.red,
    })).add(rb.RigidBody({
        "bounciness": 1,
        "velocity": rb.Vector(-10, 0),
        "moment": 100
    }))
)

main.add(
    rb.GameObject({
        "pos": rb.Display.res / 2 - rb.Vector(100, 0)
    }).add(
        rb.Polygon(
            {
                "verts": rb.Polygon.generate_polygon(7, rb.Display.res.x / 20),
                "color": rb.Color.red,
                "on_collide": handle
            }
        )
    ).add(rb.RigidBody({
        "bounciness": 1,
        "velocity": rb.Vector(20, 0),
        "ang_vel": 120,
        "moment": 100
    }))
)

rb.begin()
