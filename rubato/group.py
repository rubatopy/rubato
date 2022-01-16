from rubato import Vector
from rubato.scenes import Camera
from rubato.sprite import Sprite, RigidBody


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

    def draw(self, camera: Camera, game):
        """Draws all the sprites in the group."""
        for sprite in sorted(self.sprites, key=lambda spr: spr.z_index):
            if sprite.z_index <= camera.z_index:
                if isinstance(sprite, Group):
                    sprite.draw(camera, game)
                elif sprite.is_in_frame(camera, game):
                    sprite.in_frame = True
                    sprite.draw(camera)
                else:
                    sprite.in_frame = False
    
    def collide_rb(self, rb: RigidBody):
        for sprite in self.sprites:
            if sprite.in_frame:
                sprite.collide(rb)

    def collide_group(self, group: "Group"):
        for sprite in self.sprites:
            if sprite.in_frame:
                group.collide_rb(sprite)

    def collide_self(self):
        for sprite in self.sprites:
            for sprite2 in self.sprites:
                if sprite != sprite2 and sprite.in_frame and sprite2.in_frame:
                    sprite.collide(sprite2)
