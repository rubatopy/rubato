import rubato.utils as util
from rubato import *

import ctypes

# Load DLL into memory.

hllDll = ctypes.WinDLL ("PixelEditor.h")

# Set up prototype and parameters for the desired function call.
# HLLAPI

hllApiProto = ctypes.WINFUNCTYPE (
    ctypes.c_int,      # Return type.
    ctypes.c_void_p,   # Parameters 1 ...
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_void_p)   # ... thru 4.
hllApiParams = (1, "p1", 0), (1, "p2", 0), (1, "p3",0), (1, "p4",0),

# Actually map the call ("HLLAPI(...)") to a Python name.

hllApi = hllApiProto (("HLLAPI", hllDll), hllApiParams)

# This is how you can actually call the DLL function.
# Set up the variables and call the Python name with them.

p1 = ctypes.c_int (1)
p2 = ctypes.c_char_p (sessionVar)
p3 = ctypes.c_int (1)
p4 = ctypes.c_int (0)
hllApi (ctypes.byref (p1), p2, ctypes.byref (p3), ctypes.byref (p4))

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
    setPixelRGB(surface, start.x, start.y, 255, 0, 0)
    # end = Vector(28, 28)
    # end.x += i
    # sdl2.ext.line(
    #             surface,
    #             sdl2.ext.rgba_to_color(Color.random_default().rgba32),
    #             (*start, *end),
    #             1,
    #         )

sdl2.surface.SDL_SetColorKey(
            surface, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(surface.format, *Color.yellow.to_tuple()[:-1])
        )

print(surface.pixels)

texture = sdl2.ext.Texture(Display.renderer, surface)

def update():
    Draw.queue_texture(texture, Display.center)

mainS.update = update
begin()


