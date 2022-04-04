"""A place to test new WIP features"""  # pylint: disable=all
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

from rubato import *

init({"res": Vector(600, 600)})

main = Scene()
Game.scenes.add(main, "main")

main.add(GameObject({"pos": Vector(250, 250)}).add(Rectangle({"width": 100, "height": 100, "debug": True})))


def update():
    print(Input.mouse_in(Vector(250, 250), Vector(100, 100)))


main.update = update

begin()
