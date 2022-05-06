"""
Drawing to specific pixels

Draws a bunch or random pixels to a surface. Requires rubato 2.1.0 or later and numpy.
"""
import numpy, random
import rubato as rb

rb.init({
    "name": "Point drawing",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()

image = rb.Image()
image.resize(rb.Vector(90, 90))
pixel_obj = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)


def draw_on(surf):
    pixels: numpy.ndarray = rb.sdl2.ext.pixelaccess.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            random.shuffle((new := list(rb.Defaults.color_defaults.values())))
            pixels[x][y] = rb.Color(*(new[0])).rgba32
    return surf


def draw():
    image.image = draw_on(image.image)
    # draw_horizontal_stripes(image.image, 0, 40, 0, 40)  # Doesn't currently work


main_scene.update = draw

main_scene.add(pixel_obj)

rb.begin()
