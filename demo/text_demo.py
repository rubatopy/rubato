"""Text demo for rubato"""  # pylint: disable=all
import sys, os

sys.path.insert(0, os.path.abspath("../"))

from rubato import *

init()

main = Scene()
Game.scenes.add(main, "main")

text = Text(
    {
        "font": "Roboto",
        "size": 128,
        "text": "Hello World!\nThis is a test",
        "style": [],
        "align": "center",
        "width": -1,
    }
)

main.add(GameObject({"pos": Display.center}).add(text))
begin()
