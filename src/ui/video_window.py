from PyQt6.QtWidgets import QLabel, QMainWindow, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import cv2

from observers.visual_observer import VisualObserver

class VideoWindow(QMainWindow):
    def __init__(self, observer: VisualObserver):
        super().__init__()
        self.setWindowTitle("Motion Detection Viewer")
        self.label = QLabel(self)
        self.label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setCentralWidget(self.label)

        observer.new_frame_signal.connect(self.on_new_frame)

    def on_new_frame(self, frame):
        if frame.shape[2] == 4:
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            rgba = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            qt_image = QImage(rgba.data, w, h, bytes_per_line, QImage.Format.Format_RGBA8888)
        else:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,  # remplit tout sans bandes noires
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)