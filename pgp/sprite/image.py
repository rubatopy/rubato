from pgp.sprite.sprite import Sprite
from pygame.image import load
from pgp.utils import GD, Point

class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    :param image_location: The path to the image.
    :param pos: The position of the sprite.
    """

    def __init__(self, image_location: str, pos: Point = Point()):
        self.image = load(image_location if image_location != "" else "pgp/static/default.png")
        super().__init__(pos)

    def update(self):
        pass

    def draw(self, camera):
        """
        Draws the image if the z index is below the camera's

        :param camera: The current Camera viewing the scene
        """
        GD.update(self.image, camera.transform(self.pos))
