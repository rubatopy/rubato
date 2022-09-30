"""Primitive shapes integrated into the physics engine."""
from __future__ import annotations
from typing import Callable

from .. import Component
from .... import Vector, Color, Game, Draw, Math, Camera, Input, Surface


class Hitbox(Component):
    """
    A hitbox superclass. Do not use this class to attach hitboxes to your game objects.
    Instead, use Polygon or Circle, which inherit Hitbox properties.

    Args:
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to (1, 1).
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to (0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
        hidden: Whether the hitbox is hidden. Defaults to False.
    """

    def __init__(
        self,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: Vector | tuple[float, float] = (1, 1),
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index, hidden=hidden)
        self.debug: bool = debug
        """Whether to draw a green outline around the hitbox or not."""
        self.trigger: bool = trigger
        """Whether this hitbox is just a trigger or not."""
        self.scale: Vector = Vector.create(scale)
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
        self.color: Color | None = color
        """The color of the hitbox."""
        self._image: Surface = Surface()
        self._debug_image: Surface = Surface()
        self.uptodate: bool = False
        """Whether the hitbox image is up to date or not."""
        self._old_rot_offset: float = self.rot_offset
        self._old_offset: Vector = self.offset.clone()
        self._old_scale: Vector = self.scale
        self._old_color: Color | None = self.color.clone() if self.color is not None else None

    def regen(self):
        """
        Regenerates internal hitbox information.
        """
        return

    def contains_pt(self, pt: Vector | tuple[float, float]):  # pylint: disable=unused-argument
        """
        Checks if a point is inside the Hitbox.

        Args:
            pt: The point to check, in game-world coordinates.

        Returns:
            Whether the point is inside the Hitbox.
        """
        return False

    def redraw(self):
        """
        Regenerates the image of the hitbox.
        """
        self._image.clear()
        self._debug_image.clear()

    def get_aabb(self) -> tuple[Vector, Vector]:
        """
        Gets top left and bottom right corners of the axis-aligned bounding box of the hitbox in world coordinates.

        Returns:
            tuple[Vector, Vector]:
                The top left and bottom right corners of the bounding box as Vectors as a tuple.
                (top left, bottom right)
        """
        true_pos = self.true_pos()
        return true_pos, true_pos

    def update(self):
        reset = False
        if self.scale != self._old_scale:
            reset = True
            self.uptodate = False

        if not self.uptodate or self.rot_offset != self._old_rot_offset or self.offset != self._old_offset:
            self.regen()
            self._old_rot_offset = self.rot_offset
            self._old_offset = self.offset.clone()

        if not self.uptodate or self.color != self._old_color:
            self.redraw()
            self._old_color = self.color.clone() if self.color is not None else None

        if not self.uptodate:
            self.uptodate = True

        if reset:
            self._old_scale = self.scale

    def draw(self, camera: Camera):
        if self.color:
            self._image.rotation = self.true_rotation()

            Draw.queue_surface(self._image, self.true_pos(), self.true_z(), camera)

        if self.debug or Game.debug:
            self._debug_image.rotation = self.true_rotation()

            Draw.queue_surface(self._debug_image, self.true_pos(), camera=camera)


class Polygon(Hitbox):
    """
    A Polygonal Hitbox component.

    Danger:
        If creating vertices by hand, make sure you generate them in a CLOCKWISE direction.
        Otherwise, polygons may not behave or draw properly.
        We recommend using Vector.poly() to generate the vertex list for regular polygons.

    Warning:
        rubato does not currently support concave polygons.
        Creating concave polygons will result in undesired behavior.

    Args:
        verts: The vertices of the polygon. Defaults to [].
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to (1, 1).
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to (0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
        hidden: Whether the hitbox is hidden. Defaults to False.
    """

    def __init__(
        self,
        verts: list[Vector] | list[tuple[float, float]] = [],
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: Vector | tuple[float, float] = (1, 1),
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
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
            z_index=z_index,
            hidden=hidden,
        )
        self._verts: list[Vector] = [Vector.create(v) for v in verts]

        self.regen()

    @property
    def verts(self) -> list[Vector]:
        """A list of the vertices in the Polygon."""
        return self._verts

    @verts.setter
    def verts(self, new: list[Vector]):
        self._verts = new
        self.uptodate = False

    @property
    def radius(self) -> float:
        """The radius of the Polygon. (get-only)"""
        verts = self.offset_verts()
        max_dist = -Math.INF
        for vert in verts:
            dist = vert.dist_to(self.offset)
            if dist > max_dist:
                max_dist = dist
        return round(max_dist, 10)

    def get_aabb(self) -> tuple[Vector, Vector]:
        verts = self.true_verts()
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

    def offset_verts(self) -> list[Vector]:
        """The list of polygon vertices offset by the Polygon's offsets."""
        return self._offset_verts

    def true_verts(self) -> list[Vector]:
        """
        Returns a list of the Polygon's vertices in world coordinates. Accounts for gameobject position and rotation.
        """
        return [v.rotate(self.gameobj.rotation) + self.gameobj.pos for v in self.offset_verts()]

    def regen(self):
        self._offset_verts = [(vert * self.scale).rotate(self.rot_offset) + self.offset for vert in self.verts]

    def redraw(self):
        super().redraw()

        w = round(self.radius * self.scale.x * 2)
        h = round(self.radius * self.scale.y * 2)
        if w != self._image.width or h != self._image.height:
            self._image = Surface(w, h)
            self._debug_image = Surface(w, h)

        verts = [v + Vector(w // 2, h // 2) for v in self.verts]

        if self.color is not None:
            self._image.draw_poly(verts, fill=self.color, aa=True)
        self._debug_image.draw_poly(verts, Color.debug, 2)

    def contains_pt(self, pt: Vector | tuple[float, float]) -> bool:
        return Input.pt_in_poly(pt, self.true_verts())

    def clone(self) -> Polygon:
        """Clones the Polygon"""
        return Polygon(
            verts=[v.clone() for v in self.verts],
            color=self.color.clone() if self.color is not None else None,
            tag=self.tag,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )


class Rectangle(Hitbox):
    """
    A Rectangular Hitbox component.

    Args:
        width: The width of the rectangle. Defaults to 0.
        height: The height of the rectangle. Defaults to 0.
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Defaults to (1, 1).
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to (0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
        hidden: Whether the hitbox is hidden. Defaults to False.
    """

    def __init__(
        self,
        width: int | float = 0,
        height: int | float = 0,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: Vector | tuple[float, float] = (1, 1),
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False
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
            z_index=z_index,
            hidden=hidden,
        )
        self._width: int | float = width
        self._height: int | float = height
        self._verts: list[Vector] = []

        self.regen()

    @property
    def width(self) -> int | float:
        """The width of the Rectangle."""
        return self._width

    @width.setter
    def width(self, value: int | float):
        self._width = value
        self.uptodate = False

    @property
    def height(self) -> int | float:
        """The height of the Rectangle."""
        return self._height

    @height.setter
    def height(self, value: int | float):
        self._height = value
        self.uptodate = False

    @property
    def verts(self) -> list[Vector]:
        """The list of Rectangle vertices. (get-only)"""
        return self._verts

    @property
    def radius(self) -> float:
        """The radius of the Rectangle. (get-only)"""
        verts = self.offset_verts()
        max_dist = -Math.INF
        for vert in verts:
            dist = vert.dist_to(self.offset)
            if dist > max_dist:
                max_dist = dist
        return round(max_dist, 10)

    @property
    def top_left(self):
        """
        The top left corner of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[0]

    @top_left.setter
    def top_left(self, new: Vector):
        self.gameobj.pos += new - self.get_aabb()[0]

    @property
    def bottom_left(self):
        """
        The bottom left corner of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        aabb = self.get_aabb()
        return Vector(aabb[0].x, aabb[1].y)

    @bottom_left.setter
    def bottom_left(self, new: Vector):
        aabb = self.get_aabb()
        self.gameobj.pos += new - Vector(aabb[0].x, aabb[1].y)

    @property
    def top_right(self):
        """
        The top right corner of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        aabb = self.get_aabb()
        return Vector(aabb[1].x, aabb[0].y)

    @top_right.setter
    def top_right(self, new: Vector):
        aabb = self.get_aabb()
        self.gameobj.pos += new - Vector(aabb[1].x, aabb[0].y)

    @property
    def bottom_right(self):
        """
        The bottom right corner of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[1]

    @bottom_right.setter
    def bottom_right(self, new: Vector):
        self.gameobj.pos += new - self.get_aabb()[1]

    @property
    def top(self):
        """
        The y value of the top side of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[0].y

    @top.setter
    def top(self, new: float):
        self.gameobj.pos.y += new - self.get_aabb()[0].y

    @property
    def left(self):
        """
        The x value of the left side of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[0].x

    @left.setter
    def left(self, new: float):
        self.gameobj.pos.x += new - self.get_aabb()[0].x

    @property
    def bottom(self):
        """
        The y value of the bottom side of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[1].y

    @bottom.setter
    def bottom(self, new: float):
        self.gameobj.pos.y += new - self.get_aabb()[1].y

    @property
    def right(self):
        """
        The x value of the right side of the AABB surrounding the rectangle.
        Setting to this value changes the gameobject's position, not the hitbox offset.
        """
        return self.get_aabb()[1].x

    @right.setter
    def right(self, new: float):
        self.gameobj.pos.x += new - self.get_aabb()[1].x

    def get_aabb(self) -> tuple[Vector, Vector]:
        verts = self.true_verts()
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

    def offset_verts(self) -> list[Vector]:
        """The list of rectangle vertices offset by the Rectangles's offsets."""
        return self._offset_verts

    def true_verts(self) -> list[Vector]:
        """
        Returns a list of the Rectangle's vertices in world coordinates. Accounts for gameobject position and rotation.
        """
        return [v.rotate(self.gameobj.rotation) + self.gameobj.pos for v in self.offset_verts()]

    def regen(self):
        w = self.width / 2
        h = self.height / 2
        self._verts = [Vector(-w, -h), Vector(w, -h), Vector(w, h), Vector(-w, h)]
        self._offset_verts = [(vert * self.scale).rotate(self.rot_offset) + self.offset for vert in self._verts]

    def redraw(self):
        super().redraw()

        w = round(self.width * self.scale.x)
        h = round(self.height * self.scale.y)
        if w != self._image.width or h != self._image.height:
            self._image = Surface(w, h)
            self._debug_image = Surface(w, h)

        if self.color is not None:
            self._image.fill(self.color)
        self._debug_image.draw_rect((0, 0), (w, h), Color.debug, 2)

    def contains_pt(self, pt: Vector | tuple[float, float]) -> bool:
        return Input.pt_in_poly(pt, self.true_verts())

    def clone(self) -> Rectangle:
        return Rectangle(
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            color=self.color.clone() if self.color is not None else None,
            tag=self.tag,
            width=self.width,
            height=self.height,
            z_index=self.z_index,
        )


class Circle(Hitbox):
    """
    A Circular Hitbox component.

    Args:
        radius: The radius of the circle. Defaults to 0.
        color: The color of the hitbox. Set to None to not show the hitbox. Defaults to None.
        tag: A string to tag the hitbox. Defaults to "".
        debug: Whether to draw the hitbox. Defaults to False.
        trigger: Whether the hitbox is a trigger. Defaults to False.
        scale: The scale of the hitbox. Note that only the largest value will determine the scale. Defaults to (1, 1).
        on_collide: A function to call when the hitbox collides with another hitbox. Defaults to lambda manifold: None.
        on_exit: A function to call when the hitbox exits another hitbox. Defaults to lambda manifold: None.
        offset: The offset of the hitbox from the gameobject. Defaults to (0, 0).
        rot_offset: The rotation offset of the hitbox. Defaults to 0.
        z_index: The z-index of the hitbox. Defaults to 0.
        hidden: Whether the hitbox is hidden. Defaults to False.
    """

    def __init__(
        self,
        radius: int | float = 0,
        color: Color | None = None,
        tag: str = "",
        debug: bool = False,
        trigger: bool = False,
        scale: Vector | tuple[float, float] = (1, 1),
        on_collide: Callable | None = None,
        on_exit: Callable | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
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
            z_index=z_index,
            hidden=hidden,
        )
        self._radius = radius

    @property
    def radius(self) -> int | float:
        """The radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, value: int | float):
        self._radius = value
        self.uptodate = False

    @property
    def center(self) -> Vector:
        """The center of the circle. Equivalent to true_pos. Setting to this will change the Gameobject position."""
        return self.true_pos()

    def get_aabb(self) -> tuple[Vector, Vector]:
        offset = self.true_radius()
        true_pos = self.true_pos()
        return true_pos - offset, true_pos + offset

    def true_radius(self) -> int | float:
        """Gets the true radius of the circle"""
        return self.radius * self.scale.max()

    def redraw(self):
        super().redraw()

        int_r = round(self.radius * self.scale.max())
        center = (int_r, int_r)
        size = int_r * 2 + 1

        if self._image.width != size:
            self._image = Surface(size, size)
            self._debug_image = Surface(size, size)

        if self.color is not None:
            self._image.draw_circle(center, int_r, fill=self.color, aa=True)
        self._debug_image.draw_circle(center, int_r, Color.debug, 2)

    def contains_pt(self, pt: Vector | tuple[float, float]) -> bool:
        r = self.true_radius()
        return (pt - self.true_pos()).mag_sq <= r * r

    def clone(self) -> Circle:
        return Circle(
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            debug=self.debug,
            trigger=self.trigger,
            scale=self.scale,
            on_collide=self.on_collide,
            on_exit=self.on_exit,
            color=self.color.clone() if self.color is not None else None,
            tag=self.tag,
            radius=self.radius,
            z_index=self.z_index,
        )
