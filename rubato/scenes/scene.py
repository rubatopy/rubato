"""
We create the Scene class which is is a collection of sprites. Interactions
between sprites is handled here.
"""

from rubato.scenes import Camera
from rubato.sprite import Sprite
from rubato.group import Group


class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is
    handled here.
    """

    def __init__(self):
        self.sprites = {}
        self.min_id = 0
        self.camera = Camera()
        self.id = ""

    def add(self, sprite: Sprite | Group, sprite_id: int | str = ""):
        """
        Adds a sprite to the scene.

        :param sprite_id: The id of the sprite
        :param sprite: The sprite object to be added.
        """
        if sprite_id == "":
            sprite_id = self.min_id
            self.min_id += 1

        if sprite_id in self.sprites.keys():
            raise ValueError(f"The sprite id {sprite_id} is not unique in this "
                             f"scene")

        self.sprites[sprite_id] = sprite
        return sprite_id

    def remove(self, sprite_id: int | str):
        """
        Removes a sprite with a given sprite id

        :param sprite_id: The id of the sprite to remove
        """
        if sprite_id not in self.sprites.keys():
            raise ValueError(f"The sprite corresponding to {sprite_id} does not"
                             f" exist in this scene")

        del self.sprites[sprite_id]

    def update(self):
        """
        The update loop for this scene.
        """
        for sprite in self.sprites.values():
            sprite.update()

    def draw(self, game):
        """
        The draw loop for this scene.
        """
        for sprite in sorted(self.sprites.values(),
                             key=lambda spr: spr.z_index):
            if sprite.z_index <= self.camera.z_index:
                if isinstance(sprite, Group):
                    sprite.draw(self.camera, game)
                elif sprite.is_in_frame(self.camera, game):
                    sprite.draw(self.camera)
                    sprite.in_frame = True
                else:
                    sprite.in_frame = False
