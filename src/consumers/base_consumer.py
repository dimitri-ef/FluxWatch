from abc import ABC, abstractmethod

import queue
import threading

from observers.observer_manager import ObserverManager

class BaseConsumer(ABC, ObserverManager):
    def __init__(self, in_queue: queue.Queue):
        ObserverManager.__init__(self)
        ABC.__init__(self)

        self.queue = in_queue
        self.thread = None
        self.running = False
        
    def start(self) -> None:
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self) -> None:
        if not self.running:
            return
        
        self.running = False
        
        if self.thread is not None:
            self.thread.join()
    
    def run(self) -> None:
        while self.running:
            try:
                frame = self.queue.get(timeout=0.5)
            except queue.Empty:
                continue

            processed_frame = self.process(frame)

            if processed_frame is None:
                continue

            self.notify_all(processed_frame)

    @abstractmethod
    def process(self, frame):
        pass