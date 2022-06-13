"""
Drawing to specific pixels

Draws a bunch or random pixels to a surface. Requires rubato 2.1.0 or later and numpy.
"""  # pylint: disable=W0613
import numpy, random
import rubato as rb

rb.init(
    name="Point drawing",
    res=rb.Vector(300, 300),
    window_size=rb.Vector(600, 600),
    background_color=rb.Color.black,
)
main_scene = rb.Scene()


def draw_on(surf):  # --------------------------------------------------------------- The important pixel mutation part
    pixels: numpy.ndarray = rb.sdl2.ext.pixelaccess.pixels2d(surf)
    for x in range(pixels.shape[0]):
        for y in range(pixels.shape[1]):
            # random color from our default palette
            # pixels[x][y] = rb.Color(*choice).rgba32
            pixels[x][y] = rb.Color.random_default().rgba32
    return surf


# Implementation 1:
# Extend the Component class and be added to a GameObject.
# Note, must use setup method instead of __init__. **Preferable**
class WanderingImage(rb.Component):
    """
    A component that draws randomly to its gameobjects image.
    """

    def setup(self):
        self.image: rb.Raster = self.gameobj.get(rb.Raster)

    def update(self):
        ranx = random.random() * 2 - 1
        rany = random.random() * 2 - 1
        self.gameobj.pos = self.gameobj.pos.lerp(self.gameobj.pos + rb.Vector(ranx, rany), rb.Time.delta_time * 50)
        self.image.rotation_offset += 1
        self.image.scale += rb.Vector(ranx / 1000, rany / 1000)

        if rb.Input.key_pressed("k"):
            rb.Display.save_screenshot("pixel_mutation")

    def draw(self, camera):
        self.image.raster = draw_on(self.image.raster)
        self.image.set_colorkey(rb.Color.red)


go = rb.GameObject(pos=rb.Vector(150, 150),)
image = rb.Raster(width=90, height=90)
go.add(image)
go.add(WanderingImage())


# Implementation 2:
# Extend the GameObject class and be added to a Scene directly.
# Note, must call all super() methods that you override.
class WanderingPixelMutation(rb.GameObject):
    """
    A gameobject that draws randomly to its image.
    """

    def __init__(self):
        super().__init__(pos=rb.Vector(150, 150))
        self.image = rb.Raster(width=90, height=90)
        self.add(self.image)

    def update(self):
        super().update()
        ranx = random.random() * 2 - 1
        rany = random.random() * 2 - 1
        self.pos = self.pos.lerp(self.pos + rb.Vector(ranx, rany), rb.Time.delta_time * 50)

        if rb.Input.key_pressed("k"):
            rb.Display.save_screenshot("pixel_mutation")
            go.get(rb.Raster).get_pixel_tuple((0, 0))

    def draw(self, camera):
        super().draw(camera)
        self.image.raster = draw_on(self.image.raster)


wgo = WanderingPixelMutation()

main_scene.add(wgo, go)

rb.begin()
