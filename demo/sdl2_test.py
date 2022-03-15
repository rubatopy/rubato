# pylint: disable=all
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.sdlimage
import sdl2.sdlgfx
import time

import os
import sys

sys.path.insert(0, os.path.abspath("../rubato"))

from rubato.classes.components.image import Image

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

sdl2.ext.fill(window.get_surface(), (255, 255, 255))

render = sdl2.ext.Renderer(window,
                           flags=(sdl2.SDL_RENDERER_ACCELERATED
                                  | sdl2.SDL_RENDERER_PRESENTVSYNC))

render.fill((0, 0, render.logical_size[0], render.logical_size[1]), 0xFFFFFFFF)

sdl2.sdlgfx.aacircleRGBA(render.sdlrenderer, 50, 50, 25, 0, 0, 0, 255)
sdl2.sdlgfx.filledCircleRGBA(render.sdlrenderer, 50, 50, 25, 0, 0, 0, 255)

img = Image({"image_location": os.path.abspath("demo/testing/Death/0.png")})

render.copy(sdl2.ext.Texture(render.sdlrenderer, img.image),
            dstrect=(100, 100))

window.refresh()
render.present()
time.sleep(5)
