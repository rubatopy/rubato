"""
Describes a QuadTree implementation for optimized collision detection.
Do not use this in your own projects as it is tailored only to this use case.
"""
from typing import List

from . import Hitbox, Engine
from .... import Vector

class QTree:
    """The Quadtree itself."""
    def __init__(self, top_left: Vector, bottom_right: Vector):
        self.stack = []

        center = (top_left + bottom_right) / 2

        self.northeast = STree(Vector(center.x, top_left.y), Vector(bottom_right.x, center.y))
        self.northwest = STree(top_left, center)
        self.southeast = STree(center, bottom_right)
        self.southwest = STree(Vector(top_left.x, center.y), Vector(center.x, bottom_right.y))

    def insert(self, hbs: List[Hitbox], bb: tuple[Vector]):
        if not self.northeast.insert(hbs, bb) and not self.northwest.insert(hbs, bb) \
            and not self.southeast.insert(hbs, bb) and not self.southwest.insert(hbs, bb):
            self.stack.append(hbs)

    def collide(self, hbs: List[Hitbox], bb: tuple[Vector]):
        for hb in hbs:
            for current in self.stack:
                for item in current:
                    Engine.collide(hb, item)

        self.northeast.collide(hbs, bb)
        self.northwest.collide(hbs, bb)
        self.southeast.collide(hbs, bb)
        self.southwest.collide(hbs, bb)

    @staticmethod
    def calc_bb(hbs: List[Hitbox]):
        tl, br = Vector.infinity, -1 * Vector.infinity
        for hb in hbs:
            aabb = hb.get_aabb()
            tl.x = min(tl.x, aabb[0].x)
            tl.y = min(tl.y, aabb[0].y)
            br.x = max(br.x, aabb[1].x)
            br.y = max(br.y, aabb[1].y)

        return (tl, br)

class STree:
    """A Subtree."""
    def __init__(self, top_left: Vector, bottom_right: Vector):
        self.top_left = top_left
        self.bottom_right = bottom_right

        self.stack = []

        self.northeast: STree = None
        self.northwest: STree = None
        self.southeast: STree = None
        self.southwest: STree = None

    def insert(self, hbs: List[Hitbox], bb: tuple[Vector]) -> bool:
        if (bb[0].x < self.top_left.x) or (bb[0].y < self.top_left.y) \
            or (bb[1].x > self.bottom_right.x) or (bb[1].y > self.bottom_right.y):
            return False

        if not self.stack:
            self.stack.append(hbs)
            return True

        if self.northeast is None:
            center = (self.top_left + self.bottom_right) / 2
            self.northeast = STree(Vector(center.x, self.top_left.y), Vector(self.bottom_right.x, center.y))
            self.northwest = STree(self.top_left, center)
            self.southeast = STree(center, self.bottom_right)
            self.southwest = STree(Vector(self.top_left.x, center.y), Vector(center.x, self.bottom_right.y))

        if not self.northeast.insert(hbs, bb) and not self.northwest.insert(hbs, bb) \
            and not self.southeast.insert(hbs, bb) and not self.southwest.insert(hbs, bb):
            self.stack.append(hbs)

        return True

    def collide(self, hbs: List[Hitbox], bb: tuple[Vector]) -> bool:
        if (bb[1].y < self.top_left.y) or (bb[1].x < self.top_left.x) \
            or (bb[0].y > self.bottom_right.y) or (bb[0].x > self.bottom_right.x):
            return

        for hb in hbs:
            for current in self.stack:
                for item in current:
                    Engine.collide(hb, item)

        if self.northeast is not None:
            self.northeast.collide(hbs, bb)
            self.northwest.collide(hbs, bb)
            self.southeast.collide(hbs, bb)
            self.southwest.collide(hbs, bb)
