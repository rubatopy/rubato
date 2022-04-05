"""
The component module that represents the template for all components.

Attention:
    Each component can only be attached to one game object. To add one component to multiple game objects, use the
    ``clone()`` method.
"""
from __future__ import annotations
from typing import Union, TYPE_CHECKING

from ... import Vector

if TYPE_CHECKING:
    from .. import GameObject


class Component:
    """
    A component adds functionality to the game object it is attached to.

    Attributes:
        gameobj (GameObject): The game object this component is attached to.
        singular (bool): Whether multiple components of the same type are allowed on a game object.
        offset (Vector): The offset from the center of the game object that the hitbox should be placed.
    """

    def __init__(self) -> None:
        """
        Initializes a Component.
        This is a superclass and as such does not take parameters.
        """
        self.gameobj: Union[GameObject, None] = None
        self.singular: bool = False
        self.offset: Vector = Vector(0, 0)

    def draw(self) -> None:
        """The draw function template for a component subclass."""
        pass

    def update(self) -> None:
        """The update function template for a component subclass."""
        pass

    def setup(self) -> None:
        """The setup function template for a component subclass."""
        pass

    def fixed_update(self):
        """The physics function template for a component subclass."""
        pass

    def delete(self):
        """The delete function template for a component subclass."""
        pass

    def clone(self) -> Component:
        """Clones the component."""
        new = Component()
        new.gameobj = self.gameobj
        new.offset = self.offset
        return new
