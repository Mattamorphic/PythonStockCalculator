'''
    Name:
        Stock Selector
    Description:
        Input widget selecting from selected stock
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.model.stock_node import StockValue
from .value_data import ValueData
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout


class AverageStockValueData(QVBoxLayout):

    def __init__(self, stockValue=None, parent=None):
        super().__init__(parent)
        if stockValue is None:
            stockValue = AverageStockValueData.createEmptyValue()
        self.stockValue = stockValue
        self.initUI()

    @staticmethod
    def createEmptyValue():
        return StockValue(
            0.0,
            0.0,
            0.0,
            0.0
        )

    def initUI(self):
        group = ValueData()
        self.lowComponent = group.addRow(
            'Low:', self.stockValue.getLowValue()
        )
        self.highComponent = group.addRow(
            'High:', self.stockValue.getHighValue()
        )
        group.addColumn()
        self.openComponent = group.addRow(
            'Open:', self.stockValue.getOpeningValue()
        )
        self.closeComponent = group.addRow(
            'Close:', self.stockValue.getCloseValue()
        )
        self.addLayout(group.done())


    def updateAverageValues(self, stockValue):
        self.stockValue = stockValue
        self.lowComponent.updateValue(
            self.stockValue.getLowValue()
        )
        self.highComponent.updateValue(
            self.stockValue.getHighValue()
        )
        self.openComponent.updateValue(
            self.stockValue.getOpeningValue()
        )
        self.closeComponent.updateValue(
            self.stockValue.getCloseValue()
        )

    def addRow(self, *components):
        row = QHBoxLayout()
        for component in components:
            row.addLayout(component)
        return row


class SpecificStockValueData:
    pass


class VariationStockValueData:
    pass
