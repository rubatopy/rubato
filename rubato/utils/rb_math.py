"""
The math module includes some helper functions for commonly used equations.
"""
import math
from . import InitError


# THIS IS A STATIC CLASS
class Math:
    """
    Adds additonal functionality to the math module that is commonly used in game development.
    """
    INF: int = 2147483647
    """The max value of a 32-bit integer."""
    PI_HALF: float = math.pi / 2
    """The value of pi / 2."""
    PI_TWO: float = math.tau
    """The value of pi * 2."""

    def __init__(self) -> None:
        raise InitError(self)

    @staticmethod
    def clamp(a: float | int, lower: float | int, upper: float | int) -> float:
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
    def sign(n: float | int) -> int:
        """
        Checks the sign of n.

        Args:
            n: A number to check.

        Returns:
            The sign of the number. (1 for positive, 0 for 0, -1 for negative)
        """
        if n == 0:
            return 0
        return (n >= 0) - (n < 0)

    @staticmethod
    def lerp(a: float | int, b: float | int, t: float) -> float:
        """
        Linearly interpolates between lower and upper bounds by t

        Args:
            a: The lower bound.
            b: The upper bound.
            t: Distance between upper and lower (1 gives b, 0 gives a).

        Returns:
            float: The linearly interpolated value.
        """
        return a + t * (b - a)

    @classmethod
    def map(cls, variable, variable_lower, variable_upper, map_lower, map_upper):
        """
        Maps the variable from its range defined by lower and upper to a new range defined by map_lower and map_upper.

        Args:
            variable: The variable to map.
            variable_lower: The lower bound of the variable.
            variable_upper: The upper bound of the variable.
            map_lower: The lower bound of the new range.
            map_upper: The upper bound of the new range.

        Returns:
            float: The mapped value.
        """
        return cls.clamp(
            ((variable - variable_lower) / (variable_upper - variable_lower)) * (map_upper - map_lower) + map_lower,
            map_lower, map_upper
        )

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
    def is_int(x: float, error: float = 0) -> bool:
        """
        Checks if a float can be rounded to an integer without dropping decimal places (within a certain error).

        Args:
            x: The number to check.
            error: The error margin from int that we accept, used for float inaccuracy.

        Returns:
            True if the number is an integer within the error.
        """
        return abs(round(x) - x) <= error

    @staticmethod
    def simplify_sqrt(square_rooted: int) -> tuple:
        """
        Simplifies a square root.

        Args:
            square_rooted: The sqrt to simplify (inside the sqrt).

        Returns:
            The simplified square root, (multiple, square rooted).

        Example:
            Will try to simplify radicals.

            >>> Math.simplify_sqrt(16) # √16 = 4√1
            (4, 1)
            >>> Math.simplify_sqrt(26) # √26 = 1√26
            (1, 26)
            >>> Math.simplify_sqrt(20) # √20 = 2√5
        """

        error = 1e-10
        if Math.is_int(square_rooted**(1 / 2), error):
            return square_rooted**(1 / 2), 1
        generator = Math.gen_primes()
        divisible_by = (1, square_rooted)
        keep = False
        val = 1
        possible = 1
        while possible >= 1:
            val = (val * val if keep else next(generator))
            possible = square_rooted / val**2
            if Math.is_int(possible, error):
                keep = True
                divisible_by = (round(val), round(possible))
            else:
                keep = False
        return divisible_by

    @staticmethod
    def simplify(a: int, b: int) -> tuple:
        """
        Simplifies a fraction.

        Args:
            a: numerator.
            b: denominator.

        Returns:
            The simplified fraction, (numerator, denominator).
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("a and b must be integers.")
        div = math.gcd(a, b)

        return a // div, b // div

    @staticmethod
    def gen_primes():
        """
        Generate an infinite sequence of prime numbers. A python generator ie. must use next().

        Notes:
            Sieve of Eratosthenes
            Code by David Eppstein, UC Irvine, 28 Feb 2002
            http://code.activestate.com/recipes/117119/

        Returns:
            generator: A generator of prime numbers.

        Example:
            >>> generator = Math.gen_primes()
            >>> next(generator)
            2
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

    @staticmethod
    def north_deg_to_rad(deg: float) -> float:
        """
        Converts a north-degrees (naturally used in rubato) to east-radians.

        Args:
            deg: North-degrees.

        Returns:
            East-radians.
        """
        return math.radians(-(deg - 90))

    @staticmethod
    def rad_to_north_deg(rad: float) -> float:
        """
        Converts east-radians to north-degrees (naturally used in rubato).

        Args:
            rad: East-radians.

        Returns:
            North-degrees.
        """
        return -math.degrees(rad - Math.PI_HALF)
