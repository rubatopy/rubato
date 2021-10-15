from pgp import check_types


class Radio:
    """
    Broadcast system manages all events and inter-class communication. Has a buffer system and a handler system.
    """

    def __init__(self):
        self.events = []
        self.listeners = {}

    def broadcast(self, event: str):
        """
        Broadcast a custom event.

        :param event: The name of your custom event.
        """
        check_types(Radio.broadcast, locals())
        self.events.append(event)
        for func in self.listeners.get(event, []):
            func()

    def listen(self, event: str, func: type(lambda:None)):
        """
        Allows you to call a function everytime a specific event occurs.

        :param event: The event code to subscribe to
        :param func: The function that needs to run once the event occurs
        """
        check_types(Radio.listen, locals())
        if event in self.listeners.keys():
            self.listeners.get(event).append(func)
        else:
            self.listeners[event] = [func]
