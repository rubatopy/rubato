"""
Global display class that allows for easy screen and window management.
"""
import sdl2
import sdl2.ext
from rubato.utils.vector import Vector


class Display:
    """
    A static class that houses all of the display information

    Attributes:
        window (sdl2.ext.Window): The pysdl2 window element.
        renderer (sdl2.ext.Renderer): The pysdl2 renderer element.
    """

    window: sdl2.ext.Window = None
    renderer: sdl2.ext.Renderer = None

    def __get_window_size(self) -> Vector:
        """
        The pixel size of the physical window.

        Warning:
            Using this value to determine the placement of your game objects will
            lead to unexpected results. Instead you should use
            :func:`Display.res <rubato.utils.display.Display.res>`
        """
        return Vector(*self.window.size)

    def __set_window_size(self, new: Vector):
        self.window.size = new.to_int().to_tuple()

    window_size = classmethod(property(__get_window_size, __set_window_size, doc=__get_window_size.__doc__))

    def __get_res(self) -> Vector:
        """
        The pixel resolution of the game. This is the number of virtual
        pixels on the window.

        Example:
            The window (:func:`Display.window_size <rubato.utils.display.Display.window_size>`)
            could be rendered at 720p while the resolution is still at 1080p.
            This means that you can place game objects
            at 1000, 1000 and still have them draw despite the window not being
            1000 pixels wide.

        Warning:
            While this value can be changed, it is recommended that you do not
            change it as it will scale your entire project in ways you might
            not expect.
        """
        return Vector(*self.renderer.logical_size)

    def __set_res(self, new: Vector):
        self.renderer.logical_size = new.to_int().to_tuple()

    res = classmethod(property(__get_res, __set_res, doc=__get_res.__doc__))

    def __get_window_pos(self) -> Vector:
        """The current position of the window in terms of screen pixels"""
        return Vector(*self.window.position)

    def __set_window_pos(self, new: Vector):
        self.window.position = new.to_int().to_tuple()

    window_pos = classmethod(property(__get_window_pos, __set_window_pos, doc=__get_window_pos.__doc__))

    def __get_window_name(self):
        return self.window.title

    def __set_window_name(self, new: str):
        self.window.title = new

    window_name = classmethod(property(__get_window_name, __set_window_name, doc=__get_window_name.__doc__))

    @classmethod
    @property
    def display_ratio(cls) -> Vector:
        """The ratio of the renderer resolution to the window size.

        Returns:
            Vector: The vector value of this ratio
        """
        return cls.res / cls.window_size

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
        try:
            w, h = surface.w, surface.h
        except AttributeError:
            w, h = surface.contents.w, surface.contents.h

        texture = sdl2.ext.Texture(cls.renderer, surface)

        cls.renderer.copy(
            texture,
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
        """Clones an SDL surface."""
        return sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            surface.pixels,
            surface.w,
            surface.h,
            64,
            surface.pitch,
            sdl2.SDL_PIXELFORMAT_RGBA32,
        ).contents

    @classmethod
    @property
    def top_left(cls) -> Vector:
        """Returns the position of the top left of the window."""
        return Vector(0, 0)

    @classmethod
    @property
    def top_right(cls) -> Vector:
        """Returns the position of the top right of the window."""
        return Vector(cls.res.x, 0)

    @classmethod
    @property
    def bottom_left(cls) -> Vector:
        """Returns the position of the bottom left of the window."""
        return Vector(0, cls.res.y)

    @classmethod
    @property
    def bottom_right(cls) -> Vector:
        """Returns the position of the bottom right of the window."""
        return Vector(cls.res.x, cls.res.y)

    @classmethod
    @property
    def top_center(cls) -> Vector:
        """Returns the position of the top center of the window."""
        return Vector(cls.res.x / 2, 0)

    @classmethod
    @property
    def bottom_center(cls) -> Vector:
        """Returns the position of the bottom center of the window."""
        return Vector(cls.res.x / 2, cls.res.y)

    @classmethod
    @property
    def center_left(cls) -> Vector:
        """Returns the position of the center left of the window."""
        return Vector(0, cls.res.y / 2)

    @classmethod
    @property
    def center_right(cls) -> Vector:
        """Returns the position of the center right of the window."""
        return Vector(cls.res.x, cls.res.y / 2)

    @classmethod
    @property
    def center(cls) -> Vector:
        """Returns the position of the center of the window."""
        return Vector(cls.res.x / 2, cls.res.y / 2)
