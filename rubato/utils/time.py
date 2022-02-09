"""
A time class to monitor time and to call functions in the future.
"""
from typing import Callable
from pygame.time import Clock, get_ticks

clock = Clock()
calls = {}
sorted_call_times = []  # of the call keys


def delta_time(form: str = "milli") -> int:
    """
    Gets the time since the last frame.

    Args:
        form: The format the output should be (sec, milli). Defaults to milli.

    Raises:
        ValueError: The form is not "sec" or "milli".

    Returns:
        int: Time since the last frame, in the given form.
    """
    if form == "sec":
        return milli_to_sec(clock.get_time())
    elif form == "milli":
        return clock.get_time()
    else:
        raise ValueError(f"Style {form} is not valid")


def now() -> int:
    """
    Gets the time since the start of the game, in milliseconds.

    Returns:
        int: Time since the start of the game, in milliseconds.
    """
    return get_ticks()


def delayed_call(time_delta: int, func: Callable):
    """
    Calls the function func at a later

    Args:
        time_delta: The time from now (in milliseconds)
            to run the function at.
        func: The function to call.
    """
    run_at = time_delta + now()

    if calls.get(run_at):
        calls[run_at].append(func)
    else:
        calls[run_at] = [func]

    proper_index = _binary_search(sorted_call_times, 0,
                                  len(sorted_call_times) - 1, run_at)
    if proper_index < 0:  # time stamp not currently in array
        proper_index = ~proper_index
        sorted_call_times.insert(proper_index, run_at)
    # otherwise we do not want to re-add time stamp


def milli_to_sec(milli: int) -> float:
    """
    Converts milliseconds to seconds.

    Args:
        milli: A number in milliseconds.
    Returns:
        float: The converted number in seconds.
    """
    return milli / 1000


def set_clock(new_clock: "Clock"):
    """
    Allows you to set the clock object property to a Pygame Clock object.

    Args:
        clock: A pygame Clock object.
    """
    global clock
    clock = new_clock


def process_calls():
    """Processes the calls needed"""
    for call in sorted_call_times:
        if call <= now():
            for func in calls[call]:
                func()
            del calls[call]
            sorted_call_times.remove(call)
        else:
            break


def _binary_search(arr: list, low: int, high: int, val: any) -> int:
    """
    A binary search algorithm.

    Args:
        arr: Array to be find index of insertion. Array must be pre sorted.
        low: The low interval in which you want to find the position.
        high: The high interval in which you want to find the position.
        val: Value in the array of which you want to find the position.

    Returns:
        int: The index of value in the array if it exists, otherwise it bit
        inverts (unary operator) the index if the element is not in the array.
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
            return _binary_search(arr, low, mid - 1, val)

        # Else the element can only be present in right subarray
        else:
            return _binary_search(arr, mid + 1, high, val)

    else:
        # Element is not present in the array
        if high < len(arr) - 1:
            return ~(high + 1)
            # this way it will be negative if it is not present
        else:
            return ~len(arr)
