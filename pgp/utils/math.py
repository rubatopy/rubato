# from pygame.math import Vector2

class PgpMath:
    @staticmethod
    def clamp(a, upper, lower):
        return min(max(a, lower), upper)


class Vector:
    """
    A Vector object that defines a 3D point in space

    :param x: The x coordinate.
    :param y: The y coordinate.
    :param z: The z coordinate.
    """

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x, self.y, self.z = x, y, z

    def translate(self, x: int, y: int, z: int = 0):
        """
        Translates the point's x y and z coordinates by some constants

        :param x: The change in x.
        :param y: The change in y.
        :param z: The change in z.
        """
        self.x, self.y, self.z = self.x + x, self.y + y, self.z + z

    def offset2(self, other):
        """
        Offsets the x and y coordinates of a point by those of another point

        :param other: Another point
        :return: A new point with the translated x and y coordinates
        """
        return Vector(self.x - other.x, self.y - other.y, self.z)

    def to_tuple2(self):
        """
        Returns the x and y coordinates of the point as a tuple
        """
        return self.x, self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

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
        if type(lower) != type(Vector):
            Vector(*lower)
        if type(upper) != type(Vector):
            Vector(*upper)
        self.x = PgpMath.clamp(self.x, lower.x, upper.x)
        self.y = PgpMath.clamp(self.y, lower.y, upper.y)

    def __eq__(self, other):
        return False if (other is None or type(other) != type(Vector)) else self.__equals(other)
