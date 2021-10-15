from rubato.utils import Vector, PMath
import math

# Credit for original JavaScript separating axis theorem implementation to Andrew Sevenson
# https://github.com/sevdanski/SAT_JS

class Polygon:
    def __init__(self, verts, pos = Vector(), scale = 1, rotation = 0):
        self.verts, self.pos, self.scale, self.rotation = verts, pos, scale, rotation

    @staticmethod
    def generate_polygon(num_sides, radius=1):
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
        return list(map(lambda v: v.transform(self.scale, self.rotation), self.verts))

    def __str__(self):
        return f"{list(map(lambda v: str(v), self.verts))}, {self.pos}, {self.scale}, {self.rotation}"

class Circle:
    def __init__(self, pos = Vector(0, 0), radius = 1, scale = 1):
        self.pos, self.radius, self.scale, self.rotation = pos, radius, scale, 0

    def clone(self):
        return Circle(self.pos.clone(), self.radius, self.scale)

    def transformed_radius(self):
        return self.radius * self.scale

class CollisionInfo:
    def __init__(self):
        self.shape_a, self.shape_b, self.distance, self.vector = None, None, 0, Vector()
        self.a_contained, self.b_contained, self.separation = False, False, Vector()

    def __str__(self):
        return f"{self.distance}, {self.vector}, {self.a_contained}, {self.b_contained}, {self.separation}"

class SAT:
    @staticmethod
    def overlap(shape_a: Polygon | Circle, shape_b: Polygon | Circle):
        isinstance(shape_a, Circle)

        if isinstance(shape_a, Circle) and isinstance(shape_b, Circle):
            return SAT._circle_circle_test(shape_a, shape_b)

        if isinstance(shape_a, Polygon) and isinstance(shape_b, Polygon):
            print("polygon test")
            test_a_b = SAT._polygon_polygon_test(shape_a, shape_b)
            if not test_a_b: return None

            test_b_a = SAT._polygon_polygon_test(shape_b, shape_a, True)
            if not test_b_a: return None

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
        shortest_dist = PMath.INFINITY

        result = CollisionInfo()
        result.shape_a = shape_a if flip else shape_b
        result.shape_b = shape_b if flip else shape_a
        result.a_contained = True
        result.b_contained = True

        verts_1 = shape_a.transformed_verts()
        verts_2 = shape_b.transformed_verts()

        offset = Vector(shape_a.pos.x - shape_b.pos.x, shape_a.pos.y - shape_b.pos.y)

        for i in range(len(verts_1)):
            axis = SAT._get_perpendicular_axis(verts_1, i)

            a_range = SAT._project_verts_for_min_max(axis, verts_1)
            b_range = SAT._project_verts_for_min_max(axis, verts_2)

            scalar_offset = axis.dot(offset)
            a_range["min"] += scalar_offset
            a_range["max"] += scalar_offset

            if (a_range["min"] > b_range["max"]) or (b_range["min"] > a_range["max"]): return None

            SAT._check_ranges_for_containment(a_range, b_range, result, flip)

            min_dist = a_range["min"] - b_range["max"]
            if flip: min_dist *= -1

            abs_min = abs(min_dist)
            if abs_min < shortest_dist:
                shortest_dist = abs_min
                result.distance, result.vector = min_dist, axis

        result.separation = Vector(result.vector.x * result.distance, result.vector.y * result.distance)

        return result

    @staticmethod
    def _check_ranges_for_containment(a_range, b_range, result, flip):
        if flip:
            if (a_range["max"] < b_range["max"]) or (a_range["min"] > b_range["min"]): result.a_contained = False
            if (b_range["max"] < a_range["max"]) or (b_range["min"] > a_range["min"]): result.b_contained = False
        else:
            if (a_range["max"] > b_range["max"]) or (a_range["min"] < b_range["min"]): result.a_contained = False
            if (b_range["max"] > a_range["max"]) or (b_range["min"] < a_range["min"]): result.b_contained = False

    @staticmethod
    def _get_perpendicular_axis(verts, index):
        pt_1, pt_2 = verts[index], verts[0] if index >= len(verts)-1 else verts[index+1]
        axis = Vector(pt_1.y - pt_2.y, pt_2.x - pt_1.x)
        axis.normalize()
        return axis

    @staticmethod
    def _project_verts_for_min_max(axis, verts):
        min = max = axis.dot(verts[0])

        for j in range(len(verts)):
            temp = axis.dot(verts[j])
            if temp < min: min = temp
            if temp > max: max = temp

        return {"min": min, "max": max}
