"""
The component module that represents the template for all components.

Attention:
    Each component can only be attached to one game object. To add one component to multiple game objects, use the
    ``clone()`` method.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import cython

from ... import Vector, Camera

if TYPE_CHECKING:
    from .. import GameObject


@cython.cclass
class Component:
    """
    A component adds functionality to the game object it is attached to. Note that this is a template class and should
    not be used directly. Instead, create another class and extend from this one.

    Args:
        offset: The offset of the component from the game object. Defaults to (0, 0).
        rot_offset: The rotation offset of the component from the game object. Defaults to 0.
        z_index: The vertical offset of where to draw the component. Defaults to 0.
    """

    def __init__(self, offset: Vector | tuple[float, float] = (0, 0), rot_offset: float = 0, z_index: int = 0):
        self.gameobj: GameObject | None = None
        """The game object this component is attached to."""
        self.singular: bool = False
        """Whether multiple components of the same type are allowed on a game object."""
        self.offset: Vector = Vector.create(offset)
        """The offset from the center of the game object that the hitbox should be placed."""
        self.rot_offset: float = rot_offset
        """The rotational offset from the game object's rotation."""
        self.z_index: int = z_index
        """Where to draw the component in the z direction."""
        self.started = False
        """Whether the component has run its setup method."""
        self.hidden = False
        """Whether the component should not draw."""

    def true_z(self) -> int:
        """Returns the z_index of the component offset by its parent gameobject z_index."""
        return self.z_index + (self.gameobj.z_index if self.gameobj else 0)

    def true_pos(self) -> Vector:
        """Returns the world position of the component."""
        return (self.gameobj.pos if self.gameobj else 0) + self.offset.rotate(
            (self.gameobj.rotation if self.gameobj else 0)
        )

    def true_rotation(self) -> float:
        """Returns the rotation of the component offset by its parent gameobject rotation."""
        return (self.gameobj.rotation if self.gameobj else 0) + self.rot_offset

    def draw(self, camera: Camera):
        """The draw function template for a component subclass."""
        pass

    def private_update(self):
        if not self.started:
            self.private_setup()

        self.update()

    def update(self):
        """The update function template for a component subclass."""
        pass

    def private_setup(self):
        self.started = True
        self.setup()

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
        new = Component(offset=self.offset.clone(), rot_offset=self.rot_offset, z_index=self.z_index)
        new.singular = self.singular
        return new

    def __repr__(self):
        if self.gameobj is not None:
            return f"{type(self).__name__} with game object {self.gameobj.name} at {hex(id(self))}"
        else:
            return f"{type(self).__name__} with no game object at {hex(id(self))}"
