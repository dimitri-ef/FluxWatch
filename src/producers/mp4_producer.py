import cv2
import queue

from producers.base_producer import BaseProducer
from decorators.fps import limit_fps

class Mp4Producer(BaseProducer):
    def __init__(self, outqueue: queue.Queue, filepath: str):
        super().__init__(outqueue)
        self.vidcap = cv2.VideoCapture(filepath)
        if not self.vidcap.isOpened():
            print("Impossible d'ouvrir la vidéo :", filepath)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS) or 30
    
    @limit_fps
    def produce(self):
        super().produce()
    
    def read_source(self):
        success,frame = self.vidcap.read()
        if not success:
            return None
        return frame
