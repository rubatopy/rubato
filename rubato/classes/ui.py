"""
A UIElement is a game object that is drawn to the screen at a constant position no matter how the camera moves.
They are drawn at the camera's z-index, meaning they will usually draw on top of other game objects.
"""
from typing import Union

from . import GameObject
from .. import Defaults, Vector, Game


class UIElement(GameObject):
    """
    Defines a UIElement.

    Attributes:
        name (str): The name of the UI. Will default to:
            "UI {number in group}"
        pos (Vector): The current position of the UI.
        components (List[Component]): All the components attached to this
            UI.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a UIElement.

        Args:
            options: A UIElement config. Defaults to the |default| for `UIElement`.
        """
        param = Defaults.ui_defaults | options
        super().__init__(param)

    @property
    def z_index(self):
        """The z_index of the UIElement."""
        return Game.camera.z_index

    @z_index.setter
    def z_index(self, _):
        pass

    @property
    def relative_pos(self) -> Vector:
        """The relative position of the UIElement."""
        return self.pos

    @staticmethod
    def map_coord(coord: Vector) -> Vector:
        """
        Maps a coordinate to the UIElement's coordinate system.

        Args:
            coord: The coordinate to map.

        Returns:
            Vector: The mapped coordinate.
        """
        return coord

    @staticmethod
    def scale_value(value: Union[int, float]) -> Union[int, float]:
        """
        Scales a value to match the UIElement's scale.

        Args:
            value: The value to scale.

        Returns:
            Union[int, float]: The scaled value.
        """
        return value
