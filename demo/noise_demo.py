"""
A Perlin Noise demo for rubato

Draws a sample of Perlin noise to the screen. Requires rubato 2.1.0 or later.
"""
from random import randint
import random
import rubato as rb

rb.init(
    name="Perlin Test",
    res=rb.Vector(480, 270),
    size=rb.Vector(960, 540),
)

main_scene = rb.Scene()

scale = 100
offset = rb.Vector(100, 100)
true_random = True

rb.Noise.seed = randint(-100, 100)

saved = []
for x in range(rb.Display.res.x):
    saved.append([])
    for y in range(rb.Display.res.y):
        if true_random:
            noise = random.random() * 2 - 1
        else:
            noise = rb.Noise.noise2((x + offset.x) / scale, (y + offset.y) / scale)
        gray = (noise + 1) / 2 * 255  # Note simplex perlin noise ranges from -1 to 1 and is being scaled to 0-255
        color = rb.Color(gray, gray, gray)
        saved[x].append((rb.Vector(x, y), color))


def draw():
    for i in range(rb.Display.res.x):
        for j in range(rb.Display.res.y):
            rb.Draw.queue_point(saved[i][j][0], color=saved[i][j][1])


main_scene.draw = draw

rb.begin()
