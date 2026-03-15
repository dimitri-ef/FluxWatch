from abc import ABC, abstractmethod

import threading
import queue

class BaseProducer(ABC):
    def __init__(self, out_queue: queue.Queue):
        super().__init__()
        self.thread = None
        self.running = False
        self.queue = out_queue

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
        while self.running :
            self.produce()
    
    def produce(self):
        frame = self.read_source()

        if frame is None:
            self.running = False
            return
            
        self.queue.put(frame)


    @abstractmethod
    def read_source(self):
        pass