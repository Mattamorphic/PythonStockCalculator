'''
    Name:
        Stock Model
    Description:
        Model for interacting with stock
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from datetime import datetime
from app.lib.constants import Constants
from PyQt5.QtCore import QObject, pyqtSignal
from .stock_node import StockNode, StockValue


class Stock(QObject):
    '''
        Stock model representing stock
    '''

    # Model Data
    stockData = {}

    # The date bounds of our data
    earliestDate = None
    latestDate = None

    # The value bounds of our data
    highestValue = None
    lowestValue = None

    # Used during loading the data to provide progress
    currentLabel = None
    loadedBytes = 0
    currentLoadLabel = pyqtSignal(str)
    currentLoadBytes = pyqtSignal(int)

    def __init__(self, parent=None):
        '''
            On instantiation populate the model with data

            Args:
                stock_source (StockSource)  The source of our data
        '''
        super(Stock, self).__init__(parent)

    def load(self, stock_source):
        '''
            Load the data into the model

            Args:
                stock_source (StockSource)  The source of our data

        '''
        self.stockData = {}
        # TODO : validate headers
        valueFields = ["open", "high", "low", "close"]
        # genRow is a generator that will yield rows till it completes
        for row in stock_source.genRow():
            self.loadedBytes += stock_source.getLineSize()
            label = row["name"]
            date_string = row["date"]
            # create and insert a stock node if it doesnt exist
            if label not in self.stockData:
                self.insertStockNode(
                    self.createStockNode(label)
                )
            # cast the string values
            for field in valueFields:
                if row[field] == '':
                    row[field] = 0.0
                else:
                    row[field] = float(row[field])

            # update the node
            self.stockData[label].addData(
                date_string,
                StockValue(
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"]
                )
            )
            # track the global bounds
            date = datetime.strptime(date_string, Constants.PY_DATE_FORMAT)
            if self.earliestDate is None or date < self.earliestDate:
                self.earliestDate = date
            elif self.latestDate is None or date > self.latestDate:
                self.latestDate = date
            if self.highestValue is None or row["high"] > self.highestValue:
                self.highestValue = row["high"]
            elif self.lowestValue is None or row["low"] < self.lowestValue:
                self.lowestValue = row["low"]
            if self.currentLabel is None or label != self.currentLabel:
                self.currentLabel = label
                self.currentLoadLabel.emit(label)
                self.currentLoadBytes.emit(self.loadedBytes)

    def createStockNode(self, label):
        '''
            Given a label create a node

            Args:
                label   str     The node label

            Returns:
                StockNode
        '''
        return StockNode(label)

    def insertStockNode(self, node):
        '''
            Insert the nodes

            Args:
                node    StockNode   The node to insert
        '''
        label = node.getLabel()
        if label in self.stockData:
            raise ValueError(label + " already exists")
        self.stockData[label] = node

    def findByName(self, label):
        '''
            Return a single stock node by name

            Returns:
                StockNode
        '''
        if label in self.stockData:
            return self.stockData[label]
        return None

    def findByDate(self, date):
        '''
            Return all stock nodes for a given date

            Returns:
                List<StockNode>
        '''
        raise RuntimeError("Not implemented")

    def selectAll(self):
        '''
            Return all the stock nodes

            Returns:
                dict<string, StockNode>
        '''
        return self.stockData

    def selectAllNames(self):
        '''
            Return all stock labels

            Returns:
                list<string>
        '''
        return self.stockData.keys()

    def getEarliestDate(self):
        '''
            Returns a datetime representing the lower bound

            Returns:
                datetime
        '''
        return self.earliestDate

    def getLatestDate(self):
        '''
            Returns a datettime representing the upper bound

            Returns:
                datetime
        '''
        return self.latestDate

    def getEarliestDateString(self):
        '''
            Returns date as a string (yyyy-mm-dd)

            Returns:
                string
        '''
        return self.earliestDate.strftime(Constants.PY_DATE_FORMAT)

    def getLatestDateString(self):
        '''
            Returns date as a string (yyyy-mm-dd)

            Returns: string
        '''
        return self.latestDate.strftime(Constants.PY_DATE_FORMAT)

    def getLowestValue(self):
        '''
            Get the lowest value found

            Return:
                float
        '''
        return self.lowestValue

    def getHighestValue(self):
        '''
            Get the highest value found

            Return:
                float
        '''
        return self.highestValue
