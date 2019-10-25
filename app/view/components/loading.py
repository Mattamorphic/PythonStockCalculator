'''
    Loading
    Loading components

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''

from PyQt5.QtWidgets import QProgressBar


class LoadingProgress(QProgressBar):
    '''
        A Loading bar
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

    def update(self, value):
        '''
            Update the progress bar

            Args:
                value (float): The progress < 100
        '''
        if value < 0.0 or value > 100.0:
            raise ValueError("%d is out of bounds, 0 to 100")
        self.setValue(value)
