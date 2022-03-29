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

onto_renderer = True
scale = 0.02


if onto_renderer:
    saved = []
    for x in range(rb.Display.res.x):
        saved.append([])
        for y in range(rb.Display.res.y):
            noise = opensimplex.noise2(x * scale, y * scale)
            gray = (noise + 1) / 2 * 255  # Note simplex perlin noise ranges from -1 to 1
            color = (gray, gray, gray)
            saved[x].append(([x, y], color))
            rb.Display.renderer.draw_point([x, y], color)

    def draw():
        for x in range(rb.Display.res.x):
            for y in range(rb.Display.res.y):
                rb.Display.renderer.draw_point(*saved[x][y])

    main_scene.draw = draw

else:
    image = rb.Image()
    image.resize(rb.Vector(rb.Display.res.x, rb.Display.res.y))
    perlin = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)

    def draw(image: sdl2.SDL_Surface):

        pixels: numpy.ndarray = pixel_access.pixels2d(image)

        for x in range(rb.Display.res.x):
            for y in range(rb.Display.res.y):
                noise = opensimplex.noise2(x*scale, y*scale)  # Note simplex perlin noise ranges from -1 to 1
                gray = (noise + 1) / 2 * 255
                color = (gray, gray, gray)
                color = rb.Color(*color)
                pixels[x][y] = color.rgba32

        return image
    image.image = draw(image.image)
    main_scene.add(perlin)

rb.begin()
