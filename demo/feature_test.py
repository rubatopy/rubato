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

rb.Game.debug = True

main = rb.Scene()
rb.Game.scenes.add(main, "main")


def handle(e):
    print(e)


player = rb.GameObject({
    "pos": rb.Display.center
}).add(rb.Rectangle({
    "width": 64,
    "height": 64,
    "color": rb.Color.blue,
    "on_collide": handle
})).add(rb.RigidBody({
    "gravity": rb.Vector(y=rb.Display.res.y / 2),
    "pos_correction": 1
}))

ground = rb.GameObject().add(rb.Rectangle({"width": rb.Display.res.x, "height": 50, "color": rb.Color.green}))
ground.get(rb.Rectangle).bottom_left = rb.Display.bottom_left

main.add(player, ground)

rb.begin()
