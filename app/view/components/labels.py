'''
    Custom Labels
    Module containing all of the custom labels

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class BaseLabel(QLabel):
    '''
        Base Label extends from QLabel

        Args:
            value  (str):     The value for the label
            parent (QWidget): The parent to attach widget to
    '''
    def __init__(self, prefix: str = '', value: str = '', parent=None):
        super().__init__(parent)
        self.prefix = prefix
        self.update(value)

    def update(self, value):
        '''
            Sets the text on the widget affixing value to prefix

            Args:
                value (mixed): The value to affix and display
        '''
        self.setStyleSheet("")
        self.setText(self.prefix + str(value))

    def error(self, error):
        '''
            Turn label red

            Args:
                error (str): The error message
        '''
        self.setStyleSheet("background: red")
        self.setText(error)


class AmountLabel(BaseLabel):
    '''
        Amount Label extends from Base Label
    '''
    prefix = "Quantity of stock units to purchase:"

    def __init__(self, parent=None):
        super().__init__(self.prefix)


class AnalysisOverviewLabel(BaseLabel):
    '''
        AnalysisOverviewLabel

        Args:
            value (str): The value for the label
    '''
    def __init__(self, value: str, parent=None):
        super().__init__('', value, parent)
        self.setWordWrap(True)

    @staticmethod
    def createOverviewString(fromDate: str, toDate: str, stockLabel=None):
        '''
            Helper method to generate an analysis overview

            Args:
                fromDate    (str): A string in yyyy-mm-dd format
                toDate      (str): A string in yyyy-mm-dd format

            Returns:
                str
        '''
        return (
            "This overview is covering %s to %s and is covering the %s stock."
            % (fromDate, toDate, stockLabel if stockLabel else 'selected') +
            " The averages are taken from the entire range of dates." +
            " Data is also provided on the most profitable date, the least profitable date."
            +
            " The variation data provides you some information on how voltaile the stock is."
        )


class CalendarLabel(BaseLabel):
    '''
        Calendar Label extends from BaseLabel

        Args:
            value (str): The value for the label
    '''
    prefix = "Date Selected:"

    def __init__(self, value, prefix=None, parent=None):
        self.prefix = prefix if prefix is not None else self.prefix
        super().__init__(self.prefix, value, parent)


class GraphLabel(BaseLabel):
    '''
        Graph Label

        Args:
            value (str): The value for the label
    '''
    prefix = "Graph:"

    def __init__(self, value: str, parent=None):
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

        Args:
            value (str): The value for the label
    '''

    prefix = "Stock Label:"

    def __init__(self, value=None, parent=None):
        value = value if value else 'processing'
        super().__init__(self.prefix, value, parent)


class StockLabel(BaseLabel):
    '''
        Stock selected label

        Args:
            value (List[str]): The value for the label
    '''
    prefix = "Stock Selected:"

    def __init__(self, values, parent=None):
        super().__init__(self.prefix, values, parent)

    def update(self, values):
        '''
            Update the set of values

            Args:
                values (List[str]): The stock labels
        '''
        super().update(str(len(values)))
