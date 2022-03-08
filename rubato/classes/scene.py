"""
We create the Scene class which is is a collection of sprites. Interactions
between sprites is handled here.
"""
from typing import Union, Dict
from rubato.classes.camera import Camera
import rubato.classes as rb
from rubato.utils.error import IdError


class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled
    here.

    Attributes:
        sprites (dict[Union[int, str], Sprite]): The collection
            of sprites housed in this scene.
        camera (Camera): The camera of this scene.
        id (Union[str, int]): The id of this scene.
    """

    def __init__(self):
        """
        Initializes a scene with an empty collection of sprites, a new camera,
        and a blank id.
        """
        self.sprites: Dict[Union[int, str], rb.Sprite] = {}
        self.__min_id = 0
        self.camera = Camera()
        self.id: Union[str, int] = ""

    def add(self,
            sprite: rb.Sprite,
            sprite_id: Union[int, str] = None) -> Union[str, int]:
        """
        Adds a sprite to the scene.

        Args:
            sprite: The sprite to add to the scene.
            sprite_id: The id of the sprite. Defaults to None.

        Raises:
            IdError: The given id is already used.

        Returns:
            Union[str, int]: The id of the added sprite.
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
        Removes a sprite from the scene.

        Args:
            sprite_id: The id of the sprite.
        """
        try:
            del self.sprites[sprite_id]
        except KeyError:
            pass

    def private_draw(self):
        for sprite in self.sprites.values():
            sprite.draw()

    def private_update(self):
        self.update()
        for sprite in self.sprites.values():
            sprite.update()

    def private_fixed_update(self):
        self.fixed_update()
        for sprite in self.sprites.values():
            sprite.fixed_update()

    def update(self):
        """
        The update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass

    def fixed_update(self):
        """
        The fixed update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass
