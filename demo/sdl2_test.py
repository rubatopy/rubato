# pylint: disable=all
import sdl2
import sdl2.ext
import sdl2.surface
import sdl2.sdlimage
import ctypes

import os
import sys

sys.path.insert(0, os.path.abspath("../rubato"))

from rubato.classes.components.image import Image
from rubato.utils.vector import Vector

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

sdl2.ext.fill(window.get_surface(), (255, 255, 255))

im = Image({"image_location": "rubato/static/default.png"})

im.scale = Vector(2, 2)
im.rotation = 45

sdl2.surface.SDL_BlitSurface(
    im.image,
    None,
    window.get_surface(),
    sdl2.rect.SDL_Rect(
        50,
        50,
        im.get_size().x,
        im.get_size().y,
    ),
)

processor = sdl2.ext.TestEventProcessor()
processor.run(window)
