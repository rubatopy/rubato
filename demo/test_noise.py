"""A Perlin Noise demo for Rubato"""
import opensimplex
import rubato as rb

rb.init({
    "name": "Perlin Test",
    "res": rb.Vector(480, 270),
    "window_size": rb.Vector(960, 540),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

scale = 20
offset = rb.Vector(100, 100)

saved = []
for x in range(rb.Display.res.x):
    saved.append([])
    for y in range(rb.Display.res.y):
        noise = opensimplex.noise2((x + offset.x) / scale, (y + offset.y) / scale)
        gray = (noise + 1) / 2 * 255  # Note simplex perlin noise ranges from -1 to 1
        color = (gray, gray, gray)
        saved[x].append(([x, y], color))
        rb.Display.renderer.draw_point([x, y], color)

def draw():
    for i in range(rb.Display.res.x):
        for j in range(rb.Display.res.y):
            rb.Display.renderer.draw_point(*saved[i][j])

main_scene.draw = draw

rb.begin()
