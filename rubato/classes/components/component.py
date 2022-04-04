"""A component gives functionally to game objects."""
from typing import Union, TYPE_CHECKING

from ... import Vector

if TYPE_CHECKING:
    from .. import GameObject


class Component:
    """
    A base component. Does nothing by itself.

    Attributes:
        gameobj (GameObject): The game object this component is attached to.
        singular (bool): Whether multiple components of the same type are allowed on a game object.
        offset (Vector): The offset from the center of the game object that the hitbox should be placed.
    """

    def __init__(self) -> None:
        """Initializes a component"""
        self.gameobj: Union["GameObject", None] = None
        self.singular: bool = False
        self.offset: Vector = Vector(0, 0)

    def draw(self) -> None:
        """The draw loop"""
        pass

    def update(self) -> None:
        """
        The main update loop for the component.
        """
        pass

    def setup(self) -> None:
        """
        Run after initialization and before update loop begins
        """
        pass

    def fixed_update(self):
        """The fixed update loop"""
        pass

    def delete(self):
        """Deletes the component"""
        pass
