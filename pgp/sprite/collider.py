from pgp.utils import Vector


class Collider:
    def __init__(self, x1, x2, y1, y2):
        self.rect = [x1, x2, y1, y2]
        if not self.valid():
            raise Exception("x1 needs to be smaller than x2 and y1 needs to be smaller than y2")
        self.enabled = True

    def valid(self):
        return self.x1 < self.x2 and self.y1 < self.y2

    def collide_point(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def collide(self, other):
        if not isinstance(other, Collider):
            raise Exception("other should always be another collider when trying to collide with another collider")
        for x, y in other.vectors:
            if not self.collide_point(x,y):
                return False
        return True

    @property
    def collider(self):
        return self.rect if self.enabled else None

    @property
    def x1(self):
        return self.rect[0]

    @property
    def x2(self):
        return self.rect[1]

    @property
    def y1(self):
        return self.rect[2]

    @property
    def y2(self):
        return self.rect[3]

    @property
    def x_vector(self):
        return Vector(self.x1, self.x2)

    @property
    def y_vector(self):
        return Vector(self.y1, self.y2)

    @property
    def left(self):
        return self.x1

    @property
    def top(self):
        return self.y1

    @property
    def right(self):
        return self.x2

    @property
    def bottom(self):
        return self.y2

    @property
    def vectors(self):
        return self.x_vector, self.y_vector

    def set_topleft(self, x, y):
        x_mag = self.x_vector.magnitude()
        y_mag = self.y_vector.magnitude()
        self.rect[0] = x
        self.rect[2] = y
        self.rect[1] = x + x_mag
        self.rect[3] = y + y_mag
