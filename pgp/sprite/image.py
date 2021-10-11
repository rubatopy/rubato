from pgp.sprite.sprite import Sprite
from pygame.image import load
from pgp.utils import Vector, check_types
from pgp.scenes import Camera


class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    :param image_location: The path to the image.
    :param pos: The position of the sprite.
    """
    # TODO Sprite Scaling
    def __init__(self, image_location: str, pos: Vector = Vector()):
        check_types(Image.__init__, locals())
        super().__init__(pos)
        self.image = load(image_location if image_location != "" else "pgp/static/default.png")

    def update(self):
        check_types(Image.update, locals())
        pass

    def draw(self, camera: Camera):
        """
        Draws the image if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        check_types(Image.draw, locals())
        super().draw(self.image, camera)
