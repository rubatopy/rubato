from pgp.utils import Vector

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

    def draw(self, camera):
        """The draw loop"""
        pass
