import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options

from consumers.base_consumer import BaseConsumer
import queue

class BackgroundRemoverConsumer(BaseConsumer):
    def __init__(self, in_queue: queue.Queue, model_path: str, bg_image_path: str):
        super().__init__(in_queue)
        self.bg_image = cv2.imread(bg_image_path)
        options = vision.ImageSegmenterOptions(
            base_options=base_options.BaseOptions(
                model_asset_path=model_path
            ),
            output_category_mask=True,
        )
        self.segmenter = vision.ImageSegmenter.create_from_options(options)

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        result = self.segmenter.segment(mp_image)
        confidence = result.confidence_masks[0].numpy_view()

        alpha = (confidence * 255).astype(np.uint8)
        alpha = cv2.GaussianBlur(alpha, (7, 7), 0)
        _, alpha = cv2.threshold(alpha, 128, 255, cv2.THRESH_BINARY)

        bg = cv2.resize(self.bg_image, (frame.shape[1], frame.shape[0]))

        mask = alpha[:, :, None] / 255.0
        output = (frame * mask + bg * (1 - mask)).astype(np.uint8)

        return output
