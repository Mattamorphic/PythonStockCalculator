'''
    Name:
        Analysis Controller
    Description:
        Controller for the analysis widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.analysis import (
    AverageStockValueData
)
from app.view.components.stock import (
    StockSelector
)
from app.view.components.labels import AnalysisOverviewLabel
from app.view.layouts import AnalysisLayout
from PyQt5.QtWidgets import QWidget


class AnalysisController(QWidget):
    '''
        Analysis Controller
    '''

    def __init__(
        self,
        fromDateString,
        toDateString,
        stockNodes=[],
        selectedStock=None,
        parent=None
    ):
        '''
            Initialize the controller and set the instance variables

            Args:
                fromDateString  string      The from (buy) date
                toDateString    string      The to (sell) date
                stockNodes      StockNode[] All of the selected nodes
                selectedStock   StockNode   The node we are analysing
        '''
        super().__init__(parent)
        self.fromDate = fromDateString
        self.toDate = toDateString
        self.stockNodes = stockNodes
        self.selectedStock = None
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
        self.overviewComponent = AnalysisOverviewLabel(
            AnalysisOverviewLabel.createOverviewString(
                self.fromDate,
                self.toDate,
                self.selectedStock.getLabel() if self.selectedStock is not None else None
            )
        )

        self.averageValues = AverageStockValueData(self.getAverageValues())

        self.setLayout(
            AnalysisLayout(
                self.stockSelectorComponent,
                self.overviewComponent,
                self.averageValues
            )
        )

    def getAverageValues(self):
        '''
            A wrapper to get the average value from either the current node
            or an empty value

            Returns:
                StockValue
        '''
        if self.selectedStock is None:
            return AverageStockValueData.createEmptyValue()
        return self.selectedStock.getAverageValues(
            self.fromDate,
            self.toDate
        )

    def updateAverageValues(self):
        '''
            Update the average values component
        '''
        self.averageValues.updateAverageValues(self.getAverageValues())

    def updateSelectedStock(self, node):
        '''
            Updated the current stock node being analysed

            Args:
                node    StockNode   The node being analysed
        '''
        self.selectedStock = node
        self.overviewComponent.update(
            self.overviewComponent.createOverviewString(
                self.fromDate,
                self.toDate,
                self.selectedStock.getLabel()
            )
        )
        self.updateAverageValues()

    def updateSelectedStockByLabel(self, label):
        '''
            Given a label, find this in all our potentoal nodes, and update
            the selectedStock instance variable

            Args:
                label   string  The label for a stock
        '''
        # next returns the next item in an interator, our first occurance.
        node = next(
            (node for node in self.stockNodes if node.getLabel() == label),
            None
        )
        if node is not None:
            self.updateSelectedStock(node)

    def updateFromDate(self, fromDate):
        '''
            Update the fromDate in our analysis

            Args:
                fromDate    string  The from (buy) date
        '''
        self.fromDate = fromDate
        self.updateAverageValues()

    def updateToDate(self, toDate):
        '''
            Update the toDate in our analysis

            Args:
                toDate    string  The to (sell) date
        '''
        self.toDate = toDate
        self.updateAverageValues()

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
        if stockNodes:
            self.updateSelectedStock(self.stockNodes[0])
