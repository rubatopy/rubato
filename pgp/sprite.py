from pygame.image import load
from pgp.utils.DISPLAY import GD
from pgp.input import Input

class Sprite:
    """
    The base sprite class.

    :param x: The x position of the sprite (in pixels).
    :param y: The y position of the sprite (in pixels).
    :param image_location: The location of the sprite.
    """

    def __init__(self, image_location: str, x: int, y: int, z: int = 0):
        self.image = load(image_location)
        self.pos = (x, y)
        self.z_index = z
        self.state = {}

    def update(self):
        """The update loop"""
        pass

    def draw(self, camera):
        """The draw loop"""
        if camera.z >= self.z_index: GD.update(self.image, (self.pos[0] - camera.x, self.pos[1] - camera.y))
