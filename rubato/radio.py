"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using the :meth:`Radio.broadcast` function.
"""

from typing import Callable, List
import rubato.game as Game


class Radio:
    """
    Broadcast system manages all events and inter-class communication.
    Has a buffer system and a handler system.

    Attributes:
        events (List[str]): A list with all the event keys in the queue.
        listeners (dict[str, Callable]): A dictionary with all of the
            active listeners.
    """

    def __init__(self):
        """Initializes the Radio class"""
        self.events: List[tuple] = []
        self.listeners: dict[str, List] = {}

    def listen(self, event: str, func: Callable):
        """
        Creates an event listener and registers it.

        Args:
            event: The event key to listen for.
            func: The function to run once the event is
                broadcast. It may take in a params dictionary argument.
        """
        listener = Listener(event, func)
        listener.registered = True

        if event in self.listeners:
            self.listeners[event].append(listener)
        else:
            self.listeners[event] = [listener]

        return listener

    def register(self, listener: "Listener"):
        """
        Registers an event listener.

        Args:
            listener: The listener object to be registered
        """
        listener.registered = True
        if listener.registered:
            raise ValueError("Listener already registered")

        if listener.event in self.listeners:
            if listener in self.listeners[listener.event]:
                raise ValueError("Listener already registered")

            self.listeners[listener.event].append(listener)
        else:
            self.listeners[listener.event] = [listener]

        return listener

    def broadcast(self, event: str, params: dict):
        """
        Broadcast an event to be caught by listeners.

        Args:
            event: The event key to broadcast.
            params: A parameters dictionary
        """
        self.events.append((event, params))
        for listener in self.listeners.get(event, []):
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

    def ping(self, params: dict):
        """
        Calls the callback of this listener.

        Args:
            params: A parameters dictionary
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
            Game.radio.listeners[self.event].remove(self)
            self.registered = False
        except ValueError as e:
            raise ValueError("Listener not registered in the radio") from e
