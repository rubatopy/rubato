"""
A static time class to monitor time and to call functions in the future.

"""
from typing import Callable
import heapq
import sdl2
from rubato.helpers import *


class Time(metaclass=StaticClass):
    """
    The time class

    Attributes:
        frames (int): The total number of elapsed frames since the start of the
            game.
        fps (float): The current fps of this frame.
        smooth_fps (float): The average fps over the past 5 frames.
        target_fps (float): The fps that the game should try to run at. 0 means that the game's fps will not be capped.
            Defaults to 0.
        physics_fps (float): The fps that the physics should run at. Defaults to 60.
        now(int): The time since the start of the game, in milliseconds.
        delta_time (int): The number of milliseconds since the last frame.
        fixed_delta (int): The number of milliseconds since the last fixed update.
    """

    frames = 0
    frame_tasks = {}
    sorted_frame_times = []

    tasks = {}
    sorted_task_times = []

    delta_time: int = 0
    fixed_delta: int = 0
    fps = 60

    physics_counter = 0

    _past_fps = [0]

    target_fps = 0  # this means no cap
    physics_fps = 60

    @classproperty
    def smooth_fps(self) -> float:
        """The average fps over the past 5 frames."""
        return sum(self._past_fps) / len(self._past_fps)

    @classproperty
    def now(self) -> int:
        """
        The time since the start of the game, in milliseconds.
        """
        return sdl2.timer.SDL_GetTicks64()

    @classmethod
    def delayed_call(cls, time_delta: int, func: Callable):
        """
        Calls the function func at a later

        Args:
            time_delta: The time from now (in milliseconds)
                to run the function at.
            func: The function to call.
        """
        run_at = time_delta + cls.now

        if cls.tasks.get(run_at):
            cls.tasks[run_at].append(func)
        else:
            cls.tasks[run_at] = [func]
            heapq.heappush(cls.sorted_task_times, run_at)

    @classmethod
    def delayed_frames(cls, frames_delta: int, func: Callable):
        """
        Calls the function func at a later frame.

        Args:
            frames_delta: The number of frames to wait.
            func: The function to call
        """
        frame_call = cls.frames + frames_delta

        if cls.frame_tasks.get(frame_call):
            cls.frame_tasks[frame_call].append(func)
        else:
            cls.frame_tasks[frame_call] = [func]
            heapq.heappush(cls.sorted_frame_times, frame_call)

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

        if len(cls._past_fps) > 5:
            cls._past_fps.pop(0)
        cls._past_fps.append(cls.fps)

        if len(cls.sorted_frame_times) > 0:
            processing = True
            while processing:
                if cls.sorted_frame_times[0] <= cls.now:
                    task_time = heapq.heappop(cls.sorted_frame_times)
                    for func in cls.frame_tasks[task_time]:
                        func()
                    del cls.frame_tasks[task_time]
                else:
                    processing = False

        if len(cls.sorted_task_times) > 0:
            processing = True
            while processing:
                if cls.sorted_task_times[0] <= cls.now:
                    task_time = heapq.heappop(cls.sorted_task_times)
                    for func in cls.tasks[task_time]:
                        func()
                    del cls.tasks[task_time]
                else:
                    processing = False
