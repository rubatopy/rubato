"""Text demo for rubato"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({
    "window_size": rb.Vector(512, 512),
    "res": rb.Vector(1024, 1024),
})

main = rb.Scene()
rb.Game.scenes.add(main, "main")

text = rb.Text({
    "font": rb.Font({
        "font": "Fredoka",
        "size": 64
    }),
    "text": "hello world",
})

main.add(rb.UI({"pos": rb.Display.center}).add(text))
rb.begin()
