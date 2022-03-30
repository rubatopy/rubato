"""Text demo for rubato"""  # pylint: disable=all
import sdl2, sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init()
import sdl2.sdlttf as ttf

main = rb.Scene()
rb.Game.scenes.add(main, "main")
ttf.TTF_Init()

font = ttf.TTF_OpenFont(b"FreeSans.ttf", 32)
text_color = sdl2.SDL_Color()
surface = ttf.TTF_RenderText_Solid(font, b"hi", text_color)
print(surface.__class__)
rb.begin()

# https://stackoverflow.com/questions/22886500/how-to-render-text-in-sdl2
