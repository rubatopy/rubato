"""A place to test new WIP features"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({"res": rb.Vector(600, 600)})

main = rb.Scene()
rb.Game.scenes.add(main, "main")

gm = rb.GameObject({
    "pos": rb.Vector(250, 250)
}).add(rb.Image({
    "rel_path": "testing/Run/0.png",
    "scale_factor": rb.Vector(2, 2)
}))

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


rb.Radio.listen("keydown", listener)

main.update = update

rb.begin()
