"""
A vector implementation.
"""
from __future__ import annotations
import cython
from typing import Any, Iterator
import math, random

from . import Math, raise_operator_error


@cython.cclass
class Vector:
    """
    A Vector object that defines a 2D point in space

    Args:
        x: The x coordinate. Defaults to 0.
        y: The y coordinate. Defaults to 0.

    Attributes:
        x (float): The x coordinate.
        y (float): The y coordinate.
    """
    x = cython.declare(cython.float, visibility="public")
    y = cython.declare(cython.float, visibility="public")

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
        """The angle of the vector degrees (readonly)."""
        return -math.degrees(math.atan2(-self.y, self.x) - Math.PI_HALF)

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
        mag: Vector = self.rationalized_mag_vector.to_int()
        no_root = mag.y == 1  # No square root in the answer.

        num_dem1: Vector = Vector(*Math.simplify(round(self.x), mag.x))
        num_dem2: Vector = Vector(*Math.simplify(round(self.y), mag.x))

        if no_root:
            return f"<{num_dem1.x}/{num_dem1.y}, {num_dem2.x}/{num_dem2.y}>"
        return f"<{num_dem1.x}/{num_dem1.y}√{mag.y}, {num_dem2.x}/{num_dem2.y}√{mag.y}>"

    def normalized(self, out: Vector = None) -> Vector:
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
        self.normalized(self)

    def sum(self):
        """
        Sums the x and y coordinates of the vector.
        """
        return self.x + self.y

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
        # note using matrix determinant
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
        Rotates the vector by a given number of degrees.

        Args:
            angle: The rotation amount in north-degrees you want to rotate by (relative).
            out: The output vector to set to. Defaults to a new vector.
                If you want the function to act on itself, set this value to the reference of the vector.

        Returns:
            The resultant Vector.
        """
        if out is None:
            out = Vector()

        radians = math.radians(-angle)
        c, s = math.cos(radians), math.sin(radians)
        out.x, out.y = round(self.x * c - self.y * s, 10), round(self.x * s + self.y * c, 10)

        return out

    def to_int(self) -> Vector:
        """Returns a new vector with values that are ints."""
        return Vector(int(self.x), int(self.y))

    def tuple_int(self) -> tuple:
        """Returns a tuple with rounded values."""
        return int(self.x), int(self.y)

    def clone(self) -> Vector:
        """Returns a copy of the vector."""
        return Vector(self.x, self.y)

    def lerp(self, target: Vector, t: float | int, out: Vector = None) -> Vector:
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
        base = (other - self).normalized()
        return base

    def distance_between(self, other: Vector) -> float:
        """
        Finds the pythagorean distance between two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The distance.
        """
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    @staticmethod
    def from_radial(magnitude: float | int, angle: float | int) -> Vector:
        """
        Generates a Vector from the given angle and magnitude.

        Args:
            magnitude: Length of vector.
            angle: Direction of vector in North degrees.

        Returns:
            Vector from the given direction and distance
        """
        radians = math.radians(-(angle - 90))

        return Vector(round(math.cos(radians), 10) * magnitude, -round(math.sin(radians), 10) * magnitude)

    @staticmethod
    def clamp_magnitude(vector: Vector, max_magnitude: float | int, min_magnitude: float | int = 0) -> Vector:
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
        magnitude = vector_c.magnitude
        new = Math.clamp((magnitude), min_magnitude, max_magnitude)
        if new != magnitude:
            vector_c.magnitude = new

        return vector_c

    @classmethod
    def angle_between(cls, a: Vector, b: Vector) -> float:
        """
        Returns the smallest possible angle between two vectors.

        Args:
            a: First vector.
            b: Second vector.

        Returns:
            Angle in degrees between the two vectors.
        """
        return round(math.degrees(math.acos((a.dot(b)) / (a.magnitude * b.magnitude))), 10)

    @classmethod
    def rand_unit_vector(cls) -> Vector:
        """
        Returns a random unit vector inside the unit circle.

        Returns:
            Random vector inside the unit circle.
        """
        return cls.from_radial(1, random.random() * 360)

    @staticmethod
    def zero():
        """A zeroed Vector"""
        return Vector(0, 0)

    @staticmethod
    def one() -> Vector:
        """A Vector with all ones"""
        return Vector(1, 1)

    @staticmethod
    def up():
        """A Vector in the up direction"""
        return Vector(0, -1)

    @staticmethod
    def left():
        """A Vector in the left direction"""
        return Vector(-1, 0)

    @staticmethod
    def down():
        """A Vector in the down direction"""
        return Vector(0, 1)

    @staticmethod
    def right():
        """A Vector in the right direction"""
        return Vector(1, 0)

    @staticmethod
    def infinity():
        """A Vector at positive infinity"""
        return Vector(Math.INF, Math.INF)

    def __eq__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x == other[0] and self.y == other[1]
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __gt__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x > other[0] and self.y > other[1]
        raise_operator_error(">", self, other)

    def __lt__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x < other[0] and self.y < other[1]
        raise_operator_error("<", self, other)

    def __ge__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x >= other[0] and self.y >= other[1]
        raise_operator_error(">=", self, other)

    def __le__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x <= other[0] and self.y <= other[1]
        raise_operator_error("<=", self, other)

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"

    def __pow__(self, other: Any, mod: float | int) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(pow(self.x, other, mod), pow(self.y, other, mod))
        if isinstance(other, (Vector, tuple, list)):
            return Vector(pow(self.x, other[0], mod), pow(self.y, other[1], mod))
        raise_operator_error("**", self, other)

    def __ipow__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(pow(self.x, other), pow(self.y, other))
        if isinstance(other, (Vector, tuple, list)):
            return Vector(pow(self.x, other[0]), pow(self.y, other[1]))
        raise_operator_error("**", self, other)

    def __mul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        raise_operator_error("*", self, other)

    def __add__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        raise_operator_error("+", self, other)

    def __imul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        raise_operator_error("*", self, other)

    def __iadd__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        raise_operator_error("+", self, other)

    def __rmul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        raise_operator_error("*", self, other)

    def __radd__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        raise_operator_error("+", self, other)

    def __sub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x - other[0], self.y - other[1])
        raise_operator_error("-", self, other)

    def __rsub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other - self.x, other - self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] - self.x, other[1] - self.y)
        raise_operator_error("-", other, self)

    def __isub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x - other[0], self.y - other[1])
        raise_operator_error("-", self, other)

    def __truediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x / other[0], self.y / other[1])
        raise_operator_error("/", self, other)

    def __rtruediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other / self.x, other / self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] / self.x, other[1] / self.y)
        raise_operator_error("/", other, self)

    def __itruediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x / other[0], self.y / other[1])
        raise_operator_error("/", self, other)

    def __floordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            print(repr(self))
            return Vector(self.x // other, self.y // other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x // other[0], self.y // other[1])
        raise_operator_error("//", self, other)

    def __rfloordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other // self.x, other // self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] // self.x, other[1] // self.y)
        raise_operator_error("//", other, self)

    def __ifloordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            print(repr(self))
            return Vector(self.x // other, self.y // other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x // other[0], self.y // other[1])
        raise_operator_error("//", self, other)

    def __mod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x % other, self.y % other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x % other[0], self.y % other[1])
        raise_operator_error("%", self, other)

    def __rmod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other % self.x, other % self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] % self.x, other[1] % self.y)
        raise_operator_error("%", other, self)

    def __imod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x % other, self.y % other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x % other[0], self.y % other[1])
        raise_operator_error("%", self, other)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __iter__(self) -> Iterator[int | float]:
        return iter([self.x, self.y])

    def __repr__(self):
        return f"rubato.Vector({self.x}, {self.y}) at {hex(id(self))}"

    def __getitem__(self, index: int) -> int | float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Vector index of {index} out of range (should be 0 or 1)")

    def __setitem__(self, index: int, value: int | float):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(f"Vector index of {index} out of range (should be 0 or 1)")

    def __len__(self) -> int:
        return 2


# Developer notes:
# Angles are north degrees (clockwise from the +y-axis).
# We do not use the built-in Math conversion functions, because they will just bloat our stack.
