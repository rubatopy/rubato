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
        interpolates between lower and upper by t
        :param lower: the lower bound
        :param upper: the upper bound
        :param t: how far you go between lower and upper
        """
        return (t * upper) + ((1 - t) * lower)

    @staticmethod
    def deg_2_rad(deg):
        return deg * math.pi / 180

    @staticmethod
    def rad_2_deg(rad):
        return rad * 180 / math.pi


class Vector(Vector2):
    """
    A Vector object that defines a 3D point in space

    :param x: The x coordinate.
    :param y: The y coordinate.
    :param z: The z coordinate.
    """

    # TODO ask tomer if its ok to have float precision in the Vectors was int
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
        return f"({self.x}, {self.y})"

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other, self.z)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z)

    @staticmethod
    @property
    def ZERO():
        return Vector(0, 0)

    @staticmethod
    @property
    def ONE():
        return Vector(1, 1)

    @staticmethod
    @property
    def TWO():
        return Vector(2, 2)

    @staticmethod
    @property
    def UP():
        return Vector(0, -1)

    @staticmethod
    @property
    def LEFT():
        return Vector(-1, 0)

    @staticmethod
    @property
    def DOWN():
        return Vector(0, 1)

    @staticmethod
    @property
    def RIGHT():
        return Vector(1, 0)

    def __equals(self, v):
        return self.y == v.y and self.x == v.y

    def clamp(self, lower, upper):
        """
        Clamps x and y between the two vectors given

        :param lower: The lower bound
        :param upper: The upper bound
        :return: None
        """
        if not isinstance(lower, Vector):
            Vector(*lower)
        if not isinstance(upper, Vector):
            Vector(*upper)
        self.x = PgpMath.clamp(self.x, lower.x, upper.x)
        self.y = PgpMath.clamp(self.y, lower.y, upper.y)

    def __eq__(self, other):
        return False if (other is None or not isinstance(other, Vector)) else self.__equals(other)

    @staticmethod
    def from_direction_distance(direction: float, distance: float):
        """
        Gives you a Vector from the given direction and distance
        :param direction: direction of vector in radians
        :param distance: length of vector
        :return: Vector from the given direction and distance
        """
        x, y = math.cos(direction) * distance, math.sin(direction) * distance
        return Vector(x, y)
