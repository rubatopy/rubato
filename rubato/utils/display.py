"""
Global display class that allows for easy screen and window management.
"""
from __future__ import annotations

import ctypes, cython
from typing import Literal

import sdl2, sdl2.ext, sdl2.sdlimage
import os

from . import Vector, get_path, InitError


class _Res:

    def __get__(self, *_):
        return Vector(*Display.renderer.logical_size)

    def __set__(self, _, new: Vector):
        Display.renderer.logical_size = new.tuple_int()


class _WindowPos:

    def __get__(self, *_):
        return Vector(*Display.window.position)

    def __set__(self, _, new: Vector):
        Display.window.position = new.tuple_int()


class _WindowName:

    def __get__(self, *_) -> str:
        return Display.window.title

    def __set__(self, _, new: str):
        Display.window.title = new


class _WindowSize:

    def __get__(self, *_):
        return Vector(*Display.window.size)

    def __set__(self, _, new: Vector):
        Display.window.size = new.tuple_int()


@cython.cclass
class Display:
    """
    A static class that houses all of the display information
    """
    window = None
    """sdl2.ext.Window | None: The pysdl2 window element."""
    renderer = None
    """sdl2.ext.Renderer | None: The pysdl2 renderer element."""
    format = sdl2.SDL_CreateRGBSurfaceWithFormat(0, 1, 1, 32, sdl2.SDL_PIXELFORMAT_RGBA8888).contents.format.contents

    window_pos = type("Vector", (_WindowPos,), {})()
    """Vector: The current position of the window in terms of screen pixels"""
    res = type("Vector", (_Res,), {})()
    """
    Vector: The pixel resolution of the game. This is the number of virtual
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
        :func:`camera zoom <rubato.struct.camera.Camera.zoom>` property in your scene's camera.
    """
    window_name = type("str", (_WindowName,), {})()
    """str: The name of the window."""
    window_size = type("Vector", (_WindowSize,), {})()
    """
    Vector: The pixel size of the physical window.

    Warning:
        Using this value to determine the placement of your game objects may
        lead to unexpected results. You should instead use
        :func:`Display.res <rubato.utils.display.Display.res>`
    """

    _saved_window_size: Vector | None
    _saved_window_pos: Vector | None

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def display_ratio(cls) -> Vector:
        """The ratio of the renderer resolution to the window size. This is a read-only property.

        Returns:
            Vector: The ratio of the renderer resolution to the window size seperated by x and y.
        """
        return cls.res / cls.window_size

    @classmethod
    def border_size(cls) -> int:
        """The size of the black border on either side of the drawing area when the aspect ratios don't match."""
        # if a smart programmer can actually understand this, please check that its working correctly.
        # Thank you.
        render_rat = cls.res.y / cls.res.x
        window_rat = cls.window_size.y / cls.window_size.x

        if render_rat > window_rat:  # side burns
            rat = render_rat / window_rat  # how much fatter the window is than the render
            return round((cls.window_size.x - cls.window_size.x / rat) / 2)
        elif render_rat < window_rat:  # top burns
            rat = window_rat / render_rat  # how thinner the window is than the render
            return round((cls.window_size.y - cls.window_size.y / rat) / 2)
        return 0

    @classmethod
    def has_x_border(cls) -> bool:
        """Whether or not the window has a black border on the left or right side."""
        render_rat = cls.res.y / cls.res.x
        window_rat = cls.window_size.y / cls.window_size.x

        return render_rat > window_rat

    @classmethod
    def has_y_border(cls) -> bool:
        """Whether or not the window has a black border on the top or bottom."""
        render_rat = cls.res.y / cls.res.x
        window_rat = cls.window_size.y / cls.window_size.x

        return render_rat < window_rat

    @classmethod
    def set_window_icon(cls, path: str):
        """
        Set the icon of the window.

        Args:
            path: The path to the icon.
        """

        image = sdl2.ext.image.load_img(get_path(path))

        sdl2.SDL_SetWindowIcon(
            cls.window.window,
            image,
        )

    @classmethod
    def set_fullscreen(cls, on: bool = True, mode: Literal["desktop", "exclusive"] = "desktop"):
        """
        Set the window to fullscreen.

        Args:
            on: Whether or not to set the window to fullscreen.
            mode: The type of fullscreen to use. Can be either "desktop" or "exclusive".
        """
        if on:
            if cls._saved_window_pos is None and cls._saved_window_size is None:
                cls._saved_window_size = cls.window_size.clone()
                cls._saved_window_pos = cls.window_pos.clone()
            if mode == "desktop":
                sdl2.SDL_SetWindowFullscreen(cls.window.window, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
            elif mode == "exclusive":
                sdl2.SDL_SetWindowFullscreen(cls.window.window, sdl2.SDL_WINDOW_FULLSCREEN)
            else:
                raise ValueError(f"Invalid fullscreen type: {mode}")
        else:
            if cls._saved_window_size is not None and cls._saved_window_pos is not None:
                cls.window_size = cls._saved_window_size
                cls.window_pos = cls._saved_window_pos
                cls._saved_window_size = None
                cls._saved_window_pos = None
            sdl2.SDL_SetWindowFullscreen(cls.window.window, 0)

    @classmethod
    def update(cls, tx: sdl2.ext.Texture, pos: Vector):
        """
        Update the current screen.

        Args:
            tx: The texture to draw on the screen.
            pos: The position to draw the texture on.
        """
        cls.renderer.copy(src=tx, dstrect=(pos.x, pos.y))

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
    def get_window_border_size(cls):
        """
        Get the size of the window border. pixels on the top sides and bottom of the window.

        Returns:
            The size of the window border.
        """
        top, left, bottom, right = ctypes.c_int(), ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
        sdl2.SDL_GetWindowBordersSize(
            cls.window.window, ctypes.byref(top), ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right)
        )
        return top.value, left.value, bottom.value, right.value

    @classmethod
    def save_screenshot(
        cls,
        filename: str,
        path: str = "./",
        extension: str = "png",
        save_to_temp_path: bool = False,
        quality: int = 100
    ) -> bool:
        """
        Save the current screen to a file.

        Args:
            filename: The name of the file to save to.
            path: Path to output folder.
            extension: The extension to save the file as. (png, jpg, bmp supported)
            save_to_temp_path: Whether to save the file to a temporary path (i.e. MEIPASS used in exe).
            quality: The quality of the jpg 0-100 (only used for jpgs).

        Returns:
            If save was successful.
        """
        if extension not in ["png", "jpg", "bmp"]:
            raise ValueError("Invalid extension. Only png, jpg, bmp are supported.")

        render_surface = sdl2.SDL_CreateRGBSurfaceWithFormat(
            0, cls.window_size.x, cls.window_size.y, 32, sdl2.SDL_PIXELFORMAT_ARGB8888
        )
        if not render_surface:
            raise RuntimeError(f"Could not create surface: {sdl2.SDL_GetError()}")
        try:
            if sdl2.SDL_RenderReadPixels(
                cls.renderer.sdlrenderer, sdl2.SDL_Rect(0, 0, cls.window_size.x, cls.window_size.y),
                sdl2.SDL_PIXELFORMAT_ARGB8888, render_surface.contents.pixels, render_surface.contents.pitch
            ) != 0:
                raise RuntimeError(f"Could not read screenshot: {sdl2.SDL_GetError()}")

            path_bytes: bytes = path.encode("utf-8")
            if save_to_temp_path:
                path_bytes = bytes(get_path(os.path.join(path, filename, filename + "." + extension)), "utf-8")
            else:
                path_bytes = bytes(os.path.join(path, filename + "." + extension), "utf-8")

            if extension == "png":
                return sdl2.sdlimage.IMG_SavePNG(render_surface, path_bytes) == 0
            elif extension == "jpg":
                return sdl2.sdlimage.IMG_SaveJPG(render_surface, path_bytes, quality) == 0
            elif extension == "bmp":
                return sdl2.SDL_SaveBMP(render_surface, path_bytes) == 0

        finally:
            sdl2.SDL_FreeSurface(render_surface)

    top_left = type("Vector", (), {"__get__": lambda *_: Vector()})()
    """Vector: The position of the top left of the window."""
    top_right = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x, 0)})()
    """Vector: The position of the top right of the window."""
    bottom_left = type("Vector", (), {"__get__": lambda *_: Vector(0, Display.res.y)})()
    """Vector: The position of the bottom left of the window."""
    bottom_right = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x, Display.res.y)})()
    """Vector: The position of the bottom right of the window."""
    top_center = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x // 2, 0)})()
    """Vector: The position of the top center of the window."""
    bottom_center = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x // 2, Display.res.y)})()
    """Vector: The position of the bottom center of the window."""
    center_left = type("Vector", (), {"__get__": lambda *_: Vector(0, Display.res.y // 2)})()
    """Vector: The position of the center left of the window."""
    center_right = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x, Display.res.y // 2)})()
    """Vector: The position of the center right of the window."""
    center = type("Vector", (), {"__get__": lambda *_: Vector(Display.res.x // 2, Display.res.y // 2)})()
    """Vector: The position of the center of the window."""
    top = type("int", (), {"__get__": lambda *_: 0})()
    """int: The position of the top of the window."""
    bottom = type("int", (), {"__get__": lambda *_: int(Display.res.y)})()
    """int: The position of the bottom of the window."""
    left = type("int", (), {"__get__": lambda *_: 0})()
    """int: The position of the left of the window."""
    right = type("int", (), {"__get__": lambda *_: int(Display.res.x)})()
    """int: The position of the right of the window."""
