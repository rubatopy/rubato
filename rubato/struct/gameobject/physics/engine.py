"""Utility methods for colliding hitbox components."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import math

from . import RigidBody, Circle, Polygon, Rectangle
from .... import Math, Vector, InitError

if TYPE_CHECKING:
    from . import Hitbox


# THIS IS A STATIC CLASS
class Engine:
    """
    rubato's physics engine.
    Handles overlap tests for Hitboxes and resolves Rigidbody collisions.
    """

    def __init__(self) -> None:
        raise InitError(self)

    @staticmethod
    def resolve(col: Manifold):
        """
        Resolve the collision between two rigidbodies.

        Args:
            col: The collision information.
        """
        # INITIALIZATION STEP
        rb_a: RigidBody | None = col.shape_a.gameobj.get(RigidBody) if (RigidBody in col.shape_a.gameobj) else None
        rb_b: RigidBody | None = col.shape_b.gameobj.get(RigidBody) if (RigidBody in col.shape_b.gameobj) else None

        if not rb_a and not rb_b:
            return

        # calculate restitution
        e = max(rb_a.bounciness if rb_a else 0, rb_b.bounciness if rb_b else 0)

        # calculate friction coefficient
        if not rb_a:
            rv = rb_b.velocity  # type: ignore
            mu = rb_b.friction * rb_b.friction  # type: ignore
        elif not rb_b:
            rv = -rb_a.velocity
            mu = rb_a.friction * rb_a.friction
        else:
            rv = rb_b.velocity - rb_a.velocity
            mu = (rb_a.friction * rb_a.friction + rb_b.friction * rb_b.friction) / 2

        # find inverse masses
        inv_mass_a: float = rb_a.inv_mass if rb_a else 0
        inv_mass_b: float = rb_b.inv_mass if rb_b else 0

        # handle infinite mass cases
        if inv_mass_a == inv_mass_b == 0:
            if not rb_a:
                inv_mass_b = 1
            elif not rb_b:
                inv_mass_a = 1
            else:
                inv_mass_a, inv_mass_b = 1, 1

        col.normal *= -1

        # RESOLUTION STEP
        contact_vel = rv.dot(col.normal)

        inv_inert = 1 / (inv_mass_a + inv_mass_b)

        j = -(1 + e) * contact_vel * inv_inert

        impulse = col.normal * j

        t = rv - col.normal * rv.dot(col.normal)
        t.normalized(t)

        jt = -rv.dot(t) * inv_inert

        if abs(jt) < j * mu:
            t_impulse = t * jt
        else:
            t_impulse = -mu * t * j

        correction = max(col.penetration - 0.01, 0) * col.normal

        # Corrections
        if rb_a and not rb_a.static:
            rb_a.velocity -= impulse * inv_mass_a
            rb_a.velocity -= t_impulse * inv_mass_a
            col.shape_a.gameobj.pos -= correction * rb_a.pos_correction

        if rb_b and not rb_b.static:
            rb_b.velocity += impulse * inv_mass_b
            rb_b.velocity += t_impulse * inv_mass_b
            col.shape_b.gameobj.pos += correction * rb_b.pos_correction

    @staticmethod
    def overlap(hitbox_a: Hitbox, hitbox_b: Hitbox) -> Optional[Manifold]:
        """
        Determines if there is overlap between two hitboxes.
        Returns a Manifold manifold if a collision occurs but does not resolve.
        Note that this is only implemented for native rubato hitbox types (Rectangle, Polygon, Circle).

        Args:
            hitbox_a: The first hitbox to collide with.
            hitbox_b: The second hitbox to collide with.

        Returns:
            Returns a collision info object if overlap is detected or None if no collision is detected.
        """
        if not isinstance(hitbox_a,
                          Rectangle | Polygon | Circle) or not isinstance(hitbox_b, Rectangle | Polygon | Circle):
            raise TypeError("Engine.overlap() only supports Rectangle, Polygon, and Circle objects.")

        if isinstance(hitbox_a, Circle):
            if isinstance(hitbox_b, Circle):
                return Engine._circle_circle_test(hitbox_a, hitbox_b)

            return Engine._circle_polygon_test(hitbox_a, hitbox_b)

        if isinstance(hitbox_b, Circle):
            r = Engine._circle_polygon_test(hitbox_b, hitbox_a)
            return None if r is None else r._flip()

        return Engine._polygon_polygon_test(hitbox_a, hitbox_b)

    @staticmethod
    def collide(hitbox_a: Hitbox, hitbox_b: Hitbox) -> Optional[Manifold]:
        """
        Collides two hitboxes (if they overlap), calling their callbacks if they exist.
        Resolves the collision using Rigidbody impulse resolution if applicable.
        Note that this is only implemented for native rubato hitbox types (Rectangle, Polygon, Circle).

        Args:
            hitbox_a: The first hitbox to collide with.
            hitbox_b: The second hitbox to collide with.

        Returns:
            Returns a collision info object if a collision is detected or None if no collision is detected.
        """
        col = Engine.overlap(hitbox_a, hitbox_b)
        if col is None:
            if hitbox_b in hitbox_a.colliding:
                mani = Manifold(hitbox_a, hitbox_b)
                hitbox_a.colliding.remove(hitbox_b)
                hitbox_a.on_exit(mani)

            if hitbox_a in hitbox_b.colliding:
                mani = Manifold(hitbox_b, hitbox_a)
                hitbox_b.colliding.remove(hitbox_a)
                hitbox_b.on_exit(mani)

            return

        hitbox_a.colliding.add(hitbox_b)
        hitbox_b.colliding.add(hitbox_a)

        if not (hitbox_a.trigger or hitbox_b.trigger):
            Engine.resolve(col)

        hitbox_a.on_collide(col)
        hitbox_b.on_collide(col._flip())

    @staticmethod
    def _circle_circle_test(circle_a: Circle, circle_b: Circle) -> Optional[Manifold]:
        """Checks for overlap between two circles"""
        a_rad = circle_a.true_radius()
        b_rad = circle_b.true_radius()
        a_pos = circle_a.true_pos()
        b_pos = circle_b.true_pos()

        t_rad = a_rad + b_rad
        d_x, d_y = a_pos.x - b_pos.x, a_pos.y - b_pos.y
        dist = d_x * d_x + d_y * d_y

        if dist > t_rad * t_rad:
            return

        dist = math.sqrt(dist)

        if dist == 0:
            pen = a_rad
            norm = Vector(1, 0)
        else:
            pen = t_rad - dist
            norm = Vector(d_x / dist, d_y / dist)

        return Manifold(circle_a, circle_b, pen, norm)

    @staticmethod
    def _circle_polygon_test(circle: Circle, polygon: Polygon | Rectangle) -> Optional[Manifold]:
        """Checks for overlap between a circle and a polygon"""
        verts = polygon.offset_verts()
        circle_rad = circle.true_radius()
        circle_pos = circle.true_pos()
        poly_pos = polygon.true_pos()

        center = (circle_pos - poly_pos).rotate(-polygon.gameobj.rotation)

        separation = -Math.INF
        face_normal = 0

        for i in range(len(verts)):
            s = Engine._get_normal(verts, i).dot(center - verts[i])

            if s > circle_rad:
                return

            if s > separation:
                separation = s
                face_normal = i

        if separation <= 0:
            norm = Engine._get_normal(verts, face_normal).rotate(polygon.gameobj.rotation)
            return Manifold(circle, polygon, circle_rad, norm)

        v1, v2 = verts[face_normal], verts[(face_normal + 1) % len(verts)]

        dot_1 = (center - v1).dot(v2 - v1)
        dot_2 = (center - v2).dot(v1 - v2)
        pen = circle_rad - separation

        if dot_1 <= 0:
            offs = center - v1
            if offs.mag_sq > circle_rad * circle_rad:
                return

            return Manifold(circle, polygon, pen, offs.rotate(polygon.gameobj.rotation).normalized())
        elif dot_2 <= 0:
            offs = center - v2
            if offs.mag_sq > circle_rad * circle_rad:
                return

            return Manifold(circle, polygon, pen, offs.rotate(polygon.gameobj.rotation).normalized())
        else:
            norm = Engine._get_normal(verts, face_normal)
            if norm.dot(center - v1) > circle_rad:
                return

            return Manifold(circle, polygon, pen, norm.rotate(polygon.gameobj.rotation))

    @staticmethod
    def _polygon_polygon_test(shape_a: Polygon | Rectangle, shape_b: Polygon | Rectangle) -> Optional[Manifold]:
        """Checks for overlap between two polygons"""
        a_verts = shape_a.offset_verts()
        b_verts = shape_b.offset_verts()

        pen_a, face_a = Engine._axis_least_penetration(shape_a, shape_b, a_verts, b_verts)
        if pen_a is None or face_a is None:
            return

        pen_b, face_b = Engine._axis_least_penetration(shape_b, shape_a, b_verts, a_verts)
        if pen_b is None or face_b is None:
            return

        if pen_b < pen_a:
            man = Manifold(shape_a, shape_b, abs(pen_a))

            v1 = a_verts[face_a].rotate(shape_a.gameobj.rotation) + shape_a.gameobj.pos
            v2 = a_verts[(face_a + 1) % len(a_verts)].rotate(shape_a.gameobj.rotation) + shape_a.gameobj.pos

            side_plane_normal = (v2 - v1).normalized()
            man.normal = side_plane_normal.perpendicular() * Math.sign(pen_a)
        else:
            man = Manifold(shape_a, shape_b, abs(pen_b))

            v1 = b_verts[face_b].rotate(shape_b.gameobj.rotation) + shape_b.gameobj.pos
            v2 = b_verts[(face_b + 1) % len(b_verts)].rotate(shape_b.gameobj.rotation) + shape_b.gameobj.pos

            side_plane_normal = (v2 - v1).normalized()
            man.normal = side_plane_normal.perpendicular() * -Math.sign(pen_b)

        return man

    @staticmethod
    def _axis_least_penetration(
        a: Polygon | Rectangle, b: Polygon | Rectangle, a_verts: list[Vector], b_verts: list[Vector]
    ) -> tuple[float, int] | tuple[None, None]:
        """Finds the axis of least penetration between two possibly colliding polygons."""
        best_dist = -Math.INF
        best_ind = 0

        for i in range(len(a_verts)):
            n = Engine._get_normal(a_verts, i).rotate(a.gameobj.rotation).rotate(-b.gameobj.rotation)
            s = Engine._get_support(b_verts, -n)
            v = (a_verts[i].rotate(a.gameobj.rotation) + a.gameobj.pos - b.gameobj.pos).rotate(-b.gameobj.rotation)
            d = n.dot(s - v)

            if d > best_dist:
                best_dist = d
                best_ind = i
                if d >= 0:
                    return None, None

        return best_dist, best_ind

    @staticmethod
    def _get_support(verts: list[Vector], direction: Vector) -> Vector | None:
        """Gets the furthest support vertex in a given direction."""
        best_proj = -Math.INF
        best_vert = None

        for v in verts:
            projection = v.dot(direction)

            if projection > best_proj:
                best_vert = v
                best_proj = projection

        return best_vert

    @staticmethod
    def _get_normal(verts: list[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""
        face = (verts[(index + 1) % len(verts)] - verts[index]).perpendicular()
        face.magnitude = 1
        return face


class Manifold:
    """
    A class that represents information returned in collision callbacks.

    Args:
        shape_a: The first shape involved in the collision (the reference shape).
        shape_b: The second shape involved in the collision (the incident shape).
        penetration: The amount of penetration between the two shapes.
        normal: The normal of the collision.
    """

    def __init__(
        self,
        shape_a: Hitbox,
        shape_b: Hitbox,
        penetration: float = 0,
        normal: Vector = Vector(),
    ):
        self.shape_a: Hitbox = shape_a
        """The reference shape."""
        self.shape_b: Hitbox = shape_b
        """The incident (colliding) shape."""
        self.penetration: float = penetration
        """The amount by which the colliders are intersecting."""
        self.normal: Vector = normal
        """The direction that would most quickly separate the two colliders."""

    def __repr__(self) -> str:
        return (
            f"Manifold(shape_a={self.shape_a}, shape_b={self.shape_b}, penetration={self.penetration}, "
            f"normal={self.normal})"
        )

    def _flip(self) -> Manifold:
        """
        Flips the reference shape in a collision manifold and inverts the normal vector.

        Returns:
            A reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.normal *= -1
        return self
