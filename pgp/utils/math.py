def clamp(a, upper, lower):
    return min(max(a, lower), upper)


class Point:
    """
    A Point object that defines a 3D point in space

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
        return Point(self.x - other.x, self.y - other.y, self.z)

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
        return Point(0, 0)

    @staticmethod
    @property
    def ONE():
        return Point(1, 1)

    @staticmethod
    @property
    def TWO():
        return Point(2, 2)

    @staticmethod
    @property
    def UP():
        return Point(0, -1)

    @staticmethod
    @property
    def LEFT():
        return Point(-1, 0)

    @staticmethod
    @property
    def DOWN():
        return Point(0, 1)

    @staticmethod
    @property
    def RIGHT():
        return Point(1, 0)

    def __equals(self, c):
        return self.y_pos == c.y_pos and self.x_pos == c.x_pos

    def clamp(self, lower, upper):
        if type(lower) != type(Point):
            Point(*lower)
        if type(upper) != type(Point):
            Point(*upper)
        self.x_pos = clamp(self.x_pos, lower.x, upper.x)
        self.y_pos = clamp(self.y_pos, lower.y, upper.y)

    def __eq__(self, other):
        return False if (other is None or type(other) != type(Point)) else self.__equals(other)
