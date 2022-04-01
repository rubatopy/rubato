"""Text demo for rubato"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init()

main = rb.Scene()
rb.Game.scenes.add(main, "main")

text = rb.Text(
    {
        "font": "testing/fonts/32bit Regular.ttf",
        "size": 128,
        "text": "Hello World!",
        "style": ["italic", "bold"],
    }
)

main.add(rb.GameObject({"pos": rb.Vector(100, 100)}).add(text))
rb.begin()
