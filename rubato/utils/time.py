"""
A time class to monitor time and to call functions in the future.

Attributes:
    frames (int): The total number of elapsed frames since the start of the
        game.
"""
from typing import Callable
import heapq
import sdl2

frames = 0
frame_tasks = {}
sorted_frame_times = []

tasks = {}
sorted_task_times = []

fixed_delta_time = 20
delta_time = 16
fps = 60

_past_fps = [0]

fps_cap = 0  # this means no cap

_last_frame = 0


def tick():
    global _last_frame, delta_time, fps

    if fps_cap > 0:
        cap = 1 / fps_cap
        cap = sec_to_milli(cap)
        sdl2.timer.SDL_Delay(now() - (_last_frame + cap))

    delta_time = now() - _last_frame
    fps = 1 / milli_to_sec(delta_time)

    if len(_past_fps) > 5:
        _past_fps.pop(0)
    _past_fps.append(fps)

    _last_frame = now()


def smooth_fps():
    return sum(_past_fps) / len(_past_fps)


def now() -> int:
    """
    Gets the time since the start of the game, in milliseconds.

    Returns:
        int: Time since the start of the game, in milliseconds.
    """
    return sdl2.timer.SDL_GetTicks64()


def delayed_call(time_delta: int, func: Callable):
    """
    Calls the function func at a later

    Args:
        time_delta: The time from now (in milliseconds)
            to run the function at.
        func: The function to call.
    """
    run_at = time_delta + now()

    if tasks.get(run_at):
        tasks[run_at].append(func)
    else:
        tasks[run_at] = [func]
        heapq.heappush(sorted_task_times, run_at)


def delayed_frames(frames_delta: int, func: Callable):
    """
    Calls the function func at a later frame.

    Args:
        frames_delta: The number of frames to wait.
        func: The function to call
    """
    frame_call = frames + frames_delta

    if frame_tasks.get(frame_call):
        frame_tasks[frame_call].append(func)
    else:
        frame_tasks[frame_call] = [func]
        heapq.heappush(sorted_frame_times, frame_call)


def milli_to_sec(milli: int) -> float:
    """
    Converts milliseconds to seconds.

    Args:
        milli: A number in milliseconds.
    Returns:
        float: The converted number in seconds.
    """
    return milli / 1000


def sec_to_milli(sec: int) -> float:
    """
    Converts seconds to milliseconds.

    Args:
        sec: A number in seconds.
    Returns:
        float: The converted number in milliseconds.
    """
    return sec * 1000


def process_calls():
    """Processes the calls needed"""
    global frames
    frames += 1

    if len(sorted_frame_times) > 0:
        processing = True
        while processing:
            if sorted_frame_times[0] <= now():
                task_time = heapq.heappop(sorted_frame_times)
                for func in frame_tasks[task_time]:
                    func()
                del frame_tasks[task_time]
            else:
                processing = False

    if len(sorted_task_times) > 0:
        processing = True
        while processing:
            if sorted_task_times[0] <= now():
                task_time = heapq.heappop(sorted_task_times)
                for func in tasks[task_time]:
                    func()
                del tasks[task_time]
            else:
                processing = False


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
