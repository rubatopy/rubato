"""
A UI is a an object that is drawn to the screen at a constant position no matter how the camera moves. They are also
always drawn on top of everything else.
"""
from typing import Union

from . import GameObject
from .. import Defaults, Vector, Game


class UI(GameObject):
    """
    An empty UI element.

    Attributes:
        name (str): The name of the game object. Will default to:
            "Game Object {number in group}"
        pos (Vector): The current position of the game object.
        z_index (int): The z_index of the game object.
        components (List[Component]): All the components attached to this
            game object.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a UI.

        Args:
            options: A UI config. Defaults to the |default| for `UI`.
        """
        param = Defaults.ui_defaults | options
        super().__init__(param)

    @property
    def z_index(self):
        """
        The z_index of the UI.
        """
        return Game.camera.z_index

    @z_index.setter
    def z_index(self, value: int):
        pass

    @property
    def relative_pos(self) -> Vector:
        """
        The relative position of the UI.
        """
        return self.pos

    def map_coord(self, coord: Vector) -> Vector:
        """
        Maps a coordinate to the UI's coordinate system.

        Args:
            coord: The coordinate to map.

        Returns:
            Vector: The mapped coordinate.
        """
        return coord

    def scale_value(self, value: Union[int, float]) -> Union[int, float]:
        """
        Scales a value to match the UI's scale.

        Args:
            value: The value to scale.

        Returns:
            Union[int, float]: The scaled value.
        """
        return value
