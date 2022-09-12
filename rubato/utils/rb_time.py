"""
A static class to monitor time and to call functions at delay/interval.
"""
from dataclasses import dataclass, field
from typing import Callable
import heapq
import sdl2
from . import InitError


@dataclass(order=True)
class DelayedTask:
    """A task that is run after a specified number of milliseconds."""
    delay: int
    task: Callable = field(compare=False)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the DelayedTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class FramesTask:
    """A task that is run after a specified number of frames."""
    delay: int
    task: Callable = field(compare=False)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the FramesTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class ScheduledTask:
    """A task that is run every specified number of milliseconds."""
    interval: int = field(compare=False)
    task: Callable = field(compare=False)
    delay: int = field(default=0)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the ScheduledTask from invoking."""
        self.is_stopped = True


# THIS IS A STATIC CLASS
class Time:
    """
    Implements time-related functions in rubato.
    """

    frames: int = 0
    """The total number of elapsed frames since the start of the game."""

    _frame_queue: list[FramesTask] = []
    _task_queue: list[DelayedTask] = []
    _schedule_queue: list[ScheduledTask] = []

    _next_queue: list[Callable] = []

    _delta_time: float = 0.001
    fixed_delta: float = 0.1
    """The number of seconds since the last fixed update."""
    _normal_delta: float = 0
    fps = 60
    """The fps estimate using the last frame."""
    _frame_start: int = 0

    physics_counter: float = 0

    _fps_history: int = 120
    _past_fps = [0] * _fps_history
    _fps_index: int = 0

    target_fps = 0  # this means no cap
    """The fps that the game should try to run at. 0 means that the game's fps will not be capped. Defaults to 0."""
    capped: bool = False

    physics_fps = 60
    """The fps that the physics should run at. Defaults to 60."""

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    @property
    def delta_time(cls) -> float:
        """The number of seconds between the last frame and the current frame."""
        return cls._delta_time

    @classmethod
    @property
    def smooth_fps(cls) -> int:
        """The average fps over the past 120 frames. (get-only)."""
        return int(sum(cls._past_fps) / cls._fps_history)

    @classmethod
    def now(cls) -> int:
        """The time since the start of the game, in milliseconds."""
        return sdl2.SDL_GetTicks64()

    @classmethod
    @property
    def frame_start(cls) -> int:
        """
        Time from the start of the game to the start of the current frame, in milliseconds. (get-only)
        """
        return cls._frame_start

    @classmethod
    def _start_frame(cls):
        cls._frame_start = cls.now()

    @classmethod
    def _end_frame(cls):
        if cls.capped:
            delay = cls._normal_delta - cls.delta_time
            if delay > 0:
                sdl2.SDL_Delay(int(1000 * delay))

        while cls.now() == cls._frame_start:
            sdl2.SDL_Delay(1)

        cls._delta_time = (cls.now() - cls._frame_start) / 1000

    @classmethod
    def schedule(cls, task: DelayedTask | FramesTask | ScheduledTask):
        """
        Schedules a task for delayed execution based on what type of task it is.

        Args:
            task (DelayedTask | FramesTask | ScheduledTask): The task to queue.
        """
        if isinstance(task, DelayedTask):
            task.delay += cls.now()
            heapq.heappush(cls._task_queue, task)
        elif isinstance(task, FramesTask):
            task.delay += cls.frames
            heapq.heappush(cls._frame_queue, task)
        elif isinstance(task, ScheduledTask):
            task.delay += cls.now()
            heapq.heappush(cls._schedule_queue, task)
        else:
            raise TypeError("Task argument must of of type DelayedTask, FramesTask or ScheduledTask.")

    @classmethod
    def delayed_call(cls, delay: int, func: Callable):
        """
        Calls the function func at a later time.

        Args:
            delay: The time from now (in milliseconds) to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._task_queue, DelayedTask(delay + cls.now(), func))

    @classmethod
    def delayed_frames(cls, delay: int, func: Callable):
        """
        Calls the function func at a later frame.

        Args:
            delay: The number of frames to wait.
            func: The function to call
        """

        heapq.heappush(cls._frame_queue, FramesTask(cls.frames + delay, func))

    @classmethod
    def scheduled_call(cls, interval: int, func: Callable):
        """
        Calls the function func at a scheduled interval.

        Args:
            interval: The interval (in milliseconds) to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._schedule_queue, ScheduledTask(interval, func, interval + cls.now()))

    @classmethod
    def next_frame(cls, func: Callable):
        """
        Calls the function func on the next frame.

        Args:
            func: The function to call.
        """
        cls._next_queue.append(func)

    @classmethod
    def milli_to_sec(cls, milli: float | int) -> float | int:
        """
        Converts milliseconds to seconds.

        Returns:
            The converted number in seconds.
        """
        return milli / 1000

    @classmethod
    def sec_to_milli(cls, sec: float | int) -> int:
        """
        Converts seconds to milliseconds.

        Returns:
            The converted number in milliseconds.
        """
        return int(sec * 1000)

    @classmethod
    def process_calls(cls):
        """Processes the delayed function call as needed"""
        cls.frames += 1
        cls.fps = 1 / cls.delta_time

        cls._past_fps[cls._fps_index] = int(cls.fps)
        cls._fps_index = (cls._fps_index + 1) % cls._fps_history

        if cls._next_queue:
            for func in cls._next_queue:
                func()
            cls._next_queue.clear()

        while cls._frame_queue:
            if cls._frame_queue[0].delay <= cls.frames:
                timer_task = heapq.heappop(cls._frame_queue)
                if not timer_task.is_stopped:
                    timer_task.task()
            else:
                break

        while cls._task_queue:
            if cls._task_queue[0].delay <= cls.now():
                timer_task = heapq.heappop(cls._task_queue)
                if not timer_task.is_stopped:
                    timer_task.task()
            else:
                break

        while cls._schedule_queue:
            if cls._schedule_queue[0].delay <= cls.now():
                scheduled_task = heapq.heappop(cls._schedule_queue)

                if not scheduled_task.is_stopped:
                    scheduled_task.task()

                if not scheduled_task.is_stopped:
                    scheduled_task.delay += scheduled_task.interval
                    heapq.heappush(cls._schedule_queue, scheduled_task)
            else:
                break
