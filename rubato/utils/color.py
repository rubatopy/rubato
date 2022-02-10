"""
A Color implementation.
"""
from typing import Tuple
from rubato.utils import Math


class Color:
    """
    An Color implentation.

    Attributes:
        r (float): The red value.
        g (float): The green value.
        b (float): The blue value.
    """

    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0):
        """
        Initializes an Color class.

        Args:
            r: The red value. Defaults to 0.0.
            g: The green value. Defaults to 0.0.
            b: The blue value. Defaults to 0.0.
        """
        self.r: float = r
        self.g: float = g
        self.b: float = b
        self.check_values()

    def __str__(self):
        return str((self.r, self.g, self.b))

    def __eq__(self, other):
        if isinstance(other, type(Color)):
            return \
                abs(self.r - other.r) < 0.0001 and \
                abs(self.g - other.g) < 0.0001 and \
                abs(self.b - other.b) < 0.0001
        return False

    def to_tuple(self) -> Tuple[int, int, int]:
        """
        Converts the Color to a tuple.

        Returns:
            tuple(int, int, int): The tuple representing the color.
        """
        return (self.r, self.g, self.b)

    def check_values(self):
        """
        Makes the Color values legit. In other words, clamps them between 0 and
        255.
        """
        self.r = Math.clamp(self.r, 0, 255)
        self.g = Math.clamp(self.g, 0, 255)
        self.b = Math.clamp(self.b, 0, 255)

    def lerp(self, other: "Color", t: float) -> "Color":
        """
        Lerps between this color and another.

        Args:
            other: The other Color to lerp with.
            t: The amount to lerp.

        Returns:
            Color: The lerped Color. This Color remains unchanged.
        """
        t = Math.clamp(t, 0, 1)
        return Color(
            self.r + (other.r - self.r) * t,
            self.g + (other.g - self.g) * t,
            self.b + (other.b - self.b) * t,
        )

    def to_hex(self) -> str:
        """
        Converts the Color to hexadecimal.

        Returns:
            str: The hexadecimal output in lowercase. (i.e. ffffff)
        """
        return (f"{format(self.r, '02x')}" + f"{format(self.g, '02x')}" +
                f"{format(self.b, '02x')}")

    @staticmethod
    def from_hex(h: str) -> "Color":
        """
        Creates an Color from a hex string.

        Args:
            h: The hexadecimal value in lowercase.

        Returns:
            Color: The Color value.
        """
        lv = len(h)
        h = tuple(int(h[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return Color(h[0], h[1], h[2])

    @staticmethod
    def from_hsv(h: int, s: int, v: int) -> "Color":
        """
        Creates an Color from an HSV.

        Args:
            h: The hue amount.
            s: The saturation amount.
            v: The value amount.

        Returns:
            Color: The Color value.
        """
        out = Color()
        if s == 0:
            out.set(v)
        hh = h
        if hh >= 360.0:
            hh = 0.0
        hh /= 60.0
        i = int(hh)
        ff = hh - i
        p = v * (1.0 - s)
        q = v * (1.0 - (s * ff))
        t = v * (1.0 - (s * (1.0 - ff)))
        if i == 0:
            out.r = v
            out.g = t
            out.b = p
        elif i == 1:
            out.r = q
            out.g = v
            out.b = p
        elif i == 2:
            out.r = p
            out.g = v
            out.b = t
        elif i == 3:
            out.r = p
            out.g = q
            out.b = v
        elif i == 4:
            out.r = t
            out.g = p
            out.b = v
        elif i == 5:
            out.r = v
            out.g = p
            out.b = q
        else:
            out.r = v
            out.g = p
            out.b = q

        return out

    @classmethod
    @property
    def black(cls):
        """
        An Color class of the color black.

        Returns:
            Color: (0, 0, 0)
        """
        return Color(0, 0, 0)

    @classmethod
    @property
    def white(cls):
        """
        An Color class of the color white.

        Returns:
            Color: (255, 255, 255)
        """
        return Color(255, 255, 255)

    @classmethod
    @property
    def red(cls):
        """
        An Color class of the color red.

        Returns:
            Color: (255, 0, 0)
        """
        return Color(255, 0, 0)

    @classmethod
    @property
    def lime(cls):
        """
        An Color class of the color lime.

        Returns:
            Color: (0, 255, 0)
        """
        return Color(0, 255, 0)

    @classmethod
    @property
    def blue(cls):
        """
        An Color class of the color blue.

        Returns:
            Color: (0, 0, 255)
        """
        return Color(0, 0, 255)

    @classmethod
    @property
    def yellow(cls):
        """
        An Color class of the color yellow.

        Returns:
            Color: (255, 255, 0)
        """
        return Color(255, 255, 0)

    @classmethod
    @property
    def cyan(cls):
        """
        An Color class of the color cyan.

        Returns:
            Color: (0, 255, 255)
        """
        return Color(0, 255, 255)

    @classmethod
    @property
    def magenta(cls):
        """
        An Color class of the color magenta.

        Returns:
            Color: (255, 0, 255)
        """
        return Color(255, 0, 255)

    @classmethod
    @property
    def silver(cls):
        """
        An Color class of the color silver.

        Returns:
            Color: (192, 192, 192)
        """
        return Color(192, 192, 192)

    @classmethod
    @property
    def gray(cls):
        """
        An Color class of the color gray.

        Returns:
            Color: (128, 128, 128)
        """
        return Color(128, 128, 128)

    @classmethod
    @property
    def maroon(cls):
        """
        An Color class of the color maroon.

        Returns:
            Color: (128, 0, 0)
        """
        return Color(128, 0, 0)

    @classmethod
    @property
    def olive(cls):
        """
        An Color class of the color olive.

        Returns:
            Color: (128, 128, 0)
        """
        return Color(128, 128, 0)

    @classmethod
    @property
    def green(cls):
        """
        An Color class of the color green.

        Returns:
            Color: (0, 128, 0)
        """
        return Color(0, 128, 0)

    @classmethod
    @property
    def purple(cls):
        """
        An Color class of the color purple.

        Returns:
            Color: (128, 0, 128)
        """
        return Color(128, 0, 128)

    @classmethod
    @property
    def teal(cls):
        """
        An Color class of the color teal.

        Returns:
            Color: (0, 128, 128)
        """
        return Color(0, 128, 128)

    @classmethod
    @property
    def navy(cls):
        """
        An Color class of the color navy.

        Returns:
            Color: (0, 0, 128)
        """
        return Color(0, 0, 128)
