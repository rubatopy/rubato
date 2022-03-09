"""
A sprite is a basic element that holds components, postion, and z_index.
"""
from typing import List, Union, TYPE_CHECKING
from rubato.classes.components import Hitbox
from rubato.utils import Vector, Configs
from rubato.utils.error import ComponentNotAllowed, DuplicateComponentError

if TYPE_CHECKING:
    from rubato.classes.component import Component


class Sprite:
    """
    The base sprite class.

    Attributes:
        pos (Vector): The current position of the sprite.
        z_index (int): The z_index of the sprite.
        components (List[Component]): All the components attached to this
            sprite.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a sprite.

        Args:
            options: A sprite config. Defaults to the |default| for
                `Sprite`.
        """
        param = Configs.merge_params(options, Configs.sprite_defaults)
        self.pos: Vector = param["pos"]
        self.z_index: int = param["z_index"]
        self._components: List["Component"] = []

    @property
    def components(self):
        return self._components

    def add_component(self, component: "Component") -> "Sprite":
        """
        Add a component to the sprite.

        Args:
            component: The component to add.

        Raises:
            DuplicateComponentError: Raised when there is already a component
                of the same type on the sprite.

        Returns:
            Sprite: The current sprite
        """
        comp_type = type(component)

        if isinstance(component, Hitbox):
            component._pos = lambda: self.pos  # pylint: disable=protected-access

        if any(isinstance(comp, comp_type) for comp in self.components):
            raise DuplicateComponentError(
                "There is already a component of type " + str(comp_type) +
                " on this sprite")

        for not_allowed_type in component.not_allowed:
            if any(
                    isinstance(comp, not_allowed_type)
                    for comp in self.components):
                raise ComponentNotAllowed(
                    "The component of type " + str(not_allowed_type) +
                    " conflicts with another component on the sprite.")

        self._components.append(component)
        component.sprite = self

        return self

    def get_component(self, comp_type: type) -> Union["Component", None]:
        """
        Gets a component from the sprite.

        Args:
            comp_type: The type of the component to search for.

        Returns:
            Union[Component, None]: The component if it was found or None if it
            wasn't.
        """
        for comp in self.components:
            if isinstance(comp, comp_type):
                return comp

    def draw(self):
        """The draw loop"""
        for comp in self.components:
            comp.draw()

    def update(self):
        """The update loop"""
        for comp in self.components:
            comp.update()

    def fixed_update(self):
        for comp in self.components:
            comp.fixed_update()

    @staticmethod
    def center_to_tl(center: Vector, dims: Vector) -> Vector:
        """
        Converts center coordinates to top left coordinates

        Args:
            center: The top left coordinate as a Vector
            dims: The width and the height of the item as a sprite as a Vector

        Returns:
            Vector: The new coordinates.
        """
        return (center - (dims / 2)).ceil()
