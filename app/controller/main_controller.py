'''
    Main Controller
    Controller for the main controls / functions

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from datetime import datetime, timedelta
from .amount_controller import AmountController
from .analysis_controller import AnalysisController
from .calendar_controller import CalendarController
from .graph_controller import GraphController
from .profit_controller import ProfitController
from app.lib.constants import Constants
from .stock_controller import StockController
from PyQt5.QtWidgets import QHBoxLayout, QTabWidget, QVBoxLayout, QWidget


class MainController(QWidget):
    '''
        MainController serves the initial layout and adds the controllers to the interface
    '''
    def __init__(self, model):
        '''
            Upon instantiation initialize the state
                setup the controllers and init the UI
        '''
        super().__init__()
        self.model = model
        self.state = MainState()
        self.state.fromDate = self.model.getEarliestDateString()
        self.state.toDate = self.model.getLatestDateString()
        self.initControllers()
        self.initUI()

    def initControllers(self):
        '''
            Initialize the controllers with the state
                tie each of these controllers to the main controller
        '''
        self.amountController = AmountController(self.state.amount)
        self.amountController.update.connect(self.updateAmountState)
        self.analysisController = AnalysisController(self.state.fromDate,
                                                     self.state.toDate)
        self.profitController = ProfitController(self.state.amount,
                                                 self.state.fromDate,
                                                 self.state.toDate)
        self.fromCalendarController = CalendarController(
            self.state.fromDate, self.state.fromDate, self.state.toDate,
            "Buy date")
        self.fromCalendarController.update.connect(self.updateFromDateState)
        self.toCalendarController = CalendarController(self.state.toDate,
                                                       self.state.fromDate,
                                                       self.state.toDate,
                                                       "Sell date")
        self.toCalendarController.update.connect(self.updateToDateState)
        self.selectedStockController = StockController(
            self.model.selectAllNames())
        self.selectedStockController.update.connect(
            self.updateSelectedStockState)
        self.graphController = GraphController(self.state.option)
        self.graphController.update.connect(self.updateGraphData)

    def initUI(self):
        '''
            Build the UI from the controller components
        '''
        layout = QVBoxLayout()
        self.setLayout(layout)
        config = QHBoxLayout()
        config.addWidget(self.selectedStockController)
        config.addWidget(self.fromCalendarController)
        config.addWidget(self.toCalendarController)
        layout.addLayout(config)

        layout.addWidget(self.amountController)

        tabs = QTabWidget()
        tabs.addTab(self.profitController, 'Profit Estimates')
        tabs.addTab(self.graphController, 'Value Graph')
        tabs.addTab(self.analysisController, 'Stock Analysis')

        layout.addWidget(tabs)

    def updateAmountState(self, number: int):
        '''
            State management for the amount, on change reprocess the data

            Args:
                number (int): Amount
        '''
        self.state.amount = number
        self.profitController.updateMultiplier(number)
        self.process()

    def updateFromDateState(self, dateString: str):
        '''
            State management for the from date, on change reprocess the data

            Args:
                dateString (str): Date in yyyy-mm-dd format
        '''
        self.state.fromDate = dateString
        self.analysisController.updateFromDate(dateString)
        self.profitController.updateFromDate(dateString)
        self.toCalendarController.setEarliestDate(dateString)
        self.process()

    def updateToDateState(self, dateString: str):
        '''
            State management for the to date, on change reprocess the data

            Args:
                dateString (str): Date in yyyy-mm-dd format
        '''
        self.state.toDate = dateString
        self.analysisController.updateToDate(dateString)
        self.profitController.updateToDate(dateString)
        self.fromCalendarController.setLatestDate(dateString)
        self.process()

    def updateGraphData(self, option: str):
        '''
            Update the option

            Args:
                option (str):  Check Constants.GraphOptions for enumerable
        '''
        self.state.option = option
        self.process()

    def updateSelectedStockState(self, stock: str):
        '''
            State management for the selected sock, on change reprocess the data

            Args:
                stock (str): stock label
        '''
        self.state.selectedStock = stock
        self.process()

    def process(self):
        '''
            Using the state, process the selected stock nodes
        '''
        # Create a new graph (clearing the previous)
        self.graphController.clear()
        # Fetch the stotck nodes from the model
        stockNodes = [
            self.model.findByName(label) for label in self.state.selectedStock
        ]
        self.analysisController.updateStockNodes(stockNodes)
        self.profitController.updateStockNodes(stockNodes)
        data = []
        # Process each node
        for node in stockNodes:
            data.append(self.processNode(node))

    def processNode(self, node):
        '''
            Process a stock node

            Args:
                node (StockNode): A node represnting a stock entry
        '''
        data = []    # The data
        dates = []    # Dates we have data for
        # Create date boundary objects we can iterate with
        currentDate = datetime.strptime(self.state.fromDate,
                                        Constants.PY_DATE_FORMAT)
        endDate = datetime.strptime(self.state.toDate,
                                    Constants.PY_DATE_FORMAT)

        # The low/high for that stock
        low = None
        high = None
        # Create a time delta to iterate with
        delta = timedelta(days=1)
        while currentDate <= endDate:
            # We don't have data at weekdays, lets skip,
            if currentDate.weekday() < 5:
                # Try and fetch the StockValue object for the currentDate
                nodeValue = node.getValueForDate(
                    currentDate.strftime(Constants.PY_DATE_FORMAT))
                # If we have a value, process, and append with the date
                if nodeValue is not None:
                    if self.state.option == Constants.GraphOptions.LOW:
                        value = nodeValue.getLowValue()
                    elif self.state.option == Constants.GraphOptions.HIGH:
                        value = nodeValue.getHighValue()
                    elif self.state.option == Constants.GraphOptions.OPEN:
                        value = nodeValue.getOpeningValue()
                    elif self.state.option == Constants.GraphOptions.DIFF:
                        value = nodeValue.getHighLowDiff()
                    else:
                        value = nodeValue.getCloseValue()

                    if high is None or value > high:
                        high = value
                    elif low is None or value < low:
                        low = value
                    dates.append(currentDate.timestamp())
                    data.append(value)
            # move the currentData by our 1 day delta
            currentDate += delta

        self.graphController.plotStock(label=node.getLabel(),
                                       x=dates,
                                       y=data,
                                       low=low,
                                       high=high)


class MainState:
    '''
        A tiny wrapper class for our state
    '''
    amount = 1
    option = Constants.GraphOptions.LOW
    selectedStock = []
    fromDate = None
    toDate = None
