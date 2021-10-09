from pgp.utils import Point

class Camera:
    def __init__(self, pos: Point = Point()):
        self.pos = pos

    def transform(self, point):
        return point.offset2(self.pos).to_tuple2()
