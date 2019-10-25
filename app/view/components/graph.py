'''
    Name:
        Graph Axis
    Description:
        Holds helper classes sfor specific graph axis items
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
import datetime
import pyqtgraph as pg
from app.lib.constants import Constants
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QRadioButton, QWidget


class NonScientificAxis(pg.AxisItem):
    '''
        This is used to print full value ticks on the axis
            not to use scientific notation
    '''
    def __init__(self, *args, **kwargs):
        '''
            Initialize this, and the super class with the args/kwargs
                passing these to the parent

            Args:
                *args       args    Unnamed parameters
                **kwargs    kwargs  Named parameters
        '''
        super(NonScientificAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        '''
            For tick strings, round them to 2 decimal places

            Args:
                values      float[]     The values to use as ticks
                scale       float       The scaling to use
                spacing     float       The spacing between the ticks
        '''
        # TODO : Validation
        return [round(value, 2) for value in values]  # This line return the NonScie


class DateAxis(pg.AxisItem):
    '''
        This is used to print the date string on the axis
    '''

    def __init__(self, *args, **kwargs):
        '''
            Initialize this, and the super class with the args/kwargs
                passing these to the parent

            Args:
                *args       args    Unnamed parameters
                **kwargs    kwargs  Named parameters
        '''
        super(DateAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        '''
            For tick strings, round them to 2 decimal places

            Args:
                value                   The values to use as ticks
                scale       float       The scaling to use
                spacing     float       The spacing between the ticks
        '''
        return [
            datetime.date.fromtimestamp(int(value)).strftime(Constants.PY_DATE_FORMAT)
            for value in values
        ]


class StockLineGraph(pg.GraphicsLayoutWidget):

    def __init__(self, title):
        super().__init__()
        self.setStyleSheet("min-height: 300px")
        self.title = title
        self.initGraph()

    def initGraph(self):
        self.clear()
        self.lowestValue = 0
        self.highestValue = 0
        self.plotCount = 0
        self.plot = self.addPlot(
            title=self.title,
            axisItems={
                'left': NonScientificAxis(orientation='left'),
                'bottom': DateAxis(orientation='bottom')
            }
        )
        self.plot.addLegend(offset=(0, 0))

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
        # Redraw the y axis depending on the high and low points
        if self.highestValue is None or high > self.highestValue:
            self.highestValue = high
            self.plot.setYRange(self.lowestValue, self.highestValue)
        elif self.lowestValue is None or low < self.lowestValue:
            self.lowestValue = low
            self.plot.setYRange(self.lowestValue, self.highestValue)
        # Add a plot to the plot
        plot = self.plot.plot(
            antialias=True,
            # symbol = 'o',
            x=x,
            y=y,
            name=label,
            pen=pg.intColor(self.plotCount)
        )
        plot.sigClicked.connect(self.test)

        # print(self.plot.viewRange())
        # currentRange = self.plot.viewRange()
        # track the amount of plots we have
        self.plotCount += 1

    def test(self):
        print('click')


class GraphOptions(QWidget):

    onChecked = pyqtSignal(str)

    def __init__(self, initial):
        super().__init__()
        self.options = []
        for option in Constants.GraphOptions.all():
            radio = GraphOptionButton(option)
            radio.toggled.connect(
                self.radioToggle
            )
            if option == initial:
                radio.setChecked(True)
            self.options.append(radio)

    def getOptions(self):
        return self.options

    def radioToggle(self):
        option = self.sender()
        if option.isChecked():
            self.onChecked.emit(option.text())


class GraphOptionButton(QRadioButton):

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setText(label)
        self.setChecked(False)
