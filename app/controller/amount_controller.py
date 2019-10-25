'''
    Name:
        Amount Controller
    Description:
        Controller for the return amount widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.amount import Amount
from app.view.components.labels import AmountLabel
from app.view.layouts import AmountLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class AmountController(QWidget):
    '''
        Amount controller handles delivering and monitoring the widgets related to the stock amount
    '''

    update = pyqtSignal(int)

    def __init__(self, amount):
        '''
            Initialize the amount controller

            Args
                amount  int     The initial amount
        '''
        super().__init__()
        amountComponent = Amount(amount)
        amountComponent.onChange.connect(
            lambda amount: self.update.emit(
                amount if amount is not None or '' else 0
            )
        )
        self.setLayout(AmountLayout(
            AmountLabel(),
            amountComponent
        ))
