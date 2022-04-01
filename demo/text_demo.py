"""Text demo for rubato"""  # pylint: disable=all
import sdl2, sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init()
import sdl2.sdlttf as ttf
import sdl2.ext

main = rb.Scene()
rb.Game.scenes.add(main, "main")
image = rb.Image({"rel_path": "testing/Run/0.png"})
image.resize(rb.Vector(200, 200))
ttf.TTF_Init()

fontfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testing/fonts", "32bit Regular.ttf").encode("utf-8")
font = ttf.TTF_OpenFont(fontfile, 64).contents
# ttf.TTF_SetFontStyle(font, ttf.TTF_STYLE_BOLD)
# ttf.TTF_SetFontStyle(font, ttf.TTF_STYLE_BOLD |
#                                 ttf.TTF_STYLE_ITALIC)
text_color = sdl2.SDL_Color(30, 30, 20, 200)
surface = ttf.TTF_RenderText_Solid(font, b"Hello World!", text_color).contents
main.draw = lambda: rb.Display.update(sdl2.ext.Texture(rb.Display.renderer, surface), rb.Vector(100, 100))
image.image = surface
print(surface.__class__)
text = rb.GameObject({"pos": rb.Vector(200, 200)}).add(image)
main.add(text)
rb.begin()
ttf.TTF_CloseFont(font)


# def get_size():
#     ret = sdlttf.TTF_MeasureUTF8(font, tst, 180, byref(extent), byref(count))
#     success = True if ret == 0 else False


# https://stackoverflow.com/questions/22886500/how-to-render-text-in-sdl2
