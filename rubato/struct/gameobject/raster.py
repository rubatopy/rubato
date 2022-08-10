"""A Raster is a grid of pixels that you can draw shapes onto or edit individual pixels."""
from typing import Dict, Tuple
import sdl2, sdl2.ext, sdl2.sdlgfx, cython

from . import Component
from ... import Display, Vector, Color, Radio, Draw, Camera


class Raster(Component):
    """
    A raster area for drawings. Rasters are used to draw shapes and manipulate individual pixels. Once a rasters size is
    set, it cannot be changed. You can however change the scale and rotation of the raster.

    Args:
        width: The width of the raster. Defaults to 32.
        height: The height of the raster. Defaults to 32.
        offset: The offset of the raster from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the raster from the gameobject. Defaults to 0.
        scale: The scale of the raster. Defaults to Vector(1, 1).
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)

        self.singular = False

        self._raster: sdl2.SDL_Surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0,
            width,
            height,
            32,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
        ).contents

        self._drawn = Display.clone_surface(self._raster)  # The raster with rotation and scale
        self._texture = sdl2.ext.Texture(Display.renderer, self._raster)

        self._scale = scale
        self._rot = self.rot_offset

        self._cam_zoom = 1
        Radio.listen("ZOOM", self.cam_update)

        self._changed = False
        self._update_rotozoom()
        self._go_rotation = 0

    @property
    def raster(self) -> sdl2.SDL_Surface:
        """The raster surface."""
        return self._raster

    @raster.setter
    def raster(self, new: sdl2.SDL_Surface):
        self._raster = sdl2.SDL_ConvertSurfaceFormat(new, sdl2.SDL_PIXELFORMAT_RGBA8888, 0).contents
        self._update_rotozoom()

    @property
    def width(self) -> int:
        """The height of the raster in pixels."""
        return self._raster.w

    @property
    def height(self) -> int:
        """The width of the raster in pixels."""
        return self._raster.h

    @property
    def rendered_size(self) -> Vector:
        """The size of the raster after scaling (ie. the size it will be rendered at)."""
        return Vector(self._raster.w, self._raster.h) * self.scale

    @property
    def scale(self) -> Vector:
        """The scale of the raster."""
        return self._scale

    @scale.setter
    def scale(self, new: Vector):
        self._scale = new
        self._changed = True

    @property
    def rot_offset(self) -> float:
        """The rotation offset of the raster."""
        return self._rot

    @rot_offset.setter
    def rot_offset(self, new: float):
        self._rot = new
        self._changed = True

    def draw_point(self, pos: Vector, color: Color = Color.black):
        """
        Draws a point on the image.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
        """
        raise NotImplementedError()

    def draw_line(self, start: Vector, end: Vector, color: Color = Color.black, width: int = 1):
        """
        Draws a line on the image.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        raise NotImplementedError()

    def draw_rect(self, top_left: Vector, bottom_right: Vector, color: Color = Color.black, width: int = 1):
        """
        Draws a rectangle border on the image.
        Args:
            top_left: The top left corner of the rectangle.
            bottom_right: The bottom right corner of the rectangle.
            color: The color of the rectangle. Defaults to black.
            width: Width of the rectangle border. Defaults to 1.
        """
        raise NotImplementedError()

    def get_pixel(self, x: int, y: int):
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            Color: The color of the pixel.
        """
        raise NotImplementedError()

    def get_pixel_tuple(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        r, g, b, a = 0, 0, 0, 0
        p = self._raster.pixels + y * self._raster.pitch + x * 4
        sdl2.SDL_GetRGBA(p, self._raster.format, r, g, b, a)

    def set_pixel(self, pos: Vector, color: Color):
        """
        Sets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.
            color: The color of the pixel.
        """
        raise NotImplementedError()

    def switch_color(self, color: Color, new_color: Color):
        """
        Switches a color in the image.

        Args:
            color: The color to switch.
            new_color: The new color to switch to.
        """
        raise NotImplementedError()

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the image.
        Args:
            color: Color to set as the colorkey.
        """
        sdl2.surface.SDL_SetColorKey(
            self._raster, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(self._raster.format, color.r, color.g, color.b)
        )

    def cam_update(self, info: dict[str, Camera]):
        """Updates the raster size when the camera zoom changes"""
        self._cam_zoom = info["camera"].zoom
        self._changed = True

    def _update_rotozoom(self):
        """Updates the image surface. Called automatically when image scale or rotation are updated"""
        if self.gameobj:
            self._drawn = sdl2.sdlgfx.rotozoomSurfaceXY(
                self._raster,
                -self.gameobj.rotation - self.rot_offset,
                self.scale.x * self._cam_zoom,
                self.scale.y * self._cam_zoom,
                0,
            ).contents
            self._texture = sdl2.ext.Texture(Display.renderer, self._drawn)

    def draw(self, camera: Camera):
        if self.hidden:
            return

        if self._changed or self._go_rotation != self.gameobj.rotation:
            self._go_rotation = self.gameobj.rotation
            self._changed = False
            self._update_rotozoom()

        Draw.push(
            self.true_z,
            lambda: Display.
            update(self._texture, camera.transform(self.gameobj.pos + self.offset - Vector(*self._texture.size) / 2)),
        )

    # TODO when we make raster actually work make sure to add a clone function
