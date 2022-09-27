"""A static class for drawing things directly to the window."""
from __future__ import annotations
from typing import Optional, Callable
import cython

import sdl2, sdl2.ext

from . import Vector, Color, Font, Display, Math, InitError, Camera, Surface


@cython.cclass
class DrawTask:
    priority: int = cython.declare(int, visibility="public")  # type: ignore
    func: Callable = cython.declare(object, visibility="public")  # type: ignore

    def __init__(self, priority: int, func: Callable):
        self.priority = priority
        self.func = func


# THIS IS A STATIC CLASS
class Draw:
    """A static class allowing drawing items to the window."""
    _queue: list[DrawTask] = []
    _cached_surfs: dict[int, Surface] = {}

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def clear(cls, background_color: Color = Color.white, border_color: Color = Color.black):
        """
        Clears the renderer and draws the background of the frame.

        Args:
            background_color: The background color. Defaults to white.
            border_color: The border color. Defaults to black.
                Shown when the aspect ratio of the game does not match the aspect ratio of the window.
        """
        Display.renderer.clear(border_color.to_tuple())
        Display.renderer.fill(
            (0, 0, *Display.renderer.logical_size),
            background_color.to_tuple(),
        )

    @classmethod
    def push(cls, z_index: int, callback: Callable):
        """
        Add a custom draw function to the frame queue.

        Args:
            z_index: The z_index to call at (lower z_indexes get called first).
            callback: The function to call.
        """
        cls._queue.append(DrawTask(z_index, callback))

    @classmethod
    def dump(cls):
        """Draws all queued items. Is called automatically at the end of every frame."""
        if not cls._queue:
            return

        cls._queue.sort(key=lambda x: x.priority)

        for task in cls._queue:
            task.func()

        cls._queue.clear()

    @classmethod
    def queue_point(
        cls,
        pos: Vector | tuple[float, float],
        color: Color = Color.cyan,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draw a point onto the renderer at the end of the frame.

        Args:
            pos: The position of the point.
            color: The color to use for the pixel. Defaults to Color.cyan.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.point(pos, color, camera))

    @classmethod
    def point(cls, pos: Vector | tuple[float, float], color: Color = Color.cyan, camera: Camera | None = None):
        """
        Draw a point onto the renderer immediately.

        Args:
            pos: The position of the point.
            color: The color to use for the pixel. Defaults to Color.cyan.
            camera: The camera to use. Defaults to None.
        """
        if (surf := cls._cached_surfs.get(hash(color), None)) is None:
            surf = Surface(1, 1)
            surf.fill(color)
            cls._cached_surfs[hash(color)] = surf

        cls.surface(surf, pos, camera)

    @classmethod
    def queue_line(
        cls,
        p1: Vector | tuple[float, float],
        p2: Vector | tuple[float, float],
        color: Color = Color.cyan,
        width: int | float = 1,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draw a line onto the renderer at the end of the frame.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to Color.cyan.
            width: The width of the line. Defaults to 1.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.line(p1, p2, color, width, camera))

    @staticmethod
    def line(
        p1: Vector | tuple[float, float],
        p2: Vector | tuple[float, float],
        color: Color = Color.cyan,
        width: int | float = 1,
        camera: Camera | None = None
    ):
        """
        Draw a line onto the renderer immediately.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to Color.cyan.
            width: The width of the line. Defaults to 1.
            camera: The camera to use. Defaults to None.
        """
        hashed = hash((p1, p2, color, width))

        if (surf := Draw._cached_surfs.get(hashed, None)) is None:
            surf = Surface(*Display.res.tuple_int())
            surf.draw_line(p1, p2, color, thickness=round(width))
            Draw._cached_surfs[hashed] = surf

        Draw.surface(surf, Display.center, camera)

    @classmethod
    def queue_rect(
        cls,
        center: Vector | tuple[float, float],
        width: int | float,
        height: int | float,
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        angle: float = 0,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draws a rectangle onto the renderer at the end of the frame.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.rect(center, width, height, border, border_thickness, fill, angle, camera))

    @classmethod
    def rect(
        cls,
        center: Vector | tuple[float, float],
        width: int | float,
        height: int | float,
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        angle: float = 0,
        camera: Camera | None = None
    ):
        """
        Draws a rectangle onto the renderer immediately.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
            camera: The camera to use. Defaults to None.
        """
        hashed = hash((width, height, border, border_thickness, fill))

        if (surf := cls._cached_surfs.get(hashed, None)) is None:
            surf = Surface(round(width), round(height))
            surf.draw_rect((0, 0), (width, height), border, round(border_thickness), fill)
            cls._cached_surfs[hashed] = surf

        surf.rotation = angle
        cls.surface(surf, center, camera)

    @classmethod
    def queue_circle(
        cls,
        center: Vector | tuple[float, float],
        radius: int = 4,
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draws a circle onto the renderer at the end of the frame.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.circle(center, radius, border, border_thickness, fill, camera))

    @classmethod
    def circle(
        cls,
        center: Vector | tuple[float, float],
        radius: int | float = 4,
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        camera: Camera | None = None
    ):
        """
        Draws a circle onto the renderer immediately.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            camera: The camera to use. Defaults to None.
        """
        hashed = hash((radius, border, border_thickness, fill))
        if (surf := cls._cached_surfs.get(hashed, None)) is None:
            surf = Surface(round(radius * 2) + 1, round(radius * 2) + 1)
            surf.draw_circle((radius, radius), round(radius), border, round(border_thickness), fill)
            cls._cached_surfs[hashed] = surf

        cls.surface(surf, center, camera)

    @classmethod
    def queue_poly(
        cls,
        points: list[Vector] | list[tuple[float, float]],
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draws a polygon onto the renderer at the end of the frame.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.poly(points, border, border_thickness, fill, camera))

    @classmethod
    def poly(
        cls,
        points: list[Vector] | list[tuple[float, float]],
        border: Color = Color.cyan,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        camera: Camera | None = None
    ):
        """
        Draws a polygon onto the renderer immediately.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to Color.cyan.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            camera: The camera to use. Defaults to None.
        """
        hashed = hash((tuple(points), border, border_thickness, fill))
        if (surf := cls._cached_surfs.get(hashed, None)) is None:
            surf = Surface(*Display.res.tuple_int())
            surf.draw_poly(points, border, round(border_thickness), fill)
            cls._cached_surfs[hashed] = surf

        cls.surface(surf, Display.center, camera)

    @classmethod
    def queue_text(
        cls,
        text: str,
        font: Font,
        pos: Vector | tuple[float, float] = (0, 0),
        justify: str = "left",
        align: Vector | tuple[float, float] = (0, 0),
        width: int | float = 0,
        scale: Vector | tuple[float, float] = (1, 1),
        shadow: bool = False,
        shadow_pad: int = 0,
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draws some text onto the renderer at the end of the frame.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to (0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to (0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
            scale: The scale of the text. Defaults to (1, 1).
            shadow: Whether to draw a basic shadow box behind the text. Defaults to False.
            shadow_pad: What padding to use for the shadow. Defaults to 0.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.text(text, font, pos, justify, align, width, scale, shadow, shadow_pad, camera))

    @classmethod
    def text(
        cls,
        text: str,
        font: Font,
        pos: Vector | tuple[float, float] = (0, 0),
        justify: str = "left",
        align: Vector | tuple[float, float] = (0, 0),
        width: int | float = 0,
        scale: Vector | tuple[float, float] = (1, 1),
        shadow: bool = False,
        shadow_pad: int = 0,
        camera: Camera | None = None
    ):
        """
        Draws some text onto the renderer immediately.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to (0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to (0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
            scale: The scale of the text. Defaults to (1, 1).
            shadow: Whether to draw a basic shadow box behind the text. Defaults to False.
            shadow_pad: What padding to use for the shadow. Defaults to 0.
            camera: The camera to use. Defaults to None.
        """
        if camera is not None:
            pos = camera.transform(pos)
            scale = camera.zoom * scale[0], camera.zoom * scale[1]
            shadow_pad = round(camera.zoom * shadow_pad)

        surf = font.generate_surface(text, justify, width)
        tx = sdl2.ext.Texture(Display.renderer, surf)
        sdl2.SDL_FreeSurface(surf)
        w, h = tx.size[0] * scale[0], font.size * scale[1]
        center = (
            pos[0] + (align[0] * w) / 2,
            pos[1] + (align[1] * h) / 2,
        )
        if shadow:
            cls.rect(center, w + shadow_pad, h + shadow_pad, fill=Color(a=200))
        Display.update(tx, center, scale)
        tx.destroy()

    @classmethod
    def queue_texture(
        cls,
        texture: sdl2.ext.Texture,
        pos: Vector | tuple[float, float] = (0, 0),
        z_index: int = Math.INF,
        scale: Vector | tuple[float, float] = (1, 1),
        angle: float = 0,
        camera: Camera | None = None
    ):
        """
        Draws an texture onto the renderer at the end of the frame.

        Args:
            texture: The texture to draw.
            pos: The position of the texture. Defaults to (0, 0).
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            scale: The scale of the texture. Defaults to (1, 1).
            angle: The clockwise rotation of the texture. Defaults to 0.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.texture(texture, pos, scale, angle, camera))

    @staticmethod
    def texture(
        texture: sdl2.ext.Texture,
        pos: Vector | tuple[float, float] = (0, 0),
        scale: Vector | tuple[float, float] = (1, 1),
        angle: float = 0,
        camera: Camera | None = None
    ):
        """
        Draws an SDL Texture onto the renderer immediately.

        Args:
            texture: The texture to draw.
            pos: The position to draw the texture at. Defaults to (0, 0).
            scale: The scale of the texture. Defaults to (1, 1).
            angle: The clockwise rotation of the texture. Defaults to 0.
            camera: The camera to use. Defaults to None.
        """
        if camera is not None:
            pos = camera.transform(pos)
            scale = camera.zoom * scale[0], camera.zoom * scale[1]

        Display.update(texture, pos, scale, angle)

    @classmethod
    def queue_surface(
        cls,
        surface: Surface,
        pos: Vector | tuple[float, float] = (0, 0),
        z_index: int = Math.INF,
        camera: Camera | None = None
    ):
        """
        Draws an surface onto the renderer at the end of the frame.

        Args:
            surface: The surface to draw.
            pos: The position to draw the surface at. Defaults to (0, 0).
            z_index: The z-index of the surface. Defaults to 0.
            camera: The camera to use. Defaults to None.
        """
        cls.push(z_index, lambda: cls.surface(surface, pos, camera))

    @classmethod
    def surface(cls, surface: Surface, pos: Vector | tuple[float, float] = (0, 0), camera: Camera | None = None):
        """
        Draws an surface onto the renderer immediately.

        Args:
            surface: The surface to draw.
            pos: The position to draw the surface at. Defaults to (0, 0).
            camera: The camera to use. Defaults to None.
        """
        if not surface._surf:
            return

        if not surface.uptodate:
            surface.regen()

        cls.texture(surface._tx, pos, surface.scale, surface.rotation, camera)
