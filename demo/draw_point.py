"""Drawing to specific pixels"""
import numpy, random, sdl2.ext.pixelaccess as pixel_access
from rubato import *

init({
    "name": "Point drawing",
    "res": Vector(300, 300),
    "window_size": Vector(600, 600),
})

main_scene = Scene()
Game.scenes.add(main_scene, "main")

image = Image()
image.resize(Vector(90, 90))
pixel_obj = GameObject({"pos": Vector(150, 150)}).add(image)


def draw_on(surf: sdl2.SDL_Surface):
    pixels: numpy.ndarray = pixel_access.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            random.shuffle((new := list(Defaults.color_defaults.values())))
            pixels[x][y] = Color(*(new[0])).rgba32
    return surf


def draw():
    image.image = draw_on(image.image)


main_scene.update = draw

main_scene.add(pixel_obj)

begin()
