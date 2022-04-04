"""A place to test new WIP features"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({"res": rb.Vector(600, 600)})

main = rb.Scene()
rb.Game.scenes.add(main, "main")


def update():
    pass


def listener(info):
    if info["key"] == "space":
        print(rb.Color.from_hex("aaffffff"))


rb.Radio.listen("KEYDOWN", listener)

main.update = update

rb.begin()
