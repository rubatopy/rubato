"""
A vector implementation.
"""
from typing import Union
from rubato.utils import Math
import math


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

    def offset(self, other: "Vector") -> "Vector":
        """
        Offsets the x and y coordinates of a vector by those of another vector.

        Args:
            other: Another vector.

        Returns:
            Vector: A new vector with the translated x and y coordinates.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def to_tuple(self) -> tuple:
        """
        Returns the x and y coordinates of the vector as a tuple.
        """
        return self.x, self.y

    @staticmethod
    def from_tuple(coords: tuple) -> "Vector":
        """
        Returns a Vector from a coordinate tuple
        Args:
            coords: tuple with an x and y coordinate [float | int].

        Returns: Vector with specified coordinates.

        """
        return Vector(coords[0], coords[1])

    def dot(self, other: "Vector") -> Union[float, int]:
        """
        Takes the dot product of vectors.

        Args:
            other: The other vector.

        Returns:
            Union[float, int]: The resulting dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector") -> Union[float, int]:
        """
        Takes the cross product of vectors.

        Args:
            other: The other vector.

        Returns:
            Union[float, int]: The resulting cross product.
        """
        return self.x * other.y - self.y * other.x

    def crossp(self) -> "Vector":
        """
        Does `Vector(self.y, -self.x)`.

        Returns:
            Vector: The resulting vector.
        """
        return Vector(self.y, -self.x)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __mul__(self, other: any) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

    def __add__(self, other: any) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, Vector):
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

    @classmethod
    @property
    def zero(cls):
        return Vector(0, 0)

    @classmethod
    @property
    def one(cls):
        return Vector(1, 1)

    @classmethod
    @property
    def two(cls):
        return Vector(2, 2)

    @classmethod
    @property
    def up(cls):
        return Vector(0, -1)

    @classmethod
    @property
    def left(cls):
        return Vector(-1, 0)

    @classmethod
    @property
    def down(cls):
        return Vector(0, 1)

    @classmethod
    @property
    def right(cls):
        return Vector(1, 0)

    @classmethod
    @property
    def infinity(cls):
        return Vector(Math.INFINITY, Math.INFINITY)

    def _equals(self, v: "Vector") -> bool:
        return self.y == v.y and self.x == v.x

    def __eq__(self, other: "Vector") -> bool:
        return (other is None or not isinstance(other, Vector)
                or self._equals(other))

    def clamp(self,
              lower: Union["Vector", int, float],
              upper: Union["Vector", int, float],
              absolute: bool = False):
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
        """Returns the magnitude of the vector."""
        return (self.x**2 + self.y**2)**.5

    @property
    def mag(self) -> float:
        """Returns the squared magnitude of the vector."""
        return self.x**2 + self.y**2

    @magnitude.setter
    def magnitude(self, value: Union[float, int]):
        """Sets the magnitude of a vector."""
        mag = self.magnitude
        if mag == 0: return
        ratio = value / mag
        self.x *= ratio
        self.y *= ratio

    def normalize(self):
        """Normalize the vector."""
        self.magnitude = 1

    def unit(self) -> "Vector":
        """Returns the unit vector of this vector."""
        copy = self.clone()
        copy.normalize()
        return copy

    @staticmethod
    def from_radial(angle: float, magnitude: float) -> "Vector":
        """
        Gives you a Vector from the given direction and distance.

        Args:
            angle: Direction of vector in radians.
            magnitude: Length of vector.

        Returns:
            Vector: Vector from the given direction and distance
        """
        return Vector(math.cos(angle) * magnitude, math.sin(angle) * magnitude)

    @property
    def angle(self) -> float:
        """Returns the angle of the vector"""
        return math.atan2(self.y, self.x)

    def transform(self, scale, rotation):
        new_vector = self.clone()
        if rotation != 0:
            hyp, angle = self.magnitude, self.angle + rotation * math.pi / 180
            new_vector.x, new_vector.y = math.cos(angle) * hyp, math.sin(
                angle) * hyp

        new_vector.x *= scale
        new_vector.y *= scale
        return new_vector

    def invert(self, axis: str):
        """
        Inverts the vector in the axis given

        Args:
            axis: The axis to invert the vector in (x or y).

        Raises:
            ValueError: The value for axis is not "x" or "y"
        """

        if axis == "x":
            self.x = -self.x
        elif axis == "y":
            self.y = -self.y
        else:
            raise ValueError(f"{axis} is not a valid axis")

    def to_int(self) -> "Vector":
        """Returns a new vector with values that are ints."""
        return Vector(int(self.x), int(self.y))

    def clone(self) -> "Vector":
        """Returns a copy of the vector."""
        return Vector(self.x, self.y)

    def lerp(self, target: "Vector", t: float) -> "Vector":
        """
        Changes its values x and y to fit the target vector by amount t.

        Args:
            target: the target velocity.
            t: the amount you lerp between 0 and 1.

        Returns:
            Vector: The resulting vector.
        """
        t = Math.clamp(t, 0, 1)
        return Vector(Math.lerp(self.x, target.x, t),
                      Math.lerp(self.y, target.y, t))

    def round(self, decimal_places: int):
        """
        Rounds x and y to decimal_places

        Args:
            decimal_places: the amount of decimal places rounded to.
        """
        self.x = round(self.x, decimal_places)
        self.y = round(self.y, decimal_places)

    def ceil(self) -> "Vector":
        """
        Returns the cieled vector.
        """

        return Vector(math.ceil(self.x), math.ceil(self.y))

    def direction_to(self, vector: "Vector") -> float:
        """
        Treating vectors as points the direction to the other vector from the
        current vector.

        Args:
            vector: The other vector.

        Returns:
            float: The direction to the new vector in radians.
        """
        d_x = self.x - vector.x
        d_y = self.y - vector.y
        direction = math.atan2(d_y, d_x)
        return direction

    def distance_to(self, vector: "Vector") -> float:
        """
        Treating vectors as points the distance to the other vector from
        the current vector.

        Args:
            vector: The other vector.

        Returns:
            float: Distance to new vector.
        """
        d_x = self.x - vector.x
        d_y = self.y - vector.y
        distance = math.sqrt(d_x**2 + d_y**2)
        return distance

    def absolute(self) -> "Vector":
        """
        Returns a vector representing the absolute values of the current vector
        """
        return Vector(abs(self.x), abs(self.y))

    def __gt__(self, other) -> bool:
        return self.x > other.x and self.y > other.y

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y

    def __ge__(self, other) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y
