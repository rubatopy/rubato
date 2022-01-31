"""
A time class to monitor time and to call functions in the future.
"""
from typing import Callable
from pygame.time import Clock, get_ticks
from rubato.utils.sorting import binary_search

clock = Clock()
calls = {}
sorted_call_times = []  # of the call keys


def delta_time(form: str = "milli") -> int:
    """
    Gets the time since the last frame, in milliseconds.

    :param form: The format the output should be (sec, milli)
    :return: Time since the last frame, in the given form.
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

    :return: Time since the start of the game, in milliseconds.
    """
    return get_ticks()


def set_clock(new_clock: "Clock"):
    """
    Allows you to set the clock object property to a Pygame Clock object.

    :param clock: A pygame Clock object.
    """
    global clock
    clock = new_clock


def milli_to_sec(milli: int) -> float:
    """
    Converts milliseconds to seconds.

    :param milli: A number in milliseconds.
    :return: The converted number in seconds.
    """
    return milli / 1000


def delayed_call(time_delta: int, func: Callable):
    """
    Calls the function func at a later

    :param time_delta: The time from now (in milliseconds)
    to run the function at.
    :param func: The function to call.
    """
    run_at = time_delta + now()

    if calls.get(run_at):
        calls[run_at].append(func)
    else:
        calls[run_at] = [func]

    proper_index = binary_search(sorted_call_times, 0,
                                 len(sorted_call_times) - 1, run_at)
    if proper_index < 0:  # time stamp not currently in array
        proper_index = ~proper_index
        sorted_call_times.insert(proper_index, run_at)
    # otherwise we do not want to re-add time stamp


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
