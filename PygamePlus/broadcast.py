class Broadcast:
    """
    Broadcast system manages all events and inter-class communication. Has a buffer system and a handler system.
    """

    def __init__(self):
        self.events = []
        self.listeners = {}

    def broadcast_event(self, event: str):
        """
        Broadcast a custom event.

        :param event: The name of your custom event.
        """
        self.events.append(event)
        for func in self.listeners.get(event, []):
            func()

    def add_listener(self, event: str, func):
        """
        Allows you to call a function everytime a specific event occurs.

        :param event: The event code to subscribe to
        :param func: The function that needs to run once the event occurs
        """
        if event in self.listeners.keys():
            self.listeners.get(event).append(func)
        else:
            self.listeners[event] = [func]