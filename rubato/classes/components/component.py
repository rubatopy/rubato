"""
The component module that represents the template for all components.

Attention:
    Each component can only be attached to one game object. To add one component to multiple game objects, use the
    ``clone()`` method.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from ... import Vector, Defaults

if TYPE_CHECKING:
    from .. import GameObject, Camera


class Component:
    """
    A component adds functionality to the game object it is attached to. Note that this is a template class and should
    not be used directly. Instead create another class and extend from this one.

    Args:
        options: A Component config. Defaults to the :ref:`Component defaults <componentdef>`.

    Attributes:
        gameobj (GameObject): The game object this component is attached to.
        singular (bool): Whether multiple components of the same type are allowed on a game object.
        offset (Vector): The offset from the center of the game object that the hitbox should be placed.
        rotation_offset (float): The rotational offset from the game object's rotation.
    """

    def __init__(self, options: dict = {}):
        p = Defaults.component_defaults | options
        self.gameobj: Optional[GameObject] = None
        self.singular: bool = False
        self.offset: Vector = p["offset"]
        self.rotation_offset: float = p["rot_offset"]

    def draw(self, camera: Camera):
        """The draw function template for a component subclass."""
        pass

    def update(self):
        """The update function template for a component subclass."""
        pass

    def setup(self):
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
        new.rotation_offset = self.rotation_offset
        new.singular = self.singular
        return new
