"""Drawing to specific pixels"""  # pylint: disable=all
import numpy, random, sdl2.ext.pixelaccess as pixel_access
import sys, os

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({
    "name": "Point drawing",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

image = rb.Image()
image.resize(rb.Vector(90, 90))
pixel_obj = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)


def draw_on(surf):
    pixels: numpy.ndarray = pixel_access.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            random.shuffle((new := list(rb.Defaults.color_defaults.values())))
            pixels[x][y] = rb.Color(*(new[0])).rgba32
    return surf


def draw():
    image.image = draw_on(image.image)


main_scene.update = draw

main_scene.add(pixel_obj)

rb.begin()
