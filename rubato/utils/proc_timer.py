# pylint: disable=all
"""
An internal file for the rubato project.
"""
import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, Optional


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class ProcTimer(ContextDecorator):
    """Time your code using a class, context manager, or decorator"""

    timers: ClassVar[Dict[str, float]] = {}
    name: Optional[str] = None
    text: str = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def start(self):
        """Start a new timer"""

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.name:
            if self.name not in ProcTimer.timers:
                ProcTimer.timers[self.name] = []
            ProcTimer.timers[self.name].append(elapsed_time)

        return elapsed_time

    @classmethod
    def end(cls):
        for key, value in cls.timers.items():
            print(f"{key}: {(sum(value) * 1000) / len(value)}")

    def __enter__(self) -> "ProcTimer":
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any):
        """Stop the context manager timer"""
        self.stop()
