"""
A vector implementation.
"""
from __future__ import annotations
from typing import Iterator
import math, random

from . import Math


class Vector:
    """
    A Vector object that defines a 2D point in space

    Args:
        x: The x coordinate. Defaults to 0.
        y: The y coordinate. Defaults to 0.

    Attributes:
        x (float | int): The x coordinate.
        y (float | int): The y coordinate.
    """

    def __init__(self, x: float | int = 0, y: float | int = 0):
        if type(x) in (float, int) and type(y) in (float, int):
            self.x, self.y = x, y
        else:
            raise TypeError(f"Vector must be initialized with two numbers (float or int) not: {x, y}.")

    @property
    def magnitude(self) -> float:
        """The magnitude of the vector. You can set to this value."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    @magnitude.setter
    def magnitude(self, value: float | int):
        if self.x == self.y == 0:
            return
        ratio = value * math.sqrt((self.x * self.x + self.y * self.y)**-1)
        self.x *= ratio
        self.y *= ratio

    @property
    def mag_sq(self) -> float:
        """The squared magnitude of the vector (readonly)."""
        return self.x * self.x + self.y * self.y

    @property
    def angle(self) -> float:
        """The angle of the vector in radians (readonly)."""
        return -math.degrees(math.atan2(self.y, self.x)) + 90

    @property
    def rationalized_mag(self) -> str:
        """
        Returns a string representation of a rationalized vector magnitude as you would use in math class.

        Example:
            >>> Vector(8, 8).rationalized_mag
            4√8

        Warnings:
            Should only be used on vectors with integer components.
        """
        divisible_by = Math.simplify_sqrt(round(self.mag_sq))

        return f"{divisible_by[0] if divisible_by[0] != 1 else ''}√{divisible_by[1]}"

    @property
    def rationalized_mag_vector(self) -> Vector:
        """
        Returns a vector with the rationalized magnitude.

        Example:
            >>> Vector(8, 8).rationalized_mag
            rubato.Vector(4, 8)

        Warnings:
            Should only be used on vectors with integer components.
        """
        return Vector(*Math.simplify_sqrt(round(self.mag_sq)))

    @property
    def rationalized_unit(self) -> str:
        """
        Returns a string representation of a rationalized unit vector as you would use in math class.

        Warnings:
            Should only be used on vectors with integer components.
        """
        mag: Vector = self.rationalized_mag_vector
        mag = mag.to_int()
        no_root = mag.y == 1  # No square root in the answer.

        num_dem1: Vector = Vector(*Math.simplify(round(self.x), mag.x))
        num_dem2: Vector = Vector(*Math.simplify(round(self.y), mag.x))

        if no_root:
            return f"<{num_dem1.x}/{num_dem1.y}, {num_dem2.x}/{num_dem2.y}>"
        return f"<{num_dem1.x}/{num_dem1.y}√{mag.y}, {num_dem2.x}/{num_dem2.y}√{mag.y}>"

    def unit(self, out: Vector = None) -> Vector:
        """
        Determines the unit vector of this vector.

        Args:
            out (Vector, optional): The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            Vector: The vector output of the operation.
        """
        if out is None:
            out = Vector()

        if self.mag_sq != 0:
            inv_mag = 1 / math.sqrt(self.mag_sq)
        else:
            inv_mag = 0

        out.x, out.y = round(self.x * inv_mag, 10), round(self.y * inv_mag, 10)

        return out

    def normalize(self):
        """
        Normalizes the current vector.
        """
        self.unit(self)

    def to_tuple(self) -> tuple:
        """
        Returns the x and y coordinates of the vector as a tuple.
        """
        return (*self,)

    def dot(self, other: Vector) -> float | int:
        """
        Takes the dot product of two vectors.

        Args:
            other: The other vector.

        Returns:
            The resulting dot product.
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector) -> float | int:
        """
        Takes the cross product of two vectors.

        Args:
            other: The other vector.

        Returns:
            The resultant scalar magnitude of the orthogonal vector along an imaginary z-axis.
        """
        return self.x * other.y - self.y * other.x

    def perpendicular(self, scalar: float | int = 1, out: Vector = None) -> Vector:
        """
        Computes a scaled 90 degree clockwise rotation on a given vector.

        Args:
            scalar: The scalar value.
            out: The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            The resultant vector when transformed.
        """
        if out is None:
            out = Vector()

        out.x, out.y = scalar * self.y, -scalar * self.x

        return out

    def clamp(
        self, lower: Vector | float | int, upper: Vector | float | int, absolute: bool = False, out: Vector = None
    ):
        """
        Clamps x and y between the two values given.

        Args:
            lower: The lower bound.
                If a vector is specified, its x coord is used to clamp the x coordinate and same for y.
            upper: The upper bound.
                If a vector is specified, its x coord is used to clamp the x coordinate and same for y.
            absolute: Whether to clamp the absolute value of the vector
                instead of the actual value. Defaults to False.
            out: The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.
        """
        if out is None:
            out = Vector()

        if not isinstance(lower, Vector):
            lower = Vector(lower, lower)
        if not isinstance(upper, Vector):
            upper = Vector(upper, upper)

        out.x = Math.clamp(self.x, lower.x, upper.x)
        out.y = Math.clamp(self.y, lower.y, upper.y)

        if absolute:
            out.x = abs(out.x)
            out.y = abs(out.y)

        return out

    def rotate(self, angle: float | int, out: Vector = None) -> Vector:
        """
        Rotates the vector by a given number of degees.

        Args:
            angle: The counterclockwise rotation amount in degrees.
            out: The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            The resultant Vector.
        """
        if out is None:
            out = Vector()

        radians = -math.radians(angle)
        c, s = math.cos(radians), math.sin(radians)
        out.x, out.y = round(self.x * c - self.y * s, 10), round(self.x * s + self.y * c, 10)

        return out

    def to_int(self) -> Vector:
        """Returns a new vector with values that are ints."""
        return Vector(round(self.x), round(self.y))

    def tuple_int(self) -> tuple:
        """Returns a tuple with rounded values."""
        return int(self.x), int(self.y)

    def clone(self) -> Vector:
        """Returns a copy of the vector."""
        return Vector(self.x, self.y)

    def lerp(self, target: Vector, t: float, out: Vector = None) -> Vector:
        """
        Lerps the current vector to target by a factor of t.

        Args:
            target: The target Vector.
            t: The lerping amount (between 0 and 1).
            out: The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            The resulting vector.
        """
        if out is None:
            out = Vector()

        out.x, out.y = Math.lerp(self.x, target.x, t), Math.lerp(self.y, target.y, t)

        return out

    def round(self, decimal_places: int = 0, out: Vector = None):
        """
        Returns a new vector with the coordinates rounded.

        Args:
            decimal_places: The amount of decimal places rounded to. Defaults to 0.
            out (Vector, optional): The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            Vector: The resultant Vector.
        """
        if out is None:
            out = Vector()

        out.x, out.y = round(self.x, decimal_places), round(self.y, decimal_places)

        return out

    def ceil(self, out: Vector = None) -> Vector:
        """
        Returns a new vector with the coordinates ciel-ed.

        Args:
            out (Vector, optional): The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            Vector: The resultant Vector.
        """
        if out is None:
            out = Vector()

        out.x, out.y = math.ceil(self.x), math.ceil(self.y)

        return out

    def floor(self, out: Vector = None) -> Vector:
        """
        Returns a new vector with the coordinates floored.

        Args:
            out (Vector, optional): The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            Vector: The resultant Vector.
        """
        if out is None:
            out = Vector()

        out.x, out.y = math.floor(self.x), math.floor(self.y)

        return out

    def abs(self, out: Vector = None) -> Vector:
        """
        Returns a new vector with the absolute value of the original coordinates.

        Args:
            out (Vector, optional): The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            Vector: The resultant Vector.
        """
        if out is None:
            out = Vector()

        out.x, out.y = abs(self.x), abs(self.y)

        return out

    def dir_to(self, other: Vector) -> Vector:
        """
        Direction from the Vector to another Vector.

        Args:
            other: the position to which you are pointing

        Returns:
            A unit vector that is in the pointing to the other position passed in
        """
        base = (other - self).unit()
        return base

    def distance_between(self, other: Vector) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    @staticmethod
    def from_radial(magnitude: float, angle: float) -> Vector:
        """
        Generates a Vector from the given angle and magnitude.

        Args:
            magnitude: Length of vector.
            angle: Direction of vector in degrees.

        Returns:
            Vector from the given direction and distance
        """
        radians = math.radians(angle)

        # This is needed because otherwise an angle multiple of 360 will set the x to -0.
        if angle > 0 and angle % 360 == 0:
            return Vector(0, magnitude)

        return Vector(round(math.sin(radians), 10) * magnitude, round(math.cos(radians), 10) * magnitude)

    @staticmethod
    def clamp_magnitude(vector: Vector, max_magnitude: float, min_magnitude: float = 0) -> Vector:
        """
        Clamps the magnitude of the vector to the given range.

        Args:
            vector: The vector to clamp.
            max_magnitude: The maximum magnitude of the vector.
            min_magnitude: The minimum magnitude of the vector. Defaults to 0.

        Returns:
            A new vector with the magnitude clamped to the given range.
        """
        vector_c = vector.clone()
        if (new := Math.clamp((magnitude := vector_c.magnitude), min_magnitude, max_magnitude)) != magnitude:
            vector_c.magnitude = new

        return vector_c

    @classmethod
    def angle_between(cls, a: Vector, b: Vector) -> float:
        """
        Returns the angle between two vectors (0 <= theta <= pi).

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Angle in degrees between the two vectors.
        """
        return round(math.degrees(math.acos((a.dot(b)) / (a.magnitude * b.magnitude))), 10)

    @classmethod
    def random_inside_unit_circle(cls) -> Vector:
        """
        Returns a random unit vector inside the unit circle.

        Returns:
            Random vector inside the unit circle.
        """
        return cls.from_radial(1, random.random() * 360)

    @classmethod
    @property
    def zero(cls):
        """A zeroed Vector"""
        return Vector(0, 0)

    @classmethod
    @property
    def one(cls) -> Vector:
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

    def __hash__(self):
        return hash((self.x, self.y))

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

    def __repr__(self):
        return f"rubato.Vector({self.x}, {self.y}) at {hex(id(self))}"
