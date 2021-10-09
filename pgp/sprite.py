from pygame.image import load
from pgp.utils import GD, Point
from pgp.input import Input

class Sprite:
    """
    The base sprite class.

    :param x: The x position of the sprite (in pixels).
    :param y: The y position of the sprite (in pixels).
    :param image_location: The location of the sprite.
    """

    def __init__(self, image_location: str, pos: Point):
        self.image = load(image_location)
        self.pos = pos
        self.state = {}

    def update(self):
        """The update loop"""
        pass

    def draw(self, camera):
        """The draw loop"""
        if camera.pos.z >= self.pos.z:
            GD.update(self.image, self.pos.offset2(camera.pos).to_tuple())
