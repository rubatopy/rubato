"""Various hitbox components that enable collisions"""
from __future__ import annotations
from typing import Callable, Dict, List, Optional, Union, TYPE_CHECKING, Set
import math
import sdl2
import sdl2.sdlgfx
from ctypes import c_int16

from . import Component
from ... import Display, Vector, Defaults, Color, Error, SideError, Game

if TYPE_CHECKING:
    from .. import Camera


class Hitbox(Component):
    """
    A hitbox superclass. Do not use this class to attach hitboxes to your game objects.
    Instead, use Polygon, Rectangle, or Circle, which inherit Hitbox properties.

    Attributes:
        debug (bool): Whether to draw a green outline around the hitbox or not.
        trigger (bool): Whether this hitbox is just a trigger or not.
        scale (int): The scale of the hitbox
        on_collide (Callable): The on_collide function to call when a collision happens with this hitbox.
        on_exit (Callable): The on_exit function to call when a collision ends with this hitbox.
        color (Color) The color to fill this hitbox with.
        tag (str): The tag of the hitbox (can be used to identify hitboxes in collision callbacks)
        colliding (Set[Hitbox]): An unordered set of hitboxes that the Hitbox is currently colliding with.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Hitbox.

        Args:
            options: A Hitbox config. Defaults to the :ref:`Hitbox defaults <hitboxdef>`.
        """
        params = Defaults.hitbox_defaults | options
        super().__init__(params)
        self.debug: bool = params["debug"]
        self.trigger: bool = params["trigger"]
        self.scale: int = params["scale"]
        self.on_collide: Callable = params["on_collide"]
        self.on_exit: Callable = params["on_exit"]
        self.color: Color = params["color"]
        self.singular: bool = False
        self.tag: str = params["tag"]
        self.colliding: Set[Hitbox] = set()

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the hitbox's center"""
        return self.gameobj.pos + self.offset


class Polygon(Hitbox):
    """
    A polygon Hitbox implementation. Supports an arbitrary number of custom vertices, as long as the polygon is convex.

    Danger:
        If generating vertices by hand, make sure you generate them in a counter-clockwise direction.
        Otherwise, polygons will neither behave nor draw properly.

    Warning:
        Rubato does not currently support concave polygons explicitly.
        Creating concave polygons will result in undesired collision behavior.
        However, you can still use concave polygons in your projects:
        Simply break them up into multiple convex Polygon hitboxes and add them individually to a gameobject.

    Attributes:
        verts (List[Vector]): A list of the vertices in the Polygon, in anticlockwise direction.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Polygon.

        Args:
            options: A Polygon config. Defaults to the :ref:`Polygon defaults <polygondef>`.
        """
        super().__init__(options)
        params = Defaults.polygon_defaults | options
        self.verts: List[Vector] = params["verts"]

    def clone(self) -> Polygon:
        """Clones the Polygon"""
        return Polygon(
            {
                "debug": self.debug,
                "trigger": self.trigger,
                "scale": self.scale,
                "on_collide": self.on_collide,
                "color": self.color,
                "tag": self.tag,
                "offset": self.offset,
                "verts": self.verts,
            }
        )

    def translated_verts(self) -> List[Vector]:
        """Offsets each vertex with the Polygon's offset"""
        return [v * self.scale + self.offset for v in self.verts]

    def transformed_verts(self) -> List[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return [v.rotate(self.gameobj.rotation) for v in self.translated_verts()]

    def real_verts(self) -> List[Vector]:
        """Returns the a list of vertices in absolute coordinates"""
        return [self.gameobj.pos + v for v in self.transformed_verts()]

    def __str__(self):
        return f"{[str(v) for v in self.verts]}, {self.pos}, " + f"{self.scale}, {self.gameobj.rotation}"

    def draw(self, camera: Camera):
        list_of_points: List[tuple] = [camera.transform(v).tuple_int() for v in self.real_verts()]

        x_coords, y_coords = zip(*list_of_points)

        vx = (c_int16 * len(x_coords))(*x_coords)
        vy = (c_int16 * len(y_coords))(*y_coords)

        if self.color is not None:
            sdl2.sdlgfx.filledPolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(list_of_points),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
            sdl2.sdlgfx.aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(list_of_points),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )

        if self.debug or Game.debug:
            for i in range(len(list_of_points)):
                sdl2.sdlgfx.thickLineRGBA(
                    Display.renderer.sdlrenderer, list_of_points[i][0], list_of_points[i][1],
                    list_of_points[(i + 1) % len(list_of_points)][0], list_of_points[(i + 1) % len(list_of_points)][1],
                    int(2 * Display.display_ratio.x), 0, 255, 0, 255
                )

    @staticmethod
    def generate_polygon(num_sides: int,
                         radius: Union[float, int] = 1,
                         options: Optional[Dict] = None) -> Union[List[Vector], Polygon]:
        """
        Generates the vertices of a regular polygon with a specified number of sides and a radius.
        You can use this as the `verts` option in the Polygon constructor if you wish to generate a regular polygon.

        Args:
            num_sides (int): The number of sides of the polygon.
            radius (Union[float, int]): The radius of the polygon. Defaults to 1.
            option: A Polygon config. If set, will return a Polygon object. Otherwise it will return
                a list of vertices. Defaults to the None.

        Raises:
            SideError: Raised when the number of sides is less than 3.

        Returns:
            The vertices of the polygon or the Polygon object (depending on whether options is set).
        """
        if num_sides < 3:
            raise SideError("Can't create a polygon with less than three sides")

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle) / 2
            verts.append(Vector(math.cos(angle) * radius, math.sin(angle) * radius))

        if isinstance(options, dict):
            return Polygon(options | {"verts": verts})
        else:
            return verts


class Rectangle(Hitbox):
    """
    A rectangle implementation of the Hitbox subclass.

    Attributes:
        width (int): The width of the rectangle
        height (int): The height of the rectangle
    """

    def __init__(self, options: dict):
        """
        Initializes a Rectangle.

        Args:
            options: A Rectangle config. Defaults to the :ref:`Rectangle defaults <rectangledef>`.
        """
        super().__init__(options)
        params = Defaults.rectangle_defaults | options

        self.width: int = int(params["width"])
        self.height: int = int(params["height"])

    @property
    def top_left(self):
        """
        The top left corner of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / 2, self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @top_left.setter
    def top_left(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / 2, self.height / 2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom_left(self):
        """
        The bottom left corner of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / 2, self.height / -2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom_left.setter
    def bottom_left(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / 2, self.height / -2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def top_right(self):
        """
        The top right corner of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / -2, self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @top_right.setter
    def top_right(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / -2, self.height / 2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom_right(self):
        """
        The bottom right corner of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos - Vector(self.width / -2, self.height / -2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom_right.setter
    def bottom_right(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new + Vector(self.width / -2, self.height / -2)
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def bottom(self):
        """
        The bottom side of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return self.pos.y - self.height / -2
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom.setter
    def bottom(self, new: float):
        if self.gameobj:
            self.gameobj.pos.y += new + self.height / -2
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    def vertices(self) -> List[Vector]:
        """
        Generates a list of the rectangle's vertices with no transformations applied.

        Returns:
            List[Vector]: The list of vertices
        """
        x, y = self.width / 2, self.height / 2
        return [Vector(-x, -y), Vector(x, -y), Vector(x, y), Vector(-x, y)]

    def translated_verts(self) -> List[Vector]:
        """
        Offsets each vertex with the Polygon's offset.

        Returns:
            List[Vector]: The list of vertices
        """
        return [v * self.scale + self.offset for v in self.vertices()]

    def transformed_verts(self) -> List[Vector]:
        """
        Generates a list of the rectangle's vertices, scaled and rotated.

        Returns:
            List[Vector]: The list of vertices
        """
        return [v.rotate(self.gameobj.rotation) for v in self.translated_verts()]

    def real_verts(self) -> List[Vector]:
        """
        Generates a list of the rectangle's vertices, relative to its position.

        Returns:
            List[Vector]: The list of vertices
        """
        return [self.gameobj.pos + v for v in self.transformed_verts()]

    def draw(self, camera: Camera):
        list_of_points: List[tuple] = [camera.transform(v).tuple_int() for v in self.real_verts()]

        x_coords, y_coords = zip(*list_of_points)

        vx = (c_int16 * 4)(*x_coords)
        vy = (c_int16 * 4)(*y_coords)

        if self.color is not None:
            sdl2.sdlgfx.filledPolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                4,
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
            sdl2.sdlgfx.aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                4,
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )

        if self.debug or Game.debug:
            for i in range(4):
                sdl2.sdlgfx.thickLineRGBA(
                    Display.renderer.sdlrenderer, list_of_points[i][0],
                    list_of_points[i][1], list_of_points[(i + 1) % 4][0], list_of_points[(i + 1) % 4][1],
                    int(2 * Display.display_ratio.x), 0, 255, 0, 255
                )

    def clone(self) -> Rectangle:
        return Rectangle(
            {
                "width": self.width,
                "height": self.height,
                "debug": self.debug,
                "trigger": self.trigger,
                "scale": self.scale,
                "on_collide": self.on_collide,
                "color": self.color,
                "tag": self.tag,
                "offset": self.offset,
            }
        )


class Circle(Hitbox):
    """
    A circle Hitbox subclass defined by a position, radius, and scale.

    Attributes:
        radius (int): The radius of the circle.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Circle.

        Args:
            options: A Circle config. Defaults to the :ref:`Circle defaults <circledef>`.
        """
        super().__init__(options)
        params = Defaults.circle_defaults | options
        self.radius = params["radius"]

    def transformed_radius(self) -> int:
        """Gets the true radius of the circle"""
        return self.radius * self.scale

    def draw(self, camera: Camera):
        relative_pos = camera.transform(self.pos)
        scaled_rad = camera.scale(self.radius)

        if self.color is not None:
            sdl2.sdlgfx.filledCircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.a,
            )

        if self.debug or Game.debug:
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(relative_pos.x),
                int(relative_pos.y),
                int(scaled_rad),
                0,
                255,
                0,
                255,
            )

    def clone(self) -> Circle:
        return Circle(
            {
                "debug": self.debug,
                "trigger": self.trigger,
                "scale": self.scale,
                "on_collide": self.on_collide,
                "color": self.color,
                "tag": self.tag,
                "offset": self.offset,
                "radius": self.radius,
            }
        )
