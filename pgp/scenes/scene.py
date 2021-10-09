from pgp.scenes import Camera
from pgp.sprite import Sprite

class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled here.
    """

    def __init__(self):
        self.sprites = []
        self.camera = Camera()

    # TODO Sprite remove function
    def add(self, sprite: Sprite):
        self.sprites.append(sprite)

    def update(self):
        """
        The update loop for this scene.
        """
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        """
        The draw loop for this scene.
        """
        for sprite in self.sprites:
            sprite.draw(self.camera)
