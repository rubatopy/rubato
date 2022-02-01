"""
A simple button. A button is a text sprite that has mouse over detection.
"""
from rubato.sprite import Text
from rubato.sprite.sprite import Sprite
from rubato.utils import Vector, RGB
import rubato.input as Input


class Button(Text):
    """
    The button class. It inherits from the text class.
    """

    default_options = {
        "text": "default_text",
        "pos": Vector(),
        "size": 16,
        "z_index": 0,
        "font_name": "Arial",
        "color": RGB.black
    }

    def __init__(self, options={}):
        """
        Initializes a button.

        Args:
            options: A button config. Defaults to the
                :ref:`default button config <defaultbutton>`.
        """
        param = Sprite.merge_params(options, Button.default_options)
        super().__init__(param)

    def mouse_is_over(self) -> bool:
        """
        Checks if the mouse is above the button.

        Returns:
            bool: True if the mouse is over the button. False otherwise.
        """
        return Input.mouse_over(
            self.pos, Vector(self.image.get_width(), self.image.get_height()))
