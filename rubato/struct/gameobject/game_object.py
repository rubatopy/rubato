"""
A game object is a basic element that holds components, postion, and z_index.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Type, TypeVar

from . import Hitbox, Polygon, Circle, Rectangle, Component
from ... import Game, Vector, Display, DuplicateComponentError, Draw, Color, ImplementationError, Camera

T = TypeVar("T")


class GameObject:
    """
    The base game object class.

    Args:
        name: The name of the game object. Defaults to "".
        pos: The position of the game object. Defaults to Vector(0, 0).
        rotation: The rotation of the game object. Defaults to 0.
        z_index: The z-index of the game object. Defaults to 0.
        debug: Whether or not to draw the center of the game object. Defaults to False.

    Attributes:
        name (str): The name of the game object. Will default to:
            "Game Object {number in group}"
        pos (Vector): The current position of the game object.
        z_index (int): The z_index of the game object.
        rotation (float): The rotation of the game object in degrees.
        debug (bool): Whether or not to draw a debug crosshair for the game object.
    """

    def __init__(
        self,
        name: str = "",
        pos: Vector = Vector(),
        rotation: float = 0,
        z_index: int = 0,
        debug: bool = False,
    ):
        self.name: str = name
        self.pos: Vector = pos
        self.debug: bool = debug
        self.z_index: int = z_index
        self._components: Dict[type, List[Component]] = {}
        self.rotation: float = rotation

    def add(self, *components: Component) -> GameObject:
        """
        Add a component to the game object.

        Args:
            components (Component): The component(s) to add.

        Raises:
            DuplicateComponentError: Raised when there is already a component of the same type on the game object.

        Returns:
            GameObject: This GameObject.
        """
        for component in components:
            comp_type = type(component)

            try:
                if component.singular and comp_type in self._components:
                    raise DuplicateComponentError(
                        f"There is already a component of type {comp_type} on the game object {self.name}"
                    )
            except AttributeError as err:
                raise ImplementationError(
                    "The component does not have a singular attribute. You most likely overrode the"
                    "__init__ method of the component without calling super().__init__()."
                ) from err

            if isinstance(component, Hitbox):
                comp_type = Hitbox

            if comp_type not in self._components:
                self._components[comp_type] = []
            self._components[comp_type].append(component)
            component.gameobj = self

        return self

    def remove(self, comp_type: Type[T]):
        """
        Removes a component from the game object.

        Args:
            comp_type: The type of the component to remove.

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

    def remove_all(self, comp_type: Type[T]):
        """
        Removes all components of a type from the game object.

        Args:
            comp_type: The type of the component to remove.

        Raises:
            Warning: The components were not in the game object and nothing was removed.
        """
        if comp_type in self._components:
            del self._components[comp_type]
        else:
            raise Warning(
                f"The components of type {comp_type} are not in the game object {self.name} and were not removed."
            )

    def get(self, comp_type: Type[T]) -> Optional[T]:
        """
        Gets a component from the game object.

        Args:
            comp_type: The type of the component to search for.

        Returns:
            The component if it was found or None if it wasn't.
        """
        if comp_type in (Rectangle, Polygon, Circle):
            comp_type = Hitbox
        if comp_type in self._components:
            return self._components[comp_type][0]
        return None

    def get_all(self, comp_type: Type[T]) -> List[T]:
        """
        Gets all the components of a type from the game object.

        Args:
            comp_type: The type of component to search for.

        Returns:
            A list containing all the components of that type. If no components were found, the
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

    def draw(self, camera: Camera):
        for comps in self._components.values():
            for comp in comps:
                comp.draw(camera)

        if self.debug or Game.debug:
            rotated_x = Vector(int(camera.scale(10)), 0).rotate(self.rotation)
            rotated_y = Vector(0, int(camera.scale(10))).rotate(self.rotation)
            p1 = (camera.transform(self.pos) + rotated_x).rounded()
            p2 = (camera.transform(self.pos) - rotated_x).rounded()

            p3 = (camera.transform(self.pos) + rotated_y).rounded()
            p4 = (camera.transform(self.pos) - rotated_y).rounded()

            Draw.queue_line(p1, p2, Color(0, 255), int(2 * max(1, Display.display_ratio.y)))
            Draw.queue_line(p3, p4, Color(0, 255), int(2 * max(1, Display.display_ratio.y)))

    def update(self):
        all_comps = list(self._components.values())
        for comps in all_comps:
            for comp in comps:
                comp.private_update()

    def fixed_update(self):
        for comps in self._components.values():
            for comp in comps:
                comp.fixed_update()

    def clone(self) -> GameObject:
        """
        Clones the game object.
        """
        new_obj = GameObject(
            name=f"{self.name} (clone)",
            pos=self.pos,
            rotation=self.rotation,
            z_index=self.z_index,
            debug=self.debug
        )
        for component in self._components.values():
            for comp in component:
                new_obj.add(comp.clone())

        return new_obj
