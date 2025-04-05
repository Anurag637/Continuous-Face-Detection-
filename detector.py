# detector.py
import cv2
import numpy as np
from openvino.runtime import Core

class FaceDetector:
    def __init__(self, model_path, device='AUTO'):
        self.core = Core()
        self.model_path = model_path
        self.load_model(device)

    def load_model(self, device):
        self.model = self.core.read_model(model=self.model_path)
        self.compiled_model = self.core.compile_model(model=self.model, device_name=device)
        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)
        self.device = device

    def change_device(self, device):
        if device != self.device:
            self.load_model(device)

    def detect(self, frame):
        h, w = frame.shape[:2]
        resized = cv2.resize(frame, (384, 384))
        blob = resized.transpose((2, 0, 1))[np.newaxis, :]
        result = self.compiled_model([blob])[self.output_layer]

        for box in result[0][0]:
            if box[2] > 0.6:
                xmin = int(box[3] * w)
                ymin = int(box[4] * h)
                xmax = int(box[5] * w)
                ymax = int(box[6] * h)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        return frame
