'''
    Loading Controller
    Controller for the loading widget widget

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.labels import (CurrentLoadingLabel, LoadingLabel)
from app.view.components.loading import LoadingProgress
from app.view.layouts import LoadingLayout
from PyQt5.QtWidgets import QWidget


class LoadingController(QWidget):
    '''
        Loading controller
    '''
    def __init__(self):
        '''
            Inject a loading label
        '''
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
            Initializes the UI
        '''
        self.label = CurrentLoadingLabel()
        self.progress = LoadingProgress()
        self.setLayout(LoadingLayout(LoadingLabel(), self.label,
                                     self.progress))

    def updateProgress(self, value: str):
        '''
            A setter function that exposes the loading label

            Args:
                value (str): The new value
        '''
        self.label.update(value)

    def updateProgressBar(self, value: float):
        '''
            A setter functiton for updating the progress bar

            Args:
                value (float): The progress percentage
        '''
        self.progress.update(value)
