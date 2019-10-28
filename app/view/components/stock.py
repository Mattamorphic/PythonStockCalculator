'''
    Stock Selector Components
    All the widgets for handling stock selection

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QComboBox, QPushButton, QLineEdit, QListWidget,
                             QAbstractItemView)


class StockClear(QPushButton):
    '''
        Small button wrapper for a clear selectiton button
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('Clear Selection')


class StockFilter(QLineEdit):
    '''
        Stock Filter widget extends from QLineEdit

        Args:
            value   (str):     Base value
            parent  (QWidget): The parent to attach the widget to
    '''
    onChange = pyqtSignal(str)
    onError = pyqtSignal(str)

    def __init__(self, value: str = '', parent=None):
        super().__init__(value, parent)
        self.setValidator(
            QRegExpValidator(QRegExp(Constants.STOCK_LABEL_REGEX), self))
        self.textChanged.connect(self.filterChange)
        self.setPlaceholderText('Filter Stock...')

    def filterChange(self, value: str):
        '''
            On filter change validate and emit custom signal

            Args:
                value (str): The value provided
        '''
        self.onChange.emit(value)


class StockList(QListWidget):
    '''
        Stock list widget extends QListWidget

        Args:
            values (List[str]):     Base values
            selected (List[str]):   Any pre selected values
            parent (QWidget):       The parent to attach the widget to
    '''
    onChange = pyqtSignal(object)

    def __init__(self, values, selected, parent=None):
        super().__init__(parent)
        self.addItems(values)
        # We override the selection mode to allow for multiple values to be selected
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.itemSelectionChanged.connect(self.stockChange)

    def updateValues(self, values, clearSelected: bool = False):
        '''
            Overwrite the list of values, retaining the current selected

            Args:
                values          (List[str]):    Update values
                clearSelected   bool:           Allow busting the selected options
        '''
        # temporary store the selected items
        selected = [
            item.text() for item in self.selectedItems() if not clearSelected
        ]
        self.clear()
        # add the selected + new values
        self.addItems(selected + values)
        # update the selected items
        for i in range(len(selected)):
            self.item(i).setSelected(True)

    def stockChange(self, selected=[]):
        '''
            On the stock selection changing, get the values, and emit signal

            Args:
                selected (List[str]): The selected options
        '''
        items = list([item.text() for item in self.selectedItems()] + selected)
        self.onChange.emit(items)


class StockSelector(QComboBox):
    '''
        Stock selector

        Args:
            values      (List[str]):   Base values
            selected    (int)
    '''
    onChange = pyqtSignal(str)

    placeholder = 'No stock selected'

    def __init__(self, values=[], selectedIndex: int = 0, parent=None):
        super().__init__(parent)
        self.values = values
        self.updateValues(values)
        self.currentIndexChanged.connect(self.stockIndexChange)

    def updateValues(self, values):
        '''
            Overwrite the list of values

            Args:
                values (List[str]): Update values
        '''
        self.clear()
        if values:
            self.values = values
            self.addItems(values)
        else:
            self.values = []
            self.addItems([self.placeholder])
        self.setCurrentIndex(0)

    def stockIndexChange(self, index: int):
        '''
            On the stock selection changing, get the values, and emit signal

            Args:
                index (int): New index
        '''
        if self.values:
            self.onChange.emit(self.values[index])
