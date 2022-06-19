"""A slider component that can be used in UI."""
from __future__ import annotations

from . import Component, Button
from ... import Input, Vector, Math, Draw
from ... import Color  # testing

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .. import Camera


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
        button (Button): The button component.
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
        onexit: Callable = lambda: None,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self.dims: Vector = Vector(button_width, button_height)
        self.pressed: bool = False
        self.hover: bool = False
        self.onclick: Callable = onclick
        self.onrelease: Callable = onrelease
        self.onhover: Callable = onhover
        self.onexit: Callable = onexit
        self.slider_length: int = slider_length
        self.slider_direction: Vector = slider_direction

        # button handled by slider and not by game object
        self.button = Button(
            width=button_width, height=button_height, onclick=onclick, onrelease=onrelease, onexit=onexit
        )

    def update(self):
        """The update function for buttons."""
        # custom button update
        if not self.button.hover and Input.mouse_in(
            self.gameobj.pos + self.offset + self.button.offset, self.button.dims,
            self.gameobj.rotation + self.rotation_offset
        ):
            self.button.hover = True
            self.button.onhover()
        elif self.button.hover and not Input.mouse_in(
            self.gameobj.pos + self.offset + self.button.offset, self.button.dims,
            self.gameobj.rotation + self.rotation_offset
        ):

            self.button.hover = False
            self.button.onexit()

        if (not self.button.pressed) and Input.mouse_state()[0] and self.button.hover:
            self.button.pressed = True
            self.button.onclick()
        elif self.button.pressed and not Input.mouse_state()[0]:
            self.button.pressed = False
            self.button.onrelease()
        # end custom button update

        slider_direction: Vector = Vector.from_radial(1, self.gameobj.rotation + self.rotation_offset)
        mouse_projection = Math.clamp(
            (Input.get_mouse_pos() - self.gameobj.pos - self.offset).dot(slider_direction) / slider_direction.mag_sq, 0,
            self.slider_length
        )
        self.button.offset = Math.clamp(mouse_projection, 0, self.slider_length)
        Draw.circle(self.gameobj.pos + self.offset, 5, Color.red, fill=Color.red)
        Draw.circle(self.gameobj.pos + self.offset + slider_direction * self.slider_length, 5, fill=Color.green)
        Draw.line(
            self.gameobj.pos + self.offset,
            self.gameobj.pos + self.offset + slider_direction * self.slider_length,
            width=3
        )

        Draw.circle(
            self.gameobj.pos + self.offset + slider_direction * mouse_projection,
            5,
            fill=Color.purple if self.button.pressed else Color.blue
        )

    def draw(self, camera: Camera):
        """The draw function for buttons."""
        super().draw(camera)
        self.button.draw(camera)


# TODO: force direction to unit vector
# TODO: figure out slider projection.
# TODO: Ask Martin abt rotation offset.
