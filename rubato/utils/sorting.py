"""
sorting algorithms
"""


def binary_search(arr: list, low: int, high: int, val: any) -> int:
    """
    A binary search algorithm.

    Args:
        arr: Array to be find index of insertion.
        low: The low interval in which you want to find the position.
        high: The high interval in which you want to find the position.
        val: Value in the array of which you want to find the position.

    Returns:
        int: The index of value in the array if it exists, otherwise it bit inverts
        (unary operator) the index if the element is not in the array.
    """

    # Check base case
    if high >= low:

        mid = (high + low) // 2
        # If element is present at the middle itself
        if arr[mid] == val:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > val:
            return binary_search(arr, low, mid - 1, val)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, val)

    else:
        # Element is not present in the array
        if high < len(arr) - 1:
            return ~(high + 1)
            # this way it will be negative if it is not present
        else:
            return ~len(arr)
