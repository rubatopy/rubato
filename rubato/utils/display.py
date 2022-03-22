"""
Global display class that allows for easy screen and window management.

Should be accessed through :code:`rubato.Display`
"""
import sdl2
import sdl2.ext
from rubato.utils.vector import Vector


class _Display(type):
    """
    A static class that houses all of the display information

    Attributes:
        window (sdl2.ext.Window): The pysdl2 window element.
        renderer (sdl2.ext.Renderer): The pysdl2 renderer element.
    """

    @property
    def window_size(self) -> Vector:
        """
        The pixel size of the physical window.

        Warning:
            Using this value to determine the placement of your sprites will
            lead to unexpected results. Instead you should use
            :func:`Display.resolution <rubato.utils.display.Display.resolution>`
        """
        return Vector(*self.window.size)

    @window_size.setter
    def window_size(self, new: Vector):
        self.window.size = new.to_int().to_tuple()

    @property
    def resolution(self) -> Vector:
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
        """  # pylint: disable=line-too-long
        return Vector(*self.renderer.logical_size)

    @resolution.setter
    def resolution(self, new: Vector):
        self.renderer.logical_size = new.to_int().to_tuple()

    @property
    def window_pos(self) -> Vector:
        """The current position of the window in terms of screen pixels"""
        return Vector(*self.window.position)

    @window_pos.setter
    def window_pos(self, new: Vector):
        self.window.position = new.to_int().to_tuple()

    @property
    def window_name(self):
        return self.window.title

    @window_name.setter
    def window_name(self, new: str):
        self.window.title = new

    def set_window_icon(self, path: str):
        """
        Set the icon of the window.

        Args:
            path: The path to the icon.
        """
        sdl2.video.SDL_SetWindowIcon(
            self.window,
            sdl2.ext.image.load_img(path),
        )

    def update(self, surface: sdl2.SDL_Surface, pos: Vector):
        """
        Update the current screen.

        Args:
            surface: The surface to draw on the screen.
            pos: The position to draw the surface on.
        """
        self.renderer.copy(
            sdl2.ext.Texture(self.renderer, surface),
            None,
            (
                pos.x,
                pos.y,
                surface.contents.w,
                surface.contents.h,
            ),
        )

    def clone_surface(self, surface: sdl2.SDL_Surface) -> sdl2.SDL_Surface:
        return sdl2.SDL_CreateRGBSurfaceWithFormatFrom(
            surface.pixels,
            surface.w,
            surface.h,
            64,
            surface.pitch,
            sdl2.SDL_PIXELFORMAT_RGBA32,
        ).contents

    @property
    def top_left(self) -> Vector:
        """Returns the position of the top left of the window."""
        return Vector(0, 0)

    @property
    def top_right(self) -> Vector:
        """Returns the position of the top right of the window."""
        return Vector(self.resolution.x, 0)

    @property
    def bottom_left(self) -> Vector:
        """Returns the position of the bottom left of the window."""
        return Vector(0, self.resolution.y)

    @property
    def bottom_right(self) -> Vector:
        """Returns the position of the bottom right of the window."""
        return Vector(self.resolution.x, self.resolution.y)

    @property
    def top_center(self) -> Vector:
        """Returns the position of the top center of the window."""
        return Vector(self.resolution.x / 2, 0)

    @property
    def bottom_center(self) -> Vector:
        """Returns the position of the bottom center of the window."""
        return Vector(self.resolution.x / 2, self.resolution.y)

    @property
    def center_left(self) -> Vector:
        """Returns the position of the center left of the window."""
        return Vector(0, self.resolution.y / 2)

    @property
    def center_right(self) -> Vector:
        """Returns the position of the center right of the window."""
        return Vector(self.resolution.x, self.resolution.y / 2)

    @property
    def center(self) -> Vector:
        """Returns the position of the center of the window."""
        return Vector(self.resolution.x / 2, self.resolution.y / 2)


class Display(metaclass=_Display):
    window: sdl2.ext.Window = None
    renderer: sdl2.ext.Renderer = None
