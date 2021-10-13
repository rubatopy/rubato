from pgp.sprite.sprite import Sprite
from pygame.image import load
from pygame.transform import scale
from pgp.utils import Vector, check_types
from pgp.scenes import Camera


class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    :param image_location: The path to the image.
    :param pos: The position of the sprite.
    """
    def __init__(self, image_location: str, pos: Vector = Vector(), scale_factor: Vector = Vector(1, 1)):
        check_types(Image.__init__, locals())
        super().__init__(pos)
        self.image = load(image_location if image_location != "" else "pgp/static/default.png")
        self.scale(scale_factor)

    def update(self):
        pass

    def draw(self, camera: Camera):
        """
        Draws the image if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        check_types(Image.draw, locals())
        super().draw(self.image, camera)

    def scale(self, scale_factor: Vector):
        """
        Let's you rescale the Image to a given scale factor.

        :param scale_factor: A Vector describing the scale in the x and y direction relative to its current size
        """
        check_types(Image.scale, locals())
        if (new_x := self.image.get_width() * scale_factor.x) < 1:
            new_x = 1
        if (new_y := self.image.get_height() * scale_factor.y) < 1:
            new_y = 1
        self.image = scale(self.image, (new_x, new_y))