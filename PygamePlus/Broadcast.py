from pygame.key import key_code


class Broadcast:
    """
    Broadcast system manages all events and inter-class communication. Has a buffer system and a handler system.
    """

    def __init__(self):
        self.events = []
        self.subscriptions = {}
        self.keys = []

    def subscribeToEvent(self, event, func):
        """
        Allows you to call a function everytime a specific event occurs.

        :param event: The event code to subscribe to
        :param func: The function that needs to run once the event occurs
        """
        if event in self.subscriptions.keys():
            self.subscriptions.get(event).append(func)
        else:
            self.subscriptions[event] = [func]

    def handleEvents(self):
        """
        Function that checks if events with subscriptions have occurred and runs their corresponding functions as
        needed.
        """
        for event in self.subscriptions.keys():
            if event in self.events:
                for func in self.subscriptions.get(event, []):
                    func()
            elif "_down" in event:
                if self.isPressed(event.split("_")[0]):
                    for func in self.subscriptions.get(event, []):
                        func()

    def addEvent(self, event):
        """
        Add an event to the event buffer and handle that events subscriptions

        :param event: The event code to add
        """
        self.events.append(event)
        for func in self.subscriptions.get(event, []):
            func()

    def isPressed(self, key):
        """
        Check if a key is pressed

        :param key: A key name
        :return: boolean
        """
        return self.keys[key_code(key)]