"""Various hitbox components that enable collisions"""
from __future__ import annotations
from typing import Callable
import math

from .. import Component
from ... import Surface
from .... import Vector, Color, Error, SideError, Game, Draw, Math, Camera, Input


class Hitbox(Component):
    """
    A hitbox superclass. Do not use this class to attach hitboxes to your game objects.
    Instead, use Polygon, Rectangle, or Circle, which inherit Hitbox properties.

    Args:
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to 1.
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
    """

    def __init__(
        self,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: int | float = 1,
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self.debug: bool = debug
        """Whether to draw a green outline around the hitbox or not."""
        self.trigger: bool = trigger
        """Whether this hitbox is just a trigger or not."""
        self.scale: int | float = scale
        """The scale of the hitbox."""
        self.on_collide: Callable = on_collide if on_collide else lambda manifold: None
        """The on_collide function to call when a collision happens with this hitbox."""
        self.on_exit: Callable = on_exit if on_exit else lambda manifold: None
        """The on_exit function to call when a collision ends with this hitbox."""
        self.singular: bool = False
        """Whether this hitbox is singular or not."""
        self.tag: str = tag
        """The tag of the hitbox (can be used to identify hitboxes in collision callbacks)"""
        self.colliding: set[Hitbox] = set()
        """An unordered set of hitboxes that the Hitbox is currently colliding with."""
        self._color: Color = color
        self._image: Surface = Surface(scale=scale)
        self._debug_image: Surface = Surface(scale=scale)
        self.up_to_date: bool = False
        """Whether the hitbox image is up to date or not."""

    @property
    def color(self) -> Color:
        """The color to fill this hitbox with."""
        return self._color

    @color.setter
    def color(self, new: Color):
        self._color = new
        self.up_to_date = False

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the hitbox's center"""
        return self.gameobj.pos + self.offset

    def regenerate_image(self):
        """
        Regenerates the image of the hitbox.
        """
        self._image.clear()
        self._debug_image.clear()

    def get_aabb(self) -> tuple[Vector, Vector]:
        """
        Gets top left and bottom right corners of the axis-aligned bounding box of the hitbox in world coordinates.

        Returns:
            The top left and bottom right corners of the bounding box as Vectors in a list. [top left, bottom right]
        """
        return self.gameobj.pos, self.gameobj.pos

    def get_obb(self) -> tuple[Vector, Vector]:
        """
        Gets the top left and bottom right corners of the oriented bounding box in world coordinates.

        Returns:
            The top left and bottom right corners of the bounding box as Vectors in a list. [top left, bottom right]
        """
        return self.gameobj.pos, self.gameobj.pos

    def draw(self, camera: Camera):
        if self.hidden:
            return

        if not self.up_to_date:
            self.regenerate_image()
            self.up_to_date = True

        if self._color:
            self._image.scale = Vector(self.scale, self.scale)
            self._image.rotation = self.gameobj.rotation + self.rot_offset

            Draw.queue_surf(self._image, self.pos, self.true_z, camera)

        if self.debug or Game.debug:
            self._debug_image.scale = Vector(self.scale, self.scale)
            self._debug_image.rotation = self.gameobj.rotation + self.rot_offset

            Draw.queue_surf(self._debug_image, self.pos, camera=camera)


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
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to 1.
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
    """

    def __init__(
        self,
        verts: list[Vector] = [],
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: int | float = 1,
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag,
            z_index=z_index
        )
        self._verts: list[Vector] = verts
        self._image: Surface = Surface()
        self._debug_image: Surface = Surface()

    @property
    def verts(self) -> list[Vector]:
        """A list of the vertices in the Polygon, in anticlockwise direction."""
        return self._verts

    @verts.setter
    def verts(self, new: list[Vector]):
        self._verts = new
        self.up_to_date = False

    @property
    def radius(self) -> float:
        """The radius of the Polygon"""
        verts = self.transformed_verts()
        max_dist = -Math.INF
        for vert in verts:
            dist = vert.distance_between(self.offset)
            if (dist) > max_dist:
                max_dist = dist
        return round(max_dist, 10)

    def clone(self) -> Polygon:
        """Clones the Polygon"""
        return Polygon(
            verts=self.verts,
            color=self._color,
            tag=self.tag,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            offset=self.offset,
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )

    def get_aabb(self) -> tuple[Vector, Vector]:
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

        return Vector(left, top), Vector(right, bottom)

    def get_obb(self) -> tuple[Vector, Vector]:
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

        return (
            Vector(left, top).rotate(self.gameobj.rotation) + self.gameobj.pos,
            Vector(right, bottom).rotate(self.gameobj.rotation) + self.gameobj.pos
        )

    def translated_verts(self) -> list[Vector]:
        """Offsets each vertex with the Polygon's offset"""
        return [v * self.scale + self.offset for v in self.verts]

    def transformed_verts(self) -> list[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return [v.rotate(self.gameobj.rotation) for v in self.translated_verts()]

    def real_verts(self) -> list[Vector]:
        """Returns the a list of vertices in world coordinates"""
        return [self.gameobj.pos + v for v in self.transformed_verts()]

    def contains_pt(self, pt: Vector) -> bool:
        """
        Checks if a point is inside the Polygon.

        Args:
            pt (Vector): The point to check, in game-world coordinates..

        Returns:
            bool: Whether the point is inside the Polygon.
        """
        return Input.pt_in_poly(pt, self.real_verts())

    def __str__(self):
        return f"{[str(v) for v in self.verts]}, {self.pos}, " + f"{self.scale}, {self.gameobj.rotation}"

    def regenerate_image(self):
        super().regenerate_image()

        r = int(self.radius * 2)
        if r != self._image.surf.w:
            self._image = Surface(r, r)
            self._debug_image = Surface(r, r)

        verts = [v + self.radius for v in self.verts]

        if self.color is not None:
            self._image.draw_poly(verts, border=self.color, fill=self.color, aa=True)
        self._debug_image.draw_poly(verts, Color.debug, 2)

    @classmethod
    def generate_polygon(cls, num_sides: int, radius: float | int = 1) -> list[Vector]:
        """
        Generates the **vertices** of a regular polygon with a specified number of sides and a radius.
        You can use this as the `verts` option in the Polygon constructor if you wish to generate a regular polygon.

        Args:
            num_sides: The number of sides of the polygon.
            radius: The radius of the polygon. Defaults to 1.

        Raises:
            SideError: Raised when the number of sides is less than 3.

        Returns:
            The vertices of the polygon.
        """
        if num_sides < 3:
            raise SideError("Can't create a polygon with less than three sides")

        rotangle = 360 / num_sides
        return [Vector.from_radial(radius, i * rotangle) for i in range(num_sides)]


class Rectangle(Hitbox):
    """
    A rectangle implementation of the Hitbox subclass.

    Args:
        width: The width of the rectangle. Defaults to 10.
        height: The height of the rectangle. Defaults to 10.
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to 1.
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
    """

    def __init__(
        self,
        width: int | float = 10,
        height: int | float = 10,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: int | float = 1,
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag,
            z_index=z_index
        )
        self._width: int = int(width)
        self._height: int = int(height)
        self._image = Surface(self.width, self.height)
        self._debug_image = Surface(self.width, self.height)

    @property
    def width(self) -> int:
        """The width of the rectangle."""
        return self._width

    @width.setter
    def width(self, new: int):
        self._width = new
        self.up_to_date = False

    @property
    def height(self) -> int:
        """The width of the rectangle."""
        return self._height

    @height.setter
    def height(self, new: int):
        self._height = new
        self.up_to_date = False

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
            self.gameobj.pos = self.gameobj.pos.round()
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
            self.gameobj.pos = self.gameobj.pos.round()
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
            self.gameobj.pos = self.gameobj.pos.round()
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
            self.gameobj.pos = self.gameobj.pos.round()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def top(self):
        """
        The top side of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return math.floor(self.pos.y + self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @top.setter
    def top(self, new: float):
        if self.gameobj:
            self.gameobj.pos.y = new - self.height / 2
            self.gameobj.pos = self.gameobj.pos.round()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def left(self):
        """
        The bottom side of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return math.floor(self.pos.x - self.width / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @left.setter
    def left(self, new: float):
        if self.gameobj:
            self.gameobj.pos.x = new + self.width / 2
            self.gameobj.pos = self.gameobj.pos.round()
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
            return math.ceil(self.pos.y + self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @bottom.setter
    def bottom(self, new: float):
        if self.gameobj:
            self.gameobj.pos.y = new - self.height / 2
            self.gameobj.pos = self.gameobj.pos.round()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def right(self):
        """
        The right side of the rectangle.

        Note:
            This can only be accessed and set after the Rectangle has been
            added to a Game Object.
        """
        if self.gameobj:
            return math.ceil(self.pos.x + self.height / 2)
        else:
            raise Error("Tried to get rect property before game object assignment.")

    @right.setter
    def right(self, new: float):
        if self.gameobj:
            self.gameobj.pos.x = new - self.height / 2
            self.gameobj.pos = self.gameobj.pos.round()
        else:
            raise Error("Tried to set rect property before game object assignment.")

    @property
    def radius(self) -> float:
        """The radius of the rectangle."""
        return round(math.sqrt(self.width**2 + self.height**2) / 2, 10)

    def contains_pt(self, pt: Vector) -> bool:
        """
        Checks if a point is inside the Rectangle.

        Args:
            pt (Vector): The point to check, in game-world coordinates.

        Returns:
            bool: Whether the point is inside the Rectangle.
        """
        return Input.pt_in_poly(pt, self.real_verts())

    def get_aabb(self) -> tuple[Vector, Vector]:
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

        return Vector(left, top), Vector(right, bottom)

    def get_obb(self) -> tuple[Vector, Vector]:
        dim = Vector(self.width / 2, self.height / 2)
        return (
            (self.offset - dim).rotate(self.gameobj.rotation) + self.gameobj.pos,
            (self.offset + dim).rotate(self.gameobj.rotation) + self.gameobj.pos
        )

    def vertices(self) -> list[Vector]:
        """
        Generates a list of the rectangle's vertices with no transformations applied.

        Returns:
            list[Vector]: The list of vertices. Top left, top right, bottom right, bottom left.
        """
        x, y = self.width / 2, self.height / 2
        return [Vector(-x, -y), Vector(x, -y), Vector(x, y), Vector(-x, y)]

    def translated_verts(self) -> list[Vector]:
        """
        Offsets each vertex with the Polygon's offset. Top left, top right, bottom right, bottom left.

        Returns:
            list[Vector]: The list of vertices.
        """
        return [v * self.scale + self.offset for v in self.vertices()]

    def transformed_verts(self) -> list[Vector]:
        """
        Generates a list of the rectangle's vertices, scaled and rotated.

        Returns:
            list[Vector]: The list of vertices. Top left, top right, bottom right, bottom left.
        """
        return [v.rotate(self.gameobj.rotation) for v in self.translated_verts()]

    def real_verts(self) -> list[Vector]:
        """
        Generates a list of the rectangle's vertices, relative to its position.

        Returns:
            list[Vector]: The list of vertices. Top left, top right, bottom right, bottom left.
        """
        return [self.gameobj.pos + v for v in self.transformed_verts()]

    def regenerate_image(self):
        super().regenerate_image()

        if self.width != self._image.surf.w or self.height != self._image.surf.h:
            self._image = Surface(self.width, self.height)
            self._debug_image = Surface(self.width, self.height)

        if self.color is not None:
            self._image.draw_rect(Vector(0, 0), Vector(self.width, self.height), fill=self.color)

        self._debug_image.draw_rect(Vector(0, 0), Vector(self.width, self.height), Color.debug, 2)

    def clone(self) -> Rectangle:
        return Rectangle(
            offset=self.offset,
            rot_offset=self.rot_offset,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            color=self._color,
            tag=self.tag,
            width=self.width,
            height=self.height,
            z_index=self.z_index,
        )


class Circle(Hitbox):
    """
    A circle Hitbox subclass defined by a position, radius, and scale.

    Args:
        radius: The radius of the circle. Defaults to 10.
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to 1.
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.

    Note:
        If color is unassigned, the circle will not be drawn. And will act like a circular hitbox.
    """

    def __init__(
        self,
        radius: int | float = 10,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: int | float = 1,
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(
            offset=offset,
            rot_offset=rot_offset,
            debug=debug,
            trigger=trigger,
            scale=scale,
            on_collide=on_collide,
            on_exit=on_exit,
            color=color,
            tag=tag,
            z_index=z_index
        )
        self._radius = radius
        r = int(self.radius * 2)
        self._image = Surface(r, r)
        self._debug_image = Surface(r, r)

    @property
    def radius(self) -> int | float:
        """The radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, value: int | float):
        self._radius = value
        self.up_to_date = False

    @property
    def center(self) -> Vector:
        """The center of the circle. Equivalent to pos"""
        # this is required to make the center property setter work and not have two behaviours in different classes.
        return self.pos

    @center.setter
    def center(self, new: Vector):
        """Sets the center of the circle."""
        self.gameobj.pos = new

    def get_aabb(self) -> tuple[Vector, Vector]:
        offset = self.transformed_radius()
        return self.pos - offset, self.pos + offset

    def get_obb(self) -> tuple[Vector, Vector]:
        r = self.transformed_radius()
        offset = Vector(r, r).rotate(self.gameobj.rotation)
        return self.gameobj.pos - offset, self.gameobj.pos + offset

    def transformed_radius(self) -> int | float:
        """Gets the true radius of the circle"""
        return self.radius * self.scale

    def contains_pt(self, pt: Vector) -> bool:
        """
        Checks if a point is inside the Circle.

        Args:
            pt (Vector): The point to check, in game-world coordinates..

        Returns:
            bool: Whether the point is inside the Circle.
        """
        r = self.transformed_radius()
        return (pt - self.gameobj.pos).mag_sq <= r * r

    def regenerate_image(self):
        super().regenerate_image()

        r = int(self.radius * 2)
        if self._image.surf.w != r:
            self._image = Surface(r, r)
            self._debug_image = Surface(r, r)

        if self.color is not None:
            self._image.draw_circle(Vector(self.radius, self.radius), int(self.radius), fill=self.color)
        self._debug_image.draw_circle(Vector(self.radius, self.radius), int(self.radius), Color.debug, 2)

    def clone(self) -> Circle:
        return Circle(
            offset=self.offset,
            rot_offset=self.rot_offset,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            color=self._color,
            tag=self.tag,
            radius=self.radius,
            z_index=self.z_index,
        )
