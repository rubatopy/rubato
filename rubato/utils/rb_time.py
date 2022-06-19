"""
A static time class to monitor time and to call functions in the future.

"""
from dataclasses import dataclass, field
from typing import Callable, List
import heapq
import sdl2


@dataclass(order=True)
class TimerTask:
    time: int
    task: Callable = field(compare=False)


@dataclass(order=True)
class ScheduledTask:
    time: int
    interval: int = field(compare=False)
    task: Callable = field(compare=False)


class Time:
    """
    The time class

    Attributes:
        frames (int): The total number of elapsed frames since the start of the game.

        fps (float): The current fps of this frame.

        target_fps (float): The fps that the game should try to run at. 0 means that the game's fps will not be capped.
            Defaults to 0.
        physics_fps (float): The fps that the physics should run at. Defaults to 60.

        delta_time (int): The number of seconds since the last frame.
        fixed_delta (int): The number of seconds since the last fixed update.
    """

    frames = 0
    _sorted_frame_times: List[TimerTask] = []

    _sorted_task_times: List[TimerTask] = []

    _sorted_scheduled_times: List[ScheduledTask] = []

    delta_time: float = 0.001
    fixed_delta: float = 0
    normal_delta: float = 0
    fps = 60

    physics_counter = 0

    _past_fps = [0] * 250

    target_fps = 0  # this means no cap
    capped = False

    physics_fps = 60

    @classmethod
    @property
    def smooth_fps(cls) -> float:
        """The average fps over the past 250 frames. This is a get-only property."""
        return sum(cls._past_fps) / 250

    @classmethod
    @property
    def now(cls) -> int:
        """The time since the start of the game, in milliseconds. This is a get-only property."""
        return sdl2.SDL_GetTicks64()

    @classmethod
    def delayed_call(cls, time_delta: int, func: Callable):
        """
        Calls the function func at a later time.

        Args:
            time_delta: The time from now (in milliseconds)
                to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._sorted_task_times, TimerTask(time_delta + cls.now, func))

    @classmethod
    def delayed_frames(cls, frames_delta: int, func: Callable):
        """
        Calls the function func at a later frame.

        Args:
            frames_delta: The number of frames to wait.
            func: The function to call
        """

        heapq.heappush(cls._sorted_frame_times, TimerTask(cls.frames + frames_delta, func))

    @classmethod
    def scheduled_call(cls, interval: int, func: Callable):
        """
        Calls the function func at a scheduled interval.

        Args:
            interval: The interval (in milliseconds) to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._sorted_scheduled_times, ScheduledTask(interval + cls.now, interval, func))

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
        cls.fps = 1 / cls.delta_time

        del cls._past_fps[0]
        cls._past_fps.append(cls.fps)

        # pylint: disable=comparison-with-callable
        processing = True
        while processing and cls._sorted_frame_times:
            if cls._sorted_frame_times[0].time <= cls.now:
                timer_task = heapq.heappop(cls._sorted_frame_times)
                timer_task.task()
            else:
                processing = False

        processing = True
        while processing and cls._sorted_task_times:
            if cls._sorted_task_times[0].time <= cls.now:
                timer_task = heapq.heappop(cls._sorted_task_times)
                timer_task.task()
            else:
                processing = False

        processing = True
        while processing and cls._sorted_scheduled_times:
            if dt := (cls._sorted_scheduled_times[0].time - cls.now) <= 0:
                scheduled_task = heapq.heappop(cls._sorted_scheduled_times)
                scheduled_task.task()
                scheduled_task.time += scheduled_task.interval - dt
                heapq.heappush(cls._sorted_scheduled_times, scheduled_task)
            else:
                processing = False
