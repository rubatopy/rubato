"""A slider component that can be used in UI."""
from typing import Callable

from . import Component
from ... import Defaults, Input, Vector, Math, Debug
from ... import Color  # testing


class Slider(Component):
    """
    A Slider component. Still needs to be added to a :func:`GameObject <rubato.classes.game_object.GameObject>`.

    Args:
        options: A Slider config. Defaults to the :ref:`Slider defaults <buttondef>`.

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
        params = Defaults.slider_defaults | options
        super().__init__(params)
        self.dims: Vector = Vector(params["button_width"], params["button_height"])
        self.pressed: bool = False
        self.hover: bool = False
        self.onclick: Callable = params["onclick"]
        self.onrelease: Callable = params["onrelease"]
        self.onhover: Callable = params["onhover"]
        self.onexit: Callable = params["onexit"]
        self.offset: Vector = params["slider_origin_offset"]
        self.slider_length: int = params["slider_length"]
        self.slider_direction: Vector = params["slider_direction"]
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
        # print(mouse_projection)
        self._button_pos_offset = Math.clamp(mouse_projection, 0, self.slider_length)
        Debug.circle(self.gameobj.pos + self.offset, 5, Color.red, fill=Color.red)
        Debug.circle(self.gameobj.pos + self.offset + self.slider_direction * self.slider_length, 5, fill=Color.green)
        Debug.line(self.gameobj.pos + self.offset,
                   self.gameobj.pos + self.offset + self.slider_direction * self.slider_length, width=3)

        Debug.circle(self.gameobj.pos + self.offset + self.slider_direction * mouse_projection, 5, fill=Color.purple)

# TODO: force direction to unit vector
