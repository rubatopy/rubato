"""
The math module includes some helper functions for commonly used equations.
"""
from typing import Union


class Math:
    """
    A more complete math class.

    Attributes:
        INF (float): The max value of a float.
    """
    INF = float('inf')

    @staticmethod
    def clamp(a: Union[float, int], lower: Union[float, int], upper: Union[float, int]) -> float:
        """
        Clamps a value.

        Args:
            a: The value to clamp.
            lower: The lower bound of the clamp.
            upper: The upper bound of the clamp.

        Returns:
            float: The clamped result.
        """
        return min(max(a, lower), upper)

    @staticmethod
    def sign(n: Union[float, int]) -> int:
        """
        Checks the sign of n.

        Args:
            n: A number to check.

        Returns:
            int: The sign of the number. (1 for positive, -1 for negative)
        """
        return (n >= 0) - (n < 0)

    @staticmethod
    def lerp(a: Union[float, int], b: Union[float, int], t: float) -> float:
        """
        Linearly interpolates between lower and upper bounds by t

        Args:
            a: The lower bound.
            b: The upper bound.
            t: Distance between upper and lower (1 gives b, 0 gives a).

        Returns:
            float: The lerped value.
        """
        return a + t * (b - a)

    @staticmethod
    def floor(x: float) -> int:
        """Quickly rounds down a number."""
        xi = int(x)
        return xi - 1 if x < xi else xi

    @staticmethod
    def ceil(x: float) -> int:
        """Quickly rounds up a number."""
        xi = int(x)
        return xi + 1 if x > xi else xi

    @staticmethod
    def round(x: float) -> int:
        """Quickly rounds a number."""
        return int(x - .5) if x < 0 else int(x + .5)
