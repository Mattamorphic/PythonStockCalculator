'''
    Value Data
    Render key value pair data

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
)


class ValueData(QHBoxLayout):
    '''
        ValueData

        Args:
            Label (str): A label for the group of data
    '''
    def __init__(self, label=None, parent=None):
        super().__init__(parent)
        self.groups = []
        self.groupIndex = 0
        self.addColumn(label)

    def addColumn(self, label=None):
        '''
            Add a column of data

            Args:
                label (str): The label to add to this column
        '''
        group = QGroupBox(label)
        innerGroup = QFormLayout()
        innerGroup.setAlignment(Qt.AlignTop)
        group.setLayout(innerGroup)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(group)
        self.groups.append(innerGroup)
        self.groupIndex = len(self.groups) - 1

    def addRow(self, name: str, value):
        '''
            Add a row to the current column, with a name and value

            Args:
                name    (str): A name for this row as a label
                value   (mixed): A value for this data
        '''
        value = Value(str(value))
        self.groups[self.groupIndex].addRow(
            name + " " if name[-1] != ' ' else name, value)
        value.setReadOnly(True)
        return value

    def done(self):
        '''
            A final method, that removes the whitespace
        '''
        self.addStretch(0)
        return self


class Value(QLineEdit):
    '''
        Helper method to gracefully wrap value

        Args:
            value (mixed):      A value
            isReadOnly (bool):  Can this value be modified?
    '''
    def __init__(self, value, isReadOnly: bool = True, parent=None):
        super().__init__(str(value), parent)
        self.setReadOnly(isReadOnly)

    def updateValue(self, value):
        '''
            Update the value

            Args:
                value (mixed): The value to update with
        '''
        self.setText(str(value))


class BaseValue:
    '''
        Base class for custom values

        Args:
            value (mixed): The value
    '''
    typeCheckers = []

    def __init__(self, value):
        self.value = value

    def isValueValid(self):
        '''
            Validate the value against the type checkers

            Returns:
                (bool)
        '''
        return any([check(self.value) for check in self.typeCheckers])


class CurrencyValue(BaseValue):
    '''
        Currency value class

        Args:
            symbol (str): Currency symbol
            value (float/int): The currency value
    '''

    # Numerical type checkers
    typeCheckers = [
        lambda v: isinstance(v, int), lambda v: isinstance(v, float)
    ]

    def __init__(self, symbol, value):
        super().__init__(value)
        self.symbol = symbol

    def __str__(self):
        '''
            Magic method (for str(...) calls)

            Returns:
                (str)
        '''
        if not self.isValueValid():
            return str(self.value)
        return self.symbol + str("{:,}".format(round(float(self.value), 2)))


class PercentageValue(BaseValue):
    '''
        Percentage value class

        Args:
            value (float/int): The Percentage value
    '''
    typeCheckers = [
        lambda v: isinstance(v, int), lambda v: isinstance(v, float)
    ]
    symbol = '%'

    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        '''
            Magic method (for str(...) calls)

            Returns:
                (str)
        '''
        if not self.isValueValid():
            return str(self.value)
        return str(self.value) + self.symbol
