"""Text demo for rubato"""  # pylint: disable=all
import sdl2, sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init()
import sdl2.sdlttf as ttf
import sdl2.ext

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

# def get_size():
#     ret = sdlttf.TTF_MeasureUTF8(font, tst, 180, byref(extent), byref(count))
#     success = True if ret == 0 else False

# https://stackoverflow.com/questions/22886500/how-to-render-text-in-sdl2
