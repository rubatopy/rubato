"""
This color module contains the Color class, which is used to represent colors in the game.
"""
from __future__ import annotations
from random import randint, choice
import sdl2

from . import Math, Display


class Color:
    """
    An RGBA color.

    Args:
        r: The red value. Defaults to 0.
        g: The green value. Defaults to 0.
        b: The blue value. Defaults to 0.
        a: The alpha value. Defaults to 255.

    Attributes:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
        a (int): The alpha value.
    """

    # [colordef]
    _color_defaults = {
        "yellow": (253, 203, 110),  # . . . . . . . . . . . . . . . tuple
        "scarlet": (214, 48, 49),  #. . . . . . . . . . . . . . . . tuple
        "violet": (108, 92, 231),  #. . . . . . . . . . . . . . . . tuple
        "turquoize": (0, 206, 201),  #. . . . . . . . . . . . . . . tuple
        "orange": (225, 112, 85),  #. . . . . . . . . . . . . . . . tuple
        "magenta": (232, 67, 147),  # . . . . . . . . . . . . . . . tuple
        "blue": (9, 132, 227),  # . . . . . . . . . . . . . . . . . tuple
        "green": (0, 184, 148),  #. . . . . . . . . . . . . . . . . tuple
        "red": (255, 118, 117),  #. . . . . . . . . . . . . . . . . tuple
        "purple": (162, 155, 254),  # . . . . . . . . . . . . . . . tuple
        "cyan": (116, 185, 255),  # . . . . . . . . . . . . . . . . tuple
        "lime": (85, 239, 196),  #. . . . . . . . . . . . . . . . . tuple

        # colorwheel used (rgb values are not identical):
        # https://upload.wikimedia.org/wikipedia/commons/5/54/RGV_color_wheel_1908.png
    }
    # [/colordef]
    # [grayscaledef]
    _grayscale_defaults = {
        "black": (0, 0, 0),  #. . . . . . . . . . . . . . . . . . . tuple
        "white": (255, 255, 255),  #. . . . . . . . . . . . . . . . tuple
        "night": (20, 20, 22),  # . . . . . . . . . . . . . . . . . tuple
        "darkgray": (45, 52, 54),  #. . . . . . . . . . . . . . . . tuple
        "gray": (99, 110, 114),  #. . . . . . . . . . . . . . . . . tuple
        "lightgray": (178, 190, 195),  #. . . . . . . . . . . . . . tuple
        "snow": (223, 230, 233),  # . . . . . . . . . . . . . . . . tuple
    }

    # [/grayscaledef]

    def __init__(self, r: int | float = 0, g: int | float = 0, b: int | float = 0, a: int | float = 255):
        self.r = int(Math.clamp(r, 0, 255))
        self.g = int(Math.clamp(g, 0, 255))
        self.b = int(Math.clamp(b, 0, 255))
        self.a = int(Math.clamp(a, 0, 255))

    @property
    def rgba32(self):
        """The RGBA32 representation of the color."""
        return sdl2.SDL_MapRGBA(Display.format, *self.to_tuple())

    def darker(self, amount: int = 20):
        """
        Returns a darker copy of the color. It subtracts ``amount`` from the RGB values.

        Args:
            amount: How much darker. Defaults to 20.

        Returns:
            Color: The resultant color.
        """
        return Color(max(self.r - amount, 0), max(self.g - amount, 0), max(self.b - amount, 0), self.a)

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
                ((1 - s) * (self.b**2.2) + s * (other.b**2.2))**(1 / 2.2),
                a * 255,
            )
        return Color(
            ((1 - t) * (self.r**2.2) + t * (other.r**2.2))**(1 / 2.2),
            ((1 - t) * (self.g**2.2) + t * (other.g**2.2))**(1 / 2.2),
            ((1 - t) * (self.b**2.2) + t * (other.b**2.2))**(1 / 2.2),
            (1 - t) * self.a + t * other.a,
        )

    def to_tuple(self) -> tuple[int, int, int, int]:
        """
        Converts the Color to a tuple.

        Returns:
            tuple(int, int, int, int): The tuple representing the color.
        """
        return self.r, self.g, self.b, self.a

    def to_hex(self) -> str:
        """
        Converts the Color to a hexadecimal string.

        Returns:
            str: The hexadecimal output in lowercase. (i.e. ffffffff)
        """
        return f"{self.r:02x}{self.g: 02x}{self.b: 02x}{self.a: 02x}".replace(" ", "")

    def to_hsv(self) -> tuple[float | int, float | int, float]:
        """
        Converts the Color to a tuple containing its HSV values.

        Returns:
            tuple[int]: The Color values as HSV in the form of a tuple.
        """
        # R, G, B values are divided by 255

        # to change the range from 0..255 to 0..1:
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0

        # h, s, v = hue, saturation, value
        cmax = max(r, g, b)  # maximum of r, g, b
        cmin = min(r, g, b)  # minimum of r, g, b
        diff = cmax - cmin  # diff of cmax and cmin.

        # if cmax and cmax are equal then h = 0
        if cmax == cmin:
            h = 0

        # if cmax equal r then compute h
        elif cmax == r:
            h = (60 * ((g - b) / diff) + 360) % 360

        # if cmax equal g then compute h
        elif cmax == g:
            h = (60 * ((b - r) / diff) + 120) % 360

        # if cmax equal b then compute h
        elif cmax == b:
            h = (60 * ((r - g) / diff) + 240) % 360

        # if cmax equal zero
        if cmax == 0:
            s = 0
        else:
            s = (diff / cmax)

        # compute v
        v = cmax
        return h, s, v, self.a / 255

    @staticmethod
    def random_default(grayscale=False) -> Color:
        """
        Returns a random default Color.

        Args:
            grayscale (bool, optional): Whether to add grayscale colors. Defaults to False.

        Returns:
            Color: A random default Color.
        """

        return Color(
            *
            choice(list(Color._color_defaults.values()) + list(Color._grayscale_defaults.values() if grayscale else []))
        )

    @classmethod
    def from_rgba32(cls, rgba32: int) -> Color:
        """
        Creates a Color object from an RGBA32 representation.

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
        Creates a Color object from a hex string.

        Args:
            h: The hexadecimal value in the format "RRGGBBAA".

        Returns:
            Color: The Color object.
        """
        lv = len(h)
        if lv < 8:
            raise ValueError(f"Invalid hex string: {h}")
        try:
            return cls(*(int(h[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
        except ValueError:
            raise ValueError(f"Invalid hex string: {h}") from ValueError

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, a: float = 1) -> Color:
        """
        Creates a Color object from HSV values.

        Args:
            h: The hue degree (0 to 360).
            s: The saturation proportion (0 to 1).
            v: The value proportion (0 to 1).
            a: The alpha proportion (0 to 1).

        Returns:
            Color: The Color object.
        """
        hh = h / 60
        i = int(hh)
        ff = hh - i
        x = v * 255
        p = x * (1 - s)
        q = x * (1 - (s * ff))
        t = x * (1 - (s * (1 - ff)))
        return cls(*((x, t, p), (q, x, p), (p, x, t), (p, q, x), (t, p, x), (x, p, q), (x, p, q))[i], a * 255)

    @classmethod
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
        The default black color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["black"])

    @classmethod
    @property
    def white(cls) -> Color:
        """
        The default white color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["white"])

    @classmethod
    @property
    def night(cls) -> Color:
        """
        The default night color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["night"])

    @classmethod
    @property
    def darkgray(cls) -> Color:
        """
        The default darkgray color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["darkgray"])

    @classmethod
    @property
    def gray(cls) -> Color:
        """
        The default gray color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["gray"])

    @classmethod
    @property
    def lightgray(cls) -> Color:
        """
        The default lightgray color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["lightgray"])

    @classmethod
    @property
    def snow(cls) -> Color:
        """
        The default snow color. To see the RGB values, check out the :ref:`Grayscale defaults <grayscaledef>`.
        """
        return Color(*Color._grayscale_defaults["snow"])

    @classmethod
    @property
    def yellow(cls) -> Color:
        """
        The default yellow color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["yellow"])

    @classmethod
    @property
    def orange(cls) -> Color:
        """
        The default orange color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["orange"])

    @classmethod
    @property
    def red(cls) -> Color:
        """
        The default red color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["red"])

    @classmethod
    @property
    def scarlet(cls) -> Color:
        """
        The default scarlet color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["scarlet"])

    @classmethod
    @property
    def magenta(cls) -> Color:
        """
        The default magenta color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["magenta"])

    @classmethod
    @property
    def purple(cls) -> Color:
        """
        The default purple color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["purple"])

    @classmethod
    @property
    def violet(cls) -> Color:
        """
        The default violet color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["violet"])

    @classmethod
    @property
    def blue(cls) -> Color:
        """
        The default blue color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["blue"])

    @classmethod
    @property
    def cyan(cls) -> Color:
        """
        The default cyan color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["cyan"])

    @classmethod
    @property
    def turquoize(cls) -> Color:
        """
        The default turquoize color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["turquoize"])

    @classmethod
    @property
    def green(cls) -> Color:
        """
        The default green color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["green"])

    @classmethod
    @property
    def lime(cls) -> Color:
        """
        The default lime color. To see the RGB values, check out the :ref:`Color defaults <colordef>`.
        """
        return Color(*Color._color_defaults["lime"])

    def __str__(self):
        return str(f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})")

    def __eq__(self, other: Color) -> bool:
        if isinstance(other, Color):
            return self.r == other.r and self.b == other.b and self.g == other.g and self.a == other.a
        return False

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))
