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
        """
        Quickly rounds down a number.

        Args:
            x (float): The number to round.

        Returns:
            int: The rounded number.
        """
        xi = int(x)
        return xi - 1 if x < xi else xi

    @staticmethod
    def ceil(x: float) -> int:
        """
        Quickly rounds up a number.

        Args:
            x (float): The number to round.

        Returns:
            int: The rounded number.
        """
        xi = int(x)
        return xi + 1 if x > xi else xi

    @staticmethod
    def round(x: float) -> int:
        """
        Quickly rounds a number.

        Args:
            x (float): The number to round.

        Returns:
            int: The rounded number.
        """
        return int(x - .5) if x < 0 else int(x + .5)

    @staticmethod
    def is_int(x: float, error: float) -> bool:
        """
        Checks if a number is an integer.

        Args:
            x (float): The number to check.
            error (float): The error margin.

        Returns:
            bool: True if the number is an integer within the error.
        """
        return abs(round(x) - x) < error

    @staticmethod
    def gen_primes():
        """
        Generate an infinite sequence of prime numbers.
        Notes:
            Sieve of Eratosthenes
            Code by David Eppstein, UC Irvine, 28 Feb 2002
            http://code.activestate.com/recipes/117119/
        Returns:
            generator: A generator of prime numbers.
        """
        # Maps composites to primes witnessing their compositeness.
        # This is memory efficient, as the sieve is not "run forward"
        # indefinitely, but only as long as required by the current
        # number being tested.
        #
        d = {}

        # The running integer that's checked for primeness
        q = 2

        while True:
            if q not in d:
                # q is a new prime.
                # Yield it and mark its first multiple that isn't
                # already marked in previous iterations
                #
                yield q
                d[q * q] = [q]
            else:
                # q is composite. D[q] is the list of primes that
                # divide it. Since we've reached q, we no longer
                # need it in the map, but we'll mark the next
                # multiples of its witnesses to prepare for larger
                # numbers
                #
                for p in d[q]:
                    d.setdefault(p + q, []).append(p)
                del d[q]

            q += 1
