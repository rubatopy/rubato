"""
The Rectangle class draws a colored rectangle. It inherits from the image class.
"""
from rubato.sprite import Image
from rubato.sprite.sprite import Sprite
from rubato.utils import Configs
from pygame.surface import Surface
from pygame.draw import rect


class Rectangle(Image):
    """
    A class that creates a colored rectangle
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a rectangle class.

        Args:
            options: A rectangle config. Defaults to the |default| for
                `Rectangle`.
        """
        param = Configs.merge_params(options, Configs.rect_defaults)
        super().__init__({
            "image_location": "",
            "pos": param["pos"],
            "z_index": param["z_index"]
        })
        param = Sprite.merge_params(options, Rectangle.default_options)
        self.image = Surface(param["dims"].to_tuple())

        rect(self.image, param["color"], [0, 0, *param["dims"].to_tuple()])
