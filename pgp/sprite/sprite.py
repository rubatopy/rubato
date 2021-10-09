from pgp.utils import Point

class Sprite:
    """
    The base sprite class.

    :param pos: The position of the sprite on screen. Defaults to (0, 0, 0)
    """

    def __init__(self, pos: Point = Point()):
        self.pos = pos
        self.state = {}

    def update(self):
        """The update loop"""
        pass

    def draw(self, camera):
        """The draw loop"""
        pass
