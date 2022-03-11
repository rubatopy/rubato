"""
Global display class that allows for easy screen and window management.
"""
import sdl2
import sdl2.ext
from rubato.utils.vector import Vector

screen: sdl2.surface.SDL_Surface = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
    0,
    0,
    0,
    64,
    sdl2.SDL_PIXELFORMAT_RGBA32,
)
window: sdl2.ext.Window = None


def update(surface: sdl2.surface.SDL_Surface, pos: Vector):
    """
    Update the current display.

    Args:
        surface: The surface to draw on the display.
        pos: The position to draw the surface on.
    """
    sdl2.surface.SDL_BlitSurface(
        surface,
        None,
        screen,
        sdl2.surface.SDL_Rect(
            pos.x,
            pos.y,
            surface.w,
            surface.h,
        ),
    )


def set_window_position(x: int, y: int):
    """
    Set the position of the window.

    Args:
        x: The x position.
        y: The y position.
    """
    window.position = (x, y)


def set_window_name(name: str):
    """
    Set the title of the window.

    Args:
        name: The name of the window.
    """
    window.title = name


def set_window_icon(path: str):
    """
    Set the icon of the window.

    Args:
        path: The path to the icon.
    """
    sdl2.video.SDL_SetWindowIcon(window, sdl2.ext.image.load_img(path))


def clone_surface(
        surface: sdl2.surface.SDL_Surface) -> sdl2.surface.SDL_Surface:
    return sdl2.surface.SDL_CreateRGBSurfaceWithFormatFrom(
        surface.pixels,
        surface.w,
        surface.h,
        64,
        surface.pitch,
        sdl2.SDL_PIXELFORMAT_RGBA32,
    ).contents
