"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using :meth:`Radio.broadcast`.

:doc:`Go here <events>` to see all the events that can be broadcast.
"""
from __future__ import annotations
import ctypes
from typing import Callable
from contextlib import suppress
import sdl2
import cython

from . import Input, Display, InitError


@cython.cclass
class Events:
    """
    Describes all rubato-fired events that can be listened for.
    """

    KEYUP = "KEYUP"
    """Fired when a key is released"""
    KEYDOWN = "KEYDOWN"
    """Fired when a key is pressed"""
    KEYHOLD = "KEYHOLD"
    """Fired when a key is held down (After the initial keydown)"""
    MOUSEUP = "MOUSEUP"
    """Fired when a mouse button is released"""
    MOUSEDOWN = "MOUSEDOWN"
    """Fired when a mouse button is pressed"""
    MOUSEWHEEL = "MOUSEWHEEL"
    """Fired when the mouse wheel is scrolled"""
    SCROLL = MOUSEWHEEL
    """Same as MOUSEWHEEL"""
    JOYAXISMOTION = "JOYAXISMOTION"
    """Fired when a controller joystick axis is moved"""
    JOYHATMOTION = "JOYHATMOTION"
    """Fired when a controller hat button is changed"""
    JOYBUTTONDOWN = "JOYBUTTONDOWN"
    """Fired when a controller button is pressed"""
    JOYBUTTONUP = "JOYBUTTONUP"
    """Fired when a controller button is released"""
    ZOOM = "ZOOM"
    """Fired when the camera is zoomed"""
    EXIT = "EXIT"
    """Fired when the game is exiting"""
    RESIZE = "RESIZE"
    """Fired when the window is resized"""


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
    def handle(cls) -> bool:
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
                        Events.RESIZE, {
                            "width": event.window.data1,
                            "height": event.window.data2,
                            "old_width": Display.window_size.x,
                            "old_height": Display.window_size.y
                        }
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
                    {
                        "key": Input.get_name(key_info.sym),
                        "unicode": unicode,
                        "code": int(key_info.sym),
                        "mods": key_info.mod,
                    },
                )
            elif event.type in (sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP):
                if event.type == sdl2.SDL_MOUSEBUTTONUP:
                    event_name = Events.MOUSEUP
                else:
                    event_name = Events.MOUSEDOWN

                cls.broadcast(
                    event_name,
                    {
                        "button": event.button.button,
                        "x": event.button.x,
                        "y": event.button.y,
                        "clicks": event.button.clicks,
                        "which": event.button.which,
                        "windowID": event.button.windowID,
                        "timestamp": event.button.timestamp,
                    },
                )
            elif event.type == sdl2.SDL_MOUSEWHEEL:
                cls.broadcast(
                    Events.MOUSEWHEEL,
                    {
                        "x": event.wheel.x,
                        "y": event.wheel.y,
                        "precise x": event.wheel.preciseX,
                        "precise y": event.wheel.preciseY,
                        "which": event.wheel.which,
                        "timestamp": event.wheel.timestamp,
                        "windowID": event.wheel.windowID,
                    },
                )
            elif event.type == sdl2.SDL_JOYAXISMOTION:
                mag: float = event.jaxis.value / Input._joystick_max
                cls.broadcast(
                    Events.JOYAXISMOTION,
                    {
                        "controller": event.jaxis.which,
                        "axis": event.jaxis.axis,
                        "value": mag,
                        "centered": Input.axis_centered(mag),
                    },
                )
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                cls.broadcast(
                    Events.JOYBUTTONDOWN,
                    {
                        "controller": event.jbutton.which,
                        "button": event.jbutton.button
                    },
                )
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                cls.broadcast(
                    Events.JOYBUTTONUP,
                    {
                        "controller": event.jbutton.which,
                        "button": event.jbutton.button
                    },
                )
            elif event.type == sdl2.SDL_JOYHATMOTION:
                cls.broadcast(
                    Events.JOYHATMOTION,
                    {
                        "controller": event.jhat.which,
                        "hat": event.jhat.hat,
                        "value": event.jhat.value,
                        "name": Input.translate_hat(event.jhat.value),
                    },
                )

        return False

    @classmethod
    def listen(cls, event: str, func: Callable):
        """
        Creates an event listener and registers it.

        Args:
            event: The event key to listen for.
            func: The function to run once the event is
                broadcast. It may take in a params dictionary argument.
        """
        return cls.register(Listener(event, func))

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
    def broadcast(cls, event: str, params={}):
        """
        Broadcast an event to be caught by listeners.

        Args:
            event: The event key to broadcast.
            params: The event parameters (usually a dictionary)
        """
        for listener in cls.listeners.get(event, []):
            listener.ping(params)


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
    callback: Callable = cython.declare(object, visibility="public")  # type: ignore
    """The function called when the event occurs"""
    registered: cython.bint = cython.declare(cython.bint, visibility="public")  # type: ignore
    """Describes whether the listener is registered"""

    def __init__(self, event: str, callback: Callable):
        self.event = event
        self.callback = callback
        self.registered = False

    def ping(self, params):
        """
        Calls the callback of this listener.

        Args:
            params: The event parameters (usually a dictionary)
        """
        try:
            self.callback(params)
        except TypeError:
            self.callback()

    def remove(self):
        """
        Removes itself from the radio register.

        Raises:
            ValueError: Raises error when listener is not registered
        """
        try:
            Radio.listeners[self.event].remove(self)
            self.registered = False
        except ValueError as e:
            raise ValueError("Listener not registered in the radio") from e
