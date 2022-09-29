"""
An abstraction for a container of x and y values.
"""
from __future__ import annotations
import cython
from typing import Any, Iterator
import math, random

from . import Math, SideError


@cython.cclass
class Vector:
    """
    A Vector object that defines a 2D point in space

    Args:
        x: The x coordinate. Defaults to 0.
        y: The y coordinate. Defaults to 0.
    """
    x: float = cython.declare(cython.float, visibility="public")  # type: ignore
    """The x coordinate."""
    y: float = cython.declare(cython.float, visibility="public")  # type: ignore
    """The y coordinate."""

    def __init__(self, x: float | int = 0, y: float | int = 0):
        self.x = x
        self.y = y

    @property
    def magnitude(self) -> float:
        """The magnitude of the vector. You can set to this value."""
        return math.sqrt(self.x * self.x + self.y * self.y)

    @magnitude.setter
    def magnitude(self, value: float | int):
        if self.x == self.y == 0:
            return
        ratio = value / math.sqrt(self.x * self.x + self.y * self.y)
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
        mag: tuple[int, int] = self.rationalized_mag_vector.tuple_int()
        no_root = mag[1] == 1  # No square root in the answer.

        num_dem1: tuple[int, int] = Math.simplify(round(self.x), mag[0])
        num_dem2: tuple[int, int] = Math.simplify(round(self.y), mag[0])

        if no_root:
            return f"<{num_dem1[0]}/{num_dem1[1]}, {num_dem2[0]}/{num_dem2[1]}>"
        return f"<{num_dem1[0]}/{num_dem1[1]}√{mag[1]}, {num_dem2[0]}/{num_dem2[1]}√{mag[1]}>"

    def normalized(self, out: Vector | None = None) -> Vector:
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

        mag = self.magnitude

        inv_mag = 1 / mag if mag != 0 else 0

        out.x = self.x * inv_mag
        out.y = self.y * inv_mag

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

    def perpendicular(self, scalar: float | int = 1, out: Vector | None = None) -> Vector:
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
        self,
        lower: Vector | float | int,
        upper: Vector | float | int,
        absolute: bool = False,
        out: Vector | None = None
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

    def rotate(self, angle: float | int, out: Vector | None = None) -> Vector:
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

        radians = math.radians(angle)
        c, s = math.cos(radians), math.sin(radians)
        out.x, out.y = round(self.x * c - self.y * s, 10), round(self.x * s + self.y * c, 10)

        return out

    def to_tuple(self) -> tuple[float, float]:
        """
        Returns the x and y coordinates of the vector as a tuple.
        """
        return self.x, self.y

    def tuple_int(self) -> tuple[int, int]:
        """Returns a tuple with int-cast values."""
        return int(self.x), int(self.y)

    def clone(self) -> Vector:
        """Returns a copy of the vector."""
        return Vector(self.x, self.y)

    def lerp(self, target: Vector, t: float | int, out: Vector | None = None) -> Vector:
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

    def round(self, decimal_places: int = 0, out: Vector | None = None):
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

    def max(self) -> float:
        """Returns the maximum of x and y."""
        return max(self.x, self.y)

    def min(self) -> float:
        """Returns the minimum of x and y."""
        return min(self.x, self.y)

    def ceil(self, out: Vector | None = None) -> Vector:
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

    def floor(self, out: Vector | None = None) -> Vector:
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

    def abs(self, out: Vector | None = None) -> Vector:
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

    def dir_to(self, other: Vector | tuple[float, float]) -> Vector:
        """
        Direction from the Vector to another Vector (or tuple of floats).

        Args:
            other: the position to which you are pointing

        Returns:
            A unit vector that is in the pointing to the other position passed in
        """
        return (other - self).normalized()

    def dist_to(self, other: Vector | tuple[float, float]) -> float:
        """
        Finds the pythagorean distance to another vector (or tuple of floats).

        Args:
            other: The other vector.

        Returns:
            The distance.
        """
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def within(self, other: Vector | tuple[float, float], distance: float | int) -> bool:
        """
        Checks if the vector is within a certain distance of another vector (or tuple of floats).

        Args:
            other: The other vector
            distance: The distance to check

        Returns:
            True if the vector is within the distance, False otherwise
        """
        return (self.x - other[0])**2 + (self.y - other[1])**2 <= distance * distance

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
        return Vector.up().rotate(angle) * magnitude

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

    @classmethod
    def poly(cls, num_sides: int, radius: float | int = 1) -> list[Vector]:
        """
        Returns a list of vectors representing a polygon with the given number of sides and radius.

        Args:
            num_sides (int): The number of sides of the polygon.
            radius (float | int, optional): The radius of the polygon. Defaults to 1.

        Raises:
            SideError: If num_sides is less than 3.

        Returns:
            list[Vector]: The list of vectors representing the polygon.
        """
        if num_sides < 3:
            raise SideError("Can't create a polygon with less than three sides.")

        rotangle = 360 / num_sides
        return [Vector.from_radial(radius, i * rotangle) for i in range(num_sides)]

    @classmethod
    def rect(cls, width: float | int, height: float | int) -> list[Vector]:
        """
        Returns a list of vectors representing a rectangle with the given width and height.

        Args:
            width (float | int): The width of the rectangle.
            height (float | int): The height of the rectangle.

        Returns:
            list[Vector]: The list of vectors representing the rectangle.
        """
        w = width / 2
        h = height / 2
        return [Vector(-w, -h), Vector(w, -h), Vector(w, h), Vector(-w, h)]

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
        return NotImplemented

    def __lt__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x < other[0] and self.y < other[1]
        return NotImplemented

    def __ge__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x >= other[0] and self.y >= other[1]
        return NotImplemented

    def __le__(self, other: Vector | tuple | list) -> bool:
        if isinstance(other, (Vector, tuple, list)):
            return self.x <= other[0] and self.y <= other[1]
        return NotImplemented

    def __pow__(self, other: Any, mod) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(pow(self.x, other, mod), pow(self.y, other, mod))
        if isinstance(other, (Vector, tuple, list)):
            return Vector(pow(self.x, other[0], mod), pow(self.y, other[1], mod))
        return NotImplemented

    def __ipow__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(pow(self.x, other), pow(self.y, other))
        if isinstance(other, (Vector, tuple, list)):
            return Vector(pow(self.x, other[0]), pow(self.y, other[1]))
        return NotImplemented

    def __mul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        return NotImplemented

    def __add__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __imul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        return NotImplemented

    def __iadd__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __rmul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x * other[0], self.y * other[1])
        return NotImplemented

    def __radd__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __sub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __rsub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other - self.x, other - self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] - self.x, other[1] - self.y)
        return NotImplemented

    def __isub__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x - other[0], self.y - other[1])
        return NotImplemented

    def __truediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x / other[0], self.y / other[1])
        return NotImplemented

    def __rtruediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other / self.x, other / self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] / self.x, other[1] / self.y)
        return NotImplemented

    def __itruediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x / other[0], self.y / other[1])
        return NotImplemented

    def __floordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x // other, self.y // other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x // other[0], self.y // other[1])
        return NotImplemented

    def __rfloordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other // self.x, other // self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] // self.x, other[1] // self.y)
        return NotImplemented

    def __ifloordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x // other, self.y // other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x // other[0], self.y // other[1])
        return NotImplemented

    def __mod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x % other, self.y % other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x % other[0], self.y % other[1])
        return NotImplemented

    def __rmod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(other % self.x, other % self.y)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(other[0] % self.x, other[1] % self.y)
        return NotImplemented

    def __imod__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x % other, self.y % other)
        if isinstance(other, (Vector, tuple, list)):
            return Vector(self.x % other[0], self.y % other[1])
        return NotImplemented

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __iter__(self) -> Iterator[int | float]:
        return iter([self.x, self.y])

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"

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

    @staticmethod
    def create(obj: Vector | tuple[float, float]) -> Vector:
        """
        Makes a Vector from a Vector-like object.

        Args:
            obj: The object to make a Vector from.
        """
        if isinstance(obj, Vector):
            return obj
        if isinstance(obj, (tuple, list)) and len(obj) == 2:
            item_zero, item_one = obj[0], obj[1]
            if isinstance(item_zero, (int, float)) and isinstance(item_one, (int, float)):
                return Vector(item_zero, item_one)
        raise TypeError(f"{obj} is not like a Vector.")
