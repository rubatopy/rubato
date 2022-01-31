"""
The Rectangle class draws a colored rectangle. It inherits from the image class.
"""
from rubato.sprite import Image
from rubato.sprite.sprite import Sprite
from rubato.utils import Vector, Color
from pygame.surface import Surface
from pygame.draw import rect


class Rectangle(Image):
    """
    A class that creates a colored rectangle
    """

    default_options = {
        "pos": Vector(),
        "dims": Vector(),
        "color": Color.black,
        "z_index": 0
    }

    def __init__(self, options: dict = {}):
        """
        Initializes a rectangle class.

        Args:
            options: A rectangle config. Defaults to the
                :ref:`default rectangle options <defaultrectangle>`.
        """
        self.params = Sprite.merge_params(options, Rectangle.default_options)
        super().__init__({
            "image_location": "",
            "pos": self.params["pos"],
            "z_index": self.params["z_index"]
        })
        self.params = Sprite.merge_params(options, Rectangle.default_options)
        self.image = Surface(self.params["dims"].to_tuple())

        rect(self.image, self.params["color"],
             [0, 0, *self.params["dims"].to_tuple()])
