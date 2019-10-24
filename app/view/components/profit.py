'''
    Name:
        Profit analysis specific components
    Description:
        Components surrounding displaying profit related data
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.model.stock_node import StockProfit
from .value_data import ValueData
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QVBoxLayout


class StockSelector(QComboBox):
    '''
        Stock selector
    '''
    onChange = pyqtSignal(str)

    def __init__(self, values=[], selectedIndex=0, parent=None):
        '''
            Initialize the widget

            Args:
                values      str[]   Base values
                selected    int
                parent      QWidget The parent to attach the widget to
        '''
        super().__init__(parent)
        self.values = values
        self.addItems(values)
        if len(values) > 0:
            self.setCurrentIndex(0)
        self.currentIndexChanged.connect(self.stockIndexChange)

    def updateValues(self, values):
        '''
            Overwrite the list of values
        '''
        # temporary store the selected items
        self.clear()
        # add the selected + new values
        self.values = values
        self.addItems(self.values)
        if len(values) > 0:
            self.setCurrentIndex(0)

    def stockIndexChange(self, index):
        '''
            On the stock selection changing, get the values, and emit signal
        '''
        self.onChange.emit(self.values[index])


class StockProfitValueData(QVBoxLayout):

    def __init__(self, stockProfit=None, parent=None):
        super().__init__(parent)
        if stockProfit is None:
            stockProfit = StockProfitValueData.createEmptyValue()
        self.stockProfit = stockProfit
        self.initUI()

    @staticmethod
    def createEmptyValue():
        return StockProfit(1)

    def initUI(self):
        group = ValueData('Lowest data')
        self.lowBuyComponent = group.addRow(
            'Buy Price:', self.stockProfit.getLowestBuyPrice()
        )
        self.lowSellComponent = group.addRow(
            'Sell Price:', self.stockProfit.getLowestSellPrice()
        )
        self.lowProfitComponent = group.addRow(
            'profit:', self.stockProfit.getLowestMargin()
        )
        group.addColumn('Highest data')
        self.highBuyComponent = group.addRow(
            'Buy Price:', self.stockProfit.getHighestBuyPrice()
        )
        self.highSellComponent = group.addRow(
            'Sell Price:', self.stockProfit.getHighestSellPrice()
        )
        self.highProfitComponent = group.addRow(
            'profit:', self.stockProfit.getHighestMargin()
        )
        self.addLayout(group.done())

    def updateProfitValues(self, stockProfit):
        self.stockProfit = stockProfit
        self.lowBuyComponent.updateValue(self.stockProfit.getLowestBuyPrice())
        self.highBuyComponent.updateValue(self.stockProfit.getHighestBuyPrice())
        self.lowSellComponent.updateValue(self.stockProfit.getLowestSellPrice())
        self.highSellComponent.updateValue(self.stockProfit.getHighestSellPrice())
        self.lowProfitComponent.updateValue(self.stockProfit.getLowestMargin())
        self.highProfitComponent.updateValue(self.stockProfit.getHighestMargin())

    def addRow(self, *components):
        row = QHBoxLayout()
        for component in components:
            row.addLayout(component)
            row.setAlignment(Qt.AlignTop)
        return row
