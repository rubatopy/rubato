import rubato.utils as util
from rubato import *
# pylint: disable=all

init(res=Vector(200, 200))
mainS = Scene()


width, height = 32, 32
surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0,
            width,
            height,
            32,
            util.pixel_format,
        ).contents

for i in range(20):
    start = Vector(0, 0)
    start.x += i
    end = Vector(28, 28)
    end.x += i
    sdl2.ext.line(
                surface,
                sdl2.ext.rgba_to_color(Color.random_default().rgba32),
                (*start, *end),
                1,
            )

sdl2.surface.SDL_SetColorKey(
            surface, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(surface.format, *Color.yellow.to_tuple()[:-1])
        )

print(surface.pixels)

texture = sdl2.ext.Texture(Display.renderer, surface)

def update():
    Draw.queue_texture(texture, Display.center)

mainS.update = update
begin()


