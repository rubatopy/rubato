"""
A modified implementation of the OpenSimplex2 algorithm.
"""
from . import Math, InitError


# THIS IS A STATIC CLASS
class Noise:
    """
    A utility for generating simple smooth noise, based on OpenSimplex2.
    """
    seed: int = 0
    """The seed for the random noise. Setting to a fixed value will result in the same noise every time."""

    _PRIME_X = 0x5205402B9270C86F
    _PRIME_Y = 0x598CD327003817B5
    _PRIME_Z = 0x5BCC226E9FA0BACB
    _PRIME_W = 0x56CC5227E58F554B
    _HASH_MULTIPLIER = 0x53A3F72DEEC546F5

    _ROOT2OVER2 = 0.7071067811865476
    _SKEW_2D = 0.366025403784439
    _UNSKEW_2D = -0.21132486540518713

    _N_GRADS_2D_EXPONENT = 7
    _N_GRADS_2D = 1 << _N_GRADS_2D_EXPONENT

    _NORMALIZER_2D = 0.01001634121365712

    _RSQUARED_2D = 0.5

    _GRADIENTS_2D = []

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def noise(cls, x: float) -> float:
        """
        Creates noise from 1 dimensional input.
        This is identical to :func:`noise2(x, 0) <rubato.utils.noise.Noise.noise2>`.

        Args:
            x (float): the x coordinate of noise.

        Returns:
            float: the random noise value.
        """
        return cls.noise2(x, 0)

    @classmethod
    def noise2(cls, x: float, y: float) -> float:
        """
        Creates noise from 2 dimensional input.

        Args:
            x (float): the x coordinate of noise.
            y (float): the y coordinate of noise.

        Returns:
            float: the random noise value.
        """
        s = cls._SKEW_2D * (x + y)
        xs = x + s
        ys = y + s
        return cls._noise2_base(cls.seed, xs, ys)

    @classmethod
    def _noise2_base(cls, seed: int, xs: float, ys: float) -> float:
        xsb = Math.floor(xs)
        ysb = Math.floor(ys)
        xi = xs - xsb
        yi = ys - ysb

        xsbp = xsb * cls._PRIME_X
        ysbp = ysb * cls._PRIME_Y

        t = (xi + yi) * cls._UNSKEW_2D
        dx0 = xi + t
        dy0 = yi + t

        value = 0
        a0 = cls._RSQUARED_2D - dx0 * dx0 - dy0 * dy0
        if a0 > 0:
            value = (a0 * a0) * (a0 * a0) * cls._grad2(seed, xsbp, ysbp, dx0, dy0)

        a1 = (2 * (1 + 2 * cls._UNSKEW_2D) *
              (1 / cls._UNSKEW_2D + 2)) * t + ((-2 * (1 + 2 * cls._UNSKEW_2D) * (1 + 2 * cls._UNSKEW_2D)) + a0)
        if a1 > 0:
            dx1 = dx0 - (1 + 2 * cls._UNSKEW_2D)
            dy1 = dy0 - (1 + 2 * cls._UNSKEW_2D)
            value += (a1 * a1) * (a1 * a1) * cls._grad2(seed, xsbp + cls._PRIME_X, ysbp + cls._PRIME_Y, dx1, dy1)

        if dy0 > dx0:
            dx2 = dx0 - cls._UNSKEW_2D
            dy2 = dy0 - (cls._UNSKEW_2D + 1)
            a2 = cls._RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls._grad2(seed, xsbp, ysbp + cls._PRIME_Y, dx2, dy2)
        else:
            dx2 = dx0 - (cls._UNSKEW_2D + 1)
            dy2 = dy0 - cls._UNSKEW_2D
            a2 = cls._RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls._grad2(seed, xsbp + cls._PRIME_X, ysbp, dx2, dy2)

        return value

    @classmethod
    def _grad2(cls, seed: int, xsvp: int, ysvp: int, dx: float, dy: float) -> float:
        hash_val = seed ^ xsvp ^ ysvp
        hash_val *= cls._HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls._N_GRADS_2D_EXPONENT + 1)
        gi = int(hash_val) & ((cls._N_GRADS_2D - 1) << 1)
        return cls._GRADIENTS_2D[gi | 0] * dx + cls._GRADIENTS_2D[gi | 1] * dy

    # below is the generator code for the gradients

    _gradient2 = [
        0.38268343236509,
        0.923879532511287,
        0.923879532511287,
        0.38268343236509,
        0.923879532511287,
        -0.38268343236509,
        0.38268343236509,
        -0.923879532511287,
        -0.38268343236509,
        -0.923879532511287,
        -0.923879532511287,
        -0.38268343236509,
        -0.923879532511287,
        0.38268343236509,
        -0.38268343236509,
        0.923879532511287,
        0.130526192220052,
        0.99144486137381,
        0.608761429008721,
        0.793353340291235,
        0.793353340291235,
        0.608761429008721,
        0.99144486137381,
        0.130526192220051,
        0.99144486137381,
        -0.130526192220051,
        0.793353340291235,
        -0.60876142900872,
        0.608761429008721,
        -0.793353340291235,
        0.130526192220052,
        -0.99144486137381,
        -0.130526192220052,
        -0.99144486137381,
        -0.608761429008721,
        -0.793353340291235,
        -0.793353340291235,
        -0.608761429008721,
        -0.99144486137381,
        -0.130526192220052,
        -0.99144486137381,
        0.130526192220051,
        -0.793353340291235,
        0.608761429008721,
        -0.608761429008721,
        0.793353340291235,
        -0.130526192220052,
        0.99144486137381,
    ]

    for _gradient_i in range(len(_gradient2)):
        _gradient2[_gradient_i] = _gradient2[_gradient_i] / _NORMALIZER_2D

    _gradient_j = 0
    for _gradient_i in range(_N_GRADS_2D * 2):
        if _gradient_j == len(_gradient2):
            _gradient_j = 0
        _GRADIENTS_2D.append(_gradient2[_gradient_j])
        _gradient_j += 1
