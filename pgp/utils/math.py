import math
from pygame.math import Vector2


class PgpMath:

    @staticmethod
    def clamp(a, lower, upper):
        """
        Clamps a to the bounds of upper and lower
        """
        return min(max(a, lower), upper)

    @staticmethod
    def lerp(lower, upper, t):
        """
        Linearly interpolates between lower and upper bounds by t

        :param lower: The lower bound
        :param upper: The upper bound
        :param t: How far you go between lower and upper
        """
        return (t * upper) + ((1 - t) * lower)

    @staticmethod
    def deg_to_rad(deg):
        return deg * math.pi / 180

    @staticmethod
    def rad_to_deg(rad):
        return rad * 180 / math.pi


class Vector(Vector2):
    """
    A Vector object that defines a 3D point in space

    :param x: The x coordinate.
    :param y: The y coordinate.
    :param z: The z coordinate.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x, self.y, self.z = x, y, z

    def translate(self, x: float, y: float, z: float = 0):
        """
        Translates the vector's x y and z coordinates by some constants

        :param x: The change in x.
        :param y: The change in y.
        :param z: The change in z.
        """
        self.x, self.y, self.z = self.x + x, self.y + y, self.z + z

    def offset2(self, other):
        """
        Offsets the x and y coordinates of a vector by those of another vector

        :param other: Another point
        :return: A new point with the translated x and y coordinates
        """
        return Vector(self.x - other.x, self.y - other.y, self.z)

    def to_tuple2(self):
        """
        Returns the x and y coordinates of the vector as a tuple
        """
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other, self.z)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z)

    @staticmethod
    def ZERO():
        return Vector(0, 0)

    @staticmethod
    def ONE():
        return Vector(1, 1)

    @staticmethod
    def TWO():
        return Vector(2, 2)

    @staticmethod
    def UP():
        return Vector(0, -1)

    @staticmethod
    def LEFT():
        return Vector(-1, 0)

    @staticmethod
    def DOWN():
        return Vector(0, 1)

    @staticmethod
    def RIGHT():
        return Vector(1, 0)

    def __equals2(self, v):
        return self.y == v.y and self.x == v.x

    def clamp(self, lower, upper):
        """
        Clamps x and y between the two vectors given

        :param lower: The lower bound
        :param upper: The upper bound
        :return: None
        """
        if not isinstance(lower, Vector):
            lower = Vector(*lower)
        if not isinstance(upper, Vector):
            upper = Vector(*upper)
        self.x = PgpMath.clamp(self.x, lower.x, upper.x)
        self.y = PgpMath.clamp(self.y, lower.y, upper.y)

    def __eq__(self, other):
        return False if (other is None or not isinstance(other, Vector)) else self.__equals2(other)

    @staticmethod
    def from_radial(angle: float, magnitude: float):
        """
        Gives you a Vector from the given direction and distance

        :param angle: Direction of vector in radians
        :param magnitude: Length of vector
        :return: Vector from the given direction and distance
        """
        return Vector(math.cos(angle) * magnitude, math.sin(angle) * magnitude)
