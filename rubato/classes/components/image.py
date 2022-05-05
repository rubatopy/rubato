"""
The image component that renders an image from the filesystem.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import sdl2
import sdl2.ext
import sdl2.sdlgfx

from . import Component
from ... import Vector, Defaults, Display, Radio, Color, get_path

if TYPE_CHECKING:
    from .. import Camera


class Image(Component):
    """
    A component that handles Images.

    Args:
        options: A Image config. Defaults to the :ref:`Image defaults <imagedef>`.

    Attributes:
        aa (bool): Whether or not to enable anti aliasing.
        flipx (bool): Whether or not to flip the image along the x axis
        flipy (bool): Whether or not to flip the image along the y axis
        visible (bool): Whether or not the image is visible.
    """

    def __init__(self, options: dict = {}):
        param = Defaults.image_defaults | options
        super().__init__(param)

        if param["rel_path"] == "":
            self._image: sdl2.SDL_Surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
                0,
                param["size"].x,
                param["size"].y,
                32,
                sdl2.SDL_PIXELFORMAT_RGBA8888,
            ).contents
        else:
            try:
                self._image: sdl2.SDL_Surface = sdl2.ext.load_img(param["rel_path"], False)
            except OSError:
                self._image = sdl2.ext.load_img(get_path(param["rel_path"]), False)
            except sdl2.ext.SDLError as e:
                fname = param["rel_path"].replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

        self.singular = False

        self.aa: bool = param["anti_aliasing"]
        self.flipx: bool = param["flipx"]
        self.flipy: bool = param["flipy"]
        self.visible: bool = param["visible"]
        self._scale: Vector = param["scale"]
        self._rot_offset: float = self.rotation_offset

        self._stored_rot: float = 0

        self._original = Display.clone_surface(self._image)
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

        self._update_rotozoom()

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
    def rotation_offset(self) -> float:
        """The rotation offset of the image in degrees."""
        return self._rot_offset

    @rotation_offset.setter
    def rotation_offset(self, new_rotation: float):
        self._rot_offset = new_rotation
        self._update_rotozoom()

    @property
    def scale(self) -> Vector:
        """The scale of the image in relation to it's original size."""
        return self._scale

    @scale.setter
    def scale(self, new_scale: Vector):
        self._scale = new_scale
        self._update_rotozoom()

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

    def draw_point(self, pos: Vector, color: Color = Color.black):
        """
        Draws a point on the image.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
        """
        sdl2.ext.fill(
            self.image,
            sdl2.ext.rgba_to_color(color.rgba32),
            (pos.x, pos.y, 1, 1),
        )

    def draw_line(self, start: Vector, end: Vector, color: Color = Color.black, width: int = 1):
        """
        Draws a line on the image.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        sdl2.ext.line(
            self.image,
            sdl2.ext.rgba_to_color(color.rgba32),
            (start.x, start.y, end.x, end.y),
            width,
        )

    def cam_update(self):
        """Updates the image sizing when the camera zoom changes."""
        width, height = self.image.w, self.image.h

        new_size = Vector(
            round(self.gameobj.scale_value(width)),
            round(self.gameobj.scale_value(height)),
        )

        self.resize(new_size)

    def draw(self, camera: Camera):
        if self._stored_rot != self.gameobj.rotation:
            self._stored_rot = self.gameobj.rotation
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
