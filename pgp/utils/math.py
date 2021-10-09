class Point:

    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.x, self.y, self.z = x, y, z

    def translate(self, x: int, y: int, z: int = 0):
        self.x, self.y, self.z = self.x + x, self.y + y, self.z + z

    def offset2(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z)

    def to_tuple2(self):
        return self.x, self.y
