'''
    Name:
        Profit Controller
    Description:
        Controller for the profitt widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.profit import (
    StockProfitValueData
)
from app.view.components.stock import (
    StockSelector
)
from app.view.layouts import ProfitLayout
from PyQt5.QtWidgets import QWidget


class ProfitController(QWidget):

    def __init__(
        self,
        multiplier,
        fromDateString,
        toDateString,
        stockNodes=[],
        selectedStock=None,
        parent=None
    ):
        '''
            Initialize the controller and set the instance variables

            Args:
                multiplier      int         The amount of stock units
                fromDateString  string      The from (buy) date
                toDateString    string      The to (sell) date
                stockNodes      StockNode[] All of the selected nodes
                selectedStock   StockNode   The node we are analysing
        '''
        super().__init__(parent)
        self.multiplier = multiplier
        self.fromDate = fromDateString
        self.toDate = toDateString
        self.stockNodes = stockNodes
        self.selectedStock = selectedStock
        self.initUI()

    def initUI(self):
        '''
            Initializes the UI
        '''
        selectedStockLabels = [node.getLabel() for node in self.stockNodes]
        self.stockSelectorComponent = StockSelector(
            selectedStockLabels
        )
        self.stockSelectorComponent.onChange.connect(
            self.updateSelectedStockByLabel
        )

        self.profitValue = StockProfitValueData(self.getStockProfit())

        layout = ProfitLayout(
            self.stockSelectorComponent,
            self.profitValue
        )
        self.setLayout(layout)

    def getStockProfit(self):
        '''
            A wrapper to get the profit value from either the current node
            or an empty value

            Returns:
                StockProfit
        '''
        empty = StockProfitValueData.createEmptyValue()
        if self.selectedStock is None:
            return empty
        profitValue = self.selectedStock.getProfitValue(
            self.multiplier,
            self.fromDate,
            self.toDate
        )
        return empty if profitValue is None else profitValue

    def updateProfitDetails(self):
        '''
            Update the profit values component
        '''
        self.profitValue.updateProfitValues(self.getStockProfit())

    def updateMultiplier(self, multiplier):
        '''
            Setter for multiplier instance variable

            Args:
                multiplier  int     The amount of stock to purchase
        '''
        self.multiplier = multiplier
        self.updateProfitDetails()

    def updateSelectedStock(self, node):
        '''
            Updated the current stock node being analysed

            Args:
                node    StockNode   The node being analysed
        '''
        self.selectedStock = node
        self.updateProfitDetails()

    def updateSelectedStockByLabel(self, label):
        '''
            Given a label, find this in all our potentoal nodes, and update
            the selectedStock instance variable

            Args:
                label   string  The label for a stock
        '''
        node = next((node for node in self.stockNodes if node.getLabel() == label), None)
        if node is not None:
            self.updateSelectedStock(node)

    def updateFromDate(self, fromDate):
        '''
            Update the fromDate in our analysis

            Args:
                fromDate    string  The from (buy) date
        '''
        self.fromDate = fromDate
        self.updateProfitDetails()

    def updateToDate(self, toDate):
        '''
            Update the toDate in our analysis

            Args:
                toDate    string  The to (sell) date
        '''
        self.toDate = toDate
        self.updateProfitDetails()

    def updateStockNodes(self, stockNodes):
        '''
            Update all the stock nodes that we can analyse

            Args:
                stockNodes  StockNodes[]    The potential stock nodes to analyse
        '''
        self.stockNodes = stockNodes
        self.stockSelectorComponent.updateValues(
            [
                node.getLabel() for node in self.stockNodes
            ]
        )
        if len(stockNodes) > 0:
            self.updateSelectedStock(self.stockNodes[0])
        else:
            self.updateSelectedStock(None)
