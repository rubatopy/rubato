"""
An empty sprite. Doesn't draw or update anything by default. This useful for
running miscellaneous code every frame.
"""
from rubato.sprite import Sprite
from rubato.scenes import Camera


class Empty(Sprite):
    """
    An empty sprite.
    """

    def __init__(self):
        super().__init__()

    def update(self):
        """
        The update loop.
        """
        pass

    def draw(self):
        """
        The draw loop.
        """
        pass

    def is_in_frame(self, camera: Camera, game):
        pass
