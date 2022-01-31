"""
We create the Scene class which is is a collection of sprites. Interactions
between sprites is handled here.
"""
from typing import Union
from rubato.scenes import Camera
from rubato.sprite import Sprite
from rubato.utils.error import IdError
from rubato.sprite import Group


class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled
    here.

    Attributes:
        sprites (dict[Union[int, str], Union[Sprite, Group]]): The collection
            of sprites housed in this scene.
        camera (Camera): The camera of this scene.
        id (Union[str, int]): The id of this scene.
    """

    def __init__(self):
        """
        Initializes a scene with an empty collection of sprites, a new camera,
        and a blank id.
        """
        self.sprites: dict[Union[int, str], Union[Sprite, Group]] = {}
        self.__min_id = 0
        self.camera = Camera()
        self.id: Union[str, int] = ""

    def add(self,
            sprite: Union[Sprite, Group],
            sprite_id: Union[int, str] = None) -> Union[str, int]:
        """
        Adds a sprite or a group to the scene.

        Args:
            sprite: The sprite or group to add to the scene.
            sprite_id: The i dof the sprite or group. Defaults to None.

        Raises:
            IdError: The given id is already used.

        Returns:
            Union[str, int]: The id of the added sprite or group
        """
        if sprite_id is None:
            sprite_id = self.__min_id
            self.__min_id += 1

        if sprite_id in self.sprites:
            raise IdError(
                f"The sprite id {sprite_id} is not unique in this scene")

        self.sprites[sprite_id] = sprite
        return sprite_id

    def remove(self, sprite_id: Union[int, str]):
        """
        Removes a sprite or group from the scene.

        Args:
            sprite_id: The id of the sprite or group.
        """
        try:
            del self.sprites[sprite_id]
        except KeyError:
            pass

    def update(self):
        """
        The update loop for this scene.
        """
        for sprite in self.sprites.values():
            sprite.update()

    def draw(self, game):
        """
        The draw loop for this scene.

        Args:
            game (Game): The game to draw too.
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
