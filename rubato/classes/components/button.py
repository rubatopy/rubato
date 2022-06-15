"""A button component that can be used in UI or to detect mouse presses in an area."""
from typing import Callable

from . import Component
from ... import Input, Vector


class Button(Component):
    """
    A Button component. Add this to game objects or UI elements to give them clickable areas.

    Args:
        offset: The offset of the button from the game object. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the button from the game object. Defaults to 0.
        width: The width of the button. Defaults to 10.
        height: The height of the button. Defaults to 10.
        onclick: The function to call when the button is clicked. Defaults to lambda: None.
        onrelease: The function to call when the button is released. Defaults to lambda: None.
        onhover: The function to call when the mouse enters the button. Defaults to lambda: None.
        onexit: The function to call when the mouse exits the button. Defaults to lambda: None.

    Attributes:
        pressed (bool): Whether the button is currently pressed.
        hover (bool): Whether the mouse is hovering over the button.
        dims (Vector): The dimensions of the button.
        onclick (Callable): The function to call when the button is clicked.
        onrelease (Callable): The function to call when the button is released.
        onhover (Callable): The function to call when the mouse enters the button.
        onexit (Callable): The function to call when the mouse exits the button.
    """

    def __init__(
        self,
        offset: Vector = Vector(),
        rot_offset: float = 0,
        width: int = 10,
        height: int = 10,
        onclick: Callable = lambda: None,
        onrelease: Callable = lambda: None,
        onhover: Callable = lambda: None,
        onexit: Callable = lambda: None,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset)
        self.dims: Vector = Vector(width, height)
        self.pressed: bool = False
        self.hover: bool = False
        self.onclick: Callable = onclick
        self.onrelease: Callable = onrelease
        self.onhover: Callable = onhover
        self.onexit: Callable = onexit

    def update(self):
        """The update function for buttons."""
        if not self.hover and Input.mouse_in(self.gameobj.pos + self.offset, self.dims,
                                             self.gameobj.rotation + self.rotation_offset):
            self.hover = True
            self.onhover()
        elif self.hover and not Input.mouse_in(
            self.gameobj.pos + self.offset, self.dims, self.gameobj.rotation + self.rotation_offset
        ):
            self.hover = False
            self.onexit()

        if (not self.pressed) and Input.mouse_state()[0] and self.hover:
            self.pressed = True
            self.onclick()
        elif self.pressed and (not Input.mouse_state()[0] or not self.hover):
            self.pressed = False
            self.onrelease()
