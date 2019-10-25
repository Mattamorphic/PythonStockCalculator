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
            value (mixed):     A value
            isReadOnly (bool): Can this value be modified?
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
