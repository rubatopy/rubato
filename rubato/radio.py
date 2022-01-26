"""
The Radio module is a system used to communicate to all parts of the game.
This is similar to event systems in other game engines.

To use this, first you need to listen for a specific key using the
:meth:`Radio.listen` function. Then from anywhere else in the code, you can
broadcast that event key using the :meth:`Radio.broadcast` function.
"""

import typing


class Radio:
    """
    Broadcast system manages all events and inter-class communication.
    Has a buffer system and a handler system.

    Attributes:
        events (List[str]): A list with all the event keys in the queue.
        listeners (dict[str, typing.Callable]): A dictionary with all of the
            active listeners.
    """

    def __init__(self):
        self.events: typing.List[str] = []
        self.listeners: dict[str, typing.Callable] = {}

    def broadcast(self, event: str):
        """
        Broadcast an event to be caught by listeners.

        Args:
            event (str): The event key to broadcast.
        """
        self.events.append(event)
        for func in self.listeners.get(event, []):
            func()

    def listen(self, event: str, func: typing.Callable):
        """
        Creates an event listener.

        Args:
            event (str): The event key to listen for.
            func (typing.Callable): The function to run once the event is
                broadcast.

        Note:
            You **CANNOT** currently delete an event listener once it's created.
        """
        if event in self.listeners:
            self.listeners.get(event).append(func)
        else:
            self.listeners[event] = [func]
