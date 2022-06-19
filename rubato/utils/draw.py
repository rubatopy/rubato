"""A static draw class for drawing things directly to the renderer."""
from ctypes import c_int16
from typing import List, Optional, Callable
from dataclasses import dataclass, field
import heapq

import sdl2.ext
from sdl2.sdlgfx import pixelRGBA, thickLineRGBA, filledPolygonRGBA, aapolygonRGBA

from . import Vector, Color, Font, Display, Math


@dataclass(order=True)
class DrawTask:
    priority: int
    func: Callable = field(compare=False)


class Draw:
    """Draws things to the renderer. Dont instantiate, instead use it as a static class."""
    _queue: List[DrawTask] = []

    @classmethod
    def dump(cls):
        """Draws all queued items. Is called automatically at the end of every frame."""

        while cls._queue:
            task = heapq.heappop(cls._queue)
            task.func()

    @classmethod
    def point(cls, pos: Vector, color: Color = Color.green, z_index: int = Math.INF):
        """
        Draw a point onto the renderer at the end of the frame.

        Args:
            pos (Vector): The position of the point.
            color (Color, optional): The color to use for the pixel. Defaults to Color.green.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(cls._queue, DrawTask(z_index, lambda: cls.immediate_point(pos, color)))

    @staticmethod
    def immediate_point(pos: Vector, color: Color = Color.green):
        """
        Draw a point onto the renderer immediately.

        Args:
            pos (Vector): The position of the point.
            color (Color, optional): The color to use for the pixel. Defaults to Color.green.
        """
        pixelRGBA(Display.renderer.sdlrenderer, round(pos.x), round(pos.y), *color.to_tuple())

    @classmethod
    def line(cls, p1: Vector, p2: Vector, color: Color = Color.green, width: int = 1, z_index: int = Math.INF):
        """
        Draw a line onto the renderer at the end of the frame.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to green.
            width: The width of the line. Defaults to 1.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(cls._queue, DrawTask(z_index, lambda: cls.immediate_line(p1, p2, color, width)))

    @staticmethod
    def immediate_line(p1: Vector, p2: Vector, color: Color = Color.green, width: int = 1):
        """
        Draw a line onto the renderer immediately.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to green.
            width: The width of the line. Defaults to 1.
        """
        thickLineRGBA(
            Display.renderer.sdlrenderer, round(p1.x), round(p1.y), round(p2.x), round(p2.y), round(width), color.r,
            color.g, color.b, color.a
        )

    @classmethod
    def rect(
        cls,
        center: Vector,
        width: int,
        height: int,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        angle: float = 0,
        z_index: int = Math.INF
    ):
        """
        Draws a rectangle onto the renderer at the end of the frame.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(
            cls._queue,
            DrawTask(z_index, lambda: cls.immediate_rect(center, width, height, border, border_thickness, fill, angle))
        )

    @staticmethod
    def immediate_rect(
        center: Vector,
        width: int,
        height: int,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        angle: float = 0
    ):
        """
        Draws a rectangle onto the renderer immediately.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
        """
        x, y = width // 2, height // 2
        verts = [Vector(-x, -y), Vector(x, -y), Vector(x, y), Vector(-x, y)]

        trans = [v.rotate(angle) for v in verts]

        real = [(center + v).to_int() for v in trans]

        Draw.immediate_poly(real, border, border_thickness, fill)

    @classmethod
    def circle(
        cls,
        center: Vector,
        radius: int = 4,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF
    ):
        """
        Draws a circle onto the renderer at the end of the frame.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(
            cls._queue, DrawTask(z_index, lambda: cls.immediate_circle(center, radius, border, border_thickness, fill))
        )

    @staticmethod
    def immediate_circle(
        center: Vector,
        radius: int = 4,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None
    ):
        """
        Draws a circle onto the renderer immediately.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
        """
        if fill:
            sdl2.sdlgfx.filledCircleRGBA(
                Display.renderer.sdlrenderer,
                int(center.x),
                int(center.y),
                int(radius),
                fill.r,
                fill.g,
                fill.b,
                fill.a,
            )

        for i in range(border_thickness):
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(center.x),
                int(center.y),
                int(radius) + i,
                border.r,
                border.g,
                border.b,
                border.a,
            )

    @classmethod
    def poly(
        cls,
        points: List[Vector],
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF
    ):
        """
        Draws a polygon onto the renderer at the end of the frame.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(
            cls._queue, DrawTask(z_index, lambda: cls.immediate_poly(points, border, border_thickness, fill))
        )

    @staticmethod
    def immediate_poly(
        points: List[Vector], border: Color = Color.green, border_thickness: int = 1, fill: Optional[Color] = None
    ):
        """
        Draws a polygon onto the renderer immediately.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
        """
        x_coords, y_coords = zip(*points)

        vx = (c_int16 * len(x_coords))(*x_coords)
        vy = (c_int16 * len(y_coords))(*y_coords)
        if fill:
            filledPolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(points),
                fill.r,
                fill.g,
                fill.b,
                fill.a,
            )
        if border_thickness == 1:
            aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(points),
                border.r,
                border.g,
                border.b,
                border.a,
            )
        else:
            for i in range(len(points)):
                Draw.immediate_line(
                    Vector(
                        points[i].x,
                        points[i].y,
                    ),
                    Vector(
                        points[(i + 1) % len(points)].x,
                        points[(i + 1) % len(points)].y,
                    ),
                    Color(0, 255),
                    border_thickness,
                )

    @classmethod
    def text(
        cls,
        text: str,
        font: Font,
        pos: Vector = Vector(),
        justify: str = "left",
        align: Vector = Vector(),
        width: int = 0,
        z_index: int = Math.INF
    ):
        """
        Draws some text onto the renderer at the end of the frame.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to Vector(0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to Vector(0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
            z_index (int, optional): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        heapq.heappush(
            cls._queue, DrawTask(z_index, lambda: cls.immediate_text(text, font, pos, justify, align, width))
        )

    @staticmethod
    def immediate_text(
        text: str, font: Font, pos: Vector = Vector(), justify: str = "left", align: Vector = Vector(), width: int = 0
    ):
        """
        Draws some text onto the renderer immediately.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to Vector(0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to Vector(0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
        """
        tx = sdl2.ext.Texture(Display.renderer, font.generate_surface(text, justify, width))
        Display.update(tx, pos + (align - 1) * Vector(*tx.size) / 2)
