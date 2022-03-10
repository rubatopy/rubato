"""A component gives functionally to sprites."""
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from rubato.classes.sprite import Sprite


class Component:
    """
    A base component. Does nothing by itself.

    Attributes:
        sprite (Sprite): The sprite this component is attached to.
        required (List[type]): A list of components that are required by this
            component. (For example, a RigidBody needs a Hitbox).
        not_allowed(List[type]): A list of components that cannot be on the
            same Sprite. (For example, an Animation and an Image cannot be
            on the same Sprite)
    """

    def __init__(self) -> None:
        """Initializes a component"""
        self.sprite: Union["Sprite", None] = None
        self.required: List[str] = []
        self.not_allowed: List[str] = []

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
