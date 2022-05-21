"""A static draw class for drawing things directly to the renderer."""
from ctypes import c_int16
from typing import List, Optional
import sdl2.ext
from sdl2.sdlgfx import pixelRGBA, thickLineRGBA, filledPolygonRGBA, aapolygonRGBA

from . import Defaults, Vector, Color, Font, Display


class Draw:
    """Draws things to the renderer. Should not instantiate this class."""

    @staticmethod
    def point(pos: Vector, color: Color = Color.green):
        """
        Draw a point onto the renderer.

        Args:
            pos: The position of the point.
            color: The color to use for the pixel. Defaults to green.
        """

        pixelRGBA(Display.renderer.sdlrenderer, round(pos.x), round(pos.y), *color.to_tuple())

    @staticmethod
    def line(p1: Vector, p2: Vector, color: Color = Color.green, width: int = 1):
        """
        Draw a line onto the renderer.

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

    @staticmethod
    def rect(
        center: Vector,
        width: int,
        height: int,
        border: Color = Color.green,
        border_thickness: int = 1,
        fill: Optional[Color] = None,
        angle: float = 0
    ):
        """
        Draws a rectangle onto the renderer.

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

        Draw.poly(real, border, border_thickness, fill)

    @staticmethod
    def circle(center: Vector, radius: int, border: Color = Color.green, border_thickness: int = 1,
               fill: Optional[Color] = None):
        """
        Draws a circle onto the renderer.

        Args:
            center: The center.
            radius: The radius.
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

    @staticmethod
    def poly(points: List[Vector], border: Color = Color.green, border_thickness: int = 1,
             fill: Optional[Color] = None):
        """
        Draws a polygon onto the renderer.

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
                Draw.line(
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

    @staticmethod
    def text(
        text: str,
        font: Font,
        pos: Vector = Vector(),
        justify: str = Defaults.text_defaults["justify"],
        align: Vector = Defaults.text_defaults["anchor"],
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
        tx = sdl2.ext.Texture(Display.renderer, font.generate_surface(text, justify, width))
        Display.update(tx, pos + (align - 1) * Vector(*tx.size) / 2)
