"""
A vector implementation.
"""
from __future__ import annotations
from typing import Iterator, Union
import math

from . import Math


class Vector:
    """
    A Vector object that defines a 2D point in space

    Attributes:
        x (Union[float, int]): The x coordinate.
        y (Union[float, int]): The y coordinate.
    """

    def __init__(self, x: Union[float, int] = 0, y: Union[float, int] = 0):
        """
        Initializes a vector.

        Args:
            x: The x coordinate. Defaults to 0.
            y: The y coordinate. Defaults to 0.
        """
        self.x, self.y = x, y

    @property
    def magnitude(self) -> float:
        """The magnitude of the vector."""
        return (self.x * self.x + self.y * self.y)**.5

    @magnitude.setter
    def magnitude(self, value: Union[float, int]):
        if self.x == self.y == 0:
            return
        ratio = value * (self.x * self.x + self.y * self.y)**-.5
        self.x *= ratio
        self.y *= ratio

    @property
    def mag_squared(self) -> float:
        """The squared magnitude of the vector."""
        return self.x * self.x + self.y * self.y

    @property
    def angle(self) -> float:
        """The angle of the vector"""
        return math.atan2(self.y, self.x)

    def unit(self) -> Vector:
        """Returns the unit vector of this vector."""
        inv_mag = (self.x * self.x + self.y * self.y)**-.5
        return Vector(self.x * inv_mag, self.y * inv_mag)

    def translate(self, x: Union[float, int], y: Union[float, int]):
        """
        Translates the vector's x y and z coordinates by some constants.

        Args:
            x: The change in x.
            y: The change in y.
        """
        self.x, self.y = self.x + x, self.y + y

    def to_tuple(self) -> tuple:
        """
        Returns the x and y coordinates of the vector as a tuple.
        """
        return (*self,)

    def dot(self, other: Vector) -> Union[float, int]:
        """
        Takes the dot product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            Union[float, int]: The resulting dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector) -> Union[float, int]:
        """
        Takes the cross product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            Union[float, int]: The resultant scalar magnitude of the orthogonal vector along an imaginary z-axis.
        """
        return self.x * other.y - self.y * other.x

    def perpendicular(self, scalar: Union[float, int]) -> Vector:
        """
        Computes a scaled 90 degree clockwise rotation on a given vector.

        Args:
            scalar (Union[float, int]): The scalar value.

        Returns:
            Vector: The resultant vector when transformed.
        """
        return Vector(scalar * self.y, -scalar * self.x)

    def clamp(self, lower: Union[Vector, int, float], upper: Union[Vector, int, float], absolute: bool = False):
        """
        Clamps x and y between the two values given.

        Args:
            lower (Union[Vector, int, float]): The lower bound.
                If a vector is specified, its x coord is used to clamp the x coordinate and same for y.
            upper (Union[Vector, int, float]): The upper bound.
                If a vector is specified, its x coord is used to clamp the x coordinate and same for y.
            absolute (bool): Whether to clamp the absolute value of the vector
                instead of the actual value. Defaults to False.
        """
        if not isinstance(lower, Vector):
            lower = Vector(*lower)
        if not isinstance(upper, Vector):
            upper = Vector(*upper)

        if not absolute:
            self.x = Math.clamp(self.x, lower.x, upper.x)
            self.y = Math.clamp(self.y, lower.y, upper.y)
        else:
            self.x = Math.abs_clamp(self.x, lower.x, upper.x)
            self.y = Math.abs_clamp(self.y, lower.y, upper.y)

    def transform(self, scale: Union[float, int], rotation: Union[float, int]) -> Vector:
        """
        Transforms the vector by a scale and rotation.

        Args:
            scale (Union[float, int]): The scale by which the vector's length is multiplied.
            rotation (Union[float, int]): The angle by which the vector angle is rotated counterclockwise, in degrees.

        Returns:
            Vector: The transformed Vector.
        """
        hyp, angle = self.magnitude * scale, self.angle + rotation * math.pi / 180
        return Vector(math.cos(angle) * hyp, math.sin(angle) * hyp)

    def rotate(self, angle: Union[float, int]) -> Vector:
        """
        Rotates the vector by a given number of degees.

        Args:
            angle (Union[float, int]): The counterclockwise rotation amount in degrees.

        Returns:
            Vector: The resultant Vector.
        """
        c, s = math.cos(angle), math.sin(angle)
        return Vector(self.x * c - self.y * s, self.x * s + self.y * c)

    def to_int(self) -> Vector:
        """Returns a new vector with values that are ints."""
        return Vector(int(self.x), int(self.y))

    def tuple_int(self) -> tuple:
        """Returns a tuple with rounded values."""
        return int(self.x), int(self.y)

    def clone(self) -> Vector:
        """Returns a copy of the vector."""
        return Vector(self.x, self.y)

    def lerp(self, target: Vector, t: float) -> Vector:
        """
        Lerps the current vector to target by a factor of t.

        Args:
            target: The target Vector.
            t: The lerping amount (between 0 and 1).

        Returns:
            Vector: The resulting vector.
        """
        return Vector(Math.lerp(self.x, target.x, t), Math.lerp(self.y, target.y, t))

    def round(self, decimal_places: int = 0):
        """
        Returns a new vector with the coordinates rounded.

        Args:
            decimal_places: The amount of decimal places rounded to. Defaults to 0.

        Returns:
            Vector: The resultant Vector.
        """
        return Vector(round(self.x, decimal_places), round(self.y, decimal_places))

    def ceil(self) -> Vector:
        """
        Returns a new vector with the coordinates ciel-ed.

        Returns:
            Vector: The resultant Vector.
        """
        return Vector(math.ceil(self.x), math.ceil(self.y))

    def floor(self) -> Vector:
        """
        Returns a new vector with the coordinates floored.

        Returns:
            Vector: The resultant Vector.
        """
        return Vector(math.floor(self.x), math.floor(self.y))

    def abs(self) -> Vector:
        """
        Returns a new vector with the absolute value of the original coordinates.

        Returns:
            Vector: The resultant Vector.
        """
        return Vector(abs(self.x), abs(self.y))

    def dir_to(self, other: Vector) -> Vector:
        """
        Direction from the Vector to another Vector.

        Args:
            other: the position to which you are pointing

        Returns:
            A unit vector that is in the direction to the position passed in
        """
        return (other - self).unit()

    @staticmethod
    def from_radial(magnitude: float, angle: float) -> Vector:
        """
        Gives you a Vector from the given direction and distance.

        Args:
            magnitude: Length of vector.
            angle: Direction of vector in radians.

        Returns:
            Vector: Vector from the given direction and distance
        """
        return Vector(math.cos(angle) * magnitude, math.sin(angle) * magnitude)

    @classmethod
    @property
    def zero(cls):
        """A zeroed Vector"""
        return Vector(0, 0)

    @classmethod
    @property
    def one(cls):
        """A Vector with all ones"""
        return Vector(1, 1)

    @classmethod
    @property
    def up(cls):
        """A Vector in the up direction"""
        return Vector(0, -1)

    @classmethod
    @property
    def left(cls):
        """A Vector in the left direction"""
        return Vector(-1, 0)

    @classmethod
    @property
    def down(cls):
        """A Vector in the down direction"""
        return Vector(0, 1)

    @classmethod
    @property
    def right(cls):
        """A Vector in the right direction"""
        return Vector(1, 0)

    @classmethod
    @property
    def infinity(cls):
        """A Vector at positive infinity"""
        return Vector(Math.INF, Math.INF)

    def __eq__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return self.y == other.y and self.x == other.x
        return False

    def __gt__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return self.x > other.x and self.y > other.y
        return False

    def __lt__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return self.x < other.x and self.y < other.y
        return False

    def __ge__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return self.x >= other.x and self.y >= other.y
        return False

    def __le__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return self.x <= other.x and self.y <= other.y
        return False

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"

    def __pow__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x**other, self.y**other)
        if isinstance(other, Vector):
            return Vector(self.x**other.x, self.y**other.y)

    def __mul__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

    def __add__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

    __rmul__ = __mul__
    __radd__ = __add__

    def __sub__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: any) -> Vector:
        return Vector(other - self.x, other - self.y)

    def __truediv__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

    def __rtruediv__(self, other: any) -> Vector:
        return Vector(other / self.x, other / self.y)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __iter__(self) -> Iterator[int]:
        return iter([self.x, self.y])
