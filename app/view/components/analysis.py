'''
    Average Stock Value Analysis

    Input widgets for average stock value analysis

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.model.stock_node import StockValue
from .value_data import ValueData, CurrencyValue
from PyQt5.QtWidgets import QVBoxLayout


class AverageStockValueData(QVBoxLayout):
    '''
        AverageStockValueData layout used for analysis

        Args:
            stockValue (StockValue): A stock value object
    '''
    def __init__(self, stockValue=None, parent=None):
        super().__init__(parent)
        if stockValue is None:
            stockValue = AverageStockValueData.createEmptyValue()
        self.stockValue = stockValue
        self.initUI()

    @staticmethod
    def createEmptyValue():
        '''
            Return an empty placeholder stock value

            Return:
                StockValue
        '''
        return StockValue(0.0, 0.0, 0.0, 0.0)

    def initUI(self):
        '''
            Iniitalize the UI
        '''
        group = ValueData()
        self.lowComponent = group.addRow(
            'Low:', CurrencyValue('$', self.stockValue.getLowValue()))
        self.highComponent = group.addRow(
            'High:', CurrencyValue('$', self.stockValue.getHighValue()))
        group.addColumn()
        self.openComponent = group.addRow(
            'Open:', CurrencyValue('$', self.stockValue.getOpeningValue()))
        self.closeComponent = group.addRow(
            'Close:', CurrencyValue('$', self.stockValue.getCloseValue()))
        self.addLayout(group.done())

    def updateAverageValues(self, stockValue):
        '''
            Update the UI

            Args:
                stockValue (StockValue): The update value
        '''
        self.stockValue = stockValue
        self.lowComponent.updateValue(
            CurrencyValue('$', self.stockValue.getLowValue()))
        self.highComponent.updateValue(
            CurrencyValue('$', self.stockValue.getHighValue()))
        self.openComponent.updateValue(
            CurrencyValue('$', self.stockValue.getOpeningValue()))
        self.closeComponent.updateValue(
            CurrencyValue('$', self.stockValue.getCloseValue()))
