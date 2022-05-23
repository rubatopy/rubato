"""A slider component that can be used in UI."""
from __future__ import annotations

from . import Component, Button
from ... import Defaults, Input, Vector, Math, Debug
from ... import Color  # testing

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Camera


class Slider(Component):
    """
    A Slider component. Still needs to be added to a :func:`GameObject <rubato.classes.game_object.GameObject>`.

    Args:
        options: A Slider config. Defaults to the :ref:`Slider defaults <buttondef>`.

    Attributes:
        button (Button): The button component.
        slider_length (int): The length of the slider.

    """

    def __init__(self, options: dict = {}):
        params = Defaults.slider_defaults | options
        super().__init__(params)
        # button handled by slider and not by game object
        params["height"] = params["width"] = params["button_width"]
        self.button = Button(params)
        # offset will offset from the slider.

        # slider
        self.slider_length: int = params["slider_length"]
        self._button_pos_offset: Vector = Vector(0, 0)

    def update(self):
        """The update function for buttons."""
        # custom button update
        if not self.button.hover and Input.mouse_in(self.gameobj.pos + self.offset + self.button.offset,
                                                    self.button.dims, self.gameobj.rotation + self.rotation_offset):
            self.button.hover = True
            self.button.onhover()
        elif self.button.hover and not Input.mouse_in(
                self.gameobj.pos + self.offset + self.button.offset, self.button.dims,
                self.gameobj.rotation + self.rotation_offset
        ):
            self.button.hover = False
            self.button.onexit()

        if (not self.button.pressed) and Input.mouse_is_pressed()[0] and self.button.hover:
            self.button.pressed = True
            self.button.onclick()
        elif self.button.pressed and (not Input.mouse_is_pressed()[0] or not self.button.hover):
            self.button.pressed = False
            self.button.onrelease()
        # end custom button update

        slider_direction: Vector = Vector.from_radial(1, self.gameobj.rotation + self.rotation_offset)
        print(slider_direction)
        mouse_projection = Math.clamp((Input.get_mouse_pos() - self.gameobj.pos - self.offset).
                                      dot(slider_direction) / slider_direction.mag_sq,
                                      0, self.slider_length)
        self._button_pos_offset = Math.clamp(mouse_projection, 0, self.slider_length)
        Debug.circle(self.gameobj.pos + self.offset, 5, Color.red, fill=Color.red)
        Debug.circle(self.gameobj.pos + self.offset + slider_direction * self.slider_length, 5, fill=Color.green)
        Debug.line(self.gameobj.pos + self.offset,
                   self.gameobj.pos + self.offset + slider_direction * self.slider_length, width=3)

        Debug.circle(self.gameobj.pos + self.offset + slider_direction * mouse_projection, 5,
                     fill=Color.purple if self.button.hover else Color.blue)

    def draw(self, camera: Camera):
        """The draw function for buttons."""
        super().draw(camera)
        self.button.draw(camera)

# TODO: force direction to unit vector
# TODO: figure out slider projectoin.
# TODO: Ask Martin abt rotation offset.
