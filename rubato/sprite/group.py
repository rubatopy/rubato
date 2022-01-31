"""
The Group class defines a group of sprites. This can used to quickly update
and render a lot of sprites at the same time. Collisions can also be applied
to entire groups.
"""
import typing
from rubato import Vector
from rubato.scenes import Camera
from rubato.sprite import Sprite, RigidBody


class Group:
    """
    A group of sprites.

    Attributes:
        z_index (int): The z-index of the entire group.
        sprites (List[Sprite]): The list of sprites in this group.
    """

    def __init__(self, z: int = 0):
        """
        Initializes a group.

        Args:
            z: The z-index of the group. Defaults to 0.
        """
        self._pos = Vector(0, 0)
        self.z_index = z
        self.sprites: typing.List[Sprite] = []

    def add(self, sprite: Sprite) -> Sprite:
        """
        Add a sprite to the group.

        Args:
            sprite: The sprite to add to the group

        Returns:
            Sprite: The sprite that was added
        """
        self.sprites.append(sprite)
        return sprite

    def collide_rb(self, rb: RigidBody):
        """
        Run a collision between the whole group and a RigidBody.

        Args:
            rb: The rigidbody to collide with.
        """
        for sprite in self.sprites:
            if sprite.in_frame:
                sprite.collide(rb)

    def collide_group(self, group: "Group"):
        """
        Run a collision between this group and another.

        Args:
            group: The group to collide with.
        """
        for sprite in self.sprites:
            if sprite.in_frame:
                group.collide_rb(sprite)

    def collide_self(self):
        """
        Run a collision between members of this group.
        """
        for sprite in self.sprites:
            for sprite2 in self.sprites:
                if sprite != sprite2 and sprite.in_frame and sprite2.in_frame:
                    sprite.collide(sprite2)

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
