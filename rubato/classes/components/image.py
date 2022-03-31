"""
The image component that renders an image from the filesystem.
"""
import sdl2
import sdl2.ext
import sdl2.sdlgfx

from . import Component
from ... import Vector, Defaults, Display, Game, Radio


class Image(Component):
    """
    A component that handles Images.

    Attributes:
        aa (bool): Whether or not to enable anti aliasing.
        flipx (bool): Whether or not to flip the image along the x axis
        flipy (bool): Whether or not to flip the image along the y axis
        visible (bool): Whether or not the image is visible.
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

        if param["rel_path"] == "":
            self._image: sdl2.SDL_Surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
                0,
                32,
                32,
                64,
                sdl2.SDL_PIXELFORMAT_RGBA32,
            ).contents
        else:
            try:
                self._image: sdl2.SDL_Surface = sdl2.ext.load_img(param["rel_path"], False)
            except sdl2.ext.SDLError as e:
                fname = param["rel_path"].replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

        self.singular = False

        self.aa: bool = param["anti_aliasing"]
        self.flipx: bool = param["flipx"]
        self.flipy: bool = param["flipy"]
        self.offset: Vector = param["offset"]
        self.visible: bool = param["visible"]

        self._original = Display.clone_surface(self._image)
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

        self._rotation: float = param["rotation"]
        self._scale: Vector = param["scale_factor"]
        self._update_rotozoom()

        Radio.listen("zoom_change", self.cam_update)

    @property
    def image(self) -> sdl2.SDL_Surface:
        """The SDL Surface of the image."""
        return self._image

    @image.setter
    def image(self, new: sdl2.SDL_Surface):
        self._image = new
        self._original = Display.clone_surface(new)
        self._update_rotozoom()

    @property
    def rotation(self) -> float:
        """The rotation of the image."""
        return self._rotation

    @rotation.setter
    def rotation(self, new_rotation: float):
        self._rotation = new_rotation
        self._update_rotozoom()

    @property
    def scale(self) -> Vector:
        """The scale of the image in relation to it's original size."""
        return self._scale

    @scale.setter
    def scale(self, new_scale: Vector):
        self._scale = new_scale
        self._update_rotozoom()

    def clone(self) -> "Image":
        """
        Clones the current image.

        Returns:
            Image: The cloned image.
        """
        new = Image({"rotation": self.rotation, "scale": self.scale})
        new.image = Display.clone_surface(self.image)
        return new

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

    def _update_rotozoom(self):
        self._image = sdl2.sdlgfx.rotozoomSurfaceXY(
            self._original,
            self.rotation,
            self.scale.x * (-1 if self.flipx else 1),
            self.scale.y * (-1 if self.flipy else 1),
            int(self.aa),
        ).contents
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

    def resize(self, new_size: Vector | tuple | list):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        # if new_size.__class__ in [tuple.__class__, list.__class__]:
        #     if len(new_size) != 2:
        #         raise ValueError("")
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

        self.image = image_scaled.contents
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

    def cam_update(self):
        width, height = self.image.w, self.image.h

        new_size = Vector(
            round(width * Game.camera.zoom),
            round(height * Game.camera.zoom),
        )

        self.resize(new_size)

    def draw(self):
        """
        Draws the image if the z index is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        if self.visible and self.gameobj.z_index <= Game.camera.z_index:

            Display.update(
                self._tx,
                Game.camera.transform(self.gameobj.pos - Vector(*self._tx.size) / 2),
            )
