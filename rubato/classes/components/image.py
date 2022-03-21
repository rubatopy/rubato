"""
The image component that renders an image from the filesystem.
"""
from rubato.classes.component import Component
from rubato.utils import Vector, Defaults, Display
import rubato.game as Game
import sdl2
import sdl2.ext
import sdl2.sdlgfx


class Image(Component):
    """
    A component that handles Images.

    Attributes:
        image (sdl2.surface.Surface): The surface containing the image.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes an Image

        Args:
            options: A Image config. Defaults to the |default| for
                    `Image`.
        """
        param = Defaults.image_defaults | options
        super().__init__()

        if param["image_location"] == "":
            self.image = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
                0,
                0,
                0,
                64,
                sdl2.SDL_PIXELFORMAT_RGBA32,
            ).contents
        else:
            self.image = sdl2.ext.load_img(param["image_location"], False)

        self._original = Display.clone_surface(self.image)

        self._rotation: float = param["rotation"]
        self._scale: Vector = param["scale_factor"]
        self._update_rotozoom(0, Vector.one)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, new_rotation: float):
        old = self.rotation
        self._rotation = new_rotation
        self._update_rotozoom(old, self.scale)

    @property
    def scale(self) -> Vector:
        return self._scale

    @scale.setter
    def scale(self, new_scale: Vector):
        old = self.scale
        self._scale = new_scale
        self._update_rotozoom(self.rotation, old)

    def get_size(self) -> Vector:
        """
        Gets the current size of the frame.

        Returns:
            Vector: The size of the image
        """
        return Vector(self.image.w, self.image.h)

    def get_size_original(self) -> Vector:
        """
        Gets the original size of the image.

        Returns:
            Vector: The original size of the image.
        """
        return Vector(self._original.w, self._original.h)

    def _update_rotozoom(self, old_rotation: float, old_scale: Vector):
        if old_scale.x == 0 or old_scale.y == 0:
            self._scale = Vector.zero
            old_scale = Vector.one

        self.image = sdl2.sdlgfx.rotozoomSurfaceXY(
            self.image,
            self.rotation - old_rotation,
            self.scale.x / old_scale.x,
            self.scale.y / old_scale.y,
            1,
        ).contents

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

        image_scaled = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
            0,
            new_size.x,
            new_size.y,
            64,
            sdl2.SDL_PIXELFORMAT_RGBA32,
        )

        sdl2.surface.SDL_BlitScaled(
            self.image,
            None,
            image_scaled,
            sdl2.rect.SDL_Rect(0, 0, new_size.x, new_size.y),
        )

        self.image = image_scaled

    def draw(self):
        """
        Draws the image if the z index is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        Game.render(self.sprite, self.image)
