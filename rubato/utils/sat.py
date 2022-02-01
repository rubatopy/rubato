"""
An SAT implementation
"""
from typing import Callable, Dict, List, Union
from rubato.utils import Vector, Math
import math

from rubato.utils.error import SideError

# Credit for original JavaScript SAT implementation to Andrew Sevenson
# https://github.com/sevdanski/SAT_JS


class Polygon:
    """
    A custom polygon class with an arbitrary number of vertices

    Attributes:
        verts (List[Vector]): A list of the vertices in the Polygon, in either
            clockwise or anticlockwise direction.
        scale (Union[float, int]): The scale of the polygon.
    """

    def __init__(self,
                 verts: List[Vector],
                 pos: Callable = lambda: Vector(0, 0),
                 scale: Union[float, int] = 1,
                 rotation: Callable = lambda: 0):
        """
        Initializes a Polygon

        Args:
            verts: A list of the vertices in the Polygon.
            pos: The position of the center of the Polygon as a function.
                Defaults to lambda: Vector(0, 0).
            scale: The scale of the polygon. Defaults to 1.
            rotation: The rotation angle of the polygon in degrees as a
                function. Defaults to lambda: 0.
        """
        self.verts, self._pos = verts, pos
        self.scale, self._rotation = scale, rotation

    @staticmethod
    def generate_rect(w: int = 32, h: int = 32) -> "Polygon":
        """
        Creates a rectangle from its dimensions.

        Args:
            w: The width of the hitbox.
            h: The height of the hitbox.

        Returns:
            Polygon: The polygon.
        """

        return Polygon([
            Vector(-w / 2, -h / 2),
            Vector(w / 2, -h / 2),
            Vector(w / 2, h / 2),
            Vector(-w / 2, h / 2)
        ])

    @staticmethod
    def generate_polygon(num_sides: int,
                         radius: Union[float, int] = 1) -> "Polygon":
        """
        Creates a normal polygon with a specified number of sides and
        an optional radius.

        Args:
            num_sides: The number of sides of the polygon.
            radius: The radius of the polygon. Defaults to 1.

        Raises:
            SideError: Raised when the number of sides is less than 3.

        Returns:
            Polygon: The constructed polygon.
        """
        if num_sides < 3:
            raise SideError(
                "Can't create a polygon with less than three sides")

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle) / 2
            verts.append(
                Vector(math.cos(angle) * radius,
                       math.sin(angle) * radius))

        return Polygon(verts)

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the Polygon's center"""
        return self._pos()

    @property
    def rotation(self) -> int:
        """The getter method for the rotation of the Polygon"""
        return self._rotation()

    def clone(self) -> "Polygon":
        """Creates a copy of the Polygon at the current position"""
        # pylint: disable=unnecessary-lambda
        return Polygon(list(map((lambda v: v.clone()),
                                self.verts)), lambda: self.pos.clone(),
                       self.scale, lambda: self.rotation.clone())

    def transformed_verts(self) -> List[Vector]:
        """Maps each vertex with the Polygon's scale and rotation"""
        return list(
            map(lambda v: v.transform(self.scale, self.rotation), self.verts))

    def real_verts(self) -> List[Vector]:
        """Returns the a list of vertices in absolute coordinates"""
        return list(
            map(lambda v: self.pos + v.transform(self.scale, self.rotation),
                self.verts))

    def __str__(self):
        return (f"{list(map(str, self.verts))}, {self.pos}, " +
                f"{self.scale}, {self.rotation}")

    def bounding_box_dimensions(self):
        real_verts = self.real_verts()
        # pylint: disable=protected-access
        x_dir = SAT._project_verts_for_min_max(Vector(1, 0), real_verts)
        y_dir = SAT._project_verts_for_min_max(Vector(0, 1), real_verts)
        return Vector(x_dir["max"] - x_dir["min"], y_dir["max"] - y_dir["min"])


class Circle:
    """
    A custom circle class defined by a position, radius, and scale

    Attributes:
        radius (int): The radius of the circle.
        scale (int): The scale of the circle.
    """

    def __init__(self,
                 pos: Callable = lambda: Vector(0, 0),
                 radius: int = 1,
                 scale: int = 1):
        """
        Initializes a Circle

        Args:
            pos: The position of the circle as a function.
                Defaults to lambda: Vector(0, 0).
            radius: The radius of the circle. Defaults to 1.
            scale: The scale of the circle. Defaults to 1.
        """
        self._pos, self.radius, self.scale = pos, radius, scale

    @property
    def pos(self) -> Vector:
        """The getter method for the position of the circle's center"""
        return self._pos()

    def clone(self) -> "Circle":
        """Creates a copy of the circle at the current position"""
        return Circle(self.pos.clone(), self.radius, self.scale)

    def transformed_radius(self) -> int:
        """Gets the true radius of the circle"""
        return self.radius * self.scale


class CollisionInfo:
    """
    A class that represents information returned in a successful collision

    Attributes:
        shape_a (Union[Circle, Polygon, None]): A reference to the first shape.
        shape_b (Union[Circle, Polygon, None]): A reference to the second shape.
        distance (float): The distance between the centers of the colliders.
        vector (Vector): The vector that would separate the two colliders.
        a_contained (bool): Whether a is contained inside of b.
        b_contained (bool): Whether b is contained inside of a.
        seperation (Vector): The vector that would separate the two colliders.
    """

    def __init__(self):
        """
        Initializes a Collision Info
        """
        self.shape_a: Union[Circle, Polygon, None] = None
        self.shape_b: Union[Circle, Polygon, None] = None
        self.distance: float = 0
        self.vector = Vector()
        self.a_contained, self.b_contained = False, False
        self.separation = Vector()

    def __str__(self):
        return (f"{self.distance}, {self.vector}, {self.a_contained}, " +
                f"{self.b_contained}, {self.separation}")


class SAT:
    """
    A general class that does the collision detection math between
    circles and polygons
    """

    @staticmethod
    def overlap(shape_a: Union[Polygon, Circle],
                shape_b: Union[Polygon, Circle]) -> Union[CollisionInfo, None]:
        """
        Checks for overlap between any two shapes (Polygon or Circle)

        Args:
            shape_a: The first shape.
            shape_b: The second shape.

        Returns:
            Union[CollisionInfo, None]: If a collision occurs, a CollisionInfo
            is returned. Otherwise None is returned.
        """

        if isinstance(shape_a, Circle) and isinstance(shape_b, Circle):
            return SAT._circle_circle_test(shape_a, shape_b)

        if isinstance(shape_a, Polygon) and isinstance(shape_b, Polygon):
            test_a_b = SAT._polygon_polygon_test(shape_a, shape_b)
            if test_a_b is None: return None

            test_b_a = SAT._polygon_polygon_test(shape_b, shape_a, True)
            if test_b_a is None: return None

            regular = abs(test_a_b.distance) < abs(test_b_a.distance)

            result = test_a_b if regular else test_b_a

            result.a_contained = (test_b_a.a_contained
                                  if regular else test_a_b.a_contained)
            result.b_contained = (test_b_a.b_contained
                                  if regular else test_a_b.b_contained)

            result.vertex_b = test_a_b.vertex
            result.vertex_a = test_b_a.vertex

            return result

        a_is_circle = isinstance(shape_a, Circle)
        return SAT._circle_polygon_test((shape_a, shape_b)[a_is_circle],
                                        (shape_b, shape_a)[a_is_circle],
                                        not a_is_circle)

    @staticmethod
    def _circle_circle_test(shape_a, shape_b):
        pass

    @staticmethod
    def _circle_polygon_test(shape_a, shape_b, flip):
        pass

    @staticmethod
    def _polygon_polygon_test(
            shape_a: Union[Polygon, Circle],
            shape_b: Union[Polygon, Circle],
            flip: bool = False) -> Union[CollisionInfo, None]:
        """Checks for overlap between two polygons"""

        shortest_dist = Math.INFINITY

        result = CollisionInfo()
        result.shape_a = shape_a if flip else shape_b
        result.shape_b = shape_b if flip else shape_a
        result.a_contained = True
        result.b_contained = True

        verts_1 = shape_a.transformed_verts()
        verts_2 = shape_b.transformed_verts()

        offset = shape_a.pos - shape_b.pos

        v_contact = []

        for i in range(len(verts_1)):
            axis = SAT._get_perpendicular_axis(verts_1, i)

            a_range = SAT._project_verts_for_min_max(axis, verts_1)
            b_range = SAT._project_verts_for_min_max(axis, verts_2)

            scalar_offset = axis.dot(offset)
            a_range["min"] += scalar_offset
            a_range["max"] += scalar_offset

            if (a_range["min"] > b_range["max"]) or (b_range["min"] >
                                                     a_range["max"]):
                return None

            SAT._check_ranges_for_containment(a_range, b_range, result, flip)

            min_dist = (b_range["min"] -
                        a_range["max"]) if flip else (a_range["min"] -
                                                      b_range["max"])

            mincheck = b_range["min"] > a_range["min"] and b_range[
                "max"] > a_range["max"]
            maxcheck = b_range["min"] < a_range["min"] and b_range[
                "max"] < a_range["max"]
            if mincheck or maxcheck:
                v_contact.append(b_range["mindex" if mincheck else "maxdex"])

            abs_min = abs(min_dist)
            if abs_min < shortest_dist:
                shortest_dist = abs_min
                result.distance, result.vector = min_dist, axis

        result.separation = result.vector * result.distance
        if v_contact is None:
            result.vertex = None
        else:
            #print(v_contact, flip)
            final_verts = []
            for i in v_contact:
                valid = True
                for j in range(len(i)):
                    if i[0] != i[j]: valid = False
                if valid:
                    final_verts.append(i)
            print(final_verts, flip)
            result.vertex = verts_2[final_verts[0]
                                    [0]] if len(final_verts) > 0 else None

        return result

    @staticmethod
    def _check_ranges_for_containment(a_range: Dict[str, Union[float, int]],
                                      b_range: Dict[str, Union[float, int]],
                                      result: CollisionInfo, flip: bool):
        """Checks if either shape is inside the other"""

        if flip:
            if (a_range["max"] < b_range["max"]) or (a_range["min"] >
                                                     b_range["min"]):
                result.a_contained = False
            if (b_range["max"] < a_range["max"]) or (b_range["min"] >
                                                     a_range["min"]):
                result.b_contained = False
        else:
            if (a_range["max"] > b_range["max"]) or (a_range["min"] <
                                                     b_range["min"]):
                result.a_contained = False
            if (b_range["max"] > a_range["max"]) or (b_range["min"] <
                                                     a_range["min"]):
                result.b_contained = False

    @staticmethod
    def _get_perpendicular_axis(verts: List[Vector], index: int) -> Vector:
        """Finds a vector perpendicular to a side"""

        pt_1, pt_2 = verts[index], verts[(index + 1) % len(verts)]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.normalize()
        return axis

    @staticmethod
    def _project_verts_for_min_max(axis: List[Vector], verts: int) -> Vector:
        """Projects the vertices onto a given axis"""

        minval, maxval = Math.INFINITY, -Math.INFINITY
        mindex = maxdex = []

        for j in range(len(verts)):
            temp = axis.dot(verts[j])
            if temp < minval:
                minval = temp
                mindex = [j]
            elif temp == minval:
                mindex.append(j)
            if temp > maxval:
                maxval = temp
                maxdex = [j]
            elif temp == maxval:
                maxdex.append(j)

        return {
            "min": minval,
            "max": maxval,
            "mindex": mindex,
            "maxdex": maxdex
        }
