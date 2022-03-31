"""A place to test new WIP features"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

import rubato as rb

rb.init({"res": rb.Vector(100, 100)})

main = rb.Scene()
rb.Game.scenes.add(main, "main")

img = rb.Image({"size": rb.Vector(100, 100)})

img.draw_point(rb.Vector(0, 0), rb.Color.blue)

img.resize(rb.Vector(100, 100))

main.add(rb.GameObject({"pos": rb.Vector(50, 50), "debug": True}).add(img))

rb.begin()
