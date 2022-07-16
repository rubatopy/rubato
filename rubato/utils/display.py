"""
Global display class that allows for easy screen and window management.
"""
from __future__ import annotations

import ctypes
from typing import Literal

import sdl2, sdl2.ext, sdl2.sdlimage
import os

from . import Vector, get_path


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
        # Another way to do this.
        # wp, hp = ctypes.c_int(), ctypes.c_int()
        # if sdl2.SDL_GetRendererOutputSize(cls.renderer.sdlrenderer, ctypes.pointer(wp), ctypes.pointer(hp)) != 0:
        #     raise RuntimeError(f"Could not get renderer size: {sdl2.SDL_GetError()}")
        # w, h = wp.value, hp.value

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
            :func:`camera zoom <rubato.struct.camera.Camera.zoom>` property in your scene's camera.
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

    @property
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

    @property
    def has_x_border(cls) -> bool:
        """Whether or not the window has a black border on the left or right side."""
        render_rat = cls.res.y / cls.res.x
        window_rat = cls.window_size.y / cls.window_size.x

        return render_rat > window_rat

    @property
    def has_y_border(cls) -> bool:
        """Whether or not the window has a black border on the top or bottom."""
        render_rat = cls.res.y / cls.res.x
        window_rat = cls.window_size.y / cls.window_size.x

        return render_rat < window_rat


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
    _saved_window_size: Vector | None = None
    _saved_window_pos: Vector | None = None

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
        cls.renderer.copy(
            tx,
            None,
            (pos.x, pos.y),
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

            if save_to_temp_path:
                path = bytes(get_path(os.path.join(path, filename, filename + "." + extension)), "utf-8")
            else:
                path = bytes(os.path.join(path, filename + "." + extension), "utf-8")

            if extension == "png":
                return sdl2.sdlimage.IMG_SavePNG(render_surface, path) == 0
            elif extension == "jpg":
                return sdl2.sdlimage.IMG_SaveJPG(render_surface, path, quality) == 0
            elif extension == "bmp":
                return sdl2.SDL_SaveBMP(render_surface, path) == 0

        finally:
            sdl2.SDL_FreeSurface(render_surface)

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
