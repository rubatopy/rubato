"""
This color module contains the Color class, which is used to represent colors in the game.
"""
from __future__ import annotations
from random import randint
from typing import Tuple
import sdl2

from . import Math, Defaults, Display


class Color:
    """
    An RGBA color.

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
        self.r = int(Math.clamp(r, 0, 255))
        self.g = int(Math.clamp(g, 0, 255))
        self.b = int(Math.clamp(b, 0, 255))
        self.a = int(Math.clamp(a, 0, 255))

    def __str__(self):
        return str(f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})")

    def __eq__(self, other: Color) -> bool:
        if isinstance(other, Color):
            return self.r == other.r and self.b == other.b and self.g == other.g and self.a == other.a
        return False

    def darker(self, amount: int = 20):
        """
        Returns a darker copy of the color. It subtracts ``amount`` from the RGB values.

        Args:
            amount: How much darker. Defaults to 20.

        Returns:
            Color: The resultant color.
        """
        return Color(self.r - amount, self.g - amount, self.b - amount, self.a)

    def lighter(self, amount: int = 20):
        """
        Returns a lighter copy of the color. It adds ``amount`` to the RGB values.

        Args:
            amount: How much lighter. Defaults to 20.

        Returns:
            Color: The resultant color.
        """
        return Color(self.r + amount, self.g + amount, self.b + amount, self.a)

    def mix(self, other: Color, t: float = 0.5, mode: str = "mix") -> Color:
        """
        Mix two colors together.

        Args:
            other: The other color.
            t: The interpolation amount (0 to 1).
                Defaults to 0.5.
            mode: The blending mode ("linear", "mix", "blend"). Linear is the linear interpolation between the two
                colors. Mix and Blend are 2 different algorithms to mix colors. They tend to look better then linear.
                Defaults to "mix".

        Returns:
            Color: The resultant color.
        """
        if mode == "linear":
            return Color(
                (1 - t) * self.r + t * other.r, (1 - t) * self.g + t * other.g, (1 - t) * self.b + t * other.b,
                (1 - t) * self.a + t * other.a
            )
        if mode == "blend":
            alpha_a = (self.a / 255) * (1 - t)
            a = 1 - (1 - alpha_a) * (1 - (other.a / 255))
            s = (other.a / 255) * (1 - alpha_a) / a
            return Color(
                ((1 - s) * (self.r**2.2) + s * (other.r**2.2))**(1 / 2.2),
                ((1 - s) * (self.g**2.2) + s * (other.g**2.2))**(1 / 2.2),
                ((1 - s) * (self.b**2.2) + s * (other.b**2.2))**(1 / 2.2), a * 255
            )
        return Color(
            ((1 - t) * (self.r**2.2) + t * (other.r**2.2))**(1 / 2.2),
            ((1 - t) * (self.g**2.2) + t * (other.g**2.2))**(1 / 2.2),
            ((1 - t) * (self.b**2.2) + t * (other.b**2.2))**(1 / 2.2), (1 - t) * self.a + t * other.a
        )

    def to_tuple(self) -> Tuple[int]:
        """
        Converts the Color to a tuple.

        Returns:
            tuple(int, int, int, int): The tuple representing the color.
        """
        return (self.r, self.g, self.b, self.a)

    def to_hex(self) -> str:
        """
        Converts the Color to a hexadecimal string.

        Returns:
            str: The hexadecimal output in lowercase. (i.e. ffffffff)
        """
        return (f"{self.r:02x}{self.g: 02x}{self.b: 02x}{self.a: 02x}").replace(" ", "")

    @property
    def rgba32(self):
        """The RGBA32 representation of the color."""
        return sdl2.SDL_MapRGBA(Display.format, *self.to_tuple())

    @classmethod
    def from_rgba32(cls, rgba32: int) -> Color:
        """
        Creates a Color from an RGBA32 representation.

        Args:
            rgba32: The RGBA32 representation as an int.

        Returns:
            Color: The color object from the RGBA32.
        """
        if rgba32 == 0:
            return cls(0, 0, 0, 0)
        rgba_str = format(rgba32, "#034b")
        new = cls()
        new.r = int(rgba_str[2:10], 2)
        new.g = int(rgba_str[10:18], 2)
        new.b = int(rgba_str[18:26], 2)
        new.a = int(rgba_str[26:34], 2)
        return new

    @classmethod
    def from_hex(cls, h: str) -> Color:
        """
        Creates an Color from a hex string.

        Args:
            h: The hexadecimal value in the format "RRGGBBAA".

        Returns:
            Color: The Color value.
        """
        lv = len(h)
        if lv < 8:
            raise ValueError(f"Invalid hex string: {h}")
        try:
            h = tuple(int(h[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        except ValueError:
            raise ValueError(f"Invalid hex string: {h}") from ValueError
        return cls(h[0], h[1], h[2], h[3])

    @classmethod
    def from_hsv(cls, h: int, s: int, v: int) -> Color:
        """
        Creates an Color from an HSV.

        Args:
            h: The hue amount.
            s: The saturation amount.
            v: The value amount.

        Returns:
            Color: The Color value.
        """
        out = cls()
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
    def random(cls) -> Color:
        """A random color."""
        return Color(randint(0, 255), randint(0, 255), randint(0, 255))

    @classmethod
    @property
    def clear(cls) -> Color:
        """A transparent color object."""
        return Color(0, 0, 0, 0)

    @classmethod
    @property
    def black(cls) -> Color:
        """
        The default black color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["black"])

    @classmethod
    @property
    def white(cls) -> Color:
        """
        The default white color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["white"])

    @classmethod
    @property
    def night(cls) -> Color:
        """
        The default night color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["night"])

    @classmethod
    @property
    def darkgray(cls) -> Color:
        """
        The default darkgray color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["darkgray"])

    @classmethod
    @property
    def gray(cls) -> Color:
        """
        The default gray color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["gray"])

    @classmethod
    @property
    def lightgray(cls) -> Color:
        """
        The default lightgray color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["lightgray"])

    @classmethod
    @property
    def snow(cls) -> Color:
        """
        The default snow color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.grayscale_defaults["snow"])

    @classmethod
    @property
    def yellow(cls) -> Color:
        """
        The default yellow color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["yellow"])

    @classmethod
    @property
    def orange(cls) -> Color:
        """
        The default orange color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["orange"])

    @classmethod
    @property
    def red(cls) -> Color:
        """
        The default red color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["red"])

    @classmethod
    @property
    def scarlet(cls) -> Color:
        """
        The default scarlet color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["scarlet"])

    @classmethod
    @property
    def magenta(cls) -> Color:
        """
        The default magenta color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["magenta"])

    @classmethod
    @property
    def purple(cls) -> Color:
        """
        The default purple color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["purple"])

    @classmethod
    @property
    def violet(cls) -> Color:
        """
        The default violet color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["violet"])

    @classmethod
    @property
    def blue(cls) -> Color:
        """
        The default blue color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["blue"])

    @classmethod
    @property
    def cyan(cls) -> Color:
        """
        The default cyan color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["cyan"])

    @classmethod
    @property
    def turquoize(cls) -> Color:
        """
        The default turquoize color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["turquoize"])

    @classmethod
    @property
    def green(cls) -> Color:
        """
        The default green color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["green"])

    @classmethod
    @property
    def lime(cls) -> Color:
        """
        The default lime color. To see the RGB values, check out the |default|.
        """
        return Color(*Defaults.color_defaults["lime"])
