'''
    Name:
        Custom Labels
    Description:
        Module containing all of the custom labels
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class BaseLabel(QLabel):
    '''
        Base Label extends from QLabel
    '''

    def __init__(self, prefix = '', value='', parent=None):
        '''
            Initializes the label

            Args:
                value   str     The value for the label
                parent  QWidget The parent to attach widget to
        '''
        super().__init__(parent)
        self.prefix = prefix
        self.update(value)

    def update(self, value):
        '''
            Sets the text on the widget affixing value to prefix

            Args:
                value   int     The value to affix and display
        '''
        self.setStyleSheet("")
        self.setText(self.prefix + str(value))

    def error(self, error):
        self.setStyleSheet("background: red")
        self.setText(error)


class AmountLabel(BaseLabel):
    '''
        Amount Label extends from Base Label
    '''
    prefix = "Quantity of stock units to purchase:"

    def __init__(self, parent=None):
        '''
            Initializes the label

            Args:
                parent  QWidget The parent to attach widget to
        '''
        super().__init__(self.prefix)


class AnalysisOverviewLabel(BaseLabel):


    def __init__(self, value, parent=None):
        '''
            Initializes the label

            Args:
                value   str     The value for the label
                parent  QWidget The parent to attach widget to
        '''
        super().__init__('', value, parent)
        self.setWordWrap(True)

    @staticmethod
    def createOverviewString(
        fromDate,
        toDate,
        stockLabel=None
    ):
        return (
            "This overview is covering %s to %s and is covering the %s stock." % (
                    fromDate,
                    toDate,
                    stockLabel if stockLabel is not None else 'selected'
                )
            + " The averages are taken from the entire range of dates."
            + " Data is also provided on the most profitable date, the least profitable date."
            + " The variation data provides you some information on how voltaile the stock is."
        )


class CalendarLabel(BaseLabel):
    '''
        Calendar Label extends from QLabel
    '''
    prefix = "Date Selected:"

    def __init__(self, value, prefix=None, parent=None):
        '''
            Initializes the label

            Args:
                value   str     The value for the label
                parent  QWidget The parent to attach widget to
        '''
        self.prefix = prefix if prefix is not None else self.prefix
        super().__init__(self.prefix, value, parent)


class GraphLabel(BaseLabel):
    '''
        Graph Label
    '''
    prefix = "Graph:"

    def __init__(self, value, parent=None):
        super().__init__(self.prefix, value, parent)


class LoadingLabel(BaseLabel):
    '''
        Indicates general loading status
    '''

    def __init__(self, parent=None):
        super().__init__("Loading...")
        self.setFont(QFont('SansSerif', 30))


class CurrentLoadingLabel(BaseLabel):
    '''
        Indicates the current loading state
    '''

    prefix = "Stock Label:"

    def __init__(self, value=None, parent=None):
        '''
            Initializes the label

            Args:
                value   str     The value for the label
                parent  QWidget The parent to attach widget to
        '''
        value = value if value is not None else 'processing'
        super().__init__(self.prefix, value, parent)


class StockLabel(BaseLabel):

    prefix = "Stock Selected:"

    def __init__(self, values, parent=None):
        '''
            Initializes the label

            Args:
                value   str[]     The value for the label
                parent  QWidget The parent to attach widget to
        '''
        super().__init__(self.prefix, values, parent)

    def update(self, values):
        super().update(str(len(values)))
