'''
    Amount
    Input widget handling amount

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSpinBox


class Amount(QSpinBox):
    '''
        Amount widget extends from QLineEdit

        Args:
            amount (int):     Base value
            parent (QWidget): The parent to attach the widget to
    '''
    onChange = pyqtSignal(int)

    def __init__(self, amount: int, parent=None):
        super().__init__(parent)
        self.setValue(amount)
        self.setRange(1, 1000000)
        self.valueChanged.connect(self.amountChange)

    def amountChange(self, value: int):
        '''
            On amount change validate and emit custom signal

            Args:
                value (int): The value provided
        '''
        self.onChange.emit(value if value > 0 else 1)
