"""
QuadTree implementation to optimize collision detection as part of the physics engine.
Do not use this in your own projects as it is tailored only to this use case.
"""
import Cython

from . import Hitbox, Engine
from .... import Vector


@Cython.cclass
class QTree:
    """The Quadtree itself."""

    def __init__(self, hbs: list[list[Hitbox]]):
        self.bbs: list[tuple[Vector, Vector]] = []

        tl: Vector = Vector.infinity()
        br: Vector = -1 * Vector.infinity()
        for gen in hbs:
            local_tl: Vector = Vector.infinity()
            local_br: Vector = -1 * Vector.infinity()
            for hb in gen:
                aabb: tuple[Vector, Vector] = hb.get_aabb()

                if aabb[0].x < local_tl.x:
                    if aabb[0].x < tl.x:
                        tl.x = local_tl.x = aabb[0].x
                    else:
                        local_tl.x = aabb[0].x
                if aabb[0].y < local_tl.y:
                    if aabb[0].y < tl.y:
                        tl.y = local_tl.y = aabb[0].y
                    else:
                        local_tl.y = aabb[0].y
                if aabb[1].x > local_br.x:
                    if aabb[1].x > br.x:
                        br.x = local_br.x = aabb[1].x
                    else:
                        local_br.x = aabb[1].x
                if aabb[1].y > local_br.y:
                    if aabb[1].y > br.y:
                        br.y = local_br.y = aabb[1].y
                    else:
                        local_br.y = aabb[1].y
            self.bbs.append((local_tl, local_br))

        self.stack: list[list[Hitbox]] = []

        center: Vector = (tl + br) / 2

        self.northeast: STree = STree(Vector(center.x, tl.y), Vector(br.x, center.y))
        self.northwest: STree = STree(tl, center)
        self.southeast: STree = STree(center, br)
        self.southwest: STree = STree(Vector(tl.x, center.y), Vector(center.x, br.y))

        for i in range(len(hbs)):
            bb: tuple[Vector, Vector] = self.bbs[i]
            hbg: list[Hitbox] = hbs[i]

            self.collide(hbg, bb)

            if not self.northeast.insert(hbg, bb) and not self.northwest.insert(hbg, bb) \
                and not self.southeast.insert(hbg, bb) and not self.southwest.insert(hbg, bb):
                self.stack.append(hbg)

    def collide(self, hbs: list[Hitbox], bb: tuple[Vector, Vector]):
        for hb in hbs:
            for li in self.stack:
                for item in li:
                    Engine.collide(hb, item)

        self.northeast.collide(hbs, bb)
        self.northwest.collide(hbs, bb)
        self.southeast.collide(hbs, bb)
        self.southwest.collide(hbs, bb)

    def calc_bb(self, hbs: list[Hitbox]) -> tuple[Vector, Vector]:
        tl: Vector = Vector.infinity()
        br: Vector = -1 * Vector.infinity()
        for hb in hbs:
            aabb: tuple[Vector, Vector] = hb.get_aabb()

            if aabb[0].x < tl.x:
                tl.x = aabb[0].x
            if aabb[0].y < tl.y:
                tl.y = aabb[0].y
            if aabb[1].x > br.x:
                br.x = aabb[1].x
            if aabb[1].y > br.y:
                br.y = aabb[1].y

        return tl, br


@Cython.cclass
class STree:
    """A Subtree."""

    def __init__(self, top_left: Vector, bottom_right: Vector):
        self.top_left: Vector = top_left
        self.bottom_right: Vector = bottom_right

        self.stack: list[list[Hitbox]] = []

        self.has_children: bool = False

        self.northeast: STree
        self.northwest: STree
        self.southeast: STree
        self.southwest: STree

    def insert(self, hbs: list[Hitbox], bb: tuple[Vector, Vector]) -> bool:
        if (bb[0].x < self.top_left.x) or (bb[0].y < self.top_left.y) \
            or (bb[1].x > self.bottom_right.x) or (bb[1].y > self.bottom_right.y):
            return False

        if not self.stack:
            self.stack.append(hbs)
            return True

        if not self.has_children:
            self.has_children = True
            center: Vector = (self.top_left + self.bottom_right) / 2
            self.northeast = STree(Vector(center.x, self.top_left.y), Vector(self.bottom_right.x, center.y))
            self.northwest = STree(self.top_left, center)
            self.southeast = STree(center, self.bottom_right)
            self.southwest = STree(Vector(self.top_left.x, center.y), Vector(center.x, self.bottom_right.y))

        if not self.northeast.insert(hbs, bb) and not self.northwest.insert(hbs, bb) \
            and not self.southeast.insert(hbs, bb) and not self.southwest.insert(hbs, bb):
            self.stack.append(hbs)

        return True

    def collide(self, hbs: list[Hitbox], bb: tuple[Vector, Vector]):
        if (bb[1].y < self.top_left.y) or (bb[1].x < self.top_left.x) \
            or (bb[0].y > self.bottom_right.y) or (bb[0].x > self.bottom_right.x):
            return

        for hb in hbs:
            for current in self.stack:
                for item in current:
                    Engine.collide(hb, item)

        if self.has_children:
            self.northeast.collide(hbs, bb)
            self.northwest.collide(hbs, bb)
            self.southeast.collide(hbs, bb)
            self.southwest.collide(hbs, bb)
