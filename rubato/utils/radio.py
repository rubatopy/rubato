"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using :meth:`Radio.broadcast`.

:ref:`Go here <api:events>` to see all the events that can be broadcast.
"""
from __future__ import annotations
import ctypes
from typing import Any, Callable
from contextlib import suppress
import sdl2
import cython

from . import Input, Display, InitError, Events, EventResponse, ResizeResponse, KeyResponse, MouseButtonResponse, \
    MouseWheelResponse, MouseMotionResponse, JoyAxisMotionResponse, JoyHatMotionResponse, JoyButtonResponse, Time


# THIS IS A STATIC CLASS
class Radio:
    """
    Broadcast system manages all events and inter-class communication.
    Handles event callbacks during the beginning of each
    :func:`Game.update() <rubato.game.update>` call.
    """
    listeners: dict[str, list[Listener]] = {}
    """A dictionary with all of the active listeners."""

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def _handle(cls) -> bool:
        """
        Handle the current SDL event queue.

        Returns:
            bool: Whether an SDL Quit event was fired.
        """
        event = sdl2.SDL_Event()

        while sdl2.SDL_PeepEvents(
            ctypes.byref(event), 1, sdl2.SDL_GETEVENT, sdl2.SDL_FIRSTEVENT, sdl2.SDL_LASTEVENT
        ) > 0:
            if event.type == sdl2.SDL_QUIT:
                return True
            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    cls.broadcast(
                        Events.RESIZE,
                        ResizeResponse(
                            event.window.timestamp,
                            event.window.data1,
                            event.window.data2,
                            Display.window_size.x,
                            Display.window_size.y,
                        )
                    )
                    Display.window_size = (
                        event.window.data1,
                        event.window.data2,
                    )
            elif event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                key_info, unicode = event.key.keysym, ""
                with suppress(ValueError):
                    unicode = chr(key_info.sym)

                if event.type == sdl2.SDL_KEYUP:
                    event_name = Events.KEYUP
                else:
                    event_name = (Events.KEYDOWN, Events.KEYHOLD)[event.key.repeat]

                cls.broadcast(
                    event_name,
                    KeyResponse(
                        event.key.timestamp,
                        Input.get_name(key_info.sym),
                        unicode,
                        int(key_info.sym),
                        key_info.mod,
                    )
                )
            elif event.type in (sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP):
                if event.type == sdl2.SDL_MOUSEBUTTONUP:
                    event_name = Events.MOUSEUP
                else:
                    event_name = Events.MOUSEDOWN

                cls.broadcast(
                    event_name,
                    MouseButtonResponse(
                        event.button.timestamp,
                        event.button.button,
                        event.button.x,
                        event.button.y,
                        event.button.clicks,
                        event.button.which,
                    )
                )
            elif event.type == sdl2.SDL_MOUSEWHEEL:
                cls.broadcast(
                    Events.MOUSEWHEEL,
                    MouseWheelResponse(
                        event.wheel.timestamp,
                        event.wheel.preciseX,
                        event.wheel.preciseY,
                        event.wheel.which,
                    )
                )
            elif event.type == sdl2.SDL_MOUSEMOTION:
                cls.broadcast(
                    Events.MOUSEMOTION,
                    MouseMotionResponse(
                        event.motion.timestamp,
                        event.motion.x,
                        event.motion.y,
                        event.motion.xrel,
                        event.motion.yrel,
                        event.motion.which,
                    )
                )
            elif event.type == sdl2.SDL_JOYAXISMOTION:
                mag: float = event.jaxis.value / Input._joystick_max
                cls.broadcast(
                    Events.JOYAXISMOTION,
                    JoyAxisMotionResponse(
                        event.jaxis.timestamp,
                        event.jaxis.which,
                        event.jaxis.axis,
                        mag,
                        Input.axis_centered(mag),
                    )
                )
            elif event.type in (sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP):
                if event.type == sdl2.SDL_JOYBUTTONUP:
                    event_name = Events.JOYBUTTONUP
                else:
                    event_name = Events.JOYBUTTONDOWN

                cls.broadcast(
                    event_name, JoyButtonResponse(
                        event.jbutton.timestamp,
                        event.jbutton.which,
                        event.jbutton.button,
                    )
                )
            elif event.type == sdl2.SDL_JOYHATMOTION:
                cls.broadcast(
                    Events.JOYHATMOTION,
                    JoyHatMotionResponse(
                        event.jhat.timestamp,
                        event.jhat.which,
                        event.jhat.hat,
                        event.jhat.value,
                        Input.translate_hat(event.jhat.value),
                    )
                )

        return False

    @classmethod
    def listen(cls, event: str | Events, func: Callable[[], None] | Callable[[EventResponse], None]):
        """
        Creates an event listener and registers it.

        Args:
            event: The event key to listen for.
            func: The function to run once the event is broadcast. It may take in an EventResponse as an argument.
        """
        return cls.register(Listener(str(event), func))

    @classmethod
    def register(cls, listener: Listener):
        """
        Registers an event listener.

        Args:
            listener: The listener object to be registered
        """
        if listener.registered:
            raise ValueError("Listener already registered")
        listener.registered = True

        if listener.event in cls.listeners:
            if listener in cls.listeners[listener.event]:
                raise ValueError("Listener already registered")

            cls.listeners[listener.event].append(listener)
        else:
            cls.listeners[listener.event] = [listener]

        return listener

    @classmethod
    def broadcast(cls, event: str | Events, params: EventResponse | None = None):
        """
        Broadcast an event to be caught by listeners.

        Args:
            event: The event key to broadcast.
            params: The event parameters (usually a dictionary)
        """
        for listener in cls.listeners.get(str(event), []):
            listener.ping(params or EventResponse(Time.now()))


@cython.cclass
class Listener:
    """
    The actual listener object itself. A backend class for the Radio.

    Args:
        event: The event key to listen for.
        callback: The function to run once the event is broadcast.
    """
    event: str = cython.declare(str, visibility="public")  # type: ignore
    """The event descriptor"""
    callback: Callable[[], None] | Callable[[EventResponse], None] = cython.declare(
        object, visibility="public"
    )  # type: ignore
    """The function called when the event occurs"""
    registered: cython.bint = cython.declare(cython.bint, visibility="public")  # type: ignore
    """Describes whether the listener is registered"""

    def __init__(self, event: str, callback: Callable):
        self.event = event
        self.callback = callback
        self.registered = False

    def ping(self, params: EventResponse):
        """
        Calls the callback of this listener.

        Args:
            params: The event parameters (usually a dictionary)
        """
        try:
            self.callback(params)  # type: ignore
        except TypeError:
            self.callback()  # type: ignore

    def remove(self):
        """
        Removes itself from the radio register.

        Raises:
            ValueError: Raises error when listener is not registered
        """
        try:
            if self.event in Radio.listeners:
                Radio.listeners[self.event].remove(self)
                if not Radio.listeners[self.event]:
                    del Radio.listeners[self.event]
                self.registered = False
            else:
                raise ValueError("Listener not registered")
        except ValueError as e:
            raise ValueError("Listener not registered") from e
