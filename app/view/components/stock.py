'''
    Name:
        Stock Filter
    Description:
        Input widget handling stock filtering
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QComboBox,
    QPushButton,
    QLineEdit,
    QListWidget,
    QAbstractItemView
)


class StockClear(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('Clear Selection')


class StockFilter(QLineEdit):
    '''
        Stock Filter widget extends from QLineEdit
    '''
    onChange = pyqtSignal(str)
    onError = pyqtSignal(str)

    def __init__(self, value='', parent=None):
        '''
            Initialize the widget

            Args:
                value   str     Base value
                parent  QWidget The parent to attach the widget to
        '''
        super().__init__(value, parent)
        self.setValidator(
            QRegExpValidator(
                QRegExp(Constants.STOCK_LABEL_REGEX),
                self
            )
        )
        self.textChanged.connect(self.filterChange)
        self.setPlaceholderText('Filter Stock...')

    def filterChange(self, value):
        '''
            On filter change validate and emit custom signal

            Args:
                value   str     The value provided
        '''
        self.onChange.emit(value)


'''
    Name:
        Stock List
    Description:
        Input widget handling the selected stock
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''


class StockList(QListWidget):
    '''
        Stock list widget extends QListWidget
    '''
    onChange = pyqtSignal(object)

    def __init__(self, values, selected, parent=None):
        '''
            Initialize the widget

            Args:
                values      str[]   Base values
                selected    str[]   Any pre selected values
                parent      QWidget The parent to attach the widget to
        '''
        super().__init__(parent)
        self.addItems(values)
        # We override the selection mode to allow for multiple values to be selected
        self.setSelectionMode(
            QAbstractItemView.MultiSelection
        )
        self.itemSelectionChanged.connect(self.stockChange)

    def updateValues(self, values, clearSelected=False):
        '''
            Overwrite the list of values, retaining the current selected
        '''
        # temporary store the selected items
        selected = [item.text() for item in self.selectedItems() if not clearSelected]
        self.clear()
        # add the selected + new values
        self.addItems(selected + values)
        # update the selected items
        for i in range(len(selected)):
            self.item(i).setSelected(True)

    def stockChange(self, selected=[]):
        '''
            On the stock selection changing, get the values, and emit signal
        '''
        items = list([item.text() for item in self.selectedItems()] + selected)
        self.onChange.emit(items)


class StockSelector(QComboBox):
    '''
        Stock selector
    '''
    onChange = pyqtSignal(str)

    placeholder = 'No stock selected'

    def __init__(self, values=[], selectedIndex=0, parent=None):
        '''
            Initialize the widget

            Args:
                values      str[]   Base values
                selected    int
                parent      QWidget The parent to attach the widget to
        '''
        super().__init__(parent)
        self.values = values
        self.updateValues(values)
        self.currentIndexChanged.connect(self.stockIndexChange)

    def updateValues(self, values):
        '''
            Overwrite the list of values
        '''
        self.clear()
        if len(values) > 0:
            self.values = values
            self.addItems(values)
            self.setCurrentIndex(0)
        else:
            self.values = []
            self.addItems([self.placeholder])
        self.setCurrentIndex(0)

    def stockIndexChange(self, index):
        '''
            On the stock selection changing, get the values, and emit signal
        '''
        if self.values:
            self.onChange.emit(self.values[index])
