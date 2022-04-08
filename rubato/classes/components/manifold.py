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
        contacts: List[Vector] = [],
        contact_count: int = 0
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
        self.contact_count = contact_count

    def flip(self) -> Manifold:
        """
        Flips the reference shape in a collision manifold

        Returns:
            Manifold: a reference to self.
        """
        self.shape_a, self.shape_b, self.penetration = self.shape_b, self.shape_a, self.penetration
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
        dist = (d_x * d_x + d_y * d_y)**.5

        if dist > t_rad:
            return None

        pen, norm = t_rad - dist, Vector(d_x / dist, d_y / dist)
        return Manifold(circle_a, circle_b, abs(pen), norm * Math.sign(pen))

    @staticmethod
    def circle_polygon_test(circle: Circle, polygon: Polygon) -> Union[Manifold, None]:
        """Checks for overlap between a circle and a polygon"""

        result = Manifold(circle, polygon)

        shortest = Math.INF

        verts = polygon.transformed_verts()
        offset = polygon.pos - circle.pos

        closest = Vector()
        for v in verts:
            dist = (circle.pos - polygon.pos - v).magnitude
            if dist < shortest:
                shortest = dist
                closest = polygon.pos + v

        axis = closest - circle.pos
        axis.magnitude = 1

        poly_range = Engine.project_verts(verts, axis) + axis.dot(offset)
        circle_range = Vector(-circle.transformed_radius(), circle.transformed_radius())

        if poly_range.x > circle_range.y or circle_range.x > poly_range.y:
            return None

        dist_min = poly_range.x - circle_range.y

        shortest = abs(dist_min)
        result.normal = axis * Math.sign(dist_min)
        result.penetration = abs(dist_min)

        for i in range(len(verts)):
            axis = Engine.perpendicular_axis(verts, i)

            poly_range = Engine.project_verts(verts, axis) + axis.dot(offset)

            if poly_range.x > circle_range.y or circle_range.x > poly_range.y:
                return None

            dist_min = poly_range.x - circle_range.y

            if abs(dist_min) < shortest:
                shortest = abs(dist_min)
                result.normal = axis * Math.sign(dist_min)
                result.penetration = abs(dist_min)

        return result

    @staticmethod
    def polygon_polygon_test(shape_a: Polygon, shape_b: Polygon) -> Union[Manifold, None]:
        """Checks for overlap between two polygons"""
        test_a_b = Engine.poly_poly_helper(shape_a, shape_b)
        if test_a_b is None:
            return None

        test_b_a = Engine.poly_poly_helper(shape_b, shape_a)
        if test_b_a is None:
            return None

        return test_a_b if abs(test_a_b.penetration) < abs(test_b_a.penetration) else test_b_a.flip()

    @staticmethod
    def poly_poly_helper(poly_a: Polygon, poly_b: Polygon) -> Union[Manifold, None]:
        """Checks for half overlap. Don't use this by itself unless you know what you are doing."""
        result = Manifold(poly_a, poly_b)

        shortest = Math.INF

        verts_a = poly_a.transformed_verts()
        verts_b = poly_b.transformed_verts()

        offset = poly_a.pos - poly_b.pos

        for i in range(len(verts_a)):
            axis = Engine.perpendicular_axis(verts_a, i)

            a_range = Engine.project_verts(verts_a, axis) + axis.dot(offset)
            b_range = Engine.project_verts(verts_b, axis)

            if a_range.x > b_range.y or b_range.x > a_range.y:
                return None

            dist_min = b_range.x - a_range.y

            if abs(dist_min) < shortest:
                shortest = abs(dist_min)
                result.normal = axis * Math.sign(dist_min)
                result.penetration = abs(dist_min)

        return result

    @staticmethod
    def perpendicular_axis(verts: List[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""

        pt_1, pt_2 = verts[index], verts[(index + 1) % len(verts)]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.magnitude = 1
        return axis

    @staticmethod
    def project_verts(verts: List[Vector], axis: Vector) -> Vector:
        """
        Projects the vertices onto a given axis.
        Returns as a vector x is min, y is max
        """

        minval, maxval = Math.INF, -Math.INF

        for v in verts:
            temp = axis.dot(v)
            minval, maxval = min(minval, temp), max(maxval, temp)

        return Vector(minval, maxval)
