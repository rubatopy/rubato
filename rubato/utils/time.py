"""
A time class to monitor time and to call functions in the future.
"""
from typing import Callable
from pygame.time import Clock, get_ticks


clock = Clock()
calls = {}
sorted_calls = []  # of the call keys

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

def set(new_clock: "Clock"):
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


def delayed_call(delta_time: int, func: Callable):
    """
    Calls the function func at a later

    :param delta_time: The time in milliseconds to run the function at.
    :param func: The function to call.
    """
    global sorted_calls
    run_at = delta_time + now()

    if calls.get(run_at):
        calls[run_at].append(func)
    else:
        calls[run_at] = [func]
    sorted_calls = sorted(calls.keys())


def process_calls():
    """Processes the calls needed"""
    for call in sorted_calls:
        if call <= now():
            for func in calls[call]:
                func()
            del calls[call]
        else:
            break
