from rubato import Vector
from rubato.scenes import Camera
from rubato.sprite import Sprite
from rubato.utils import check_types


class Group:
    """
    A group of sprites. Can render and update all of them at once.
    """
    def __init__(self, z: int=0):
        check_types(Group.__init__, locals())
        self.pos = Vector(0, 0, z)
        self.sprites = []

    def add(self, sprite: Sprite):
        """
        Adds a sprite to the groups.

        :param sprite: A sprite class to add to the group.
        :return: The sprite that was added.
        """
        check_types(Group.add, locals())
        self.sprites.append(sprite)
        return sprite

    def update(self):
        """Updates all the sprites in the group."""
        for sprite in self.sprites:
            sprite.update()

    def draw(self, camera: Camera):
        """Draws all the sprites in the group."""
        check_types(Group.draw, locals())
        for sprite in sorted(self.sprites, key=lambda spr: spr.pos.z):
            if sprite.pos.z > camera.pos.z:
                break
            sprite.draw(camera)
