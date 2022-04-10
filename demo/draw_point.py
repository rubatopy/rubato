"""Drawing to specific pixels"""
import numpy, random, sdl2.ext.pixelaccess as pixel_access
import sdl2
import sdl2.ext
import rubato as rb


rb.init({
    "name": "Point drawing",
    "res": rb.Vector(300, 300),
    "window_size": rb.Vector(600, 600),
})

main_scene = rb.Scene()
rb.Game.scenes.add(main_scene, "main")

image = rb.Image()
image.resize(rb.Vector(90, 90))
pixel_obj = rb.GameObject({"pos": rb.Vector(150, 150)}).add(image)


def draw_on(surf):
    pixels: numpy.ndarray = pixel_access.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            random.shuffle((new := list(rb.Defaults.color_defaults.values())))
            pixels[x][y] = rb.Color(*(new[0])).rgba32
    return surf

# venv\Lib\site-packages\sdl2\examples\pixelaccess.py
def draw_horizontal_stripes(surface, x1, x2, y1, y2):
    # Fill the entire surface with a black color. In contrast to
    # colorpalettes.py we use a Color() value here, just to demonstrate that
    # it really works.
    sdl2.ext.fill(surface, rb.Color.black)

    # Create a 2D view that allows us to directly access each individual pixel
    # of the surface. The PixelView class is quite slow, since it uses an non-
    # optimised read-write access to each individual pixel and offset. It
    # works on every platform, though.
    pixelview = sdl2.ext.PixelView(surface)

    # Loop over the area bounds, considering each fourth line and every column
    # on the 2D view. The PixelView uses a y-x alignment to access pixels.
    # This mkeans that the first accessible dimension of the PixelView denotes
    # the horizontal lines of an image, and the second the vertical lines.
    for y in range(y1, y2, 4):
        for x in range(x1, x2):
            # Change the color of each individual pixel. We can assign any
            # color-like value here, since the assignment method of the
            # PixelView will implicitly check and convert the value to a
            # matching color for its target surface.
            pixelview[y][x] = rb.Color.white

    # Explicitly delete the PixelView. Some surface types need to be locked
    # in order to access their pixels directly. The PixelView will do that
    # implicitly at creation time. Once we are done with all necessary
    # operations, we need to unlock the surface, which will be done
    # automatically at the time the PixelView is garbage-collected.
    del pixelview


def draw():
    image.image = draw_on(image.image)
    # draw_horizontal_stripes(image.image, 0, 40, 0, 40)  # Doesn't currently work

main_scene.update = draw

main_scene.add(pixel_obj)

rb.begin()
