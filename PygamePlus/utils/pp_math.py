import pygame.math as math


def clamp(a, upper, lower):
    return min(max(a, lower), upper)


class Vector2(math.Vector2):
    def __init__(self, *args):
        super.__init__(*args)


class Coord:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y

    @staticmethod
    @property
    def ZERO():
        return Coord(0, 0)

    @staticmethod
    @property
    def ONE():
        return Coord(1, 1)

    @staticmethod
    @property
    def TWO():
        return Coord(2, 2)

    @staticmethod
    @property
    def UP():
        return Coord(0, -1)

    @staticmethod
    @property
    def LEFT():
        return Coord(-1, 0)

    @staticmethod
    @property
    def DOWN():
        return Coord(0, 1)

    @staticmethod
    @property
    def RIGHT():
        return Coord(1, 0)

    def __equals(self, c):
        return self.y_pos == c.y_pos and self.x_pos == c.x_pos

    def clamp(self, lower, upper):
        if type(lower) != type(Coord):
            Coord(*lower)
        if type(upper) != type(Coord):
            Coord(*upper)
        self.x_pos = clamp(self.x_pos, lower.x, upper.x)
        self.y_pos = clamp(self.y_pos, lower.y, upper.y)

    def __repr__(self):
        return "(" + self.x_pos + "," + self.y_pos + ")"

    def __eq__(self, other):
        return False if (other is None or type(other) != type(Coord)) else self.__equals(other)
