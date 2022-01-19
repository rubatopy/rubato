from typing import Callable
from rubato.utils import Vector, PMath
import math


# Credit for original JavaScript separating axis theorem implementation to Andrew Sevenson
# https://github.com/sevdanski/SAT_JS

class Polygon:
    """
    A custom polygon class with an arbitrary number of vertices

    :param verts: A list of the vertices in the Polygon, in either clockwise or anticlockwise direction
    :param pos: The position of the center of the Polygon as a function
    :param scale: The scale of the polygon
    :param rotation: The rotation angle of the polygon in degrees
    """

    def __init__(self, verts: list, pos: Callable = lambda: Vector(), scale: float | int = 1,
                 rotation: Callable = lambda: 0):
        self.verts, self._pos, self.scale, self._rotation = verts, pos, scale, rotation

    @staticmethod
    def generate_rect(w: int = 32, h: int = 32) -> "Polygon":
        """
        Creates a rectangle from its dimensions

        :param w: The width of the hitbox
        :param h: The height of the hitbox
        :return: The polygon
        """

        return Polygon([Vector(-w / 2, -h / 2), Vector(w / 2, -h / 2), Vector(w / 2, h / 2), Vector(-w / 2, h / 2)])

    @staticmethod
    def generate_polygon(num_sides: int, radius: float | int = 1) -> "Polygon":
        """Creates a normal polygon with a specified number of sides and an optional radius"""
        if num_sides < 3:
            raise Exception("Can't create a polygon with less than three sides")

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle) / 2
            verts.append(Vector(math.cos(angle) * radius, math.sin(angle) * radius))

        return Polygon(verts)

    @property
    def pos(self):
        """The getter method for the position of the Polygon's center"""
        return self._pos()

    @property
    def rotation(self):
        """The getter method for the rotation of the Polygon"""
        return self._rotation()

    def clone(self):
        """Creates a copy of the Polygon at the current position"""
        return Polygon(list(map((lambda v: v.clone()), self.verts)), lambda: self.pos.clone(), self.scale,
                       lambda: self.rotation.clone())

    def transformed_verts(self):
        """Maps each vertex with the Polygon's scale and rotation"""
        return list(map(lambda v: v.transform(self.scale, self.rotation), self.verts))

    def real_verts(self):
        """Returns the a list of vertices in absolute coordinates"""
        return list(map(lambda v: self.pos + v.transform(self.scale, self.rotation), self.verts))

    def __str__(self):
        return f"{list(map(lambda v: str(v), self.verts))}, {self.pos}, {self.scale}, {self.rotation}"

    def bounding_box_dimensions(self):
        real_verts = self.real_verts()
        x_dir = SAT._project_verts_for_min_max(Vector(1, 0), real_verts)
        y_dir = SAT._project_verts_for_min_max(Vector(0, 1), real_verts)
        return Vector(x_dir["max"] - x_dir["min"], y_dir["max"] - y_dir["min"])


# TODO make circles work
class Circle:
    """
    A custom circle class defined by a position, radius, and scale
    """

    def __init__(self, pos=lambda: Vector(), radius=1, scale=1):
        self._pos, self.radius, self.scale, self.rotation = pos, radius, scale, 0

    @property
    def pos(self):
        """The getter method for the position of the circle's center"""
        return self._pos()

    def clone(self):
        """Creates a copy of the circle at the current position"""
        return Circle(self.pos.clone(), self.radius, self.scale)

    def transformed_radius(self):
        """Gets the true radius of the circle"""
        return self.radius * self.scale


class CollisionInfo:
    """
    A class that represents information returned in a successful collision
    """

    def __init__(self):
        self.shape_a, self.shape_b, self.distance, self.vector = None, None, 0, Vector()
        self.a_contained, self.b_contained, self.separation = False, False, Vector()

    def __str__(self):
        return f"{self.distance}, {self.vector}, {self.a_contained}, {self.b_contained}, {self.separation}"


class SAT:
    """
    A general class that does the collision detection math between circles and polygons
    """

    @staticmethod
    def overlap(shape_a: Polygon | Circle, shape_b: Polygon | Circle):
        """
        Checks for overlap between any two shapes (Polygon or Circle)

        :param shape_a: The first shape
        :param shape_b: The second shape

        :returns: None or CollisionInfo object
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

            result.a_contained = test_b_a.a_contained if regular else test_a_b.a_contained
            result.b_contained = test_b_a.b_contained if regular else test_a_b.b_contained

            result.vertex_b = test_a_b.vertex
            result.vertex_a = test_b_a.vertex

            return result

        a_is_circle = isinstance(shape_a, Circle)
        return SAT._circle_polygon_test(shape_a if a_is_circle else shape_b, shape_b if a_is_circle else shape_a,
                                        not a_is_circle)

    @staticmethod
    def _circle_circle_test(shape_a, shape_b):
        pass

    @staticmethod
    def _circle_polygon_test(shape_a, shape_b, flip):
        pass

    @staticmethod
    def _polygon_polygon_test(shape_a, shape_b, flip=False):
        """
        Checks for overlap between two polygons

        :param shape_a: The first shape
        :param shape_b: The second shape

        :returns: None or CollisionInfo object
        """

        shortest_dist = PMath.INFINITY

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

            if (a_range["min"] > b_range["max"]) or (b_range["min"] > a_range["max"]): return None

            SAT._check_ranges_for_containment(a_range, b_range, result, flip)

            min_dist = (b_range["min"] - a_range["max"]) if flip else (a_range["min"] - b_range["max"])

            mincheck = b_range["min"] > a_range["min"] and b_range["max"] > a_range["max"]
            maxcheck = b_range["min"] < a_range["min"] and b_range["max"] < a_range["max"]
            if mincheck or maxcheck: v_contact.append(b_range["mindex" if mincheck else "maxdex"])

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
            result.vertex = verts_2[final_verts[0][0]] if len(final_verts) > 0 else None

        return result

    @staticmethod
    def _check_ranges_for_containment(a_range, b_range, result, flip):
        """Checks if either shape is inside the other"""

        if flip:
            if (a_range["max"] < b_range["max"]) or (a_range["min"] > b_range["min"]): result.a_contained = False
            if (b_range["max"] < a_range["max"]) or (b_range["min"] > a_range["min"]): result.b_contained = False
        else:
            if (a_range["max"] > b_range["max"]) or (a_range["min"] < b_range["min"]): result.a_contained = False
            if (b_range["max"] > a_range["max"]) or (b_range["min"] < a_range["min"]): result.b_contained = False

    @staticmethod
    def _get_perpendicular_axis(verts, index):
        """Finds a vector perpendicular to a side"""

        pt_1, pt_2 = verts[index], verts[(index + 1) % len(verts)]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.normalize()
        return axis

    @staticmethod
    def _project_verts_for_min_max(axis, verts):
        """Projects the vertices onto a given axis"""

        min, max = PMath.INFINITY, -PMath.INFINITY
        mindex = maxdex = []

        for j in range(len(verts)):
            temp = axis.dot(verts[j])
            if temp < min:
                min = temp
                mindex = [j]
            elif temp == min: mindex.append(j)
            if temp > max:
                max = temp
                maxdex = [j]
            elif temp == max: maxdex.append(j)

        return {"min": min, "max": max, "mindex": mindex, "maxdex": maxdex}
