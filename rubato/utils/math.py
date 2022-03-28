"""
A more complete math class.

Attributes:
    INFINITY (float): The max value of a float.
"""
from typing import Union

INFINITY = float('inf')


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


def sign(n: Union[float, int]) -> int:
    """
    Checks the sign of n.

    Args:
        n: A number to check.

    Returns:
        int: The sign of the number. (1 for positive, -1 for negative)
    """
    return (n > 0) - (n < 0)


def lerp(a: Union[float, int], b: Union[float, int], t: float) -> float:
    """
    Linearly interpolates between lower and upper bounds by t

    Args:
        a: The lower bound.
        a: The upper bound.
        t: Distance between upper and lower (1 gives b, 0 gives a).

    Returns:
        float: The lerped value.
    """
    return a + t * (b - a)
