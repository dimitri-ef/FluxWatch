#!/bin/python3

from PyQt6.QtWidgets import QApplication

from queue import Queue
from producers.mp4_producer import Mp4Producer
from producers.camera_producer import CameraProducer
from consumers.motion_detection_consumer import MotionDetectionConsumer
from consumers.background_remover_consumer import BackgroundRemoverConsumer
from observers.visual_observer import VisualObserver
from ui.video_window import VideoWindow

app = QApplication([])

queue = Queue()
producer = CameraProducer(queue)
consumer = BackgroundRemoverConsumer(queue, "/home/descaffrefaure/projets/FluxWatch/models/selfie_segmenter.tflite", "/home/descaffrefaure/projets/FluxWatch/data/images.jpeg")
visual_observer = VisualObserver()
video_window = VideoWindow(visual_observer)

consumer.attach(visual_observer)

producer.start()
consumer.start()

video_window.show()

app.exec()

producer.stop()
consumer.stop()