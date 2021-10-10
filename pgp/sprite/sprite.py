from pgp.utils import DISPLAY, Vector
from pygame.transform import scale

class Sprite:
    """
    The base sprite class.

    :param pos: The position of the sprite on screen. Defaults to (0, 0, 0)
    """

    def __init__(self, pos: Vector = Vector()):
        self.pos = pos
        self.state = {}

    def update(self):
        """The update loop"""
        pass

    def draw(self, surface, camera):
        """A generalized draw functions for any surface"""
        width, height = surface.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        DISPLAY.update(scale(surface, new_size), camera.transform(self.pos))
