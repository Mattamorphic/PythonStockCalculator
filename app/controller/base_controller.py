class BaseController(QWidget):

    def __init__(self):
        super().__init__()
        self.components = []
        self.update = pyqtSignal()

    def buildUI(self, layout):
        self.setLayout(layout(*self.components))

    def addComponent(self, component):
        self.components.append(component)
