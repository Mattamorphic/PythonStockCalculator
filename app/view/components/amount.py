'''
    Name:
        Amount
    Description:
        Input widget handling amount
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSpinBox


class Amount(QSpinBox):
    '''
        Amount widget extends from QLineEdit
    '''
    onChange = pyqtSignal(int)

    def __init__(self, parent=None):
        '''
            Initialize the widget

            Args:
                value   int     Base value
                parent  QWidget The parent to attach the widget to
        '''
        super().__init__(parent)
        self.setRange(1, 1000000)
        self.valueChanged.connect(self.amountChange)

    def amountChange(self, value):
        '''
            On amount change validate and emit custom signal

            Args:
                value   int     The value provided
        '''
        self.onChange.emit(value if value > 0 else 1)
