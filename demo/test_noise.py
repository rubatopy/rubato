"""A Perlin Noise demo for Rubato"""
import os, sys, opensimplex, sdl2, numpy
import sdl2.ext.pixelaccess as pixel_access

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=all
import rubato as rb

rb.init({
    "name": "Perlin Test",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

image = rb.Image({
    "rel_path": "testing/Run/0.png"
})
image.resize(rb.Vector(rb.Display.res.x, rb.Display.res.y))
perlin = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)

scale = 0.02
minimum = 1
maximum = -1


def draw(image: sdl2.SDL_Surface):
    global maximum, minimum

    pixels: numpy.ndarray = pixel_access.pixels2d(image)
    print(pixels[150][150])
    print(pixels.shape)
    for x in range(rb.Display.res.x):
        for y in range(rb.Display.res.y):
            noise = opensimplex.noise2(x*scale, y*scale)
            maximum = max(maximum, noise)
            minimum = min(minimum, noise)
            gray = (noise + 1) / 2 * 255
            color = (gray, gray, gray)
            color = rb.Color(*color)
            pixels[x][y] = color.rgba32

    print(minimum, maximum)
    return image


# def draw():
#     for x in range(rb.Display.res.x):
#         for y in range(rb.Display.res.y):
#             noise = opensimplex.noise2(x * scale, y * scale)
#             gray = (noise + 1) / 2 * 255
#             color = (gray, gray, gray)
#             rb.Display.renderer.draw_point([x, y], color)
#
# main_scene.draw = draw

image.image = draw(image.image)
main_scene.add(perlin)
# main_scene.add(
#     rb.GameObject({"pos": rb.Vector(150, 150)}).add(rb.Rectangle({
#         "width": 10,
#         "height": 10,
#         "color": rb.Color.from_RGBA32(4286997840)
#     }))
# )

rb.begin()
