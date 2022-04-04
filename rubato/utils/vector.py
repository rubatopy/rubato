"""
A vector implementation.
"""
from __future__ import annotations
from typing import Iterator, Union, List, Tuple
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
        Takes the dot product of vectors.

        Args:
            other: The other vector.

        Returns:
            Union[float, int]: The resulting dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector) -> Union[float, int]:
        """
        Takes the cross product of vectors.

        Args:
            other: The other vector.

        Returns:
            Union[float, int]: The resulting cross product.
        """
        return self.x * other.y - self.y * other.x

    def clamp(self, lower: Union[Vector, int, float], upper: Union[Vector, int, float], absolute: bool = False):
        """
        Clamps x and y between the two values given.

        Args:
            lower: The lower bound.
            upper: The upper bound.
            absolute: Whether to clamp the absolute value of the vector
                instead of the actual value.
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

    def unit(self) -> Vector:
        """Returns the unit vector of this vector."""
        inv_mag = (self.x * self.x + self.y * self.y)**-.5
        return Vector(self.x * inv_mag, self.y * inv_mag)

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

    @property
    def angle(self) -> float:
        """The angle of the vector"""
        return math.atan2(self.y, self.x)

    def transform(self, scale, rotation) -> Vector:
        """
        Transforms the vector by the scale and rotation, relative to the original vector.

        Args:
            scale: The scale by which the vector's length is multiplied.
            rotation: The angle by which the vector angle is rotated counterclockwise in degrees.

        Returns:
            Vector: The newly transformed Vector (based on the parent).
        """
        new_vector = self.clone()
        if rotation != 0:
            hyp, angle = self.magnitude, self.angle + rotation * math.pi / 180
            new_vector.x, new_vector.y = math.cos(angle) * hyp, math.sin(angle) * hyp

        new_vector.x *= scale
        new_vector.y *= scale
        return new_vector

    def to_int(self) -> Vector:
        """Returns a new vector with values that are ints."""
        return Vector(int(self.x), int(self.y))

    def tuple_int(self) -> tuple:
        """Returns a tuple with rounded values."""
        return int(self.x), int(self.y)

    def clone(self) -> Vector:
        """Returns a copy of the vector."""
        return Vector(*self)

    def lerp(self, target: Vector, t: float) -> Vector:
        """
        Lerps the current vector to target by a factor of t.

        Args:
            target: The target Vector.
            t: The lerping amount (between 0 and 1).

        Returns:
            Vector: The resulting vector.
        """
        t = Math.clamp(t, 0, 1)
        return Vector(Math.lerp(self.x, target.x, t), Math.lerp(self.y, target.y, t))

    def round(self, decimal_places: int = 0):
        """
        Rounds x and y to a number of decimal places.

        Args:
            decimal_places: The amount of decimal places rounded to.
        """
        self.x = round(self.x, decimal_places)
        self.y = round(self.y, decimal_places)

    def ceil(self) -> Vector:
        """
        Ceil the X and Y values of the Vector.

        Returns:
            Vector: The "Ceil"ed Vector.
        """
        return Vector(math.ceil(self.x), math.ceil(self.y))

    def floor(self) -> Vector:
        """
        Floors the X and Y values of the Vector

        Returns:
            Vector: The "Floor"ed Vector
        """
        return Vector(math.floor(self.x), math.floor(self.y))

    def abs(self) -> Vector:
        """
        Absolute value of the Vector.

        Returns:
            Vector: The absolute valued Vector
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
        return Vector.from_radial(1, math.atan2(other.y - self.y, other.x - self.x))

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

    @staticmethod
    def is_vectorlike(subscriptable: Vector | List[int | float] | Tuple[int | float]):
        """
        Checks whether a subscriptable object is vector_like ie. length 2, handles error message.

        Args:
            subscriptable: An object to check whether it is length 2 and subscriptable.

        Returns:
            bool: True if length 2, False if not, and raises an error if wrong type.

        Example:
            >>> Vector.is_vectorlike((0, 0))
            True
            >>> Vector.is_vectorlike((0, 0, 0))
            False
        """
        try:
            return isinstance(subscriptable,
                              Vector) or (len(subscriptable) == 2 and isinstance(subscriptable[0], (int, float)))
        except TypeError as trace:
            raise TypeError(f"{subscriptable} should be a list | tuple | Vector not a {subscriptable.__class__}.")\
                .with_traceback(trace.__traceback__)

    def __eq__(self, o: Vector) -> bool:
        if isinstance(o, Vector):
            return self.y == o.y and self.x == o.x
        return False

    def __gt__(self, other: Vector) -> bool:
        return self.x > other.x and self.y > other.y

    def __lt__(self, other: Vector) -> bool:
        return self.x < other.x and self.y < other.y

    def __ge__(self, other: Vector) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other: Vector) -> bool:
        return self.x <= other.x and self.y <= other.y

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

    def __rsub__(self, other: int | float) -> Vector:
        return Vector(other - self.x, other - self.y)

    def __truediv__(self, other: any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)

    def __rtruediv__(self, other: int | float) -> Vector:
        return Vector(other / self.x, other / self.y)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __iter__(self) -> Iterator[int]:
        return iter([self.x, self.y])
