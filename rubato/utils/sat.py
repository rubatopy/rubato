from rubato.utils import Vector, PMath, check_types
import math

# Credit for original JavaScript separating axis theorem implementation to Andrew Sevenson
# https://github.com/sevdanski/SAT_JS

# TODO Helper functions
class Polygon:
    """
    A custom polygon class with an arbitrary number of vertices

    :param verts: A list of the vertices in the Polygon, in either clockwise or anticlockwise direction
    :param pos: The position of the center of the Polygon as a function
    :param scale: The scale of the polygon
    :param rotation: The rotation angle of the polygon in degrees
    """

    def __init__(self, verts: list, pos: type(lambda:None) = lambda: Vector(), scale: float | int = 1, rotation: float | int = 0):
        check_types(Polygon.__init__, locals())
        self.verts, self._pos, self.scale, self.rotation = verts, pos, scale, rotation

    @staticmethod
    def generate_polygon(num_sides: int, radius: float | int =1):
        """Creates a normal polygon with a specified number of sides and an optional radius"""

        check_types(Polygon.generate_polygon, locals())
        if num_sides < 3:
            raise "Can't create a polygon with less than three sides"

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle)/2
            verts.append(Vector(math.cos(angle) * radius, math.sin(angle) * radius))

        return Polygon(verts)

    @property
    def pos(self):
        """The getter method for the position of the Polygon's center"""
        return self._pos()

    def clone(self):
        """Creates a copy of the Polygon at the current position"""
        return Polygon(list(map((lambda v: v.clone()), self.verts)), lambda: self.pos.clone(), self.scale, self.rotation)

    def transformed_verts(self):
        """Maps each vertex with the Polygon's scale and rotation"""
        return list(map(lambda v: v.transform(self.scale, self.rotation), self.verts))

    def real_verts(self):
        """Returns the a list of vertices in absolute coordinates"""
        return list(map(lambda v: self.pos + v.transform(self.scale, self.rotation), self.verts))

    def __str__(self):
        return f"{list(map(lambda v: str(v), self.verts))}, {self.pos}, {self.scale}, {self.rotation}"

# TODO make circles work
class Circle:
    """
    A custom circle class defined by a position, radius, and scale
    """

    def __init__(self, pos = lambda: Vector(), radius = 1, scale = 1):
        check_types(Circle.__init__, locals())
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

        check_types(SAT.overlap, locals())

        if isinstance(shape_a, Circle) and isinstance(shape_b, Circle):
            return SAT._circle_circle_test(shape_a, shape_b)

        if isinstance(shape_a, Polygon) and isinstance(shape_b, Polygon):
            test_a_b = SAT._polygon_polygon_test(shape_a, shape_b)
            if test_a_b is None: return None

            test_b_a = SAT._polygon_polygon_test(shape_b, shape_a, True)
            if test_b_a is None: return None

            result = test_a_b if abs(test_a_b.distance) < abs(test_b_a.distance) else test_b_a

            result.a_contained = test_a_b.a_contained and test_b_a.a_contained
            result.b_contained = test_a_b.b_contained and test_b_a.b_contained

            return result

        a_is_circle = isinstance(shape_a, Circle)
        return SAT._circle_polygon_test(shape_a if a_is_circle else shape_b, shape_b if a_is_circle else shape_a, not a_is_circle)

    @staticmethod
    def _circle_circle_test(shape_a, shape_b):
        pass

    @staticmethod
    def _circle_polygon_test(shape_a, shape_b, flip):
        pass

    @staticmethod
    def _polygon_polygon_test(shape_a, shape_b, flip = False):
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

            abs_min = abs(min_dist)
            if abs_min < shortest_dist:
                shortest_dist = abs_min
                result.distance, result.vector = min_dist, axis

        result.separation = result.vector.clone() * result.distance

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

        pt_1, pt_2 = verts[index], verts[0] if index >= len(verts)-1 else verts[index+1]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.normalize()
        return axis

    @staticmethod
    def _project_verts_for_min_max(axis, verts):
        """Projects the vertices onto a given axis"""

        min = max = axis.dot(verts[0])

        for j in range(len(verts)):
            temp = axis.dot(verts[j])
            if temp < min: min = temp
            if temp > max: max = temp

        return {"min": min, "max": max}
