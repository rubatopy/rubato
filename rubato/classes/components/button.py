"""A button component that can be used in UI or to detect mouse presses in an area."""
from typing import Callable

from . import Component
from ... import Defaults, Input, Vector


class Button(Component):
    """
    A Button component. Add this to game objects or UI elements to give them clickable areas.

    Attributes:
        pressed (bool): Whether the button is currently pressed.
        hover (bool): Whether the mouse is hovering over the button.
        dims (Vector): The dimensions of the button.
        onclick (Callable): The function to call when the button is clicked.
        onrelease (Callable): The function to call when the button is released.
        onhover (Callable): The function to call when the mouse enters the button.
        onexit (Callable): The function to call when the mouse exits the button.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Button.

        Args:
            options: A Button config. Defaults to the :ref:`Button defaults <buttondef>`.
        """
        params = Defaults.button_defaults | options
        super().__init__(params)
        self.dims: Vector = Vector(params["width"], params["height"])
        self.pressed: bool = False
        self.hover: bool = False
        self.onclick: Callable = params["onclick"]
        self.onrelease: Callable = params["onrelease"]
        self.onhover: Callable = params["onhover"]
        self.onexit: Callable = params["onexit"]

    def update(self):
        """The update function for buttons."""
        if not self.hover and Input.mouse_in(self.gameobj.pos, self.dims, self.gameobj.rotation + self.rotation_offset):
            self.hover = True
            self.onhover()
        elif self.hover and not Input.mouse_in(
            self.gameobj.pos, self.dims, self.gameobj.rotation + self.rotation_offset
        ):
            self.hover = False
            self.onexit()

        if (not self.pressed) and Input.mouse_is_pressed()[0] and self.hover:
            self.pressed = True
            self.onclick()
        elif self.pressed and (not Input.mouse_is_pressed()[0] or not self.hover):
            self.pressed = False
            self.onrelease()
