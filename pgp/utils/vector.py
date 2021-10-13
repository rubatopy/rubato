from pgp.utils import PMath, classproperty, check_types
import math

class Vector:
    """
    A Vector object that defines a 3D point in space

    :param x: The x coordinate.
    :param y: The y coordinate.
    :param z: The z coordinate.
    """

    def __init__(self, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        check_types(Vector.__init__, locals())
        self.x, self.y, self.z = x, y, z

    def translate(self, x: float | int, y: float | int, z: float | int = 0):
        """
        Translates the vector's x y and z coordinates by some constants

        :param x: The change in x.
        :param y: The change in y.
        :param z: The change in z.
        """
        check_types(Vector.translate, locals())
        self.x, self.y, self.z = self.x + x, self.y + y, self.z + z

    def offset(self, other: "Vector") -> "Vector":
        """
        Offsets the x and y coordinates of a vector by those of another vector

        :param other: Another vector
        :return: A new vector with the translated x and y coordinates
        """
        check_types(Vector.offset, locals())
        return Vector(self.x - other.x, self.y - other.y, self.z)

    def to_tuple(self) -> tuple:
        """
        Returns the x and y coordinates of the vector as a tuple
        """
        return self.x, self.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __mul__(self, other: any) -> "Vector":
        check_types(Vector.__mul__, locals())
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other, self.z)
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z)

    def __add__(self, other: "Vector") -> "Vector":
        check_types(Vector.__add__, locals())
        return Vector(self.x + other.x, self.y + other.y)

    __rmul__ = __mul__
    __radd__ = __add__

    def __sub__(self, other: any) -> "Vector":
        check_types(Vector.__sub__, locals())
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x - other, self.y - other, self.z)
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z)

    def __rsub__(self, other: int | float) -> "Vector":
        check_types(Vector.__rsub__, locals())
        return Vector(other - self.x, other - self.y, self.z)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, self.z)

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
        check_types(Vector.__equals, locals())
        return self.y == v.y and self.x == v.x

    def clamp(self, lower: any, upper: any, absolute: bool = False):
        """
        Clamps x and y between the two vectors given

        :param absolute: Whether to clamp the absolute value of the vector instead of the actual value
        :param lower: The lower bound
        :param upper: The upper bound
        """
        check_types(Vector.clamp, locals())
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
        check_types(Vector.__eq__, locals())
        return False if (other is None or not isinstance(other, Vector)) else self.__equals(other)

    @property
    def magnitude(self) -> float:
        """Returns the magnitude of the vector"""
        return math.sqrt(self.x**2 + self.y**2)

    @staticmethod
    def from_radial(angle: float, magnitude: float) -> "Vector":
        """
        Gives you a Vector from the given direction and distance

        :param angle: Direction of vector in radians
        :param magnitude: Length of vector
        :return: Vector from the given direction and distance
        """
        check_types(Vector.from_radial, locals())
        return Vector(math.cos(angle) * magnitude, math.sin(angle) * magnitude)

    @property
    def angle(self) -> float:
        """Returns the angle of the vector"""
        angle = math.tan(self.y / self.x)
        if PMath.sign(self.x) == -1:
            angle += 180
        if PMath.sign(angle) == -1:
            angle += 360

        return angle


    def invert(self, axis: str):
        """
        Inverts the vector in the axis given

        :param axis: The axis to invert the vector in
        """
        check_types(Vector.invert, locals())

        if axis == "x":
            self.x = -self.x
        elif axis == "y":
            self.y = -self.y
        elif axis == "z":
            self.z = -self.z
        else:
            raise ValueError(f"{axis} is not a valid axis")

    def to_int(self) -> "Vector":
        return Vector(int(self.x), int(self.y), self.z)
