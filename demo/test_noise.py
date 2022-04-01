"""A Perlin Noise demo for Rubato"""
import opensimplex
import sdl2
import sdl2.ext.pixelaccess as pixel_access
import rubato as rb

rb.init({
    "name": "Perlin Test",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

onto_renderer = False
one_way = False
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
        for i in range(rb.Display.res.x):
            for j in range(rb.Display.res.y):
                rb.Display.renderer.draw_point(*saved[i][j])

    main_scene.draw = draw
elif one_way:
    image = rb.Image()
    image.resize(rb.Vector(rb.Display.res.x, rb.Display.res.y))
    perlin = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)

    def draw(pixels: pixel_access.PixelView):
        global noise, gray, color
        for i in range(rb.Display.res.x):
            for j in range(rb.Display.res.y):
                noise = opensimplex.noise2(i * scale, j * scale)  # Note simplex perlin noise ranges from -1 to 1
                gray = (noise + 1) / 2 * 255
                color = (gray, gray, gray)
                color = rb.Color(*color)
                pixels[i][j] = color.rgba32
        print("done")
        # return image

    draw(sdl2.ext.PixelView(image.image))
    main_scene.add(perlin)

else:
    image = rb.Image()
    image.resize(rb.Vector(rb.Display.res.x, rb.Display.res.y))
    perlin = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)

    for x in range(rb.Display.res.x):
        for y in range(rb.Display.res.y):
            noise = opensimplex.noise2(x * scale, y * scale)  # Note simplex perlin noise ranges from -1 to 1
            gray = (noise + 1) / 2 * 255
            color = (gray, gray, gray)
            color = rb.Color(*color)

            image.draw_point(rb.Vector(x, y), color)

    rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)
    main_scene.add(perlin)

print("done")
rb.begin()
