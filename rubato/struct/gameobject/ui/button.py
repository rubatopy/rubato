"""A button component that can be used in UI or to detect mouse presses in an area."""
from __future__ import annotations
from typing import Callable

from .. import Component
from .... import Input, Vector


class Button(Component):
    """
    A Button component. Add this to game objects or UI elements to give them clickable areas.

    Args:
        width: The width of the button. Defaults to 10.
        height: The height of the button. Defaults to 10.
        onclick: The function to call when the button is clicked. Defaults to lambda: None.
        onrelease: The function to call when the button is released. Defaults to lambda: None.
        onhover: The function to call when the mouse enters the button. Defaults to lambda: None.
        onexit: The function to call when the mouse exits the button. Defaults to lambda: None.
        offset: The offset of the button from the game object. Defaults to (0, 0).
        rot_offset: The rotation offset of the button from the game object. Defaults to 0.
        z_index: The z-index of the button. Defaults to 0.
        hidden: Whether the button is hidden or not. Defaults to False.
    """

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        onclick: Callable | None = None,
        onrelease: Callable | None = None,
        onhover: Callable | None = None,
        onexit: Callable | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index, hidden=hidden)
        self.dims: Vector = Vector(width, height)
        """The dimensions of the button."""
        self.pressed: bool = False
        """Whether the button is currently pressed."""
        self.hover: bool = False
        """Whether the mouse is hovering over the button."""
        self.onclick: Callable = onclick if onclick else lambda: None
        """The function to call when the button is clicked."""
        self.onrelease: Callable = onrelease if onrelease else lambda: None
        """The function to call when the button is released."""
        self.onhover: Callable = onhover if onhover else lambda: None
        """The function to call when the mouse enters the button."""
        self.onexit: Callable = onexit if onexit else lambda: None
        """The function to call when the mouse exits the button."""

    def update(self):
        """The update function for buttons."""
        if not self.hover and Input.mouse_in(self.true_pos(), self.dims, self.true_rotation()):
            self.hover = True
            self.onhover()
        elif self.hover and not Input.mouse_in(self.true_pos(), self.dims, self.true_rotation()):
            self.hover = False
            self.onexit()

        if (not self.pressed) and Input.mouse_state()[0] and self.hover:
            self.pressed = True
            self.onclick()
        elif self.pressed and (not Input.mouse_state()[0] or not self.hover):
            self.pressed = False
            self.onrelease()

    def clone(self) -> Button:
        return Button(
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            width=round(self.dims.x),
            height=round(self.dims.y),
            onclick=self.onclick,
            onrelease=self.onrelease,
            onhover=self.onhover,
            onexit=self.onexit,
            z_index=self.z_index,
        )
