import cv2

from consumers.base_consumer import BaseConsumer
import queue

class MotionDetectionConsumer(BaseConsumer):
    def __init__(self, in_queue: queue.Queue):
        super().__init__(in_queue)

        self.previous_frame = None

        
    def process(self, frame):
        if self.previous_frame is None:
            self.previous_frame = frame.copy()
            return frame

        gray_curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_prev = cv2.cvtColor(self.previous_frame, cv2.COLOR_BGR2GRAY)

        gray_curr = cv2.GaussianBlur(gray_curr, (21, 21), 0)
        gray_prev = cv2.GaussianBlur(gray_prev, (21, 21), 0)

        frame_delta = cv2.absdiff(gray_prev, gray_curr)

        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh.copy(), None, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame
