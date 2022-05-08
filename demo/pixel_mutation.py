"""
Drawing to specific pixels

Draws a bunch or random pixels to a surface. Requires rubato 2.1.0 or later and numpy.
"""
import numpy, random
import rubato as rb

rb.init(
    {
        "name": "Point drawing",
        "res": rb.Vector(300, 300),
        "window_size": rb.Vector(600, 600),
        "background_color": rb.Color.blue,
    }
)

main_scene = rb.Scene()

image = rb.Image()
image.resize(rb.Vector(90, 90))
pixel_obj = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)


def draw_on(surf):
    pixels: numpy.ndarray = rb.sdl2.ext.pixelaccess.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            # random color from our default palette
            choice = random.choice(list(rb.Defaults.color_defaults.values()))
            pixels[x][y] = rb.Color(*choice).rgba32
    return surf


def update():
    ranx = random.random() * 2 - 1
    rany = random.random() * 2 - 1
    pixel_obj.pos = pixel_obj.pos.lerp(pixel_obj.pos + rb.Vector(ranx, rany), rb.Time.delta_time * 0.05)

    if rb.Input.key_pressed("k"):
        rb.Display.save_screenshot("pixel_mutation")


def draw():
    image.image = draw_on(image.image)


main_scene.draw = draw
main_scene.update = update

main_scene.add(pixel_obj)

rb.begin()
