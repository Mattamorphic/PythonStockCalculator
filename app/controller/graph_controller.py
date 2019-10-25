'''
    Name:
        Graph Controller
    Description:
        Controller for the returned graph widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.view.components.graph import (
    GraphOptions,
    StockLineGraph
)
from app.view.components.labels import GraphLabel
from app.view.layouts import GraphLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class GraphController(QWidget):
    '''
        Graph Controller extends from a pyqtgraph specific widget
    '''
    update = pyqtSignal(str)

    def __init__(self, option):
        '''
            Initialize the parent and the UI component
        '''
        super().__init__()
        self.selectedOption = option
        self.initUI()

    def initUI(self):
        '''
            Initialize the UI widgets
        '''
        self.graphComponent = StockLineGraph('Stock')
        self.graphLabel = GraphLabel(self.selectedOption)
        self.graphOptions = GraphOptions(self.selectedOption)
        self.graphOptions.onChecked.connect(
            lambda option: self.update.emit(option)
        )
        self.setLayout(
            GraphLayout(
                self.graphOptions,
                self.graphLabel,
                self.graphComponent
            )
        )

    def clear(self):
        '''
            Clear the graph of all plots
        '''
        self.graphComponent.initGraph()

    def plotStock(self, label, x, y, low, high):
        '''
            Plot a stock to the graph

            Args:
                label   string      The label for the stock
                x       int[]       Each point represents a day
                y       float[]     Each entry represents the value of the stock
                low     float       The low for this stock entry
                high    float       The high for this stock entry
        '''
        self.graphComponent.plotStock(label, x, y, low, high)
