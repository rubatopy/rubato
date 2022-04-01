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
one_way = True
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

    def draw(surf):
        pixels: pixel_access.PixelView = sdl2.ext.PixelView(surf)
        global noise, gray, color
        # print(surf.format.contents.format.__class__)
        # print(sdl2.SDL_GetPixelFormatName(surf.format.contents.format))
        print(f"before: {pixels[1][0]}")

        for i in range(rb.Display.res.x):
            for j in range(rb.Display.res.y):
                noise = opensimplex.noise2(i * scale, j * scale)  # Note simplex perlin noise ranges from -1 to 1
                gray = (noise + 1) / 2 * 255
                color = (0, 0, gray)
                color = rb.Color(*color)
                if i == 0 and j == 1:
                    print(f"using converter {rb.Color.from_rgba32(color.rgba32)}")
                pixels[j][i] = rb.Color(color.a, color.r, color.g, color.b).rgba32
        print(f"after: {rb.Color.from_rgba32(pixels[1][0])}")
        # print(sdl2.SDL_GetPixelFormatName(surf.format.contents.format))
        # print(color)
        return image.image

    image.image = draw(image.image)
    # print(sdl2.SDL_GetPixelFormatName(rb.Display.format.format))
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
