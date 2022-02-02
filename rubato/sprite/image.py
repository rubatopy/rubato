"""
The image class renders an image from the file system.
"""
from os import path, walk
from pygame.image import load
from pygame.transform import scale, flip, rotate
from rubato.utils import Vector, Configs
from rubato.scenes import Camera
from rubato.sprite.sprite import Sprite


class Image(Sprite):
    """
    A subclass of Sprite that handles Images.

    Attributes:
        image (pygame.Surface): The pygame surface containing the image.
    """

    def __init__(self, options: dict = {}):
        param = Configs.merge_params(options, Configs.image_defaults)
        super().__init__({"pos": param["pos"], "z_index": param["z_index"]})

        if param["image_location"] == "" or param[
                "image_location"] == "default":
            self.image = load("rubato/static/default.png").convert_alpha()
        elif param["image_location"] == "empty":
            self.image = load("rubato/static/empty.png").convert_alpha()
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
        pass

    def draw(self, camera: Camera):
        """
        Draws the image if the z index is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        super().draw(self.image, camera)

    @staticmethod
    def import_image_folder(dictionary: dict, rel_path: str):
        """
        Imports a folder of images, creating rubato.Image for each one and
        placing it in a dictionary by its file name.

        Args:
            dictionary: A dictionary that all the images will be written to.
            rel_path: The relative path to the folder you wish to import
        """
        for _, _, files in walk(rel_path):
            # walk to directory path and ignore name and subdirectories
            for image_path in files:
                path_to_image = path.join(rel_path, image_path)
                image = Image({
                    "image_location": path_to_image,
                })
                dictionary[image_path.split(".")[0]] = image
