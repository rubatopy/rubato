from rubato import Vector
from rubato.scenes import Camera
from rubato.sprite import Sprite


class Group:
    """
    A group of sprites. Can render and update all of them at once.
    """
    def __init__(self, z: int=0):
        self.pos = Vector(0, 0)
        self.z_index = z
        self.sprites = []

    def add(self, sprite: Sprite):
        """
        Adds a sprite to the groups.

        :param sprite: A sprite class to add to the group.
        :return: The sprite that was added.
        """
        self.sprites.append(sprite)
        return sprite

    def update(self):
        """Updates all the sprites in the group."""
        for sprite in self.sprites:
            sprite.update()

    def draw(self, camera: Camera):
        """Draws all the sprites in the group."""
        for sprite in sorted(self.sprites, key=lambda spr: spr.z_index):
            if sprite.z_index > camera.z_index:
                break
            sprite.draw(camera)
