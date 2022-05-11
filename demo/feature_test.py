"""A place to test new WIP features"""  # pylint: disable=all
from random import randint, choice
import random
import sys, os

import numpy

sys.path.insert(0, os.path.abspath("../"))

import rubato as rb

rb.init({
    "name": "Physics Test",
    "physics_fps": 60,
    "window_size": rb.Vector(600, 600),
    "res": rb.Vector(1200, 1200),
})

rb.Game.debug = True

main = rb.Scene()


def draw_on(surf):  # --------------------------------------------------------------- The important pixel mutation part
    pixels: numpy.ndarray = rb.sdl2.ext.pixelaccess.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            # random color from our default palette
            choice = random.choice(list(rb.Defaults.color_defaults.values()))
            pixels[x][y] = rb.Color(*choice).rgba32
    return surf


test = rb.GameObject({
    "pos": rb.Vector(100, 100)
}).add(rb.Raster({
    "width": 100,
    "height": 100,
}))

raster: rb.Raster = test.get(rb.Raster)
raster.raster = draw_on(raster.raster)


def update():
    if rb.Input.key_pressed("w"):
        raster.rotation_offset += 1
    if rb.Input.key_pressed("s"):
        raster.rotation_offset -= 1
    if rb.Input.key_pressed("a"):
        raster.scale -= rb.Vector(0.1, 0.1)
    if rb.Input.key_pressed("d"):
        raster.scale += rb.Vector(0.1, 0.1)
    if rb.Input.key_pressed("shift"):
        rb.Game.camera.zoom += 0.1
    if rb.Input.key_pressed("ctrl"):
        rb.Game.camera.zoom -= 0.1


main.update = update
main.add(test)

rb.begin()
