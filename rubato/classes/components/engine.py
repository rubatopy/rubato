"""Handles collision manifold generation for complex geometries."""
from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional

from . import RigidBody, Circle
from ... import Math, Vector

if TYPE_CHECKING:
    from . import Hitbox, Polygon


class Engine:
    """
    Rubato's physics engine.
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

        sh_a: Hitbox = col.shape_a
        sh_b: Hitbox = col.shape_b

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

        # find inverse moments
        inv_moment_a: float = 0 if a_none else rb_a.inv_moment
        inv_moment_b: float = 0 if b_none else rb_b.inv_moment

        # handle infinite moment cases
        if inv_moment_a == inv_moment_b == 0:
            if a_none:
                inv_moment_b = 1
            elif b_none:
                inv_moment_a = 1
            else:
                inv_moment_a, inv_moment_b = 1, 1

        inv_contacts = 1 / len(col.contacts)

        col.normal *= -1
        if len(col.contacts) > 1:
            print(col.contacts[0], col.contacts[1])

        # RESOLUTION STEP
        for contact in col.contacts:
            ra = contact - sh_a.pos
            rb = contact - sh_b.pos

            rv = (0 if b_none else rb_b.velocity + rb.perpendicular(rb_b.ang_vel)
                 ) - (0 if a_none is None else rb_a.velocity + ra.perpendicular(rb_a.ang_vel))

            contact_vel = rv.dot(col.normal)

            ra_cn = ra.cross(col.normal)
            rb_cn = rb.cross(col.normal)

            inv_inert = 1 / (inv_mass_a + inv_mass_b + (ra_cn * ra_cn) * inv_moment_a + (rb_cn * rb_cn) * inv_moment_b)

            j = -(1 + e) * contact_vel * inv_inert * inv_contacts

            impulse = col.normal * j

            t = rv - col.normal * rv.dot(col.normal)
            t.unit(t)

            jt = -rv.dot(t) * inv_inert * inv_contacts

            if abs(jt) < j * mu:
                t_impulse = t * jt
            else:
                t_impulse = -mu * t * j

            if not (a_none or rb_a.static):
                rb_a.velocity -= impulse * inv_mass_a
                rb_a.ang_vel += inv_moment_a * ra.cross(impulse)

                rb_a.velocity -= t_impulse * inv_mass_a
                rb_a.ang_vel += inv_moment_a * ra.cross(t_impulse)

            if not (b_none or rb_b.static):
                rb_b.velocity += impulse * inv_mass_b
                rb_b.ang_vel -= inv_moment_b * rb.cross(impulse)

                rb_b.velocity += t_impulse * inv_mass_b
                rb_b.ang_vel -= inv_moment_b * rb.cross(t_impulse)

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

        dist = dist**.5

        if dist == 0:
            pen = circle_a.radius
            norm = Vector(1, 0)
            contacts = [circle_a.pos]
        else:
            pen = t_rad - dist
            norm = Vector(d_x / dist, d_y / dist)
            contacts = [circle_a.pos - norm * circle_a.radius]

        return Manifold(circle_a, circle_b, pen, norm, contacts)

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
            return Manifold(circle, polygon, circle.radius, norm, [circle.pos - norm * circle.radius])

        v1, v2 = verts[face_normal], verts[(face_normal + 1) % len(verts)]

        dot_1 = (center - v1).dot(v2 - v1)
        dot_2 = (center - v2).dot(v1 - v2)
        pen = circle.radius - separation

        if dot_1 <= 0:
            if (center - v1).mag_sq > circle.radius * circle.radius:
                return

            return Manifold(
                circle, polygon, pen, (center - v1).rotate(polygon.gameobj.rotation).unit(),
                [v1.rotate(polygon.gameobj.rotation) + polygon.pos]
            )
        elif dot_2 <= 0:
            if (center - v2).mag_sq > circle.radius * circle.radius:
                return

            return Manifold(
                circle, polygon, pen, (center - v2).rotate(polygon.gameobj.rotation).unit(),
                [v2.rotate(polygon.gameobj.rotation) + polygon.pos]
            )
        else:
            norm = Engine.get_normal(verts, face_normal)
            if norm.dot(center - v1) > circle.radius:
                return
            norm = norm.rotate(polygon.gameobj.rotation)

            return Manifold(circle, polygon, pen, norm, [circle.pos - norm * circle.radius])

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
            flip = False
            ref_ind = face_a
            ref_poly = shape_a
            inc_poly = shape_b
            true_pen = pen_a
        else:
            flip = True
            ref_ind = face_b
            ref_poly = shape_b
            inc_poly = shape_a
            true_pen = pen_b

        inc_face = Engine.incident_face(ref_poly, inc_poly, ref_ind)

        ref_verts = ref_poly.translated_verts()

        v1 = ref_verts[ref_ind].rotate(ref_poly.gameobj.rotation) + ref_poly.pos
        v2 = ref_verts[(ref_ind + 1) % len(ref_verts)].rotate(ref_poly.gameobj.rotation) + ref_poly.pos

        side_plane_normal = (v2 - v1).unit()

        neg_side = -side_plane_normal.dot(v1)
        pos_side = side_plane_normal.dot(v2)

        if Engine.clip(-side_plane_normal, neg_side, inc_face) < 2:
            return

        if Engine.clip(side_plane_normal, pos_side, inc_face) < 2:
            return

        man = Manifold(shape_a, shape_b)

        ref_face_normal = side_plane_normal.perpendicular()
        man.normal = ref_face_normal

        ref_c = ref_face_normal.dot(v1)

        sep_1 = ref_face_normal.dot(inc_face[0]) - ref_c
        sep_2 = ref_face_normal.dot(inc_face[1]) - ref_c

        if sep_1 <= 0:
            if sep_2 <= 0:
                man.contacts = inc_face
            else:
                man.contacts = [inc_face[0]]
        elif sep_2 <= 0:
            man.contacts = [inc_face[1]]
        else:
            return

        man.penetration = abs(true_pen)
        man.normal *= Math.sign(true_pen)

        if flip:
            man.normal *= -1

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
    def incident_face(ref_poly: Polygon, inc_poly: Polygon, ref_index: int) -> List[Vector]:
        """Finds the incident face of the incident polygon that clips into the reference polygon."""
        ref_verts = ref_poly.translated_verts()
        inc_verts = inc_poly.translated_verts()

        ref_norm = Engine.get_normal(ref_verts,
                                     ref_index).rotate(ref_poly.gameobj.rotation).rotate(-inc_poly.gameobj.rotation)

        inc_face, min_dot = 0, Math.INF
        for i in range(len(inc_verts)):
            dot = ref_norm.dot(Engine.get_normal(inc_verts, i))

            if dot < min_dot:
                min_dot = dot
                inc_face = i

        return [
            inc_verts[inc_face].rotate(inc_poly.gameobj.rotation) + inc_poly.pos,
            inc_verts[(inc_face + 1) % len(inc_verts)].rotate(inc_poly.gameobj.rotation) + inc_poly.pos
        ]

    @staticmethod
    def clip(n: Vector, c: float, face: List[Vector]) -> int:
        sp = 0
        out = [face[0].clone(), face[1].clone()]

        d1 = n.dot(face[0]) - c
        d2 = n.dot(face[1]) - c

        if d1 <= 0:
            out[sp] = face[0].clone()
            sp += 1
        if d2 <= 0:
            out[sp] = face[1].clone()
            sp += 1

        if d1 * d2 < 0:
            alpha = d1 / (d1 - d2)
            out[sp] = ((face[1] - face[0]) * alpha) + face[0]
            sp += 1

        face[0] = out[0]
        face[1] = out[1]

        return sp

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
    A class that represents information returned in a successful collision

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
        contacts: List[Vector] = []
    ):
        """
        Initializes a Collision Info manifold.
        This is used internally by :func:`Engine <rubato.classes.components.hitbox.Engine>`.
        """
        self.shape_a = shape_a
        self.shape_b = shape_b
        self.penetration = penetration
        self.normal = normal
        self.contacts = contacts

    def __str__(self) -> str:
        stringed = "[ "
        for c in self.contacts:
            stringed += str(c) + " "
        stringed += "]"
        return f"{self.penetration}, {self.normal}, {stringed}"

    def flip(self) -> Manifold:
        """
        Flips the reference shape in a collision manifold

        Returns:
            A reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.normal *= -1
        return self
