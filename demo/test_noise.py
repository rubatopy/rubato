"""A Perlin Noise demo for Rubato"""  # pylint: disable=all
import opensimplex
import sys, os

sys.path.insert(0, os.path.abspath("../"))

from rubato import *

init({
    "name": "Perlin Test",
    "res": Vector(480, 270),
    "window_size": Vector(960, 540),
})

main_scene = Scene()
Game.scenes.add(main_scene, "main")

scale = 50
offset = Vector(100, 100)

saved = []
for x in range(Display.res.x):
    saved.append([])
    for y in range(Display.res.y):
        noise = opensimplex.noise2((x + offset.x) / scale, (y + offset.y) / scale)
        gray = (noise + 1) / 2 * 255  # Note simplex perlin noise ranges from -1 to 1 and is being scaled to 0-255
        color = [gray for i in range(3)]
        color = Color(*color)
        saved[x].append((Vector(x, y), color))


def draw():
    for i in range(Display.res.x):
        for j in range(Display.res.y):
            Display.draw_point(*saved[i][j])


main_scene.draw = draw

begin()
