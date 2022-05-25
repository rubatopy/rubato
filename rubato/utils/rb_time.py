"""
A static time class to monitor time and to call functions in the future.

"""
from dataclasses import dataclass, field
from typing import Callable
import heapq
import sdl2


class TimeProperties(type):
    """
    Defines static property methods for Time.

    Warning:
        This is only a metaclass for the class below it, so you wont be able to access this class.
        To use the property methods here, simply access them as you would any other Time property.
    """

    @property
    def smooth_fps(cls) -> float:
        """The average fps over the past 250 frames. This is a get-only property."""
        return sum(cls._past_fps) / 250

    @property
    def now(cls) -> int:
        """The time since the start of the game, in milliseconds. This is a get-only property."""
        return sdl2.SDL_GetTicks64()


@dataclass(order=True)
class TimerTask:
    time: int
    task: Callable=field(compare=False)


class Time(metaclass=TimeProperties):
    """
    The time class

    Attributes:
        frames (int): The total number of elapsed frames since the start of the game.

        fps (float): The current fps of this frame.

        target_fps (float): The fps that the game should try to run at. 0 means that the game's fps will not be capped.
            Defaults to 0.
        physics_fps (float): The fps that the physics should run at. Defaults to 60.

        delta_time (int): The number of milliseconds since the last frame.
        fixed_delta (int): The number of milliseconds since the last fixed update.
    """

    frames = 0
    sorted_frame_times = []

    sorted_task_times = []

    delta_time: int = 1
    fixed_delta: int = 0
    normal_delta: int = 0
    fps = 60

    physics_counter = 0

    _past_fps = [0] * 250

    target_fps = 0  # this means no cap
    capped = False

    physics_fps = 60

    @classmethod
    def delayed_call(cls, time_delta: int, func: Callable):
        """
        Calls the function func at a later time.

        Args:
            time_delta: The time from now (in milliseconds)
                to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls.sorted_task_times, TimerTask(time_delta + cls.now, func))

    @classmethod
    def delayed_frames(cls, frames_delta: int, func: Callable):
        """
        Calls the function func at a later frame.

        Args:
            frames_delta: The number of frames to wait.
            func: The function to call
        """

        heapq.heappush(cls.sorted_frame_times, TimerTask(cls.frames + frames_delta, func))

    @classmethod
    def milli_to_sec(cls, milli: int) -> float:
        """
        Converts milliseconds to seconds.

        Args:
            milli: A number in milliseconds.
        Returns:
            float: The converted number in seconds.
        """
        return milli / 1000

    @classmethod
    def sec_to_milli(cls, sec: int) -> float:
        """
        Converts seconds to milliseconds.

        Args:
            sec: A number in seconds.
        Returns:
            float: The converted number in milliseconds.
        """
        return sec * 1000

    @classmethod
    def process_calls(cls):
        """Processes the delayed function call as needed"""
        cls.frames += 1
        cls.fps = 1000 / cls.delta_time

        del cls._past_fps[0]
        cls._past_fps.append(cls.fps)

        processing = True
        while processing and cls.sorted_frame_times:
            if cls.sorted_frame_times[0].time <= cls.now:
                timer_task = heapq.heappop(cls.sorted_frame_times)
                timer_task.task()
            else:
                processing = False

        processing = True
        while processing and cls.sorted_task_times:
            if cls.sorted_task_times[0].time <= cls.now:
                timer_task = heapq.heappop(cls.sorted_task_times)
                timer_task.task()
            else:
                processing = False
