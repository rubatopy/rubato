"""A Surface is a grid of pixels that you can draw shapes onto or edit individual pixels."""
from __future__ import annotations
import sdl2, sdl2.ext

from ..c_src import c_draw
from .. import Vector, Color, Display, Surf


class Surface(Surf):
    """
    A surface.

    Args:
        width: The width of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        height: The height of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        scale: The scale of the surface. Defaults to (1, 1).
        af: Whether to use anisotropic filtering. Defaults to False.
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector | tuple[float, float] = (1, 1),
        rotation: float = 0,
        af: bool = False,
    ):
        super().__init__(rotation, scale, af)

        self.surf = sdl2.SDL_CreateRGBSurfaceWithFormat(0, width, height, 32, Display.pixel_format).contents

        self.width: int = width
        """(READ ONLY) The width of the surface in pixels."""
        self.height: int = height
        """(READ ONLY) The height of the surface in pixels."""

    def clear(self):
        """
        Clears the surface.
        """
        c_draw.clear_pixels(self.surf.pixels, self.surf.w, self.surf.h)
        self.uptodate = False

    def draw_point(self, pos: Vector | tuple[float, float], color: Color = Color.black, blending: bool = True):
        """
        Draws a point on the surface.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
            blending: Whether to use blending. Defaults to False.
        """
        x, y = int(pos[0]), int(pos[1])
        c_draw.set_pixel(self.surf.pixels, self.surf.w, self.surf.h, x, y, color.rgba32(), blending)
        self.uptodate = False

    def draw_line(
        self,
        start: Vector | tuple[float, float],
        end: Vector | tuple[float, float],
        color: Color = Color.black,
        aa: bool = False,
        thickness: int = 1,
        blending: bool = True
    ):
        """
        Draws a line on the surface.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            aa: Whether to use anti-aliasing. Defaults to False.
            thickness: The thickness of the line. Defaults to 1.
            blending: Whether to use blending. Defaults to False.
        """
        sx, sy = int(start[0]), int(start[1])
        ex, ey = int(end[0]), int(end[1])
        c_draw.draw_line(
            self.surf.pixels, self.surf.w, self.surf.h, sx, sy, ex, ey, color.rgba32(), aa, blending, thickness
        )
        self.uptodate = False

    def draw_rect(
        self,
        top_left: Vector | tuple[float, float],
        dims: Vector | tuple[float, float],
        border: Color | None = None,
        border_thickness: int = 1,
        fill: Color | None = None,
        blending: bool = True
    ):
        """
        Draws a rectangle on the surface.

        Args:
            top_left: The top left corner of the rectangle.
            dims: The dimensions of the rectangle.
            border: The border color of the rectangle. Defaults to None.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the rectangle. Set to None for no fill. Defaults to None.
            blending: Whether to use blending. Defaults to False.
        """
        x, y = int(top_left[0]), int(top_left[1])
        w, h = int(dims[0]), int(dims[1])
        c_draw.draw_rect(
            self.surf.pixels,
            self.surf.w,
            self.surf.h,
            x,
            y,
            w,
            h,
            border.rgba32() if border else 0,
            fill.rgba32() if fill else 0,
            blending,
            border_thickness,
        )
        self.uptodate = False

    def draw_circle(
        self,
        center: Vector | tuple[float, float],
        radius: int,
        border: Color | None = None,
        border_thickness: int = 1,
        fill: Color | None = None,
        aa: bool = False,
        blending: bool = True,
    ):
        """
        Draws a circle on the surface.

        Args:
            center: The center of the circle.
            radius: The radius of the circle.
            border: The border color of the circle. Defaults to None.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the circle. Set to None for no fill. Defaults to None.
            aa: Whether to use anti-aliasing. Defaults to False.
            blending: Whether to use blending. Defaults to False.
        """
        x, y = int(center[0]), int(center[1])
        c_draw.draw_circle(
            self.surf.pixels,
            self.surf.w,
            self.surf.h,
            x,
            y,
            radius,
            border.rgba32() if border else 0,
            fill.rgba32() if fill else 0,
            aa,
            blending,
            border_thickness,
        )
        self.uptodate = False

    def draw_poly(
        self,
        points: list[Vector | tuple[float, float]],
        border: Color | None = None,
        border_thickness: int = 1,
        fill: Color | None = None,
        aa: bool = False,
        blending: bool = True,
    ):
        """
        Draws a polygon on the surface.

        Args:
            points: The points of the polygon.
            border: The border color of the polygon. Defaults to None.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the polygon. Set to None for no fill. Defaults to None.
            aa: Whether to use anti-aliasing. Defaults to False.
            blending: Whether to use blending. Defaults to False.
        """
        c_draw.draw_poly(
            self.surf.pixels,
            self.surf.w,
            self.surf.h,
            points,
            border.rgba32() if border else 0,
            fill.rgba32() if fill else 0,
            aa,
            blending,
            border_thickness,
        )
        self.uptodate = False

    def get_pixel(self, pos: Vector | tuple[float, float]) -> Color:
        """
        Gets the color of a pixel on the surface.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        x, y = int(pos[0]), int(pos[1])
        if 0 <= x < self.surf.w and 0 <= y < self.surf.h:
            return Color.from_rgba32(c_draw.get_pixel(self.surf.pixels, self.surf.w, self.surf.h, x, y))
        else:
            raise ValueError(f"Position is outside of the ${self.__class__.__name__}.")

    def get_pixel_tuple(self, pos: Vector | tuple[float, float]) -> tuple[int, int, int, int]:
        """
        Gets the color of a pixel on the surface.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.get_pixel(pos).to_tuple()

    def switch_color(self, color: Color, new_color: Color):
        """
        Switches a color in the surface.

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
        Sets the colorkey of the surface.
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
            scale=self.scale.clone(),
            rotation=self.rotation,
            af=self.af,
        )
        if self.surf:
            new.surf = Display.clone_surface(self.surf)

        return new
