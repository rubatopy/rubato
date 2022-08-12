"""A Surface is a grid of pixels that you can draw shapes onto or edit individual pixels."""
from __future__ import annotations
import sdl2, sdl2.ext

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

        self.surf = sdl2.SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, sdl2.SDL_PIXELFORMAT_RGBA8888)

        self.width: int = width
        """(READ ONLY) The width of the surface in pixels."""
        self.height: int = height
        """(READ ONLY) The height of the surface in pixels."""

    def clear(self, color: Color = Color.black):
        """
        Clears the surface.

        Args:
            color: The color to clear the surface with. Defaults to black.
        """
        pass

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
            self._surface, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(self._surface.format, color.r, color.g, color.b)
        )

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
