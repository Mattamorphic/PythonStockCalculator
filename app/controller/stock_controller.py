'''
    Name:
        Stock Controller
    Description:
        Controller for the stock widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.labels import StockLabel
from app.view.components.stock import (
    StockClear,
    StockFilter,
    StockList
)
from app.view.layouts import StockLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class StockController(QWidget):
    '''
        Stock controller handles delivering and monitoring the widgets related
        to the selected stock
    '''

    update = pyqtSignal(object)

    def __init__(self, stockLabels):
        '''
            Initalize the stock controller

            Args:
                stockLabels  str[]   String array of stock labels
        '''
        super().__init__()
        self.stockLabels = stockLabels
        self.stockFilter = ''
        self.selectedStock = []
        self.initUI()

    def initUI(self):
        '''
            Initialize the UI widget for the contoller (the view)
        '''
        self.labelComponent = StockLabel(self.selectedStock)
        self.clearComponent = StockClear()
        self.clearComponent.clicked.connect(self.clearSelected)
        self.stockListComponent = StockList(self.stockLabels, self.selectedStock)
        self.stockListComponent.onChange.connect(self.updateStock)
        self.stockFilterComponent = StockFilter(self.stockFilter)
        self.stockFilterComponent.onChange.connect(self.filterStock)
        self.stockFilterComponent.onError.connect(self.labelComponent.error)

        layout = StockLayout(
            self.labelComponent,
            self.clearComponent,
            self.stockFilterComponent,
            self.stockListComponent
        )
        self.setLayout(layout)

    def clearSelected(self):
        '''
            Clear selected stock
        '''
        self.updateStock([])
        self.stockFilterComponent.setText('')
        self.filterStock('', True)

    def updateStock(self, stock):
        '''
            Update the selected stock

            Args:
                stock  str[]     Selected stock
        '''
        self.labelComponent.update(stock)
        self.selectedStock = stock
        self.update.emit(stock)

    def filterStock(self, value, clearSelected=False):
        '''
            Filter the stock based on the value
        '''
        self.stockFilter = value.upper()
        # Here we are updating the stock label list filtering labels based
        # on our filter value, we filter out any selected stock labels
        self.stockListComponent.updateValues(
            list(
                filter(
                    (
                        lambda label:
                            (self.stockFilter in label and label not in self.selectedStock)
                    ),
                    self.stockLabels
                )
            ),
            clearSelected
        )

    def getSelected(self):
        '''
            Getter for the amount instance variable

            Returns:
                str[]
        '''
        return self.selectedStock
