from PyQt6.QtCore import QObject, pyqtSignal

class VisualObserver(QObject):
    new_frame_signal = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)

    def notify(self, frame):
        self.new_frame_signal.emit(frame) 