import math
from pgp.utils.processing import check_types


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class PMath:

    INFINITY = math.pow(2, 99)

    @staticmethod
    def clamp(a: float | int, lower: float | int, upper: float | int) -> float:
        """
        Clamps a to the bounds of upper and lower

        :param a: The number to clamp
        :param lower: The lower bound of the clamp
        :param upper: The upper bound of the clamp
        :return: The clamped result
        """
        check_types(PMath.clamp, locals())
        return min(max(a, lower), upper)

    @staticmethod
    def abs_clamp(a: float | int, lower: float | int, upper: float | int) -> float:
        """
        Clamps a to the bounds of lower and upper and takes the absolute value

        :param a: The number to clamp
        :param lower: The lower bound of the clamp
        :param upper: The upper bound of the clamp
        :return: The clamped result
        """
        check_types(PMath.abs_clamp, locals())
        return PMath.sign(a) * PMath.clamp(abs(a), lower, upper)

    @staticmethod
    def sign(n: float | int) -> int:
        """
        Checks the sign of n

        :param n: A number
        :return: The sign of the number
        """
        check_types(PMath.sign, locals())
        return (n > 0) - (n < 0)

    @staticmethod
    def lerp(lower: float | int, upper: float | int, t: float) -> float:
        """
        Linearly interpolates between lower and upper bounds by t

        :param lower: The lower bound
        :param upper: The upper bound
        :param t: Distance between upper and lower (1 gives upper, 0 gives lower)
        :return: The lerped value
        """
        check_types(PMath.lerp, locals())
        return (t * upper) + ((1 - t) * lower)

    @staticmethod
    def deg_to_rad(deg: float | int) -> float:
        """
        Convert a number from degrees to radians

        :param deg: The number in degrees to convert
        :return: The resulting number in radians
        """
        check_types(PMath.deg_to_rad, locals())
        return deg * math.pi / 180

    @staticmethod
    def rad_to_deg(rad: float | int) -> float:
        """
        Convert a number from radians to degrees

        :param rad: The number in radians to convert
        :return: The resulting number in degrees
        """
        check_types(PMath.rad_to_deg, locals())
        return rad * 180 / math.pi
