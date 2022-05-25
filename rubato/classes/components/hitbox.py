"""Various hitbox components that enable collisions"""
from __future__ import annotations
from typing import Callable, Dict, List, Optional, TYPE_CHECKING, Set
import math

from . import Component
from ... import Display, Vector, Color, Error, SideError, Game, Draw, Math

if TYPE_CHECKING:
    from .. import Camera


class Hitbox(Component):
    """
    A hitbox superclass. Do not use this class to attach hitboxes to your game objects.
    Instead, use Polygon, Rectangle, or Circle, which inherit Hitbox properties.

    Args:
        offset: The offset of the hitbox from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        debug: Whether or not to draw the hitbox. Defaults to False.
        trigger: Whether or not the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to 1.
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".

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

    def __init__(
        self,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        debug: bool = False,
        trigger: bool = False,
        scale: int = 1,
        on_collide: Callable = lambda manifold: None,
        on_exit: Callable = lambda manifold: None,
        color: Color | None = None,
        tag: str = "",
    ):
        super().__init__(offset=offset, rot_offset=rot_offset)
        self.debug: bool = debug
        self.trigger: bool = trigger
        self.scale: int = scale
        self.on_collide: Callable = on_collide
        self.on_exit: Callable = on_exit
        self.color: Color = color
        self.singular: bool = False
        self.tag: str = tag
        self.colliding: Set[Hitbox] = set()

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the hitbox's center"""
        return self.gameobj.pos + self.offset

    def get_aabb(self) -> List[Vector]:
        """
        Gets top left and bottom right corners of the axis-aligned bounding box of the hitbox in world coordinates.

        Returns:
            The top left and bottom right corners of the bounding box as Vectors in a list. [top left, bottom right]
        """
        return [self.gameobj.pos, self.gameobj.pos]

    def get_obb(self) -> List[Vector]:
        """
        Gets the top left and bottom right corners of the oriented bounding box in world coordinates.

        Returns:
            The top left and bottom right corners of the bounding box as Vectors in a list. [top left, bottom right]
        """
        return [self.gameobj.pos, self.gameobj.pos]


class Polygon(Hitbox):
    """
    A polygon Hitbox implementation. Supports an arbitrary number of custom vertices, as long as the polygon is convex.

    Danger:
        If generating vertices by hand, make sure you generate them in a counter-clockwise direction.
        Otherwise, polygons will neither behave nor draw properly.

    Warning:
        rubato does not currently support concave polygons explicitly.
        Creating concave polygons will result in undesired collision behavior.
        However, you can still use concave polygons in your projects:
        Simply break them up into multiple convex Polygon hitboxes and add them individually to a gameobject.

    Args:
        verts: The vertices of the polygon. Defaults to [].

    Attributes:
        verts (List[Vector]): A list of the vertices in the Polygon, in anticlockwise direction.
    """

    def __init__(
        self,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        debug: bool = False,
        trigger: bool = False,
        scale: int = 1,
        on_collide: Callable = lambda manifold: None,
        on_exit: Callable = lambda manifold: None,
        color: Color | None = None,
        tag: str = "",
        verts: List[Vector] = [],
    ):
        """
        Initializes a Polygon.

        Args:
            options: A Polygon config. Defaults to the :ref:`Polygon defaults <polygondef>`.
        """
        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag
        )
        self.verts: List[Vector] = verts

    @property
    def radius(self) -> float:
        """The radius of the Polygon"""
        verts = self.transformed_verts()
        max_dist = -Math.INF
        for vert in verts:
            if (dist := vert.distance_between(self.offset)) > max_dist:
                max_dist = dist
        return round(max_dist, 10)

    def clone(self) -> Polygon:
        """Clones the Polygon"""
        return Polygon(
            **{
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

    def get_aabb(self) -> List[Vector]:
        verts = self.real_verts()
        top, bottom, left, right = Math.INF, -Math.INF, Math.INF, -Math.INF

        for vert in verts:
            if vert.y > bottom:
                bottom = vert.y
            elif vert.y < top:
                top = vert.y
            if vert.x > right:
                right = vert.x
            elif vert.x < left:
                left = vert.x

        return [Vector(left, top), Vector(right, bottom)]

    def get_obb(self) -> List[Vector]:
        verts = self.translated_verts()
        top, bottom, left, right = Math.INF, -Math.INF, Math.INF, -Math.INF

        for vert in verts:
            if vert.y > bottom:
                bottom = vert.y
            elif vert.y < top:
                top = vert.y
            if vert.x > right:
                right = vert.x
            elif vert.x < left:
                left = vert.x

        return [
            Vector(left, top).rotate(self.gameobj.rotation) + self.gameobj.pos,
            Vector(right, bottom).rotate(self.gameobj.rotation) + self.gameobj.pos,
        ]

    def translated_verts(self) -> List[Vector]:
        """Offsets each vertex with the Polygon's offset"""
        return [v * self.scale + self.offset for v in self.verts]

    def transformed_verts(self) -> List[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return [v.rotate(self.gameobj.rotation) for v in self.translated_verts()]

    def real_verts(self) -> List[Vector]:
        """Returns the a list of vertices in world coordinates"""
        return [self.gameobj.pos + v for v in self.transformed_verts()]

    def __str__(self):
        return f"{[str(v) for v in self.verts]}, {self.pos}, " + f"{self.scale}, {self.gameobj.rotation}"

    def draw(self, camera: Camera):
        list_of_points: List[tuple] = [camera.transform(v).to_int() for v in self.real_verts()]

        if self.color:
            Draw.poly(list_of_points, self.color, fill=self.color)

        if self.debug or Game.debug:
            Draw.poly(list_of_points, Color(0, 255), int(2 * Display.display_ratio.x))

    @classmethod
    def generate_polygon(cls,
                         num_sides: int,
                         radius: float | int = 1,
                         options: Optional[Dict] = None) -> List[Vector] | Polygon:
        """
        Generates the vertices of a regular polygon with a specified number of sides and a radius.
        You can use this as the `verts` option in the Polygon constructor if you wish to generate a regular polygon.

        Args:
            num_sides: The number of sides of the polygon.
            radius: The radius of the polygon. Defaults to 1.
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
            return cls(options | {"verts": verts})
        else:
            return verts


class Rectangle(Hitbox):
    """
    A rectangle implementation of the Hitbox subclass.

    Args:
        width: The width of the rectangle. Defaults to 10.
        height: The height of the rectangle. Defaults to 10.

    Attributes:
        width (int): The width of the rectangle
        height (int): The height of the rectangle
    """

    def __init__(
        self,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        debug: bool = False,
        trigger: bool = False,
        scale: int = 1,
        on_collide: Callable = lambda manifold: None,
        on_exit: Callable = lambda manifold: None,
        color: Color | None = None,
        tag: str = "",
        width: int = 10,
        height: int = 10
    ):
        """
        Initializes a Rectangle.

        Args:
            options: A Rectangle config. Defaults to the :ref:`Rectangle defaults <rectangledef>`.
        """

        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag
        )
        self.width: int = int(width)
        self.height: int = int(height)

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
            return self.pos + Vector(self.width / 2, self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom_right.setter
    def bottom_right(self, new: Vector):
        if self.gameobj:
            self.gameobj.pos = new - Vector(self.width / 2, self.height / 2)
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
            return self.pos.y + self.height / 2
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom.setter
    def bottom(self, new: float):
        if self.gameobj:
            self.gameobj.pos.y += new - self.height / 2
            self.gameobj.pos = self.gameobj.pos.to_int()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def radius(self) -> float:
        """The radius of the rectangle."""
        return round(math.sqrt(self.width**2 + self.height**2) / 2, 10)

    def get_aabb(self) -> List[Vector]:
        verts = self.real_verts()
        top, bottom, left, right = Math.INF, -Math.INF, Math.INF, -Math.INF

        for vert in verts:
            if vert.y > bottom:
                bottom = vert.y
            elif vert.y < top:
                top = vert.y
            if vert.x > right:
                right = vert.x
            elif vert.x < left:
                left = vert.x

        return [Vector(left, top), Vector(right, bottom)]

    def get_obb(self) -> List[Vector]:
        dim = Vector(self.width / 2, self.height / 2)
        return [
            (self.offset - dim).rotate(self.gameobj.rotation) + self.gameobj.pos,
            (self.offset + dim).rotate(self.gameobj.rotation) + self.gameobj.pos,
        ]

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
        list_of_points: List[tuple] = [camera.transform(v).to_int() for v in self.real_verts()]

        if self.color:
            Draw.poly(list_of_points, self.color, fill=self.color)

        if self.debug or Game.debug:
            Draw.poly(list_of_points, Color(0, 255), int(2 * Display.display_ratio.x))

    def clone(self) -> Rectangle:
        return Rectangle(
            **{
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

    Args:
        radius: The radius of the circle. Defaults to 10.

    Attributes:
        radius (int): The radius of the circle.
    """

    def __init__(
        self,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        debug: bool = False,
        trigger: bool = False,
        scale: int = 1,
        on_collide: Callable = lambda manifold: None,
        on_exit: Callable = lambda manifold: None,
        color: Color | None = None,
        tag: str = "",
        radius: int = 10,
    ):
        """
        Initializes a Circle.

        Args:
            options: A Circle config. Defaults to the :ref:`Circle defaults <circledef>`.
        """
        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag
        )
        self.radius = radius

    def get_aabb(self) -> List[Vector]:
        offset = self.transformed_radius()
        return [
            self.pos - offset,
            self.pos + offset,
        ]

    def get_obb(self) -> List[Vector]:
        r = self.transformed_radius()
        offset = Vector(r, r).rotate(self.gameobj.rotation)
        return [
            self.gameobj.pos - offset,
            self.gameobj.pos + offset,
        ]

    def transformed_radius(self) -> int:
        """Gets the true radius of the circle"""
        return self.radius * self.scale

    def draw(self, camera: Camera):
        relative_pos = camera.transform(self.pos)
        scaled_rad = camera.scale(self.radius)

        if self.color is not None:
            Draw.circle(relative_pos, scaled_rad, self.color, fill=self.color)

        if self.debug or Game.debug:
            Draw.circle(relative_pos, scaled_rad, Color(0, 255), int(2 * Display.display_ratio.x))

    def clone(self) -> Circle:
        return Circle(
            **{
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
