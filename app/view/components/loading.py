from PyQt5.QtWidgets import QProgressBar


class LoadingProgress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def update(self, value):
        self.setValue(value)
