'''
    Profit analysis specific components
    Components surrounding displaying profit related data

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.model.stock_node import StockProfit
from .value_data import ValueData, CurrencyValue, PercentageValue
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QVBoxLayout


class StockSelector(QComboBox):
    '''
        Stock selector
        Args:
            values          (List[str]):   Base values
            selectedIndex   (int)
            parent          (QWidget): The parent to attach the widget to
    '''
    onChange = pyqtSignal(str)

    def __init__(self, values=[], selectedIndex: int = 0, parent=None):
        super().__init__(parent)
        self.values = values
        self.addItems(values)
        if values:
            self.setCurrentIndex(0)
        self.currentIndexChanged.connect(self.stockIndexChange)

    def updateValues(self, values):
        '''
            Overwrite the list of values

            Args:
                values (List[str]): The values to update with
        '''
        # temporary store the selected items
        self.clear()
        # add the selected + new values
        self.values = values
        self.addItems(self.values)
        if values:
            self.setCurrentIndex(0)

    def stockIndexChange(self, index):
        '''
            On the stock selection changing, get the values, and emit signal

            Args:
                index (int)
        '''
        self.onChange.emit(self.values[index])


class StockProfitValueData(QVBoxLayout):
    '''
        Present the stock value data

        Args:
            stockProfit (StockProfit): The stock profit data
    '''
    def __init__(self, stockProfit=None, parent=None):
        super().__init__(parent)
        if stockProfit is None:
            stockProfit = StockProfitValueData.createEmptyValue()
        self.stockProfit = stockProfit
        self.initUI()

    @staticmethod
    def createEmptyValue():
        '''
            Helper method for placeholder data

            Returns:
                StockProfit
        '''
        return StockProfit(1)

    def initUI(self):
        '''
            UI Initializer
        '''
        group = ValueData('Lowest data')
        self.lowBuyComponent = group.addRow(
            'Buy Price:',
            CurrencyValue('$', self.stockProfit.getLowestBuyPrice()))
        self.lowSellComponent = group.addRow(
            'Sell Price:',
            CurrencyValue('$', self.stockProfit.getLowestSellPrice()))
        self.lowProfitComponent = group.addRow(
            'profit:', CurrencyValue('$', self.stockProfit.getLowestMargin()))
        group.addColumn('Highest data')
        self.highBuyComponent = group.addRow(
            'Buy Price:',
            CurrencyValue('$', self.stockProfit.getHighestBuyPrice()))
        self.highSellComponent = group.addRow(
            'Sell Price:',
            CurrencyValue('$', self.stockProfit.getHighestSellPrice()))
        self.highProfitComponent = group.addRow(
            'profit:', CurrencyValue('$', self.stockProfit.getHighestMargin()))
        group.addColumn("Average data")
        self.averageBuyComponent = group.addRow(
            'Buy Price:',
            CurrencyValue('$', self.stockProfit.getAverageBuyPrice()))
        self.averageSellComponent = group.addRow(
            'Sell Price:',
            CurrencyValue('$', self.stockProfit.getAverageSellPrice()))
        self.averageProfitComponent = group.addRow(
            'profit:', CurrencyValue('$', self.stockProfit.getAverageMargin()))
        group.addColumn("Percentage gain")
        self.gainComponent = group.addRow(
            'Percentage',
            PercentageValue(self.stockProfit.getPercentageGain()))
        self.addLayout(group.done())

    def updateProfitValues(self, stockProfit):
        '''
            Update the UI based on a new stockProfit object

            Args:
                stockProfit (StockProfit): updated profit data
        '''
        self.stockProfit = stockProfit
        self.lowBuyComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getLowestBuyPrice()))
        self.highBuyComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getHighestBuyPrice()))
        self.averageBuyComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getAverageBuyPrice()))
        self.lowSellComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getLowestSellPrice()))
        self.highSellComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getHighestSellPrice()))
        self.averageSellComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getAverageSellPrice()))
        self.lowProfitComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getLowestMargin()))
        self.highProfitComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getHighestMargin()))
        self.averageProfitComponent.updateValue(
            CurrencyValue('$', self.stockProfit.getAverageMargin()))
        self.gainComponent.updateValue(
            PercentageValue(self.stockProfit.getPercentageGain()))
