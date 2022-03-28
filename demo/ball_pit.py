"""A physics demo for Rubato"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position
from random import randint, choice
import rubato as rb
from rubato import Game, Vector, Color, Display

num_balls = 30

rb.init({
    "name": "Ball Pit",
    "physics_fps": 30,
    "window_size": Vector(600, 600),
    "res": Vector(1200, 1200),
})

main_scene = rb.Scene()
Game.scenes.add(main_scene, "main")

top = rb.GameObject({
    "pos": Display.top_center + Vector(0, -30)
}).add(rb.Rectangle({
    "width": Display.res.x + 175,
    "height": Display.res.y / 10,
    "color": Color.gray,
}))

bottom = rb.GameObject({
    "pos": Display.bottom_center + Vector(0, 30)
}).add(rb.Rectangle({
    "width": Display.res.x + 175,
    "height": Display.res.y / 10,
    "color": Color.gray,
}))

left = rb.GameObject({
    "pos": Display.center_left + Vector(-30, 0)
}).add(rb.Rectangle({
    "width": Display.res.x / 10,
    "height": Display.res.y + 175,
    "color": Color.gray,
}))

right = rb.GameObject({
    "pos": Display.center_right + Vector(30, 0)
}).add(rb.Rectangle({
    "width": Display.res.x / 10,
    "height": Display.res.y + 175,
    "color": Color.gray,
}))

main_scene.add(top, bottom, left, right)

for _ in range(num_balls):
    main_scene.add(
        rb.GameObject(
            {
                "pos":
                    Vector(
                        randint(Display.res.x / 20, 19 * Display.res.x / 20),
                        randint(Display.res.y / 20, 19 * Display.res.y / 20)
                    )
            }
        ).add(
            rb.Circle(
                {
                    "radius": Display.res.x / num_balls,
                    "color": Color(*choice(list(rb.Defaults.color_defaults.values())))
                }
            )
        ).add(
            rb.RigidBody(
                {
                    "bounciness": 1,
                    "friction": 0.2,
                    "gravity": Vector(0, Display.res.x / 8),
                    "velocity": Vector(randint(-100, 100), randint(-100, 100))
                }
            )
        )
    )

rb.begin()
