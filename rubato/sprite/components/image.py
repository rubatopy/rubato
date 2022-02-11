"""
The image component that renders an image from the filesystem.
"""
from pygame.image import load
from pygame.transform import scale, flip, rotate
from rubato.sprite.sprite import Component
from rubato.utils import Vector, Configs
import rubato as rb


class Image(Component):
    """
    A component that handles Images.

    Attributes:
        image (pygame.Surface): The pygame surface containing the image.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes an Image component.

        Args:
            options: An image config. Defaults to the |default| for
                `Image`.
        """
        super().__init__()
        param = Configs.merge_params(options, Configs.image_defaults)

        if param["image_location"] == "" or param[
                "image_location"] == "default":
            self.image = load("rubato/static/default.png").convert_alpha()
        else:
            self.image = load(param["image_location"]).convert_alpha()

        self.image = rotate(self.image, param["rotation"])
        self.scale(param["scale_factor"])

    def scale(self, scale_factor: Vector):
        """
        Scales the image.

        Args:
            scale_factor: The 2-d scale factor relative to it's current size.
        """
        if abs(new_x := self.image.get_width() * scale_factor.x) < 1:
            new_x = 1
        if abs(new_y := self.image.get_height() * scale_factor.y) < 1:
            new_y = 1
        self.image = flip(scale(self.image, (abs(new_x), abs(new_y))),
                          new_x < 0, new_y < 0)

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        if abs(new_size.x) < 1:
            new_size.x = 1
        if abs(new_size.y) < 1:
            new_size.y = 1
        self.image = flip(
            scale(self.image, (abs(new_size.x), abs(new_size.y))),
            new_size.x < 0, new_size.y < 0)

    def update(self):
        self.draw()

    def draw(self):
        """
        Draws the image if the z index is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        rb.game.render(self.sprite, self.image)
