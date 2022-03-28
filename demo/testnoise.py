"""A Perlin Noise demo for Rubato"""
import os, sys, random
import sdl2.sdlgfx

sys.path.insert(0, os.path.abspath("../"))
# pylint: disable=wrong-import-position
import rubato as rb

rb.init({
    "name": "Perlin Test",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

scale = 0.02
def draw():
    for x in range(rb.Display.res.x):
        for y in range(rb.Display.res.y):
            gray = (rb.Math.perlin(x*scale, y*scale) + 1) / 2 * 255
            color = (gray, gray, gray)
            rb.Display.renderer.draw_point([x, y], color)

# main_scene.update = update
main_scene.draw = draw

rb.begin()
