"""A place to test new WIP features"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=all

from rubato import *

init({"res": Vector(350, 350)})

main = Scene()
Game.scenes.add(main, "main")

ui = UI({"pos": Vector(49, 49), "debug": True})

ui.add(Image({"rel_path": "testing/Run/0.png", "scale_factor": Vector(2, 2)}))


gm = GameObject({"pos": Vector(51, 51), "debug": False})

gm.add(Image({"rel_path": "testing/Run/0.png", "scale_factor": Vector(2, 2)}))

main.add(ui, gm)


def update():
    if Input.key_pressed("a"):
        Game.camera.pos.x -= 10
    if Input.key_pressed("d"):
        Game.camera.pos.x += 10
    if Input.key_pressed("w"):
        Game.camera.pos.y -= 10
    if Input.key_pressed("s"):
        Game.camera.pos.y += 10

    if Input.key_pressed("-"):
        Game.camera.zoom -= 0.01
    if Input.key_pressed("="):
        Game.camera.zoom += 0.01


main.update = update

begin()
