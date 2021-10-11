from __future__ import annotations
from pgp import Vector


class Collider:
    """
    A collider for a rigid body.

    :param rect: An array with 4 values representing the x and y displacement of the collider
     (with respect to the top left corner of the rigid body) and the width and the height of the collider.
    :param rb_pos: The function that returns the position of the rigid body that this collider is attached to.
    """
    def __init__(self, rect, rb_pos):
        self.rect = rect
        self.rb_pos = rb_pos
        if not self.valid():
            raise Exception("The width and height of the collider must be greater than zero.")

    def valid(self) -> bool:
        """
        Checks if the bounding box is valid.

        :return: A boolean.
        """
        return self.width > 0 and self.height > 0

    def collide_point(self, x, y) -> bool:
        return self.top_left.x <= x <= self.bottom_right.x and self.top_left.y <= y <= self.bottom_right.y

    def collide(self, other: Collider) -> bool or str:
        inside_eo_x = not (self.rb_pos().x > (other.rb_pos().x + other.width) or (self.rb_pos().x + self.width) < other.rb_pos().x)
        inside_eo_y = not (self.rb_pos().y > (other.rb_pos().y + other.height) or (self.rb_pos().y + self.height) < other.rb_pos().y)

        if inside_eo_x and inside_eo_y:
            if self.top_collide(other):
                return "top"
            elif self.right_collide(other):
                return "right"
            elif self.left_collide(other):
                return "left"
            elif self.bottom_collide(other):
                return "bottom"
        else:
            return False

    @property
    def top_left(self) -> Vector:
        return self.rb_pos()

    @property
    def top_right(self) -> Vector:
        return self.rb_pos() + Vector(self.width)

    @property
    def bottom_left(self) -> Vector:
        return self.rb_pos() + Vector(0, self.height)

    @property
    def bottom_right(self) -> Vector:
        return self.top_left + Vector(self.width, self.height)

    @property
    def width(self) -> int:
        return self.rect[2]

    @property
    def height(self) -> int:
        return self.rect[3]

    def top_collide(self, other: Collider) -> bool:
        return self.bottom_right.y < other.top_left.y and not self.right_collide(other) and not self.left_collide(other)

    def right_collide(self, other: Collider) -> bool:
        return False

    def left_collide(self, other: Collider) -> bool:
        return False

    def bottom_collide(self, other: Collider) -> bool:
        return self.bottom_right.y > other.top_left.y and not self.right_collide(other) and not self.left_collide(other)