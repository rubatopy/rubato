"""An abstraction for a grid of pixels that can be drawn onto."""
from __future__ import annotations
import sdl2, sdl2.ext, ctypes

from ..c_src import c_draw
from .. import Vector, Color, Display, get_path


class Surface:
    """
    A grid of pixels that can be modified without being attached to a game object.

    Args:
        width: The width of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        height: The height of the surface in pixels. Once set this cannot be changed. Defaults to 32.
        scale: The scale of the surface. Defaults to (1, 1).
        rotation: The clockwise rotation of the sprite.
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
        self.rotation: float = rotation
        """The clockwise rotation of the sprite."""
        self.scale: Vector = Vector.create(scale)
        """The scale of the sprite."""
        self._af = af

        self._surf: sdl2.SDL_Surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0, width, height, 32, Display.pixel_format
        ).contents

        self._tx: sdl2.ext.Texture
        self.uptodate: bool = False
        """
        Whether the texture is up to date with the surface.
        Can be set to False to trigger a texture regeneration at the next draw cycle.
        """

    @property
    def width(self) -> int:
        """The width of the surface in pixels (read-only)."""
        return self._surf.w

    @property
    def height(self) -> int:
        """The height of the surface in pixels (read-only)."""
        return self._surf.h

    @property
    def af(self):
        """Whether to use anisotropic filtering."""
        return self._af

    @af.setter
    def af(self, new: bool):
        self._af = new
        if hasattr(self, "tx"):
            self._tx.set_scale_mode("linear" if self.af else "nearest")

    def get_size(self) -> Vector:
        """
        Gets the current size of the image. (Scaled)

        Returns:
            The size of the image
        """
        return Vector(self._surf.w * self.scale.x, self._surf.h * self.scale.y)

    def get_size_raw(self) -> Vector:
        """
        Gets the current size of the image. (Unscaled)

        Returns:
            The size of the image
        """
        return Vector(self._surf.w, self._surf.h)

    def merge(self, other: Surface):
        """
        Merges another surface into this one.

        Args:
            other: The surface to merge into this one.
        """
        sdl2.SDL_BlitSurface(other._surf, None, self._surf, sdl2.SDL_Rect(0, 0, *self.get_size_raw().tuple_int()))
        self.uptodate = False

    def regen(self):
        """Regenerates the texture from the surface."""
        if hasattr(self, "tx"):
            self._tx.destroy()
        self._tx = sdl2.ext.Texture(Display.renderer, self._surf)
        self._tx.set_scale_mode("linear" if self.af else "nearest")
        self.uptodate = True

    def clear(self):
        """
        Clears the surface.
        """
        c_draw.clear_pixels(self._surf.pixels, self._surf.w, self._surf.h)
        self.uptodate = False

    def fill(self, color: Color):
        """
        Fill the surface with a color.

        Args:
            color: The color to fill with.
        """
        self.draw_rect((0, 0), (self._surf.w, self._surf.h), fill=color)

    def draw_point(self, pos: Vector | tuple[float, float], color: Color = Color.black, blending: bool = True):
        """
        Draws a point on the surface.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
            blending: Whether to use blending. Defaults to False.
        """
        x, y = round(pos[0]), round(pos[1])
        c_draw.set_pixel(self._surf.pixels, self._surf.w, self._surf.h, x, y, color.rgba32(), blending)
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
        sx, sy = round(start[0]), round(start[1])
        ex, ey = round(end[0]), round(end[1])
        c_draw.draw_line(
            self._surf.pixels, self._surf.w, self._surf.h, sx, sy, ex, ey, color.rgba32(), aa, blending, thickness
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
        x, y = round(top_left[0]), round(top_left[1])
        w, h = round(dims[0]), round(dims[1])
        c_draw.draw_rect(
            self._surf.pixels,
            self._surf.w,
            self._surf.h,
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
        x, y = round(center[0]), round(center[1])
        c_draw.draw_circle(
            self._surf.pixels,
            self._surf.w,
            self._surf.h,
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
        points: list[Vector] | list[tuple[float, float]],
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
            self._surf.pixels,
            self._surf.w,
            self._surf.h,
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
        x, y = round(pos[0]), round(pos[1])
        if 0 <= x < self._surf.w and 0 <= y < self._surf.h:
            return Color.from_rgba32(c_draw.get_pixel(self._surf.pixels, self._surf.w, self._surf.h, x, y))
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
        for x in range(round(self.get_size().x)):
            for y in range(round(self.get_size().y)):
                if self.get_pixel((x, y)) == color:
                    new_color.a = self.get_pixel_tuple((x, y))[0]
                    self.draw_point((x, y), new_color)
                self.draw_point((x, y), color)
        self.uptodate = False

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the surface.
        Args:
            color: Color to set as the colorkey.
        """
        sdl2.SDL_SetColorKey(self._surf, sdl2.SDL_TRUE, sdl2.SDL_MapRGB(self._surf.format, color.r, color.g, color.b))
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
        new.merge(self)

        return new

    def set_alpha(self, new: int):
        """
        Sets surface wide alpha.

        Args:
            new: The new alpha. (value between 0-255)
        """
        new = max(min(new, 255), 0)
        sdl2.SDL_SetSurfaceAlphaMod(self._surf, new)
        self.uptodate = False

    def get_alpha(self) -> int:
        """
        Gets the surface wide alpha.
        """
        y = ctypes.c_uint8()

        sdl2.SDL_GetSurfaceAlphaMod(self._surf, ctypes.byref(y))
        return y.value

    @classmethod
    def from_file(
        cls,
        path: str,
        scale: Vector | tuple[float, float] = (1, 1),
        rotation: float = 0,
        af: bool = False,
    ) -> Surface:
        """
        Loads a surface from an image file.

        Args:
            path: The path to the file.
            scale: The scale of the surface. Defaults to (1, 1).
            rotation: The clockwise rotation of the sprite.
            af: Whether to use anisotropic filtering. Defaults to False.

        Returns:
            The resultant surface.
        """
        try:
            surf = sdl2.ext.load_img(path, False)
        except OSError:
            surf = sdl2.ext.load_img(get_path(path), False)
        except sdl2.ext.SDLError as e:
            fname = path.replace("\\", "/").split("/")[-1]
            raise TypeError(f"{fname} is not a valid image file") from e

        s = cls(scale=scale, rotation=rotation, af=af)
        sdl2.SDL_FreeSurface(s._surf)
        s._surf = surf
        return s

    def __del__(self):
        if hasattr(self, "tx"):
            self._tx.destroy()
        sdl2.SDL_FreeSurface(self._surf)
