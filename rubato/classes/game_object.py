"""
A game object is a basic element that holds components, postion, and z_index.
"""
from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING, Optional

from . import Hitbox, Polygon, Circle, Rectangle, Component
from .. import Game, Vector, Defaults, Display, DuplicateComponentError, Draw, Color

if TYPE_CHECKING:
    from . import Camera


class GameObject:
    """
    The base game object class.

    Args:
        options: A game object config. Defaults to the :ref:`Game Object defaults <gameobjdef>`.

    Attributes:
        name (str): The name of the game object. Will default to:
            "Game Object {number in group}"
        pos (Vector): The current position of the game object.
        z_index (int): The z_index of the game object.
        components (List[Component]): All the components attached to this
            game object.
        rotation (float): The rotation of the game object in degrees.
    """

    def __init__(self, options: dict = {}):
        param = Defaults.gameobj_defaults | options
        self.name: str = param["name"]
        self.pos: Vector = param["pos"]
        self.debug: bool = param["debug"]
        self.z_index: int = param["z_index"]
        self._components: Dict[type, List[Component]] = {}
        self.rotation: float = param["rotation"]

    def add(self, component: Component) -> GameObject:
        """
        Add a component to the game object.

        Args:
            component (Component): The component to add.

        Raises:
            DuplicateComponentError: Raised when there is already a component of the same type on the game object.

        Returns:
            GameObject: The current game object
        """
        comp_type = type(component)

        if component.singular and comp_type in self._components:
            raise DuplicateComponentError(
                f"There is already a component of type {comp_type} on the game object {self.name}"
            )

        if isinstance(component, Hitbox):
            component._pos = lambda: self.pos  # pylint: disable=protected-access
            comp_type = Hitbox

        if comp_type not in self._components:
            self._components[comp_type] = []
        self._components[comp_type].append(component)
        component.gameobj = self

        return self

    def remove(self, comp_type: type):
        """
        Removes a component from the game object.

        Args:
            comp_type (type): The type of the component to remove.

        Raises:
            Warning: The component was not in the game object and nothing was removed.
        """
        if comp_type in self._components:
            del self._components[comp_type][0]
            if not self._components[comp_type]:
                del self._components[comp_type]
        else:
            raise Warning(
                f"The component of type {comp_type} is not in the game object {self.name} and was not removed."
            )

    def remove_all(self, comp_type: type):
        """
        Removes all components of a type from the game object.

        Args:
            comp_type (type): The type of the component to remove.

        Raises:
            Warning: The components were not in the game object and nothing was removed.
        """
        if comp_type in self._components:
            del self._components[comp_type]
        else:
            raise Warning(
                f"The components of type {comp_type} are not in the game object {self.name} and were not removed."
            )

    def get(self, comp_type: type) -> Optional[Component]:
        """
        Gets a component from the game object.

        Args:
            comp_type (type): The type of the component to search for.

        Returns:
            Optional[Component]: The component if it was found or None if it wasn't.
        """
        if comp_type in (Rectangle, Polygon, Circle):
            comp_type = Hitbox
        if comp_type in self._components:
            return self._components[comp_type][0]
        return None

    def get_all(self, comp_type: type) -> List[Component]:
        """
        Gets all the components of a type from the game object.

        Args:
            comp_type (type): The type of component to search for.

        Returns:
            List[Component]: A list containing all the components of that type. If no components were found, the
                list is empty.
        """
        if comp_type in (Rectangle, Polygon, Circle):
            comp_type = Hitbox
        if comp_type in self._components:
            return self._components[comp_type]
        return []

    def delete(self):
        """
        Deletes and frees everything from the game object. This is called when you remove it from a group or scene.

        Warning:
            Calling this will render the gameobject useless in the future.
        """
        for comps in self._components.values():
            for comp in comps:
                comp.delete()

    def setup(self):
        for comps in self._components.values():
            for comp in comps:
                comp.setup()

    def draw(self, camera: Camera):
        for comps in self._components.values():
            for comp in comps:
                comp.draw(camera)

        if self.debug or Game.debug:
            rotated_x = Vector(int(camera.scale(10)), 0).rotate(self.rotation)
            rotated_y = Vector(0, int(camera.scale(10))).rotate(self.rotation)
            p1 = (camera.transform(self.pos) + rotated_x).to_int()
            p2 = (camera.transform(self.pos) - rotated_x).to_int()

            p3 = (camera.transform(self.pos) + rotated_y).to_int()
            p4 = (camera.transform(self.pos) - rotated_y).to_int()

            Draw.line(p1, p2, Color(0, 255), int(2 * max(1, Display.display_ratio.y)))
            Draw.line(p3, p4, Color(0, 255), int(2 * max(1, Display.display_ratio.y)))

    def update(self):
        for comps in self._components.values():
            for comp in comps:
                comp.update()

    def fixed_update(self):
        for comps in self._components.values():
            for comp in comps:
                comp.fixed_update()
