'''
    Average Stock Value Analysis

    Input widgets for average stock value analysis

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.model.stock_node import StockValue
from .value_data import ValueData
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
        self.lowComponent = group.addRow('Low:', self.stockValue.getLowValue())
        self.highComponent = group.addRow('High:',
                                          self.stockValue.getHighValue())
        group.addColumn()
        self.openComponent = group.addRow('Open:',
                                          self.stockValue.getOpeningValue())
        self.closeComponent = group.addRow('Close:',
                                           self.stockValue.getCloseValue())
        self.addLayout(group.done())

    def updateAverageValues(self, stockValue):
        '''
            Update the UI

            Args:
                stockValue (StockValue): The update value
        '''
        self.stockValue = stockValue
        self.lowComponent.updateValue(self.stockValue.getLowValue())
        self.highComponent.updateValue(self.stockValue.getHighValue())
        self.openComponent.updateValue(self.stockValue.getOpeningValue())
        self.closeComponent.updateValue(self.stockValue.getCloseValue())


class SpecificStockValueData:
    pass


class VariationStockValueData:
    pass
