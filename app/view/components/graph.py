'''
    Graph
    Classes for building Graphs

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
import datetime
import pyqtgraph as pg
from app.lib.constants import Constants
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QRadioButton, QWidget


class NonScientificAxis(pg.AxisItem):
    '''
        This is used to print full value ticks on the axis
            not to use scientific notation

        Args:
            *args (args):      Unnamed parameters
            **kwargs (kwargs): Named parameters
    '''
    def __init__(self, *args, **kwargs):
        super(NonScientificAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale: float, spacing: float):
        '''
            For tick strings, round them to 2 decimal places

            Args:
                values  (List[float])   The values to use as ticks
                scale   (float)         The scaling to use
                spacing (float)         The spacing between the ticks

            Returns:
                (List[str])
        '''
        # TODO : Validation
        return [round(value, 2)
                for value in values]    # This line return the NonScie


class DateAxis(pg.AxisItem):
    '''
        This is used to print the date string on the axis

        Args:
            *args (args):      Unnamed parameters
            **kwargs (kwargs): Named parameters
    '''
    def __init__(self, *args, **kwargs):
        super(DateAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        '''
            For ticks, convert them to date strings

            Args:
                values  (List[float])   The values to use as ticks
                scale   (float)         The scaling to use
                spacing (float)         The spacing between the ticks

            Returns:
                (List[str])
        '''
        return [
            datetime.date.fromtimestamp(int(value)).strftime(
                Constants.PY_DATE_FORMAT) for value in values
        ]


class StockLineGraph(pg.GraphicsLayoutWidget):
    '''
        Creates a stock line graph widget

        Args:
            title (str): A title for the graph
    '''
    prefix = "Stock"

    def __init__(self, title: str = ''):
        super().__init__()
        self.setStyleSheet("min-height: 300px")
        self.initGraph(title)

    def initGraph(self, title: str = ''):
        '''
            Clear and initialize the graph
        '''
        self.clear()
        self.lowestValue = 0
        self.highestValue = 0
        self.plotCount = 0
        self.plot = self.addPlot(title="%s : %s" % (self.prefix, title),
                                 axisItems={
                                     'left':
                                     NonScientificAxis(orientation='left'),
                                     'bottom': DateAxis(orientation='bottom')
                                 })
        self.plot.addLegend(offset=(0, 0))

    def plotStock(self, label: str, x, y, low: float, high: float):
        '''
            Plot a stock to the graph

            Args:
                label   (str):          The label for the stock
                x       (List[str]):    Each point represents a day
                y       (List[float]):  Each entry represents the value of the stock
                low     (float):        The low for this stock entry
                high    (float):        The high for this stock entry
        '''
        # Redraw the y axis depending on the high and low points
        if self.highestValue is None or high > self.highestValue:
            self.highestValue = high
            self.plot.setYRange(self.lowestValue, self.highestValue)
        elif self.lowestValue is None or low < self.lowestValue:
            self.lowestValue = low
            self.plot.setYRange(self.lowestValue, self.highestValue)
        # Add a plot to the plot
        self.plot.plot(antialias=True,
                       x=x,
                       y=y,
                       name=label,
                       pen=pg.intColor(self.plotCount))
        self.plotCount += 1


class GraphOptions(QWidget):
    '''
        Creates a widget that holds references to 3 options

        Args:
            initial (str): An initital option to select
    '''

    onChecked = pyqtSignal(str)

    def __init__(self, initial: str):
        super().__init__()
        self.options = []
        # TODO used DI to inject the options
        availableOptions = Constants.GraphOptions.all()
        if initial not in availableOptions:
            raise IndexError("%s not found in available options" % (initial))
        for option in availableOptions:
            radio = GraphOptionButton(option)
            radio.toggled.connect(self.radioToggle)
            if option == initial:
                radio.setChecked(True)
            self.options.append(radio)

    def getOptions(self):
        '''
            Getter

            Returns:
                (List[GraphOptionButton])
        '''
        return self.options

    def radioToggle(self):
        '''
            Handles the toggled signal emitted from the GraphOptionButton
        '''
        option = self.sender()
        if option.isChecked():
            self.onChecked.emit(
                Constants.GraphOptions.getOptionOrLabel(option.text()))


class GraphOptionButton(QRadioButton):
    '''
        Small RadioButton wrapper for readability

        Args:
            label (str): A label for the graph option
    '''
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setText(Constants.GraphOptions.getOptionOrLabel(label))
        self.setChecked(False)
