"""
Defines helper methods for rtree.
"""
from typing import Callable
import math


def quickselect(arr: list[any], k: any, left: int = 0, right: int = None, compare: Callable = None):
    """
    Runs a Floyd-Rivest selection algorithm on the array, based on the javascript quickselect library.

    Args:
        arr (list[any]): The array to partially sort.
        k (int): The middle index of the partial sorting.
        left (int, optional): Left index of the range to sort. Defaults to 0.
        right (int, optional): Right index of the range to sort. Defaults to arr.length - 1.
        compare (Callable, optional): The compare function.
            Defaults to a default comparison, which is -1 if a < b, 1 if a > b, and 0 otherwise.
    """
    quickselect_step(arr, k, left, right or (arr.length - 1), compare or default_compare)


def quickselect_step(arr, k, left, right, compare):
    while right > left:
        if right - left > 600:
            n = right - left + 1
            m = k - left + 1
            z = math.log(n)
            s = .5 * math.exp(2 * z / 3)
            sd = .5 * math.sqrt(z * s * (n - s) / n) * (-1 if m - n / 2 < 0 else 1)
            new_left = max(left, math.floor(k - m * s / n + sd))
            new_right = min(right, math.floor(k + (n - m) * s / n + sd))
            quickselect_step(arr, k, new_left, new_right, compare)

        t = arr[k]
        i, j = left, right

        arr[left], arr[k] = arr[k], arr[left]
        if compare(arr[right], t) > 0:
            arr[left], arr[right] = arr[right], arr[left]

        while i < j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
            while compare(arr[i], t) < 0:
                i += 1
            while compare(arr[j], t) > 0:
                j -= 1

        if compare(arr[left], t) == 0:
            arr[left], arr[j] = arr[j], arr[left]
        else:
            j += 1
            arr[j], arr[right] = arr[right], arr[j]

        if j <= k:
            left = j + 1
        if k <= j:
            right = j - 1


def default_compare(a, b):
    return -1 if a < b else (1 if a > b else 0)
