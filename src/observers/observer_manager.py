
class ObserverManager:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify_all(self, frame):
        for obs in self.observers:
            obs.notify(frame)
