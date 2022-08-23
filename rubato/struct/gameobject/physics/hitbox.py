"""Various hitbox components that enable collisions"""
from __future__ import annotations
from typing import Callable

from .. import Component
from ... import Surface
from .... import Vector, Color, Game, Draw, Math, Camera, Input


class Hitbox(Component):
    """
    A hitbox superclass. Do not use this class to attach hitboxes to your game objects.
    Instead, use Polygon or Circle, which inherit Hitbox properties.

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
        self._scale: int | float = scale
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
        self._image: Surface = Surface()
        self._debug_image: Surface = Surface()
        self.uptodate: bool = False
        """Whether the hitbox image is up to date or not."""

    @property
    def scale(self):
        """The scale of the hitbox."""
        return self._scale

    @scale.setter
    def scale(self, value: int | float):
        self._scale = value
        self.uptodate = False

    @property
    def color(self):
        """The color of the hitbox."""
        return self._color

    @color.setter
    def color(self, value: Color):
        self._color = value
        self.uptodate = False

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
            The top left and bottom right corners of the bounding box as Vectors in a list. [top left, bottom right]
        """
        return self.gameobj.pos, self.gameobj.pos

    def draw(self, camera: Camera):
        if self.hidden:
            return

        if not self.uptodate:
            self.redraw()
            self.uptodate = True

        if self.color:
            self._image.rotation = self.true_rotation()

            Draw.queue_surf(self._image, self.true_pos(), self.true_z(), camera)

        if self.debug or Game.debug:
            self._debug_image.rotation = self.true_rotation()

            Draw.queue_surf(self._debug_image, self.true_pos(), camera=camera)


class Polygon(Hitbox):
    """
    A polygon Hitbox implementation. Supports an arbitrary number of custom vertices, as long as the polygon is convex.

    Danger:
        If creating vertices by hand, make sure you generate them in a CLOCKWISE direction.
        Otherwise, polygons may not behave or draw properly.
        We recommend using Vector.poly() to generate regular vertices for regular polygons.

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
        """The radius of the Polygon"""
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
        self.regen()
        print("ran")

        r = int(self.radius * self.scale * 2)
        if r != self._image.surf.w:
            self._image = Surface(r, r)
            self._debug_image = Surface(r, r)

        verts = [v + r // 2 for v in self.verts]

        if self.color is not None:
            self._image.draw_poly(verts, border=self.color, fill=self.color, aa=True)
        self._debug_image.draw_poly(verts, Color.debug, 2)

    def contains_pt(self, pt: Vector) -> bool:
        """
        Checks if a point is inside the Polygon.

        Args:
            pt (Vector): The point to check, in game-world coordinates..

        Returns:
            bool: Whether the point is inside the Polygon.
        """
        return Input.pt_in_poly(pt, self.true_verts())

    def clone(self) -> Polygon:
        """Clones the Polygon"""
        return Polygon(
            verts=self.verts,
            color=self.color.clone(),
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
        return self.radius * self.scale

    def redraw(self):
        super().redraw()

        int_r = int(self.radius * self.scale)
        center = Vector(int_r, int_r)
        size = int_r * 2 + 1

        if self._image.surf.w != size:
            self._image = Surface(size, size)
            self._debug_image = Surface(size, size)

        if self.color is not None:
            self._image.draw_circle(center, int_r, border=self.color, fill=self.color, aa=True)
        self._debug_image.draw_circle(center, int_r, Color.debug, 2)

    def contains_pt(self, pt: Vector) -> bool:
        """
        Checks if a point is inside the Circle.

        Args:
            pt (Vector): The point to check, in game-world coordinates..

        Returns:
            bool: Whether the point is inside the Circle.
        """
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
            color=self.color.clone(),
            tag=self.tag,
            radius=self.radius,
            z_index=self.z_index,
        )
