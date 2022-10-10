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
    """
    A task that is run after a specified number of milliseconds.

    Args:
        delay: The number of milliseconds to wait before invoking the task.
        task: The task to invoke.
        is_stopped: Whether the task is stopped.
    """
    delay: int
    """The delay until the task is run, in milliseconds."""
    task: Callable[[], None] = field(compare=False)
    """The task to run."""
    is_stopped: bool = field(default=False, compare=False)
    """Whether the DelayedTask is stopped."""
    next_run: int = field(default=0, compare=False)
    """The time at which the task will be run next, in milliseconds."""

    def stop(self):
        """Stop the DelayedTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class FramesTask:
    """
    A task that is run after a specified number of frames.

    Args:
        delay: The number of frames to wait before invoking the task.
        task: The task to invoke.
        is_stopped: Whether the task is stopped.
    """
    delay: int
    """The delay until the task is run, in frames."""
    task: Callable[[], None] = field(compare=False)
    """The task to run."""
    is_stopped: bool = field(default=False, compare=False)
    """Whether the FramesTask is stopped."""
    next_run: int = field(default=0, compare=False)
    """The frame at which the task will be run next."""

    def stop(self):
        """Stop the FramesTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class RecurrentTask:
    """
    A task that is run every specified number of milliseconds.

    Args:
        interval: The number of milliseconds between task invocations.
        task: The task to invoke.
        delay: The number of milliseconds to wait before starting the invocations.
        is_stopped: Whether the task is stopped.
    """
    interval: int = field(compare=False)
    """The interval between task invocations, in milliseconds."""
    task: Callable[[], None] | Callable[["RecurrentTask"], None] = field(compare=False)
    """The task to run."""
    delay: int = field(default=0)
    """The initial delay until the task is run, in milliseconds."""
    is_stopped: bool = field(default=False, compare=False)
    """Whether the RecurrentTask is stopped."""
    next_run: int = field(default=0, compare=False)
    """The time at which the task will be run next, in milliseconds."""

    def stop(self):
        """Stop the RecurrentTask from invoking."""
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
    _recurrent_queue: list[RecurrentTask] = []

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
    def next_frame(cls, func: Callable[[], None]):
        """
        Calls the function func to be called on the next frame.

        Args:
            func: The function to call.
        """
        cls._next_queue.append(func)

    @classmethod
    def delayed_frames(cls, delay: int, func: Callable[[], None]):
        """
        Calls the function func to be called at a later frame.

        Args:
            delay: The number of frames to wait.
            func: The function to call
        """

        cls.schedule(FramesTask(delay, func))

    @classmethod
    def delayed_call(cls, delay: int, func: Callable[[], None]):
        """
        Calls the function func to be called at a later time.

        Args:
            delay: The time from now (in milliseconds) to run the function at.
            func: The function to call.
        """

        cls.schedule(DelayedTask(delay, func))

    @classmethod
    def recurred_call(cls, interval: int, func: Callable[[], None] | Callable[[RecurrentTask], None], delay: int = 0):
        """
        Schedules the function func to be repeatedly called every interval.

        Args:
            interval: The interval (in milliseconds) to run the function at.
            func: The function to call. Can take a RecurrentTask as an argument. This is useful for stopping the task.
            delay: The delay (in milliseconds) to wait before starting the task.
        """

        cls.schedule(RecurrentTask(interval, func, delay))

    @classmethod
    def schedule(cls, task: DelayedTask | FramesTask | RecurrentTask):
        """
        Schedules a task for execution based on what type of task it is.

        Args:
            task: The task to queue.
        """
        if isinstance(task, DelayedTask):
            task.next_run = cls.now() + task.delay if task.next_run <= cls.now() else task.next_run
            heapq.heappush(cls._task_queue, task)
        elif isinstance(task, FramesTask):
            task.next_run = cls.frames + task.delay if task.next_run <= cls.frames else task.next_run
            heapq.heappush(cls._frame_queue, task)
        elif isinstance(task, RecurrentTask):
            task.next_run = cls.now() + task.delay + task.interval if task.next_run <= cls.now() else task.next_run
            heapq.heappush(cls._recurrent_queue, task)
        else:
            raise TypeError("Task argument must of of type DelayedTask, FramesTask or RecurrentTask.")

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
            if cls._frame_queue[0].next_run <= cls.frames:
                frame_task: FramesTask = heapq.heappop(cls._frame_queue)
                if not frame_task.is_stopped:
                    frame_task.task()
            else:
                break

        while cls._task_queue:
            if cls._task_queue[0].next_run <= cls.now():
                task: DelayedTask = heapq.heappop(cls._task_queue)
                if not task.is_stopped:
                    task.task()
            else:
                break

        while cls._recurrent_queue:
            if cls._recurrent_queue[0].next_run <= cls.now():
                recurrent_task: RecurrentTask = heapq.heappop(cls._recurrent_queue)

                if not recurrent_task.is_stopped:
                    try:
                        recurrent_task.task(recurrent_task)  # type: ignore
                    except TypeError:
                        recurrent_task.task()  # type: ignore

                    recurrent_task.next_run += recurrent_task.interval
                    heapq.heappush(cls._recurrent_queue, recurrent_task)
            else:
                break
