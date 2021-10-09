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
