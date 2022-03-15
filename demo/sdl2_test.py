# pylint: disable=all
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.sdlimage
import sdl2.sdlgfx

import os
import sys

sys.path.insert(0, os.path.abspath("../rubato"))

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

sdl2.ext.fill(window.get_surface(), (255, 255, 255))

render = sdl2.ext.Renderer(window, backend="direct3d")

sdl2.sdlgfx.aacircleColor(render.sdlrenderer, 50, 50, 25, 0x000000FF)

render.present()

processor = sdl2.ext.TestEventProcessor()
processor.run(window)
