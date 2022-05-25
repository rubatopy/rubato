"""
The image component that renders an image from the filesystem.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict
import sdl2, sdl2.ext, sdl2.sdlgfx, sdl2.surface, sdl2.sdlimage

from . import Component
from ... import Vector, Display, Radio, get_path

if TYPE_CHECKING:
    from .. import Camera


class Image(Component):
    """
    A component that handles Images.

    Args:
        offset: The offset of the image from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the image. Defaults to 0.
        rel_path: The relative path to the image. Defaults to "".
        size: The size of the image. Defaults to Vector(32, 32).
        scale: The scale of the image. Defaults to Vector(1, 1).
        anti_aliasing: Whether or not to use anti-aliasing. Defaults to False.
        flipx: Whether or not to flip the image horizontally. Defaults to False.
        flipy: Whether or not to flip the image vertically. Defaults to False.
        visible: Whether or not the image is visible. Defaults to True.

    Attributes:
        visible (bool): Whether or not the image is visible.
    """

    def __init__(
        self,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        rel_path: str = "",
        size: Vector = Vector(32, 32),
        scale: Vector = Vector(1, 1),
        anti_aliasing: bool = False,
        flipx: bool = False,
        flipy: bool = False,
        visible: bool = True,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset)

        if rel_path == "":
            self._image: sdl2.SDL_Surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
                0,
                size.x,
                size.y,
                32,
                sdl2.SDL_PIXELFORMAT_RGBA8888,
            ).contents
        else:
            try:
                self._image: sdl2.SDL_Surface = sdl2.ext.load_img(rel_path, False)
            except OSError:
                self._image = sdl2.ext.load_img(get_path(rel_path), False)
            except sdl2.ext.SDLError as e:
                fname = rel_path.replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

        self.singular = False

        self.visible: bool = visible
        self._aa: bool = anti_aliasing
        self._flipx: bool = flipx
        self._flipy: bool = flipy
        self._scale: Vector = scale
        self._rot = self.rotation_offset

        self._original = Display.clone_surface(self._image)
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

        self._changed = True  # TODO: if I didn't write this it didn't scale.
        self._update_rotozoom()
        self._go_rotation = 0

        Radio.listen("ZOOM", self.cam_update)

    @property
    def image(self) -> sdl2.SDL_Surface:
        """The SDL Surface of the image."""
        return self._image

    @image.setter
    def image(self, new: sdl2.SDL_Surface):
        self._image = sdl2.SDL_ConvertSurfaceFormat(new, sdl2.SDL_PIXELFORMAT_RGBA8888, 0).contents
        self._original = Display.clone_surface(self._image)
        self._update_rotozoom()

    @property
    def scale(self) -> Vector:
        """The scale of the image."""
        return self._scale

    @scale.setter
    def scale(self, new: Vector):
        self._scale = new
        self._changed = True

    @property
    def rotation_offset(self) -> float:
        """The rotation offset of the image."""
        return self._rot

    @rotation_offset.setter
    def rotation_offset(self, new: float):
        self._rot = new
        self._changed = True

    @property
    def flipx(self) -> bool:
        """Whether or not the image is flipped horizontally."""
        return self._flipx

    @flipx.setter
    def flipx(self, new: bool):
        self._flipx = new
        self._changed = True

    @property
    def flipy(self) -> bool:
        """Whether or not the image is flipped vertically."""
        return self._flipy

    @flipy.setter
    def flipy(self, new: bool):
        self._flipy = new
        self._changed = True

    @property
    def aa(self) -> bool:
        """Whether or not the image is anti-aliased."""
        return self._aa

    @aa.setter
    def aa(self, new: bool):
        self._aa = new
        self._changed = True

    def get_size(self) -> Vector:
        """
        Gets the current size of the image.

        Returns:
            Vector: The size of the image
        """
        if self.image.w == self._original.w and self.image.h == self._original.h:
            return Vector(self.image.w, self.image.h) * self.scale
        return Vector(self.image.w, self.image.h)

    def get_size_original(self) -> Vector:
        """
        Gets the original size of the image.

        Returns:
            Vector: The original size of the image.
        """
        return Vector(self._original.w, self._original.h)

    def _update_rotozoom(self):
        """Updates the image surface. Called automatically when image scale or rotation are updated"""
        if self.gameobj:
            self._image = sdl2.sdlgfx.rotozoomSurfaceXY(
                self._original,
                self.gameobj.rotation + self.rotation_offset,
                -self.scale.x if self.flipx else self.scale.x,
                -self.scale.y if self.flipy else self.scale.y,
                int(self.aa),
            ).contents
            self._tx = sdl2.ext.Texture(Display.renderer, self.image)

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        if -1 < new_size.x < 1:
            new_size.x = 1
        if -1 < new_size.y < 1:
            new_size.y = 1

        image_scaled = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
            0,
            new_size.x,
            new_size.y,
            32,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
        ).contents

        sdl2.surface.SDL_BlitScaled(
            self._original,
            None,
            image_scaled,
            sdl2.SDL_Rect(0, 0, new_size.x, new_size.y),
        )

        self._image = image_scaled
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

    def cam_update(self, info: Dict[str, Camera]):
        """Updates the image sizing when the camera zoom changes."""
        width, height = self.image.w, self.image.h

        new_size = Vector(
            round(info["camera"].scale(width)),
            round(info["camera"].scale(height)),
        )

        self.resize(new_size)

    def draw(self, camera: Camera):
        if self._changed or self._go_rotation != self.gameobj.rotation:
            self._go_rotation = self.gameobj.rotation
            self._changed = False
            self._update_rotozoom()

        if self.visible:
            Display.update(self._tx, camera.transform(self.gameobj.pos - Vector(*self._tx.size) / 2))

    def delete(self):
        """Deletes the image component"""
        self._tx.destroy()
        sdl2.SDL_FreeSurface(self._image)
        sdl2.SDL_FreeSurface(self._original)
        self._image = None
        self._tx = None
        self._original = None

    def clone(self) -> "Image":
        """
        Clones the current image.

        Returns:
            Image: The cloned image.
        """
        new = Image(
            {
                "scale": self.scale,
                "anti_aliasing": self.aa,
                "flipx": self.flipx,
                "flipy": self.flipy,
                "offset": self.offset,
                "visible": self.visible,
            }
        )
        new.image = Display.clone_surface(self.image)
        return new

    @staticmethod
    def from_surface(surface: sdl2.surface.SDL_Surface) -> "Image":
        """
        Creates an image from an SDL surface.

        Args:
            surface: the surface to create the image from.

        Returns:
            The created image.
        """
        # untested
        image = Image()
        image.image = surface
        return image

    @staticmethod
    def from_buffer(buffer: bytes) -> "Image":
        """
        Creates an image from a buffer.

        Args:
            buffer: bytes containing the image data.

        Returns:
            The image created from the buffer.
        """
        # untested
        rw = sdl2.SDL_RWFromMem(buffer, len(buffer))
        surface_temp = sdl2.sdlimage.IMG_Load_RW(rw, 1)

        if surface_temp is None:
            raise Exception(sdl2.sdlimage.IMG_GetError())

        surface = sdl2.SDL_ConvertSurfaceFormat(surface_temp, sdl2.SDL_PIXELFORMAT_RGBA8888, 0).contents
        sdl2.SDL_FreeSurface(surface_temp)

        return Image.from_SDL_Surface(surface)
