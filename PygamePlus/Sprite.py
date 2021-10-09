from pygame.image import load
from PygamePlus.utils.DISPLAY import GD

class Sprite:
    """
    The base sprite class.

    :param x: The x position of the sprite (in pixels).
    :param y: The y position of the sprite (in pixels).
    :param image_location: The location of the sprite.
    """

    def __init__(self, x: int, y: int, image_location: str):
        self.position = (x, y)
        self.image = load(image_location)

    def update(self):
        """The update loop"""
        pass

    def draw(self):
        """The draw loop"""
        GD.update(self.image, self.position)
