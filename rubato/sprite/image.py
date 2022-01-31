"""
The image class renders an image from the file system.
"""
from pygame.image import load
from pygame.transform import scale, flip, rotate
from rubato.utils import Vector
from rubato.scenes import Camera
from rubato.sprite.sprite import Sprite


class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    Attributes:
        image (pygame.Surface): The pygame surface containing the image.
    """

    default_options = {
        "image_location": "default",
        "pos": Vector(),
        "scale_factor": Vector(1, 1),
        "z_index": 0,
        "rotation": 0
    }

    def __init__(self, options: dict = {}):
        self.params = Sprite.merge_params(options, Image.default_options)
        super().__init__({
            "pos": self.params["pos"],
            "z_index": self.params["z_index"]
        })

        if self.params["image_location"] == "" or self.params[
            "image_location"] == "default":
            self.image = load("rubato/static/default.png").convert_alpha()
        elif self.params["image_location"] == "empty":
            self.image = load("rubato/static/empty.png").convert_alpha()
        else:
            self.image = load(self.params["image_location"]).convert_alpha()

        self.image = rotate(self.image, self.params["rotation"])
        self.scale(self.params["scale_factor"])

    def update(self):
        pass

    def draw(self, camera: Camera):
        """
        Draws the image if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        super().draw(self.image, camera)

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
        pass

    def draw(self, camera: Camera):
        """
        Draws the image to the camera.

        Args:
            camera: The camera to draw too.
        """
        super().draw(self.image, camera)
