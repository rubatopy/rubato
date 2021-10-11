import math

class ClassProperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class PMath:

    @staticmethod
    def clamp(a, lower, upper):
        """
        Clamps a to the bounds of upper and lower
        """
        return min(max(a, lower), upper)

    @staticmethod
    def abs_clamp(a, lower, upper):
        return PMath.sign(a) * PMath.clamp(abs(a), lower, upper)

    @staticmethod
    def sign(n):
        return (n > 0) - (n < 0)

    @staticmethod
    def lerp(lower, upper, t):
        """
        Linearly interpolates between lower and upper bounds by t

        :param lower: The lower bound
        :param upper: The upper bound
        :param t: Distance between upper and lower (1 gives upper, 0 gives lower)
        """
        return (t * upper) + ((1 - t) * lower)

    @staticmethod
    def deg_to_rad(deg):
        return deg * math.pi / 180

    @staticmethod
    def rad_to_deg(rad):
        return rad * 180 / math.pi

    @ClassProperty
    def INFINITY(self):
        return 2147483647
