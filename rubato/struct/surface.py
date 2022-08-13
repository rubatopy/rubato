"""A Surface is a grid of pixels that you can draw shapes onto or edit individual pixels."""
from __future__ import annotations
import sdl2, sdl2.ext

from ..c_src import PixelEditor
from .. import Vector, Color, Display, Surf


class Surface(Surf):
    """
    A surface.

    Args:
        width: The width of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        height: The height of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        scale: The scale of the surface. Defaults to Vector(1, 1).
        aa: Whether or not to use anti-aliasing. Defaults to False.
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector = Vector(1, 1),
        rotation: float = 0,
        aa: bool = False,
    ):
        super().__init__(rotation, scale, aa)

        self.surf = sdl2.SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, sdl2.SDL_PIXELFORMAT_RGBA8888).contents

        self.width: int = width
        """(READ ONLY) The width of the surface in pixels."""
        self.height: int = height
        """(READ ONLY) The height of the surface in pixels."""

    def clear(self):
        """
        Clears the surface.
        """
        PixelEditor.clear_pixels(self.surf.pixels, self.surf.w, self.surf.h)
        self.uptodate = False

    def draw_point(self, pos: Vector, color: Color = Color.black):
        """
        Draws a point on the image.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
        """
        PixelEditor.set_pixel_safe(self.surf.pixels, self.surf.w, self.surf.h, pos.x, pos.y, color.rgba32)
        self.uptodate = False

    def draw_line(self, start: Vector, end: Vector, color: Color = Color.black):
        """
        Draws a line on the image.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        PixelEditor.draw_line(
            self.surf.pixels,
            self.surf.w,
            self.surf.h,
            start.x,
            start.y,
            end.x,
            end.y,
            color.rgba32,
        )
        self.uptodate = False

    def draw_rect(self, top_left: Vector, dims: Vector, color: Color = Color.black):
        """
        Draws a rectangle border on the image.
        Args:
            top_left: The top left corner of the rectangle.
            dims: The dimensions of the rectangle.
            color: The color of the rectangle. Defaults to black.
        """
        PixelEditor.draw_rect(
            self.surf.pixels,
            self.surf.w,
            self.surf.h,
            top_left.x,
            top_left.y,
            dims.x - 2,
            dims.y - 2,
            color.rgba32,
        )

        self.uptodate = False

    def draw_circle(self, center: Vector, radius: int, color: Color = Color.black):
        pass

    def get_size(self) -> Vector:
        """
        Gets the current size of the surface.

        Returns:
            The size of the surface
        """
        return self._sprite.get_size()

    def get_pixel(self, pos: Vector) -> Color:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        x, y = pos.tuple_int()
        if 0 <= x < self.surf.w and 0 <= y < self.surf.h:
            return Color.from_rgba32(PixelEditor.get_pixel(self.surf.pixels, self.surf.w, x, y))
        else:
            raise ValueError(f"Position is outside of the ${self.__class__.__name__}.")

    def get_pixel_tuple(self, pos: Vector) -> tuple[int, int, int, int]:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.get_pixel(pos).to_tuple()

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
                    self.draw_point(Vector(x, y), new_color)
                self.draw_point(Vector(x, y), color)  # Set the color of the pixel.
        self.uptodate = False

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the image.
        Args:
            color: Color to set as the colorkey.
        """
        sdl2.SDL_SetColorKey(self.surf, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(self.surf.format, color.r, color.g, color.b))
        self.uptodate = False

    def clone(self) -> Surface:
        """
        Clones the current surface.

        Returns:
            The cloned surface.
        """
        new = Surface(
            self.width,
            self.height,
            scale=self.scale,
            rotation=self.rotation,
            aa=self.aa,
        )
        if self.surf:
            new.surf = Display.clone_surface(self.surf)

        return new
