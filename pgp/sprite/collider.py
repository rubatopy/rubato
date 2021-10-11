from __future__ import annotations
from pgp import Vector


class Collider:
    """
    A collider for a rigid body.

    :param rect: An array with 4 values representing the x and y displacement of the collider
     (with respect to the top left corner of the rigid body) and the width and the height of the collider.
    :param pos: The function that returns the position of the rigid body that this collider is attached to.
    """
    def __init__(self, rect, pos):
        self.offset, self.dims, self._pos = Vector(rect[0], rect[1]), Vector(rect[2], rect[3]), pos

    def overlap_point(self, x, y) -> bool:
        return self.top_left.x <= x <= self.bottom_right.x and self.top_left.y <= y <= self.bottom_right.y

    def overlap(self, other: Collider, fast: bool = True) -> bool or str:
        tl, otl = self.top_left, other.top_left
        br, obr = tl + self.dims, otl + other.dims

        if tl.x > obr.x or br.x < otl.x or tl.y > obr.y or br.y < otl.y: return False
        if fast: return True

        distances = {
            "top": min(abs(otl.y - tl.y), abs(otl.y - br.y)),
            "bottom": min(abs(obr.y - tl.y), abs(obr.y - br.y)),
            "left": min(abs(otl.x - tl.x), abs(otl.x - br.x)),
            "right": min(abs(obr.x - tl.x), abs(obr.x - br.x))
        }

        return min(distances, key=lambda dim: distances[dim])

    @property
    def pos(self):
        return self._pos()

    @property
    def top_left(self) -> Vector:
        return self.pos + self.offset

    @property
    def bottom_right(self) -> Vector:
        return self.top_left + self.dims

    @property
    def width(self) -> int:
        return self.dims.x

    @property
    def height(self) -> int:
        return self.dims.y
