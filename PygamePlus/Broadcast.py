from pygame.key import key_code


class Broadcast:
    def __init__(self):
        self.events = []
        self.subscriptions = {}
        self.keys = []

    def subscribeToEvent(self, event, func):
        if event in self.subscriptions.keys():
            self.subscriptions.get(event).append(func)
        else:
            self.subscriptions[event] = [func]

    def handleEvents(self):
        for event in self.subscriptions.keys():
            if event in self.events:
                for func in self.subscriptions.get(event, []):
                    func()
            elif "_down" in event:
                if self.keys[key_code(event.split("_")[0])]:
                    for func in self.subscriptions.get(event, []):
                        func()

    def addEvent(self, event):
        self.events.append(event)
        for func in self.subscriptions.get(event, []):
            func()

    # def isPressed(self, key):