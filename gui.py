# gui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox

class DeviceSelector(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setWindowTitle("Device Switcher")

        layout = QVBoxLayout()
        self.label = QLabel("Select Inference Device:")
        self.combo = QComboBox()
        self.combo.addItems(["AUTO", "CPU", "GPU"])
        self.combo.currentTextChanged.connect(self.on_device_change)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        self.setLayout(layout)

    def on_device_change(self, device):
        self.callback(device)
