"""
A sprite is a basic element that holds components, postion, and z_index.
"""
from typing import List, Union, TYPE_CHECKING
from rubato.classes.components import Hitbox
from rubato.utils import Vector, Defaults, Display
from rubato.utils.error import ComponentNotAllowed, DuplicateComponentError, Error
from rubato.game import Game
import sdl2
import sdl2.sdlgfx

if TYPE_CHECKING:
    from rubato.classes.component import Component


class Sprite:
    """
    The base sprite class.

    Attributes:
        name (str): The name of the sprite. Will default to:
            "Sprite {number in group}"
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
        param = Defaults.sprite_defaults | options
        self.name: str = param["name"]
        self.pos: Vector = param["pos"]
        self.debug: bool = param["debug"]
        self.z_index: int = param["z_index"]
        self.__components: List["Component"] = []

    @property
    def components(self):
        return self.__components

    def add(self, component: "Component") -> "Sprite":
        """
        Add a component to the sprite.

        Args:
            component: The component to add.

        Raises:
            DuplicateComponentError: Raised when there is already a component
                of the same type on the sprite.
            ComponentNotAllowed: Raised when an added component conflicts with
                another component.

        Returns:
            Sprite: The current sprite
        """
        comp_type = type(component)

        if any(isinstance(comp, comp_type) for comp in self.components):
            raise DuplicateComponentError(f"There is already a component of type {comp_type} on the sprite {self.name}")

        for not_allowed in component.not_allowed:
            if any(not_allowed == type(c).__name__ or any(not_allowed == base.__name__
                                                          for base in type(c).__bases__)
                   for c in self.components):
                raise ComponentNotAllowed(
                    f"The component of type {not_allowed} conflicts with another component on the sprite {self.name}")

        if isinstance(component, Hitbox):
            component._pos = lambda: self.pos  # pylint: disable=protected-access

        self.__components.append(component)
        component.sprite = self

        return self

    def remove(self, comp_type: type):
        """
        Removes a component from the sprite.

        Args:
            comp_type: The type of the component to remove.

        Raises:
            Warning: The component was not on the sprite and nothing
                was removed.
        """
        if self.get(comp_type) is not None:
            del self.components[self.components.index(self.get(comp_type))]
        else:
            raise Warning(f"The component of type {comp_type} is not on the sprite {self.name} and was not removed.")

    def get(self, comp_type: type) -> Union["Component", None]:
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
        return None

    def check_required(self):
        for comp in self.components:
            for required in comp.required:
                # Checks if required matches either the class or the parent
                if not any(required == type(c).__name__ or any(required == base.__name__
                                                               for base in type(c).__bases__)
                           for c in self.components):
                    raise Error(f"The component {comp} is missing its requirements")

    def setup(self):
        """
        Run after initialization and before update loop begins
        """
        self.check_required()
        for comp in self.components:
            comp.setup()

    def draw(self):
        """The draw loop"""
        for comp in self.components:
            comp.draw()

        if self.debug:
            relative_pos = Game.scenes.current.camera.transform(self.pos)
            sdl2.sdlgfx.hlineRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x) - int(Game.scenes.current.camera.scale(10)),
                int(relative_pos.x) + int(Game.scenes.current.camera.scale(10)),
                int(relative_pos.y),
                0,
                255,
                0,
                255,
            )
            sdl2.sdlgfx.vlineRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y) - int(Game.scenes.current.camera.scale(10)),
                int(relative_pos.y) + int(Game.scenes.current.camera.scale(10)),
                0,
                255,
                0,
                255,
            )

    def update(self):
        """The update loop"""
        for comp in self.components:
            comp.update()

    def fixed_update(self):
        for comp in self.components:
            comp.fixed_update()
