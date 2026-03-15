import cv2
import queue

from producers.base_producer import BaseProducer
from decorators.fps import limit_fps

class CameraProducer(BaseProducer):
    def __init__(self, outqueue: queue.Queue, cam_index: int = 0):
        super().__init__(outqueue)
        self.vidcap = cv2.VideoCapture(cam_index)
        if not self.vidcap.isOpened():
            print(f"Impossible d'ouvrir la caméra {cam_index}")
        self.vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS) or 30

    @limit_fps
    def produce(self):
        super().produce()

    def read_source(self):
        success,frame = self.vidcap.read()
        if not success:
            return None
        return frame