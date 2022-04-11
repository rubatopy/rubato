"""Handles collision manifold generation for complex geometries."""
from __future__ import annotations
from typing import List, Union, TYPE_CHECKING
from ... import Math, Vector

if TYPE_CHECKING:
    from . import Hitbox, Circle, Polygon


class Manifold:
    """
    A class that represents information returned in a successful collision

    Attributes:
        shape_a (Union[Hitbox, None]): A reference to the first shape.
        shape_b (Union[Hitbox, None]): A reference to the second shape.
        penetration (float): The amount by which the colliders are intersecting.
        normal (Vector): The direction that would most quickly separate the two colliders.
    """

    def __init__(
        self,
        shape_a: Union[Hitbox, None],
        shape_b: Union[Hitbox, None],
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
            Manifold: a reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.normal *= -1
        return self


class Engine:
    """
    A general class that does the collision detection math between different hitboxes.
    """

    @staticmethod
    def circle_circle_test(circle_a: Circle, circle_b: Circle) -> Union[Manifold, None]:
        """Checks for overlap between two circles"""
        t_rad = circle_a.radius + circle_b.radius
        d_x, d_y = circle_a.pos.x - circle_b.pos.x, circle_a.pos.y - circle_b.pos.y
        dist = d_x * d_x + d_y * d_y

        if dist > t_rad * t_rad:
            return None

        dist = dist**.5

        if dist == 0:
            pen = circle_a.radius
            norm = Vector(1, 0)
            contacts = [circle_a.pos]
        else:
            pen = t_rad - dist
            norm = Vector(d_x / dist, d_y / dist) * Math.sign(pen)
            contacts = [norm * circle_a.radius + circle_a.pos]

        return Manifold(circle_a, circle_b, abs(pen), norm, contacts)

    @staticmethod
    def circle_polygon_test(circle: Circle, polygon: Polygon) -> Union[Manifold, None]:
        """Checks for overlap between a circle and a polygon"""
        verts = polygon.translated_verts()
        center = (circle.pos - polygon.pos).rotate(-polygon.gameobj.rotation)

        separation = -Math.INF
        face_normal = 0

        for i in range(len(verts)):
            s = Engine.get_normal(verts, i).dot(center - verts[i])

            if s > circle.radius:
                return None

            if s > separation:
                separation = s
                face_normal = i

        if separation <= 0:
            norm = Engine.get_normal(verts, face_normal).rotate(polygon.gameobj.rotation)
            return Manifold(circle, polygon, circle.radius, norm, [-norm * circle.radius + circle.pos])

        v1, v2 = verts[face_normal], verts[(face_normal + 1) % len(verts)]

        dot_1 = (center - v1).dot(v2 - v1)
        dot_2 = (center - v2).dot(v1 - v2)
        pen = circle.radius - separation

        if dot_1 <= 0:
            if (center - v1).mag_sq > circle.radius * circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, (center - v1).rotate(polygon.gameobj.rotation).unit(),
                [-v1.rotate(polygon.gameobj.rotation) + polygon.pos]
            )
        elif dot_2 <= 0:
            if (center - v2).mag_sq > circle.radius * circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, (center - v2).rotate(polygon.gameobj.rotation).unit(),
                [-v2.rotate(polygon.gameobj.rotation) + polygon.pos]
            )
        else:
            norm = Engine.get_normal(verts, face_normal)
            if (center - v1).dot(norm) > circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, norm.rotate(polygon.gameobj.rotation), [-norm * circle.radius + circle.pos]
            )

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon, shape_b: Polygon) -> Union[Manifold, None]:
        """Checks for overlap between two polygons"""
        pen_a, face_a = Engine.axis_least_penetration(shape_a, shape_b)
        if pen_a is None:
            return None

        pen_b, face_b = Engine.axis_least_penetration(shape_b, shape_a)
        if pen_b is None:
            return None

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
            return None

        if Engine.clip(side_plane_normal, pos_side, inc_face) < 2:
            return None

        man = Manifold(ref_poly, inc_poly)

        ref_face_normal = side_plane_normal.perpendicular()
        man.normal = ref_face_normal

        ref_c = ref_face_normal.dot(v1)

        sep_1 = ref_face_normal.dot(inc_face[0]) - ref_c
        sep_2 = ref_face_normal.dot(inc_face[1]) - ref_c

        man.penetration = abs(true_pen)
        man.normal *= Math.sign(true_pen)

        if sep_1 <= 0:
            if sep_2 <= 0:
                man.contacts = inc_face
            else:
                man.contacts = [inc_face[0]]
        elif sep_2 <= 0:
            man.contacts = [inc_face[1]]
        else:
            return None

        if flip:
            man.flip()

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
