"""
A Color implementation.
"""
from random import randint
from typing import Tuple
from rubato.utils import Math, Configs


class Color:
    """
    A Color implentation.

    Attributes:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
        a (int): The alpha value.
    """

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        """
        Initializes an Color class.

        Args:
            r: The red value. Defaults to 0.
            g: The green value. Defaults to 0.
            b: The blue value. Defaults to 0.
            a: The alpha value. Defaults to 255.
        """
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a
        self.check_values()

    def __str__(self):
        return str((self.r, self.g, self.b, self.a))

    def __eq__(self, other):
        if isinstance(other, type(Color)):
            return \
                self.r == other.r and \
                self.g == other.g and \
                self.b == other.b and \
                self.a == other.a
        return False

    def to_tuple(self) -> Tuple[int, int, int]:
        """
        Converts the Color to a tuple.

        Returns:
            tuple(int, int, int): The tuple representing the color.
        """
        return (self.r, self.g, self.b, self.a)

    def check_values(self):
        """
        Makes the Color values legit. In other words, clamps them between 0 and
        255.
        """
        self.r = Math.clamp(self.r, 0, 255)
        self.g = Math.clamp(self.g, 0, 255)
        self.b = Math.clamp(self.b, 0, 255)
        self.a = Math.clamp(self.a, 0, 255)

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
            self.a + (other.a - self.a) * t,
        )

    def to_hex(self) -> str:
        """
        Converts the Color to hexadecimal.

        Returns:
            str: The hexadecimal output in lowercase. (i.e. ffffffff)
        """
        return (f"{format(self.r, '02x')}" + f"{format(self.g, '02x')}" +
                f"{format(self.b, '02x')}" + f"{format(self.a, '02x')}")

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
        return Color(h[0], h[1], h[2], h[3])

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
    def random(cls):
        return Color(randint(0, 255), randint(0, 255), randint(0, 255))

    @classmethod
    @property
    def black(cls):
        return Color(*Configs.color_defaults["black"])

    @classmethod
    @property
    def white(cls):
        return Color(*Configs.color_defaults["white"])

    @classmethod
    @property
    def darkgray(cls):
        return Color(*Configs.color_defaults["darkgray"])

    @classmethod
    @property
    def gray(cls):
        return Color(*Configs.color_defaults["gray"])

    @classmethod
    @property
    def lightgray(cls):
        return Color(*Configs.color_defaults["lightgray"])

    @classmethod
    @property
    def snow(cls):
        return Color(*Configs.color_defaults["snow"])

    @classmethod
    @property
    def yellow(cls):
        return Color(*Configs.color_defaults["yellow"])

    @classmethod
    @property
    def orange(cls):
        return Color(*Configs.color_defaults["orange"])

    @classmethod
    @property
    def red(cls):
        return Color(*Configs.color_defaults["red"])

    @classmethod
    @property
    def scarlet(cls):
        return Color(*Configs.color_defaults["scarlet"])

    @classmethod
    @property
    def magenta(cls):
        return Color(*Configs.color_defaults["magenta"])

    @classmethod
    @property
    def purple(cls):
        return Color(*Configs.color_defaults["purple"])

    @classmethod
    @property
    def violet(cls):
        return Color(*Configs.color_defaults["violet"])

    @classmethod
    @property
    def blue(cls):
        return Color(*Configs.color_defaults["blue"])

    @classmethod
    @property
    def cyan(cls):
        return Color(*Configs.color_defaults["cyan"])

    @classmethod
    @property
    def turquoize(cls):
        return Color(*Configs.color_defaults["turquoize"])

    @classmethod
    @property
    def green(cls):
        return Color(*Configs.color_defaults["green"])

    @classmethod
    @property
    def lime(cls):
        return Color(*Configs.color_defaults["lime"])

    @classmethod
    @property
    def clear(cls):
        return Color(*Configs.color_defaults["clear"])
