from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QHBoxLayout,
        QSizePolicy,
)


class ValueData(QHBoxLayout):

    def __init__(self, label=None, parent=None):
        super().__init__(parent)
        self.groups = []
        self.groupIndex = 0
        self.addColumn(label)

    def addColumn(self, label=None):
        group = QGroupBox(label)
        innerGroup = QFormLayout()
        innerGroup.setAlignment(Qt.AlignTop)
        group.setLayout(innerGroup)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(group)
        self.groups.append(innerGroup)
        self.groupIndex = len(self.groups) - 1


    def addRow(self, name, value):
        value = Value(str(value))
        self.groups[self.groupIndex].addRow(
            name + " " if name[-1] != ' ' else name,
            value
        )
        value.setReadOnly(True)
        return value

    def done(self):
        self.addStretch(0)
        return self


class Value(QLineEdit):
    def __init__(self, value, isReadOnly=True, parent=None):
        super().__init__(str(value), parent)
        self.setReadOnly(isReadOnly)

    def updateValue(self, value):
        self.setText(str(value))
