"""A slider component that can be used in UI."""
from typing import Callable

from . import Component
from ... import Input, Vector, Math, Debug
from ... import Color  # testing


class Slider(Component):
    """
    A Slider component. Still needs to be added to a :func:`GameObject <rubato.classes.game_object.GameObject>`.

    Args:
        offset: The offset of the component from the game object. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the component from the game object. Defaults to 0.
        button_width: The width of the clickable area. Defaults to 10.
        button_height: The height of the clickable area. Defaults to 10.
        slider_length: The length of the slider. Defaults to 10.
        slider_direction: The direction of the slider. Defaults to Vector(0, -1).
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
        slider_length (int): The length of the slider.
        slider_direction (Vector): The direction of the slider.
    """

    def __init__(
        self,
        offset: Vector = Vector(),
        rot_offset: float = 0,
        button_width: int = 10,
        button_height: int = 10,
        slider_length: int = 10,
        slider_direction: Vector = Vector(0, -1),
        onclick: Callable = lambda: None,
        onrelease: Callable = lambda: None,
        onhover: Callable = lambda: None,
        onexit: Callable = lambda: None
    ):
        super().__init__(offset=offset, rot_offset=rot_offset)
        self.dims: Vector = Vector(button_width, button_height)
        self.pressed: bool = False
        self.hover: bool = False
        self.onclick: Callable = onclick
        self.onrelease: Callable = onrelease
        self.onhover: Callable = onhover
        self.onexit: Callable = onexit
        self.slider_length: int = slider_length
        self.slider_direction: Vector = slider_direction
        self._button_pos_offset: Vector = Vector(0, 0)

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

        mouse_projection = (Input.get_mouse_pos().dot(self.slider_direction) / self.slider_direction.mag_sq)
        print(mouse_projection)
        self._button_pos_offset = Math.clamp(mouse_projection, 0, self.slider_length)
        Debug.circle(self.gameobj.pos + self.offset, 5, Color.red, fill=Color.red)
        Debug.circle(self.gameobj.pos + self.offset + self.slider_direction * self.slider_length, 5, fill=Color.green)
        Debug.line(
            self.gameobj.pos + self.offset,
            self.gameobj.pos + self.offset + self.slider_direction * self.slider_length,
            width=3
        )

        Debug.circle(self.gameobj.pos + self.offset + self.slider_direction * mouse_projection, 5, fill=Color.purple)


# TODO: force direction to unit vector
