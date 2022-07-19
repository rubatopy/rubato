"""Handles collision manifold generation for complex geometries."""
from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
import math

from . import RigidBody, Circle
from .... import Math, Vector

if TYPE_CHECKING:
    from . import Hitbox, Polygon


class Engine:
    """
    rubato's physics engine.
    Handles overlap tests for Hitboxes and resolves Rigidbody collisions.
    """

    @staticmethod
    def resolve(col: Manifold):
        """
        Resolve the collision between two rigidbodies.

        Args:
            col: The collision information.
        """
        # INITIALIZATION STEP

        rb_a: RigidBody = col.shape_a.gameobj.get(RigidBody)
        rb_b: RigidBody = col.shape_b.gameobj.get(RigidBody)

        a_none = rb_a is None
        b_none = rb_b is None

        if a_none and b_none:
            return

        # calculate restitution
        e = max(0 if a_none else rb_a.bounciness, 0 if b_none else rb_b.bounciness)

        # calculate friction coefficient
        if a_none:
            mu = rb_b.friction * rb_b.friction
        elif b_none:
            mu = rb_a.friction * rb_a.friction
        else:
            mu = (rb_a.friction * rb_a.friction + rb_b.friction * rb_b.friction) / 2

        # find inverse masses
        inv_mass_a: float = 0 if a_none else rb_a.inv_mass
        inv_mass_b: float = 0 if b_none else rb_b.inv_mass

        # handle infinite mass cases
        if inv_mass_a == inv_mass_b == 0:
            if a_none:
                inv_mass_b = 1
            elif b_none:
                inv_mass_a = 1
            else:
                inv_mass_a, inv_mass_b = 1, 1

        col.normal *= -1

        # RESOLUTION STEP
        rv = (0 if b_none else rb_b.velocity) - (0 if a_none else rb_a.velocity)

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

        # Velocity correction
        if not (a_none or rb_a.static):
            rb_a.velocity -= impulse * inv_mass_a
            rb_a.velocity -= t_impulse * inv_mass_a

        if not (b_none or rb_b.static):
            rb_b.velocity += impulse * inv_mass_b
            rb_b.velocity += t_impulse * inv_mass_b

        # Position correction
        correction = max(col.penetration - 0.01, 0) * col.normal

        if not (a_none or rb_a.static):
            rb_a.gameobj.pos -= correction * rb_a.pos_correction

        if not (b_none or rb_b.static):
            rb_b.gameobj.pos += correction * rb_b.pos_correction

    @staticmethod
    def overlap(hitbox_a: Hitbox, hitbox_b: Hitbox) -> Optional[Manifold]:
        """
        Determines if there is overlap between two hitboxes.
        Returns a Manifold manifold if a collision occurs but does not resolve.

        Args:
            hitbox_a: The first hitbox to collide with.
            hitbox_b: The second hitbox to collide with.

        Returns:
            Returns a collision info object if overlap is detected or None if no collision is detected.
        """
        if isinstance(hitbox_a, Circle):
            if isinstance(hitbox_b, Circle):
                return Engine.circle_circle_test(hitbox_a, hitbox_b)

            return Engine.circle_polygon_test(hitbox_a, hitbox_b)

        if isinstance(hitbox_b, Circle):
            r = Engine.circle_polygon_test(hitbox_b, hitbox_a)
            return None if r is None else r.flip()

        return Engine.polygon_polygon_test(hitbox_a, hitbox_b)

    @staticmethod
    def collide(hitbox_a: Hitbox, hitbox_b: Hitbox) -> Optional[Manifold]:
        """
        Collides two hitboxes (if they overlap), calling their callbacks if they exist.
        Resolves the collision using Rigidbody impulse resolution if applicable.

        Args:
            hitbox_a: The first hitbox to collide with.
            hitbox_b: The second hitbox to collide with.

        Returns:
            Returns a collision info object if a collision is detected or None if no collision is detected.
        """
        if (col := Engine.overlap(hitbox_a, hitbox_b)) is None:
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
        hitbox_b.on_collide(col.flip())

    @staticmethod
    def circle_circle_test(circle_a: Circle, circle_b: Circle) -> Optional[Manifold]:
        """Checks for overlap between two circles"""
        t_rad = circle_a.radius + circle_b.radius
        d_x, d_y = circle_a.pos.x - circle_b.pos.x, circle_a.pos.y - circle_b.pos.y
        dist = d_x * d_x + d_y * d_y

        if dist > t_rad * t_rad:
            return

        dist = math.sqrt(dist)

        if dist == 0:
            pen = circle_a.radius
            norm = Vector(1, 0)
        else:
            pen = t_rad - dist
            norm = Vector(d_x / dist, d_y / dist)

        return Manifold(circle_a, circle_b, pen, norm)

    @staticmethod
    def circle_polygon_test(circle: Circle, polygon: Polygon) -> Optional[Manifold]:
        """Checks for overlap between a circle and a polygon"""
        verts = polygon.translated_verts()
        center = (circle.pos - polygon.pos).rotate(-polygon.gameobj.rotation)

        separation = -Math.INF
        face_normal = 0

        for i in range(len(verts)):
            s = Engine.get_normal(verts, i).dot(center - verts[i])

            if s > circle.radius:
                return

            if s > separation:
                separation = s
                face_normal = i

        if separation <= 0:
            norm = Engine.get_normal(verts, face_normal).rotate(polygon.gameobj.rotation)
            return Manifold(circle, polygon, circle.radius, norm)

        v1, v2 = verts[face_normal], verts[(face_normal + 1) % len(verts)]

        dot_1 = (center - v1).dot(v2 - v1)
        dot_2 = (center - v2).dot(v1 - v2)
        pen = circle.radius - separation

        if dot_1 <= 0:
            offs = center - v1
            if offs.mag_sq > circle.radius * circle.radius:
                return

            return Manifold(circle, polygon, pen, offs.rotate(polygon.gameobj.rotation).normalized())
        elif dot_2 <= 0:
            offs = center - v2
            if offs.mag_sq > circle.radius * circle.radius:
                return

            return Manifold(circle, polygon, pen, offs.rotate(polygon.gameobj.rotation).normalized())
        else:
            norm = Engine.get_normal(verts, face_normal)
            if norm.dot(center - v1) > circle.radius:
                return

            return Manifold(circle, polygon, pen, norm.rotate(polygon.gameobj.rotation))

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon, shape_b: Polygon) -> Optional[Manifold]:
        """Checks for overlap between two polygons"""
        pen_a, face_a = Engine.axis_least_penetration(shape_a, shape_b)
        if pen_a is None:
            return

        pen_b, face_b = Engine.axis_least_penetration(shape_b, shape_a)
        if pen_b is None:
            return

        if pen_b < pen_a:
            man = Manifold(shape_a, shape_b, abs(pen_a))

            ref_verts = shape_a.translated_verts()

            v1 = ref_verts[face_a].rotate(shape_a.gameobj.rotation) + shape_a.pos
            v2 = ref_verts[(face_a + 1) % len(ref_verts)].rotate(shape_a.gameobj.rotation) + shape_a.pos

            side_plane_normal = (v2 - v1).normalized()
            man.normal = side_plane_normal.perpendicular() * Math.sign(pen_a)
        else:
            man = Manifold(shape_a, shape_b, abs(pen_b))

            ref_verts = shape_b.translated_verts()

            v1 = ref_verts[face_b].rotate(shape_b.gameobj.rotation) + shape_b.pos
            v2 = ref_verts[(face_b + 1) % len(ref_verts)].rotate(shape_b.gameobj.rotation) + shape_b.pos

            side_plane_normal = (v2 - v1).normalized()
            man.normal = side_plane_normal.perpendicular() * -Math.sign(pen_b)

        return man

    @staticmethod
    def axis_least_penetration(a: Polygon, b: Polygon) -> float:
        """Finds the axis of least penetration between two possibly colliding polygons."""
        a_verts = a.translated_verts()
        b_verts = b.translated_verts()

        best_dist = -Math.INF
        best_ind = 0

        for i in range(len(a_verts)):
            n = Engine.get_normal(a_verts, i).rotate(a.gameobj.rotation).rotate(-b.gameobj.rotation)
            s = Engine.get_support(b_verts, -n)
            v = (a_verts[i].rotate(a.gameobj.rotation) + a.pos - b.pos).rotate(-b.gameobj.rotation)
            d = n.dot(s - v)

            if d > best_dist:
                best_dist = d
                best_ind = i
                if d >= 0:
                    return None, None

        return best_dist, best_ind

    @staticmethod
    def get_support(verts: List[Vector], direction: Vector) -> Vector:
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
    def get_normal(verts: List[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""
        face = (verts[(index + 1) % len(verts)] - verts[index]).perpendicular()
        face.magnitude = 1
        return face


class Manifold:
    """
    A class that represents information returned in a successful collision.

    Args:
        shape_a: The first shape involved in the collision.
        shape_b: The second shape involved in the collision.
        penetration: The amount of penetration between the two shapes.
        normal: The normal of the collision.

    Attributes:
        shape_a (Optional[Hitbox]): A reference to the first shape.
        shape_b (Optional[Hitbox]): A reference to the second shape.
        penetration (float): The amount by which the colliders are intersecting.
        normal (Vector): The direction that would most quickly separate the two colliders.
    """

    def __init__(
        self,
        shape_a: Optional[Hitbox],
        shape_b: Optional[Hitbox],
        penetration: float = 0,
        normal: Vector = Vector(),
    ):
        self.shape_a = shape_a
        self.shape_b = shape_b
        self.penetration = penetration
        self.normal = normal

    def __str__(self) -> str:
        return f"Manifold <{self.penetration}, {self.normal}>"

    def flip(self) -> Manifold:
        """
        Flips the reference shape in a collision manifold

        Returns:
            A reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.normal *= -1
        return self
