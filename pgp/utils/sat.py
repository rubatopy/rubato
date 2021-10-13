from pgp.utils import Vector
import math

# Credit for original JavaScript separating axis theorem implementation to Andrew Sevenson
# https://github.com/sevdanski/SAT_JS

class Polygon:
    def __init__(self, verts, pos = Vector(), scale = 1, rotation = 0):
        self.verts, self.pos, self.scale, self.rotation = verts, pos, scale, rotation

    @staticmethod
    def generate_polygon(num_sides, radius):
        if num_sides < 3:
            raise "Can't create a polygon with less than three sides"

        rotangle = 2 * math.pi / num_sides
        angle, verts = 0, []

        for i in range(num_sides):
            angle = (i * rotangle) + (math.pi - rotangle)/2
            verts.append(Vector(math.cos(angle) * radius, math.sin(angle) * radius))

        return Polygon(verts)

    def clone(self):
        return Polygon(list(map((lambda v: v.clone()), self.verts)), self.pos.clone(), self.scale, self.rotation)

    def transformed_verts(self):
        return list(map(lambda v: v.transform(this.scale, this.rotation), self.verts))

class Circle:
    def __init__(self, pos = Vector(0, 0), radius = 1, scale = 1):
        self.pos, self.radius, self.scale, self.rotation = pos, radius, scale, 0

    def clone():
        return Circle(self.pos.clone(), self.radius, self.scale)

    def transformed_radius(self):
        return this.radius * this.scale

class CollisionInfo:
    def __init__(self, shape_a, shape_b, distance = 0, vector = Vector(), a_contained = False, b_contained = False, separation = Vector()):
        self.shape_a, self.shape_b, self.distance, self.vector = shape_a, shape_b, distance, vector
        self.a_contained, self.b_contained, self.separation = a_contained, b_contained, separation

class SAT:
    @staticmethod
    def overlap(shape_a: Polygon | Circle, shape_b: Polygon | Circle):
        if shape_a is Circle and shape_b is Circle:
            return SAT._circle_circle_test(shape_a, shape_b)

        if shape_a is Polygon and shape_b is Polygon:
            test_a_b = SAT._polygon_polygon_test(shape_a, shape_b)
            if not test_a_b: return None

            test_b_a = SAT._polygon_polygon_test(shape_b, shape_a, True)
            if not test_b_a: return None

            result = test_a_b if abs(test_a_b.distance) < abs(test_b_a.distance) else test_b_a

            result.a_contained = test_a_b.a_contained and test_b_a.a_contained
            result.b_contained = test_a_b.b_contained and test_b_a.b_contained

            return result

        a_is_circle = shape_a is Circle
        return SAT._circle_polygon_test(shape_a if a_is_circle else shape_b, shape_b if a_is_circle else shape_a, not a_is_circle)

    @staticmethod
    def _circle_circle_test(shape_a, shape_b):
        pass

    @staticmethod
    def _circle_polygon_test(shape_a, shape_b, flip):
        pass

    @staticmethod
    def _polygon_polygon_test(shape_a, shape_b, flip = False):
        pass
