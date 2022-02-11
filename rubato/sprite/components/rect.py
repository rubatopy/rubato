"""
The Rectangle component draws a colored rectangle. It inherits from the image
component.
"""
from rubato.sprite.components import Image
from rubato.utils import Configs
from pygame.surface import Surface
from pygame.draw import rect


class Rectangle(Image):
    """
    A component that creates a colored rectangle
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a rectangle component.

        Args:
            options: A rectangle config. Defaults to the |default| for
                `Rectangle`.
        """
        param = Configs.merge_params(options, Configs.rect_defaults)
        super().__init__({})
        self.image = Surface(param["dims"].to_tuple())

        rect(
            self.image,
            param["color"].to_tuple(),
            [0, 0, *param["dims"].to_tuple()],
        )
