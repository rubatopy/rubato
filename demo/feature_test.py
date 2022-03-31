"""A place to test new WIP features"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

import rubato as rb

rb.init()

main = rb.Scene()
rb.Game.scenes.add(main, "main")

img = rb.Image()

img.draw_point(rb.Vector(0, 0), rb.Color.blue)

img.resize(rb.Vector(1000, 1000))
main.add(rb.GameObject({"pos": rb.Vector(500, 500)}).add(img))

rb.begin()
