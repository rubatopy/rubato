"""A Raster is a grid of pixels that you can draw shapes onto or edit individual pixels."""
from __future__ import annotations
import sdl2, sdl2.ext

from . import Component, Sprite
from .. import Vector, Draw, Camera, Color


class Raster(Component):
    """
    A component that handles rasters.

    Args:
        width: The width of the raster in pixels. Once set this cannot be changed. Defaults to 32.
        height: The height of the raster in pixels. Once set this cannot be changed. Defaults to 32.
        scale: The scale of the raster. Defaults to Vector(1, 1).
        flipx: Whether or not to flip the raster horizontally. Defaults to False.
        flipy: Whether or not to flip the raster vertically. Defaults to False.
        offset: The offset of the raster from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the raster. Defaults to 0.
        aa: Whether or not to use anti-aliasing. Defaults to False.
        z_index: The z-index of the raster. Defaults to 0.
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector = Vector(1, 1),
        flipx: bool = False,
        flipy: bool = False,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        aa: bool = False,
        z_index: int = 0
    ):
        self._sprite = None
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)

        self._sprite = Sprite("", aa=aa)
        self._sprite.image = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0,
            width,
            height,
            32,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
        ).contents
        self._sprite.generate_tx()
        self._view = sdl2.ext.PixelView(self._sprite.image)

        self.singular = False

        self._flipx: bool = flipx
        self._flipy: bool = flipy
        self._scale: Vector = scale
        self._rot = rot_offset

        self._go_rotation = 0
        self._flip_changed = True

    @property
    def raster(self) -> sdl2.SDL_Surface:
        """The SDL Surface of the raster."""
        return self._sprite.raster

    @raster.setter
    def raster(self, new: sdl2.SDL_Surface):
        self._sprite.raster = new
        self._sprite.generate_tx()

    @property
    def scale(self) -> Vector:
        """The scale of the raster."""
        return self._scale

    @scale.setter
    def scale(self, new: Vector):
        self._scale = new
        self._sprite.scale = Vector((-new.x if self.flipx else new.x), (-new.y if self.flipy else new.y))

    @property
    def rot_offset(self) -> float:
        """The rotation offset of the raster."""
        return self._rot

    @rot_offset.setter
    def rot_offset(self, new: float):
        self._rot = new
        if self._sprite:
            self._sprite.rotation = -self._go_rotation - new

    @property
    def flipx(self) -> bool:
        """Whether or not the raster is flipped horizontally."""
        return self._flipx

    @flipx.setter
    def flipx(self, new: bool):
        self._flipx = new
        self._flip_changed = True

    @property
    def flipy(self) -> bool:
        """Whether or not the raster is flipped vertically."""
        return self._flipy

    @flipy.setter
    def flipy(self, new: bool):
        self._flipy = new
        self._flip_changed = True

    @property
    def aa(self) -> bool:
        """Whether or not the raster is anti-aliased."""
        return self._sprite.aa

    @aa.setter
    def aa(self, new: bool):
        self._sprite.aa = new

    def draw_point(self, pos: Vector, color: Color = Color.black):
        """
        Draws a point on the image.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
        """
        pass

    def draw_line(self, start: Vector, end: Vector, color: Color = Color.black, width: int = 1):
        """
        Draws a line on the image.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        pass

    def draw_rect(self, top_left: Vector, bottom_right: Vector, color: Color = Color.black, width: int = 1):
        """
        Draws a rectangle border on the image.
        Args:
            top_left: The top left corner of the rectangle.
            bottom_right: The bottom right corner of the rectangle.
            color: The color of the rectangle. Defaults to black.
            width: Width of the rectangle border. Defaults to 1.
        """
        # TODO: maybe add a fill option? SDL_FillRect?
        self.draw_line(top_left, Vector(bottom_right.x, top_left.y), color, width)
        self.draw_line(Vector(bottom_right.x, top_left.y), bottom_right, color, width)
        self.draw_line(bottom_right, Vector(top_left.x, bottom_right.y), color, width)
        self.draw_line(Vector(top_left.x, bottom_right.y), top_left, color, width)

    def get_size(self) -> Vector:
        """
        Gets the current size of the raster.

        Returns:
            The size of the raster
        """
        return self._sprite.get_size()

    def get_pixel(self, pos: Vector) -> Color:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            Color: The color of the pixel.
        """
        pass

    def get_pixel_tuple(self, pos: tuple[int | float, int | float]) \
            -> tuple[int | float, int | float, int | float, int | float]:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        pass

    def set_pixel(self, pos: Vector, color: Color):
        """
        Sets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.
            color: The color of the pixel.
        """
        pass

    def switch_color(self, color: Color, new_color: Color):
        """
        Switches a color in the image.

        Args:
            color: The color to switch.
            new_color: The new color to switch to.
        """
        for x in range(self.get_size().x):
            for y in range(self.get_size().y):
                if self.get_pixel(Vector(x, y)) == color:
                    new_color.a = self.get_pixel_tuple((x, y))[0]  # Preserve the alpha value.
                    self.set_pixel(Vector(x, y), new_color)
                self.set_pixel(Vector(x, y), color)  # Set the color of the pixel.

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the image.
        Args:
            color: Color to set as the colorkey.
        """
        sdl2.SDL_SetColorKey(
            self._raster, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(self._raster.format, color.r, color.g, color.b)
        )

    def update(self):
        if self.gameobj is not None:
            if self._go_rotation != self.gameobj.rotation:
                self._go_rotation = self.gameobj.rotation
                self.rot_offset = self.rot_offset

            if self._flip_changed:
                self._flip_changed = False
                self.scale = self.scale

    def draw(self, camera: Camera):
        if self.hidden:
            return

        Draw.queue_sprite(
            self._sprite, camera.transform(self.gameobj.pos + self.offset - Vector(*self._sprite.tx.size) / 2),
            self.true_z
        )

    def delete(self):
        """Deletes the raster component"""
        self._sprite.delete()
        self._view = None

    def clone(self) -> Raster:
        """
        Clones the current raster.

        Returns:
            The cloned raster.
        """
        new = Raster(
            offset=self.offset,
            scale=self.scale,
            flipx=self.flipx,
            flipy=self.flipy,
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )
        new._sprite = self._sprite.clone()  # pylint: disable=protected-access
        return new
