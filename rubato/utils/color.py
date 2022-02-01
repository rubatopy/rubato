"""
A Color implementation.
"""
from rubato.utils import PMath


class RGB:
    """
    An RGB implentation.

    Attributes:
        r (float): The red value.
        g (float): The green value.
        b (float): The blue value.
    """

    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0):
        """
        Initializes an RGB class.

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
        if isinstance(other, type(RGB)):
            return \
                abs(self.r - other.r) < 0.0001 and \
                abs(self.g - other.g) < 0.0001 and \
                abs(self.b - other.b) < 0.0001
        return False

    def check_values(self):
        """
        Makes the RGB values legit. In other words, clamps them between 0 and
        255.
        """
        self.r = PMath.clamp(self.r, 0, 255)
        self.g = PMath.clamp(self.g, 0, 255)
        self.b = PMath.clamp(self.b, 0, 255)

    def lerp(self, other: "RGB", t: float) -> "RGB":
        """
        Lerps between this color and another.

        Args:
            other: The other RGB to lerp with.
            t: The amount to lerp.

        Returns:
            RGB: The lerped RGB. This RGB remains unchanged.
        """
        t = PMath.clamp(t, 0, 1)
        return RGB(
            self.r + (other.r - self.r) * t,
            self.g + (other.g - self.g) * t,
            self.b + (other.b - self.b) * t,
        )

    def to_hex(self) -> str:
        """
        Converts the RGB to hexadecimal.

        Returns:
            str: The hexadecimal output in lowercase. (i.e. ffffff)
        """
        return (f"{format(self.r, '02x')}" + f"{format(self.g, '02x')}" +
                f"{format(self.b, '02x')}")

    @staticmethod
    def from_hex(h: str) -> "RGB":
        """
        Creates an RGB from a hex string.

        Args:
            h: The hexadecimal value in lowercase.

        Returns:
            RGB: The RGB value.
        """
        lv = len(h)
        h = tuple(int(h[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        return RGB(h[0], h[1], h[2])

    @classmethod
    @property
    def black(cls):
        """
        An RGB class of the color black.

        Returns:
            RGB: (0, 0, 0)
        """
        return RGB(0, 0, 0)

    @classmethod
    @property
    def white(cls):
        """
        An RGB class of the color white.

        Returns:
            RGB: (255, 255, 255)
        """
        return RGB(255, 255, 255)

    @classmethod
    @property
    def red(cls):
        """
        An RGB class of the color red.

        Returns:
            RGB: (255, 0, 0)
        """
        return RGB(255, 0, 0)

    @classmethod
    @property
    def lime(cls):
        """
        An RGB class of the color lime.

        Returns:
            RGB: (0, 255, 0)
        """
        return RGB(0, 255, 0)

    @classmethod
    @property
    def blue(cls):
        """
        An RGB class of the color blue.

        Returns:
            RGB: (0, 0, 255)
        """
        return RGB(0, 0, 255)

    @classmethod
    @property
    def yellow(cls):
        """
        An RGB class of the color yellow.

        Returns:
            RGB: (255, 255, 0)
        """
        return RGB(255, 255, 0)

    @classmethod
    @property
    def cyan(cls):
        """
        An RGB class of the color cyan.

        Returns:
            RGB: (0, 255, 255)
        """
        return RGB(0, 255, 255)

    @classmethod
    @property
    def magenta(cls):
        """
        An RGB class of the color magenta.

        Returns:
            RGB: (255, 0, 255)
        """
        return RGB(255, 0, 255)

    @classmethod
    @property
    def silver(cls):
        """
        An RGB class of the color silver.

        Returns:
            RGB: (192, 192, 192)
        """
        return RGB(192, 192, 192)

    @classmethod
    @property
    def gray(cls):
        """
        An RGB class of the color gray.

        Returns:
            RGB: (128, 128, 128)
        """
        return RGB(128, 128, 128)

    @classmethod
    @property
    def maroon(cls):
        """
        An RGB class of the color maroon.

        Returns:
            RGB: (128, 0, 0)
        """
        return RGB(128, 0, 0)

    @classmethod
    @property
    def olive(cls):
        """
        An RGB class of the color olive.

        Returns:
            RGB: (128, 128, 0)
        """
        return RGB(128, 128, 0)

    @classmethod
    @property
    def green(cls):
        """
        An RGB class of the color green.

        Returns:
            RGB: (0, 128, 0)
        """
        return RGB(0, 128, 0)

    @classmethod
    @property
    def purple(cls):
        """
        An RGB class of the color purple.

        Returns:
            RGB: (128, 0, 128)
        """
        return RGB(128, 0, 128)

    @classmethod
    @property
    def teal(cls):
        """
        An RGB class of the color teal.

        Returns:
            RGB: (0, 128, 128)
        """
        return RGB(0, 128, 128)

    @classmethod
    @property
    def navy(cls):
        """
        An RGB class of the color navy.

        Returns:
            RGB: (0, 0, 128)
        """
        return RGB(0, 0, 128)
