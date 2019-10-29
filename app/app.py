'''
    App
    Core app container for the stock calculator

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''

from app.controller.loading_controller import LoadingController
from app.controller.main_controller import MainController
from app.lib.stock_worker import StockWorker

from PyQt5.QtWidgets import (QDesktopWidget, QMainWindow)


class App(QMainWindow):
    '''
        Main window for the stock profit app
    '''
    def __init__(self, source):
        super().__init__()
        self.resourceSize = source.getResourceSize()
        self.initUI(source)

    def updateProgressPercentage(self, bytes: int):
        '''
            Update the loading percentage based on the current bytes

            Args:
                bytes (int): The byte loaded
        '''
        self.loadingController.updateProgressBar(
            (bytes / self.resourceSize) * 100)

    def loadModel(self, source):
        '''
            Load takes in a model source, and uses a QThread to load this

            Args:
                source (StockSource): A source for our stock model
        '''
        worker = StockWorker(self, source)
        worker.result.connect(self.initMain)
        worker.progressLabel.connect(self.loadingController.updateProgress)
        worker.progressBytes.connect(self.updateProgressPercentage)
        worker.start()

    def initUI(self, source):
        '''
            Initializes the Stock UI
        '''
        self.center()
        self.setWindowTitle("Stock Profit Calculator")
        self.updateStatusBar("Starting Up...")
        self.initLoading()
        self.show()
        self.loadModel(source)

    def initLoading(self):
        '''
            Initializes the loading controller and attaches the widget (as a view)
        '''
        self.updateStatusBar("Loading stock data...")
        self.loadingController = LoadingController()
        self.setCentralWidget(self.loadingController)

    def initMain(self, stock):
        '''
            Initializes the main  controller and attaches the widget (as a view)

            Args:
                model (Stock): The stock model to attach to the main controller
        '''
        self.updateStatusBar("Ready...")
        self.mainController = MainController(stock)
        self.setCentralWidget(self.mainController)

    def updateStatusBar(self, value):
        '''
            Sets the default value for the status bar
        '''
        self.statusBar().showMessage(value)

    def center(self):
        '''
            Center the GUI on this display
        '''
        # Geometry of the widget relative to its parent
        window_rectangle = self.frameGeometry()
        # Find the display center point
        center_point = QDesktopWidget().availableGeometry().center()
        # Move the geometry
        window_rectangle.moveCenter(center_point)
        self.move(window_rectangle.topLeft())
