class Point:

    def __init__(self, x: int, y: int, z: int = 0):
        self.x, self.y, self.z = x, y, z

    def offset2(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def to_tuple(self):
        return self.x, self.y
