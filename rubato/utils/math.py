"""
The math module includes some helper functions for commonly used equations.
"""
import math


class Math:
    """
    A more complete math class.

    Attributes:
        INF (float): The max value of a float.
    """
    INF = float('inf')

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
            int: The sign of the number. (1 for positive, -1 for negative)
        """
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
    def simplify_radical(square_rooted: int) -> tuple:
        """
        Simplifies a radical.
        Args:
            square_rooted (int): The radical to simplify (inside the sqrt).

        Returns:
            tuple: The simplified radical, (multiple, radical).
        """
        error = 0.0000001
        if Math.is_int(square_rooted, error):
            return 1, square_rooted
        generator = Math.gen_primes()
        divisible_by = ()
        keep = False
        val = 1
        while (possible := square_rooted / (val := (val if keep else next(generator))) ** 2) >= 1:
            if Math.is_int(possible, error):
                keep = True
                divisible_by = (val, round(possible))
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
            tuple: The simplified fraction, (numerator, denominator).
        """
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
