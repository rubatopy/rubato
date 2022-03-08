"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using the :meth:`Radio.broadcast` function.
"""

from typing import Callable, List


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
        "Initializes the Radio class"
        self.events: List[str] = []
        self.listeners: dict[str, Callable] = {}

    def listen(self, event: str, func: Callable):
        """
        Creates an event listener.

        Args:
            event: The event key to listen for.
            func: The function to run once the event is
                broadcast. It may take in a params dictionary argument.

        Warning:
            You **CANNOT** currently delete an event listener once it's created.
        """
        if event in self.listeners:
            self.listeners.get(event).append(func)
        else:
            self.listeners[event] = [func]

    def broadcast(self, event: str, params: dict):
        """
        Broadcast an event to be caught by listeners.

        Args:
            event: The event key to broadcast.
            params: A parameters dictionary
        """
        self.events.append(event)
        for func in self.listeners.get(event, []):
            try:
                func(params)
            except TypeError:
                func()
