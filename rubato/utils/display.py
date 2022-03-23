"""
Global display class that allows for easy screen and window management.
"""
import sdl2
import sdl2.ext
from rubato.utils.vector import Vector
from rubato.helpers import *


class Display(metaclass=StaticClass):
    """
    A static class that houses all of the display information

    Attributes:
        window (sdl2.ext.Window): The pysdl2 window element.
        renderer (sdl2.ext.Renderer): The pysdl2 renderer element.
    """

    window: sdl2.ext.Window = None
    renderer: sdl2.ext.Renderer = None

    @classproperty
    def window_size(self) -> Vector:
        """
        The pixel size of the physical window.

        Warning:
            Using this value to determine the placement of your sprites will
            lead to unexpected results. Instead you should use
            :func:`Display.res <rubato.utils.display.Display.res>`
        """
        return Vector(*self.window.size)

    @window_size.setter
    def window_size(self, new: Vector):
        self.window.size = new.to_int().to_tuple()

    @classproperty
    def res(self) -> Vector:
        """
        The pixel resolution of the game. This is the number of virtual
        pixels on the window.

        Example:
            The window (:func:`Display.window_size <rubato.utils.display.Display.window_size>`)
            could be rendered at 720p while the resolution is still at 1080p.
            This means that you can place sprites
            at 1000, 1000 and still have them draw despite the window not being
            1000 pixels wide.

        Warning:
            While this value can be changed, it is recommended that you do not
            change it as it will scale your entire project in ways you might
            not expect.
        """
        return Vector(*self.renderer.logical_size)

    @res.setter
    def res(self, new: Vector):
        self.renderer.logical_size = new.to_int().to_tuple()

    @classproperty
    def window_pos(self) -> Vector:
        """The current position of the window in terms of screen pixels"""
        return Vector(*self.window.position)

    @window_pos.setter
    def window_pos(self, new: Vector):
        self.window.position = new.to_int().to_tuple()

    @classproperty
    def window_name(self):
        return self.window.title

    @window_name.setter
    def window_name(self, new: str):
        self.window.title = new

    @classmethod
    def set_window_icon(cls, path: str):
        """
        Set the icon of the window.

        Args:
            path: The path to the icon.
        """
        sdl2.video.SDL_SetWindowIcon(
            cls.window,
            sdl2.ext.image.load_img(path),
        )

    @classmethod
    def update(cls, surface: sdl2.SDL_Surface, pos: Vector):
        """
        Update the current screen.

        Args:
            surface: The surface to draw on the screen.
            pos: The position to draw the surface on.
        """
        cls.renderer.copy(
            sdl2.ext.Texture(cls.renderer, surface),
            None,
            (
                pos.x,
                pos.y,
                surface.contents.w,
                surface.contents.h,
            ),
        )

    @classmethod
    def clone_surface(cls, surface: sdl2.SDL_Surface) -> sdl2.SDL_Surface:
        return sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            surface.pixels,
            surface.w,
            surface.h,
            64,
            surface.pitch,
            sdl2.SDL_PIXELFORMAT_RGBA32,
        ).contents

    @classproperty
    def top_left(self) -> Vector:
        """Returns the position of the top left of the window."""
        return Vector(0, 0)

    @classproperty
    def top_right(self) -> Vector:
        """Returns the position of the top right of the window."""
        return Vector(self.res.x, 0)

    @classproperty
    def bottom_left(self) -> Vector:
        """Returns the position of the bottom left of the window."""
        return Vector(0, self.res.y)

    @classproperty
    def bottom_right(self) -> Vector:
        """Returns the position of the bottom right of the window."""
        return Vector(self.res.x, self.res.y)

    @classproperty
    def top_center(self) -> Vector:
        """Returns the position of the top center of the window."""
        return Vector(self.res.x / 2, 0)

    @classproperty
    def bottom_center(self) -> Vector:
        """Returns the position of the bottom center of the window."""
        return Vector(self.res.x / 2, self.res.y)

    @classproperty
    def center_left(self) -> Vector:
        """Returns the position of the center left of the window."""
        return Vector(0, self.res.y / 2)

    @classproperty
    def center_right(self) -> Vector:
        """Returns the position of the center right of the window."""
        return Vector(self.res.x, self.res.y / 2)

    @classproperty
    def center(self) -> Vector:
        """Returns the position of the center of the window."""
        return Vector(self.res.x / 2, self.res.y / 2)
