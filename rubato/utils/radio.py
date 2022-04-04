"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using :meth:`Radio.broadcast`.

Global events automatically broadcasted:
EXIT - The user has requested for the application to close
RESIZE - The window was resized
KEYDOWN - A key was pressed
KEYHOLD - A key that was pressed is repeating
KEYUP - A key was unpressed
ZOOM - The camera zoom changed
"""

from typing import Callable, List


class Radio:
    """
    Broadcast system manages all events and inter-class communication.
    Handles event callbacks during the beginning of each
    :func:`Game.update() <rubato.game.update>` call.

    Attributes:
        listeners (dict[str, Callable]): A dictionary with all of the
            active listeners.
    """

    listeners: dict[str, List] = {}

    @classmethod
    def listen(cls, event: str, func: Callable):
        """
        Creates an event listener and registers it.

        Args:
            event: The event key to listen for.
            func: The function to run once the event is
                broadcast. It may take in a params dictionary argument.
        """
        listener = Listener(event, func)
        listener.registered = True

        if event in cls.listeners:
            cls.listeners[event].append(listener)
        else:
            cls.listeners[event] = [listener]

        return listener

    @classmethod
    def register(cls, listener: "Listener"):
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


class Listener:
    """
    The actual listener object itself.

    Attributes:
        event (str): The event descriptor
        callback (Callable): The function called when the event occurs
        registered (bool): Describes whether the listener is registered
    """

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
