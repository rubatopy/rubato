from pygame.image import load
from pgp.utils import GD, Point

class Sprite:
    """
    The base sprite class.

    :param image_location: The location of the sprite image.
    :param pos: The position of the sprite on screen. Defaults to (0, 0, 0)
    """

    def __init__(self, image_location: str, pos: Point = Point()):
        self.image = load(image_location)
        self.pos = pos
        self.state = {}

    def update(self):
        """The update loop"""
        pass

    def draw(self, camera):
        """The draw loop"""
        if camera.pos.z >= self.pos.z:
            GD.update(self.image, camera.transform(self.pos))
