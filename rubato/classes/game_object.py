"""
A game object is a basic element that holds components, postion, and z_index.
"""
from typing import List, Union, TYPE_CHECKING
from rubato.classes.components.hitbox import Hitbox
from rubato.utils import Vector, Defaults, Display
from rubato.utils.error import DuplicateComponentError
from rubato.game import Game
import sdl2
import sdl2.sdlgfx

if TYPE_CHECKING:
    from rubato.classes.component import Component


class GameObject:
    """
    The base game object class.

    Attributes:
        name (str): The name of the game object. Will default to:
            "Game Object {number in group}"
        pos (Vector): The current position of the game object.
        z_index (int): The z_index of the game object.
        components (List[Component]): All the components attached to this
            game object.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a game object.

        Args:
            options: A game object config. Defaults to the |default| for
                `Game Object`.
        """
        param = Defaults.gameobj_defaults | options
        self.name: str = param["name"]
        self.pos: Vector = param["pos"]
        self.debug: bool = param["debug"]
        self.z_index: int = param["z_index"]
        self.__components: List["Component"] = []

    @property
    def components(self):
        return self.__components

    def add(self, component: "Component") -> "GameObject":
        """
        Add a component to the game object.

        Args:
            component: The component to add.

        Raises:
            DuplicateComponentError: Raised when there is already a component
                of the same type on the game object.
            ComponentNotAllowed: Raised when an added component conflicts with
                another component.

        Returns:
            Game Object: The current game object
        """
        comp_type = type(component)

        if component.singular:
            for comp in self.components:
                if isinstance(comp, comp_type):
                    raise DuplicateComponentError(
                        f"There is already a component of type {comp_type} on the game object {self.name}"
                    )

        if isinstance(component, Hitbox):
            component._pos = lambda: self.pos  # pylint: disable=protected-access

        self.__components.append(component)
        component.gameobj = self

        return self

    def remove(self, comp_type: type):
        """
        Removes a component from the game object.

        Args:
            comp_type: The type of the component to remove.

        Raises:
            Warning: The component was not on the game object and nothing
                was removed.
        """
        if self.get(comp_type) is not None:
            del self.components[self.components.index(self.get(comp_type))]
        else:
            raise Warning(
                f"The component of type {comp_type} is not on the game object {self.name} and was not removed."
            )

    def get(self, comp_type: type) -> Union["Component", None]:
        """
        Gets a component from the game object.

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

    def get_all(self, comp_type: type) -> List["Component"]:
        """
        Gets all the components of a type from the game object.

        Args:
            comp_type: The type of component to search for.

        Returns:
            List["Component"]: A list containing all the components of that type. If no components were found, the
            list is empty.
        """
        return [comp for comp in self.components if isinstance(comp, comp_type)]

    def setup(self):
        """
        Run after initialization and before update loop begins
        """
        for comp in self.components:
            comp.setup()

    def draw(self):
        """The draw loop"""
        for comp in self.components:
            comp.draw()

        if self.debug or Game.debug:
            relative_pos = Game.scenes.current.camera.transform(self.pos)
            sdl2.sdlgfx.thickLineRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x) - int(Game.scenes.current.camera.scale(10)), int(relative_pos.y),
                int(relative_pos.x) + int(Game.scenes.current.camera.scale(10)), int(relative_pos.y),
                int(2 * Display.display_ratio.y), 0, 255, 0, 255
            )
            sdl2.sdlgfx.thickLineRGBA(
                Display.renderer.sdlrenderer, int(relative_pos.x),
                int(relative_pos.y) - int(Game.scenes.current.camera.scale(10)), int(relative_pos.x),
                int(relative_pos.y) + int(Game.scenes.current.camera.scale(10)), int(2 * Display.display_ratio.x), 0,
                255, 0, 255
            )

    def update(self):
        """The update loop"""
        for comp in self.components:
            comp.update()

    def fixed_update(self):
        """The fixed update loop"""
        for comp in self.components:
            comp.fixed_update()
