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
        shape_a (Union[Circle, Polygon, None]): A reference to the first shape.
        shape_b (Union[Circle, Polygon, None]): A reference to the second shape.
        penetration (float): The amount by which the colliders are intersecting.
        normal (Vector): The direction that would most quickly separate the two colliders.
    """

    def __init__(
        self,
        shape_a: Union[Hitbox, None],
        shape_b: Union[Hitbox, None],
        penetration: float = 0,
        normal: Vector = Vector(),
        contact_a: Vector = Vector(),
        contact_b: Vector = Vector(),
    ):
        """
        Initializes a Collision Info manifold.
        This is used internally by :func:`Engine <rubato.classes.components.hitbox.Engine>`.
        """
        self.shape_a = shape_a
        self.shape_b = shape_b
        self.penetration = penetration
        self.normal = normal
        self.contact_a = contact_a
        self.contact_b = contact_b

    def flip(self) -> Manifold:
        """
        Flips the reference shape in a collision manifold

        Returns:
            Manifold: a reference to self.
        """
        self.shape_a, self.shape_b = self.shape_b, self.shape_a
        self.contact_a, self.contact_b = self.contact_b, self.contact_a
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
        dist = (d_x * d_x + d_y * d_y)

        if dist > t_rad * t_rad:
            return None

        dist = dist**.5

        pen = t_rad - dist
        norm = Vector(d_x / dist, d_y / dist) * Math.sign(pen)

        return Manifold(circle_a, circle_b, abs(pen), norm, norm * circle_a.radius, -norm * circle_b.radius)

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
            norm = Engine.get_normal(verts, face_normal)
            return Manifold(
                circle, polygon, circle.radius, norm.rotate(polygon.gameobj.rotation), norm * circle.radius,
                -norm * circle.radius
            )

        v1, v2 = verts[face_normal], verts[(face_normal + 1) % len(verts)]

        dot_1 = (center - v1).dot(v2 - v1)
        dot_2 = (center - v2).dot(v1 - v2)
        pen = circle.radius - separation

        if dot_1 <= 0:
            if (center - v1).mag_sq > circle.radius * circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, (center - v1).rotate(polygon.gameobj.rotation).unit(),
                -v1.rotate(polygon.gameobj.rotation), v1.rotate(polygon.gameobj.rotation)
            )
        elif dot_2 <= 0:
            if (center - v2).mag_sq > circle.radius * circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, (center - v1).rotate(polygon.gameobj.rotation).unit(),
                -v2.rotate(polygon.gameobj.rotation), v2.rotate(polygon.gameobj.rotation)
            )
        else:
            norm = Engine.get_normal(verts, face_normal)
            if (center - v1).dot(norm) > circle.radius:
                return None

            return Manifold(
                circle, polygon, pen, norm.rotate(polygon.gameobj.rotation), norm * circle.radius, -norm * circle.radius
            )

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon, shape_b: Polygon) -> Union[Manifold, None]:
        """Checks for overlap between two polygons"""
        man = Manifold(shape_a, shape_b)
        return man

    @staticmethod
    def axis_least_penetration(face_index: List[int], shape_a: Polygon, shape_b: Polygon) -> float:
        """Finds the axis of least penetration with a given index."""
        a_verts = shape_a.translated_verts()
        b_verts = shape_b.translated_verts()

        best_dist = -Math.INF
        best_ind = 0

        for i in range(len(a_verts)):
            nw = Engine.get_normal(a_verts, i).rotate(shape_a.gameobj.rotation)
            trans = -shape_b.gameobj.rotation
            n = nw.rotate(trans)
            s = Engine.get_support(b_verts, -n)
            v = a_verts[i].rotate(shape_a.gameobj.rotation).rotate(trans)
            d = n.dot(s - v)

            if d > best_dist:
                best_dist = d
                best_ind = i

        face_index[0] = best_ind
        return best_dist

    @staticmethod
    def incident_face(ref_poly: Polygon, inc_poly: Polygon, ref_index: int) -> List[Vector]:
        """Finds the incident face between two polygons."""
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
            inc_verts[inc_face].rotate(inc_poly.gameobj.rotation),
            inc_verts[(inc_face + 1) % len(inc_verts)].rotate(inc_poly.gameobj.rotation)
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
            out[sp] = (face[1] - face[0]) * alpha + face[0]
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
