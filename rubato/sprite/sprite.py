"""
The default sprite and component class.
"""
from typing import List, Union
import rubato.scenes as sc
import rubato.sprite as sp
from rubato.utils import Vector, Configs
from rubato.utils.error import ComponentNotAllowed, DuplicateComponentError


class Sprite:
    """
    The base sprite class.

    Attributes:
        pos (Vector): The current position of the sprite.
        z_index (int): The z_index of the sprite.
        in_frame (bool): Whether or not the sprite is in the frame.
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
        self.in_frame: bool = False
        self._components: List[Component] = []

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

    def is_in_frame(self, camera: sc.Camera, game) -> bool:
        """
        Checks if the sprite is in the frame.

        Args:
            camera: The camera to check with.
            game (Game): The game the sprite is in.

        Returns:
            bool: Whether or not the sprite is in the frame.
        """
        draw_area_tl = (camera.pos - game.window_size).ceil()
        draw_area_br = (camera.pos + game.window_size).ceil()

        if any(isinstance(comp, type(sp.Image)) for comp in self.components):
            image = self.get_component(type(sp.Image))

            sprite_tl = (self.pos - Vector(image.image.get_width(),
                                           image.image.get_height())).ceil()
            sprite_br = (self.pos + Vector(image.image.get_width(),
                                           image.image.get_height())).ceil()
        else:
            sprite_tl = self.pos
            sprite_br = self.pos

        return not (sprite_tl.x > draw_area_br.x
                    or sprite_br.x < draw_area_tl.x
                    or sprite_tl.y > draw_area_br.y
                    or sprite_br.y < draw_area_tl.y)

    def update(self):
        """The update loop"""
        for comp in self.components:
            comp.update()

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


class Component:
    """
    A base component. Does nothing by itself.
    """

    def __init__(self) -> None:
        """Initializes a component"""
        self.sprite: Union[Sprite, None] = None
        self.required: List[type] = []
        self.not_allowed: List[type] = []

    def update(self) -> None:
        """
        The main update loop for the component.
        """
        pass
