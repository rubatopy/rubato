"""
Drawing to specific pixels

Draws a bunch or random pixels to a surface. Requires rubato 2.1.0 or later and numpy.
"""
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


class WanderingImage(rb.Component):
    """
    A component that draws randomly to its gameobjects image.
    """

    def __init__(self):
        super().__init__()
        self.image = None

    def setup(self):
        self.image: rb.Raster = rb.Raster(width=90, height=90)
        self.gameobj.add(self.image)
        self.singular = False

    def update(self):
        ranx = random.random() * 2 - 1
        rany = random.random() * 2 - 1
        self.image.offset = self.image.offset.lerp(self.image.offset + rb.Vector(ranx, rany), rb.Time.delta_time * 50)
        self.image.rotation_offset += random.random() * rb.Time.delta_time * 50
        self.image.scale += rb.Vector(ranx / 1000, rany / 1000)

        if rb.Input.key_pressed("k"):
            rb.Display.save_screenshot("pixel_mutation")

    def draw(self, camera):
        self.image.raster = draw_on(self.image.raster)
        self.image.set_colorkey(rb.Color.red)


go = rb.GameObject(pos=rb.Vector(150, 150),)
go.add(WanderingImage())
go.add(WanderingImage())

main_scene.add(go)

rb.begin()
