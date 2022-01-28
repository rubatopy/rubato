"""
A vector implementation.
"""
from rubato.utils import PMath, classproperty
import math


class Vector:
    """
    A Vector object that defines a 2D point in space

    :param x: The x coordinate.
    :param y: The y coordinate.
    """

    def __init__(self, x: float | int = 0, y: float | int = 0):
        self.x, self.y = x, y

    def translate(self, x: float | int, y: float | int):
        """
        Translates the vector's x y and z coordinates by some constants

        :param x: The change in x.
        :param y: The change in y.
        """
        self.x, self.y = self.x + x, self.y + y

    def offset(self, other: "Vector") -> "Vector":
        """
        Offsets the x and y coordinates of a vector by those of another vector

        :param other: Another vector
        :return: A new vector with the translated x and y coordinates
        """
        return Vector(self.x - other.x, self.y - other.y)

    def to_tuple(self) -> tuple:
        """
        Returns the x and y coordinates of the vector as a tuple
        """
        return self.x, self.y

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def crossp(self):
        return Vector(self.y, -self.x)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __mul__(self, other: any) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    __rmul__ = __mul__
    __radd__ = __add__

    def __sub__(self, other: any) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: int | float) -> "Vector":
        return Vector(other - self.x, other - self.y)

    def __truediv__(self, other: any) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

    def __rtruediv__(self, other: int | float) -> "Vector":
        return Vector(other / self.x, other / self.y)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    # pylint: disable=invalid-name
    @classproperty
    def ZERO(self):
        return Vector(0, 0)

    @classproperty
    def ONE(self):
        return Vector(1, 1)

    @classproperty
    def TWO(self):
        return Vector(2, 2)

    @classproperty
    def UP(self):
        return Vector(0, -1)

    @classproperty
    def LEFT(self):
        return Vector(-1, 0)

    @classproperty
    def DOWN(self):
        return Vector(0, 1)

    @classproperty
    def RIGHT(self):
        return Vector(1, 0)

    @classproperty
    def INFINITY(self):
        return Vector(PMath.INFINITY, PMath.INFINITY)

    def __equals(self, v: "Vector") -> bool:
        """
        Determines if if the x and y components of the vector are equal.

        :param v: The vector to compare.
        :return: True if the x and y components of the vector are equal
        """
        return self.y == v.y and self.x == v.x

    def clamp(self, lower: any, upper: any, absolute: bool = False):
        """
        Clamps x and y between the two vectors given

        :param absolute: Whether to clamp the absolute value of the vector
            instead of the actual value
        :param lower: The lower bound
        :param upper: The upper bound
        """
        if not isinstance(lower, Vector):
            lower = Vector(*lower)
        if not isinstance(upper, Vector):
            upper = Vector(*upper)
        if not absolute:
            self.x = PMath.clamp(self.x, lower.x, upper.x)
            self.y = PMath.clamp(self.y, lower.y, upper.y)
        else:
            self.x = PMath.abs_clamp(self.x, lower.x, upper.x)
            self.y = PMath.abs_clamp(self.y, lower.y, upper.y)

    def __eq__(self, other: "Vector") -> bool:
        return False if (other is None or not isinstance(other, Vector)
                         ) else self.__equals(other)

    @property
    def magnitude(self) -> float:
        """Returns the magnitude of the vector"""
        return (self.x**2 + self.y**2)**.5

    @magnitude.setter
    def magnitude(self, value):
        """Sets the magnitude of a vector"""
        mag = self.magnitude
        if mag == 0: return
        ratio = value / mag
        self.x *= ratio
        self.y *= ratio

    def normalize(self):
        self.magnitude = 1

    def unit(self):
        copy = self.clone()
        copy.normalize()
        return copy

    @staticmethod
    def from_radial(angle: float, magnitude: float) -> "Vector":
        """
        Gives you a Vector from the given direction and distance

        :param angle: Direction of vector in radians
        :param magnitude: Length of vector
        :return: Vector from the given direction and distance
        """
        return Vector(math.cos(angle) * magnitude, math.sin(angle) * magnitude)

    @property
    def angle(self) -> float:
        """Returns the angle of the vector"""
        return math.atan2(self.y, self.x)

    def transform(self, scale, rotation):
        newVector = self.clone()
        if rotation != 0:
            hyp, angle = self.magnitude, self.angle + rotation * math.pi / 180
            newVector.x, newVector.y = math.cos(angle) * hyp, math.sin(
                angle) * hyp

        newVector.x *= scale
        newVector.y *= scale
        return newVector

    def invert(self, axis: str):
        """
        Inverts the vector in the axis given

        :param axis: The axis to invert the vector in
        """

        if axis == "x":
            self.x = -self.x
        elif axis == "y":
            self.y = -self.y
        else:
            raise ValueError(f"{axis} is not a valid axis")

    def to_int(self) -> "Vector":
        return Vector(int(self.x), int(self.y))

    def clone(self) -> "Vector":
        return Vector(self.x, self.y)

    def lerp(self, target: "Vector", t: float):
        """
        changes its values x and y to fit the target vector by amount t

        :param target: the target velocity
        :param t: the amount you lerp between 0 and 1
        """
        t = PMath.clamp(t, 0, 1)
        return Vector(PMath.lerp(self.x, target.x, t),
                      PMath.lerp(self.y, target.y, t))

    def round(self, decimal_places: int) -> "Vector":
        """
        rounds x and y to decimal_places

        :param decimal_places: the amount of decimal places rounded to.
        :return: The rounded vector
        """
        self.x = round(self.x, decimal_places)
        self.y = round(self.y, decimal_places)
        return self

    def ceil(self) -> "Vector":
        """
        Returns the cieled vector

        :return: The vector
        """

        return Vector(math.ceil(self.x), math.ceil(self.y))

    def direction_to(self, vector):
        """
        treating vectors as points the direction to the new point from the
            current point
        :return: direction to new point
        """
        d_x = self.x - vector.x
        d_y = self.y - vector.y
        direction = math.atan2(d_y, d_x)
        return direction

    def distance_to(self, vector):
        """
        treating vectors as points the distance to the new point from
            the current point
        :return: distance to new point
        """
        d_x = self.x - vector.x
        d_y = self.y - vector.y
        distance = math.sqrt(d_x**2 + d_y**2)
        return distance

    def absolute(self):
        """
        :return: a vector representing the absolute values of the current vector
        """
        return Vector(abs(self.x), abs(self.y))

    def __gt__(self, other) -> bool:
        """
        :return: bool value indicating whether both values of a are greater
            than b
        """
        return self.x > other.x and self.y > other.y

    def __lt__(self, other) -> bool:
        """
        :return: bool value indicating whether both values of a are small than b
        """
        return self.x < other.x and self.y < other.y

    def __ge__(self, other) -> bool:
        """
        :return: bool value indicating whether both values of a are greater
            or equal than b
        """
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other) -> bool:
        """
        :return: bool value indicating whether both values of a are smaller
            than or equal to b
        """
        return self.x <= other.x and self.y <= other.y
