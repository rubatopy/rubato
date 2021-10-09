from pgp.scenes import Camera
from pgp.sprite import Sprite

class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled here.
    """

    def __init__(self):
        self.sprites = []
        self.camera = Camera()

    # TODO Sprite remove function. Also, index sprites by ID like in scenemanager
    def add(self, sprite: Sprite):
        """
        Adds a sprite to the scene.

        :param sprite: The sprite object to be added.
        """
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
        for sprite in sorted(self.sprites, key=lambda spr: spr.pos.z):
            if sprite.pos.z > self.camera.pos.z:
                break
            sprite.draw(self.camera)
