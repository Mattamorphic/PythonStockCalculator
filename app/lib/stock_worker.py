'''
    Stock Worker
    A thread used to load / create the model

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import QThread, pyqtSignal
from app.model.stock import Stock


class StockWorker(QThread):
    '''
        Worker thread

        Args:
            parent  (QWidget):     The owner of the thread
            source  (StockSource): A stock source
    '''
    result = pyqtSignal(object)
    progressLabel = pyqtSignal(str)
    progressBytes = pyqtSignal(int)

    def __init__(self, parent, source):
        super(StockWorker, self).__init__(parent)
        self.source = source

    def run(self):
        '''
            Start the thread
        '''
        model = Stock()
        model.currentLoadLabel.connect(
            lambda string: self.progressLabel.emit(string)
        )
        model.currentLoadBytes.connect(
            lambda bytes: self.progressBytes.emit(bytes)
        )
        model.load(self.source)
        self.result.emit(model)

    def stop(self):
        '''
            Interrupt and kill the thread
        '''
        self.terminate()
