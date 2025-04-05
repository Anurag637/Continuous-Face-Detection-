# main.py
import sys
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from detector import FaceDetector
from gui import DeviceSelector
from utils.device_monitor import suggest_device

MODEL_PATH = "model/face-detection-0200.xml"

class VideoThread(QThread):
    change_pixmap = pyqtSignal(object)

    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            frame = self.detector.detect(frame)
            cv2.imshow("Face Detection", frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

    def switch_device(self, device):
        self.detector.change_device(device)

def main():
    app = QApplication(sys.argv)
    detector = FaceDetector(MODEL_PATH, device="AUTO")
    thread = VideoThread(detector)
    thread.start()

    gui = DeviceSelector(thread.switch_device)
    gui.show()

    sys.exit(app.exec_())
    thread.stop()

if __name__ == "__main__":
    main()
