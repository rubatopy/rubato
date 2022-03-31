"""
A UI is a an object that is drawn to the screen at a constant position no matter how the camera moves. They are also
always drawn on top of everything else.
"""
from sdl2.sdlgfx import thickLineRGBA

from . import GameObject
from .. import Defaults, Game, Display


class UI(GameObject):
    """
    An empty UI element.

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
        Initializes a UI.

        Args:
            options: A UI config. Defaults to the |default| for `UI`.
        """
        param = Defaults.ui_defaults | options
        super().__init__(param)

    def draw(self):
        """The draw loop"""
        for comps in self._components.values():
            for comp in comps:
                comp.draw()

        if self.debug or Game.debug:
            thickLineRGBA(
                Display.renderer.sdlrenderer,
                int(self.pos.x) - 10, int(self.pos.y),
                int(self.pos.x) + 10, int(self.pos.y), int(2 * Display.display_ratio.y), 0, 255, 0, 255
            )
            thickLineRGBA(
                Display.renderer.sdlrenderer, int(self.pos.x),
                int(self.pos.y) - 10, int(self.pos.x),
                int(self.pos.y) + 10, int(2 * Display.display_ratio.x), 0, 255, 0, 255
            )
