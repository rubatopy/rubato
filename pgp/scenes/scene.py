from pgp.scenes import Camera
from pgp.sprite import Sprite


class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled here.
    """

    def __init__(self):
        self.sprites = {}
        self.min_id = 0
        self.camera = Camera()

    def add(self, sprite: Sprite, sprite_id: int or str = None):
        """
        Adds a sprite to the scene.

        :param sprite_id: The id of the sprite
        :param sprite: The sprite object to be added.
        """
        if sprite_id is None:
            sprite_id = self.min_id
            self.min_id += 1

        if sprite_id in self.sprites.keys():
            raise ValueError(f"The sprite id {sprite_id} is not unique in this scene")

        self.sprites[sprite_id] = sprite
        return sprite_id

    def remove(self, sprite_id: int or str):
        """
        Removes a sprite with a given sprite id

        :param sprite_id: The id of the sprite to remove
        """
        if sprite_id not in self.sprites.keys():
            raise ValueError(f"The sprite corresponding to {sprite_id} does not exist in this scene")

        del self.sprites[sprite_id]

    def update(self):
        """
        The update loop for this scene.
        """
        for sprite in self.sprites.values():
            sprite.update()

    def draw(self):
        """
        The draw loop for this scene.
        """
        for sprite in sorted(self.sprites.values(), key=lambda spr: spr.pos.z):
            if sprite.pos.z > self.camera.pos.z:
                break
            sprite.draw(self.camera)
