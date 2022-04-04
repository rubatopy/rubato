"""Text demo for rubato"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

from rubato import *

init({
    "window_size": Vector(512, 512),
    "res": Vector(1024, 1024),
})

main = Scene()
Game.scenes.add(main, "main")

text = Text({
    "font": Font({
        "font": "Fredoka",
        "size": 64
    }),
    "text": "hello world",
    "align": "center",
    "width": -1,
})

main.add(UI({"pos": Display.center}).add(text))
begin()
