"""
Drawing to specific pixels

Draws a bunch or random pixels to a surface. Requires rubato 2.1.0 or later and numpy.
"""
import numpy, random
import rubato as rb

rb.init(name="Point drawing", res=rb.Vector(300, 300), window_size=rb.Vector(600, 600))
main_scene = rb.Scene(background_color=rb.Color.black)

rb.Game.show_fps = True


class WanderingImage(rb.Component):
    """
    A component that draws randomly to its gameobjects image.
    """

    def __init__(self):
        super().__init__()
        self.image = None

    def setup(self):
        self.image: rb.Surface = rb.Surface(width=90, height=90)
        self.singular = False

    def update(self):
        ranx = random.random() * 2 - 1
        rany = random.random() * 2 - 1
        self.offset = self.offset.lerp(self.offset + rb.Vector(ranx, rany), rb.Time.delta_time * 50)
        self.image.rotation += random.random() * rb.Time.delta_time * 50
        self.image.scale += rb.Vector(ranx / 1000, rany / 1000)

        if rb.Input.key_pressed("k"):
            rb.Display.save_screenshot("pixel_mutation")

    def draw(self, camera):
        for x in range(90):
            for y in range(90):
                self.image.draw_point(rb.Vector(x, y), rb.Color.random_default())

        rb.Draw.surf(self.image, self.gameobj.pos + self.offset - 45)


go = rb.GameObject(pos=rb.Vector(150, 150),)
go.add(WanderingImage())
go.add(WanderingImage())

main_scene.add(go)

rb.begin()
