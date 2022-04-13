"""
Global display class that allows for easy screen and window management.
"""
from __future__ import annotations
import sdl2, sdl2.sdlttf, sdl2.ext
from sdl2.sdlgfx import pixelRGBA, thickLineColor
from typing import TYPE_CHECKING

from . import Vector, Defaults

if TYPE_CHECKING:
    from . import Color, Font


class DisplayProperties(type):
    """
    Defines static property methods for Display.

    Attention:
        This is only a metaclass for the class below it, so you wont be able to access this class.
        To use the property methods here, simply access them as you would any other ``Display`` property.
    """

    @property
    def window_size(cls) -> Vector:
        """
        The pixel size of the physical window.

        Warning:
            Using this value to determine the placement of your game objects may
            lead to unexpected results. You should instead use
            :func:`Display.res <rubato.utils.display.Display.res>`
        """
        return Vector(*cls.window.size)

    @window_size.setter
    def window_size(cls, new: Vector):
        cls.window.size = new.to_int().to_tuple()

    @property
    def res(cls) -> Vector:
        """
        The pixel resolution of the game. This is the number of virtual
        pixels on the window.

        Example:
            The window (:func:`Display.window_size <rubato.utils.display.DisplayProperties.window_size>`)
            could be rendered at 500x500 while the resolution is at 1000x1000.
            This would mean that you can place game objects at 900, 900 and still see them despite the window not being
            900 pixels tall.

        Warning:
            While this value can be changed, it is recommended that you do not
            alter it after initialization as it will scale your entire project in unexpected ways.
            If you wish to achieve scaling across an entire scene, simply utilize the
            :func:`camera zoom <rubato.classes.camera.Camera.zoom>` property in your scene's camera.
        """
        return Vector(*cls.renderer.logical_size)

    @res.setter
    def res(cls, new: Vector):
        cls.renderer.logical_size = new.to_int().to_tuple()

    @property
    def window_pos(cls) -> Vector:
        """The current position of the window in terms of screen pixels"""
        return Vector(*cls.window.position)

    @window_pos.setter
    def window_pos(cls, new: Vector):
        cls.window.position = new.to_int().to_tuple()

    @property
    def window_name(cls):
        return cls.window.title

    @window_name.setter
    def window_name(cls, new: str):
        cls.window.title = new

    @property
    def display_ratio(cls) -> Vector:
        """The ratio of the renderer resolution to the window size. This is a read-only property.

        Returns:
            Vector: The ratio of the renderer resolution to the window size seperated by x and y.
        """
        return cls.res / cls.window_size


class Display(metaclass=DisplayProperties):
    """
    A static class that houses all of the display information

    Attributes:
        window (sdl2.Window): The pysdl2 window element.
        renderer (sdl2.Renderer): The pysdl2 renderer element.
        format (sdl2.PixelFormat): The pysdl2 pixel format element.
    """

    window: sdl2.ext.Window = None
    renderer: sdl2.ext.Renderer = None
    format = sdl2.SDL_CreateRGBSurfaceWithFormat(0, 1, 1, 32, sdl2.SDL_PIXELFORMAT_RGBA8888).contents.format.contents

    @classmethod
    def set_window_icon(cls, path: str):
        """
        Set the icon of the window.

        Warning:
            The image must be less than 128x128

        Args:
            path: The path to the icon.
        """

        image = sdl2.ext.image.load_img(path)
        if image.w > 128 or image.h > 128:
            raise ValueError("The logo image must be less than 128x128")

        sdl2.SDL_SetWindowIcon(
            cls.window.window,
            image,
        )

    @classmethod
    def draw_point(cls, pos: Vector, color: Color):
        """
        Draw a point onto the renderer.

        Args:
            pos: The position of the point.
            color: The color to use for the pixel. Defaults to black.
        """
        pixelRGBA(cls.renderer.renderer, round(pos.x), round(pos.y), *color.to_tuple())

    @classmethod
    def draw_line(cls, p1: Vector, p2: Vector, color: Color, width: int = 1):
        """
        Draw a line onto the renderer.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        thickLineColor(cls.renderer, p1.x, p1.y, p2.x, p2.y, width, color.rgba32)

    @classmethod
    def draw_text(
        cls,
        text: str,
        font: Font,
        pos: Vector = Vector(),
        justify: str = Defaults.text_defaults["justify"],
        align: Vector = Defaults.text_defaults["align"],
        width: int = Defaults.text_defaults["width"]
    ):
        """
        Draws some text onto the renderer.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to Vector(0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to Vector(0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
        """
        tx = sdl2.ext.Texture(cls.renderer, font.generate_surface(text, justify, width))
        cls.update(tx, pos + (align - 1) * Vector(*tx.size) / 2)

    @classmethod
    def update(cls, tx: sdl2.ext.Texture, pos: Vector):
        """
        Update the current screen.

        Args:
            tx: The texture to draw on the screen.
            pos: The position to draw the texture on.
        """
        try:
            w, h = tx.size
        except AttributeError:
            w, h = tx.contents.size

        cls.renderer.copy(
            tx,
            None,
            (
                pos.x,
                pos.y,
                w,
                h,
            ),
        )

    @classmethod
    def clone_surface(cls, surface: sdl2.SDL_Surface) -> sdl2.SDL_Surface:
        """
        Clones an SDL surface.

        Args:
            surface: The surface to clone.

        Returns:
            sdl2.SDL_Surface: The cloned surface.
        """
        return sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            surface.pixels,
            surface.w,
            surface.h,
            32,
            surface.pitch,
            surface.format.contents.format,
        ).contents

    @classmethod
    @property
    def top_left(cls) -> Vector:
        """The position of the top left of the window."""
        return Vector(0, 0)

    @classmethod
    @property
    def top_right(cls) -> Vector:
        """The position of the top right of the window."""
        return Vector(cls.res.x, 0)

    @classmethod
    @property
    def bottom_left(cls) -> Vector:
        """The position of the bottom left of the window."""
        return Vector(0, cls.res.y)

    @classmethod
    @property
    def bottom_right(cls) -> Vector:
        """The position of the bottom right of the window."""
        return Vector(cls.res.x, cls.res.y)

    @classmethod
    @property
    def top_center(cls) -> Vector:
        """The position of the top center of the window."""
        return Vector(cls.res.x / 2, 0)

    @classmethod
    @property
    def bottom_center(cls) -> Vector:
        """The position of the bottom center of the window."""
        return Vector(cls.res.x / 2, cls.res.y)

    @classmethod
    @property
    def center_left(cls) -> Vector:
        """The position of the center left of the window."""
        return Vector(0, cls.res.y / 2)

    @classmethod
    @property
    def center_right(cls) -> Vector:
        """The position of the center right of the window."""
        return Vector(cls.res.x, cls.res.y / 2)

    @classmethod
    @property
    def center(cls) -> Vector:
        """The position of the center of the window."""
        return Vector(cls.res.x / 2, cls.res.y / 2)

    @classmethod
    @property
    def top(cls) -> int:
        """The position of the top of the window."""
        return 0

    @classmethod
    @property
    def right(cls) -> int:
        """The position of the right of the window."""
        return cls.res.x

    @classmethod
    @property
    def left(cls) -> int:
        """The position of the left of the window."""
        return 0

    @classmethod
    @property
    def bottom(cls) -> int:
        """The position of the bottom of the window."""
        return cls.res.y
