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
        self.amount = amount
        self.initUI()

    def initUI(self):
        '''
            Initialize the UI widget for the controller (the view)
        '''
        self.amountComponent = Amount()
        self.amountComponent.setValue(self.amount)
        self.amountComponent.onChange.connect(self.updateAmount)
        self.labelComponent = AmountLabel()

        self.setLayout(AmountLayout(
            self.labelComponent,
            self.amountComponent
        ))

    def updateAmount(self, amount):
        '''
            Update the amount of stock

            Args:
                amount  int     The amount of stock
        '''
        self.amount = amount if amount is not None or '' else 0
        # emit the custom signal with the new amount
        self.update.emit(amount)

    def getAmount(self):
        '''
            Getter for the amount instance variable

            Returns:
                int
        '''
        return self.amount
