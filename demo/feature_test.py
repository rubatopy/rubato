"""A place to test new WIP features"""
import os
import sys

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position

import rubato as rb


rb.init()

main = rb.Scene()
rb.Game.scenes.add(main, "main")

main.add(rb.Sprite({
    "pos": rb.Vector(100,100)
}).add(rb.Circle({
    "color": rb.Color.olive
})))

rb.begin()
