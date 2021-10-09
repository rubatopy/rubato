from pygame.key import key_code


class Broadcast:
    """
    Broadcast system manages all events and inter-class communication. Has a buffer system and a handler system.
    """

    def __init__(self):
        self.events = []
        self.listeners = {}
        self.keys = []

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

    def handle_events(self):
        """
        Function that checks if events with subscriptions have occurred and runs their corresponding functions as
        needed.
        """
        for event in self.listeners.keys():
            if event in self.events:
                for func in self.listeners.get(event, []):
                    func()
            elif "_down" in event:
                if self.isPressed(event.split("_")[0]):
                    for func in self.listeners.get(event, []):
                        func()

    def add_event(self, event: str):
        """
        Add an event to the event buffer and handle that events subscriptions.

        :param event: The event code to add.
        """
        self.events.append(event)
        for func in self.listeners.get(event, []):
            func()

    def is_pressed(self, key: str):
        """
        Check if a key is pressed.

        :param key: A key name.
        :return: boolean.
        """
        return self.keys[key_code(key)]
