"""A place to test new WIP features"""  # pylint: disable=all
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

from rubato import *

init({"res": Vector(600, 600)})

main = Scene()
Game.scenes.add(main, "main")

gm = GameObject({"pos": Vector(250, 250)}).add(Image({"rel_path": "testing/Run/0.png", "scale_factor": Vector(2, 2)}))

main.add(gm)


def update():
    try:
        print(gm)
    except Exception:
        pass


def listener(info):
    if info["key"] == "space":
        main.delete(gm)
    if info["key"] == "a":
        main.add(gm)


Radio.listen("keydown", listener)

main.update = update

begin()
