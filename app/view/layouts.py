'''
    Name:
        Layouts for our views
    Description:
        Each of the layouts extend from the base layouts
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QBoxLayout,
    QHBoxLayout,
    QLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)


class BaseGroupedLayout(QBoxLayout):

    def __init__(self, direction, parent=None):
        super().__init__(direction, parent)
        self.groups = []
        self.groupIndex = 0
        self.currentGroupIndex = 0
        self.currentGroup = None

    def addToCurrentGroup(self, *components):

        for component in components:
            # add widget is only available on a layout that we have added to the QGroupBox
            if isinstance(component, QWidget):
                self.groups[self.groupIndex].addWidget(component)
            elif isinstance(component, QLayout):
                self.groups[self.groupIndex].addLayout(component)

    def addToExistingGroup(self, index, component):
        if self.groups[index]:
            self.groups[index].addWidget(component)
        else:
            raise IndexError("Group at index is not set")


    def createGroup(self, layout, label=None, sizePolicy=None):
        self.currentGroup = QGroupBox(label)
        if sizePolicy:
            self.currentGroup.setSizePolicy(*sizePolicy)
        self.groups.append(layout)

    def finishGroup(self):
        self.currentGroup.setLayout(self.groups[self.groupIndex])
        self.addWidget(self.currentGroup)
        self.currentGroup = None
        self.groupIndex += 1

    def createVerticalGroup(self, label=None, sizePolicy=None, align=None):
        layout = self.getVerticalLayout()
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getVerticalLayout(), label, sizePolicy)

    def createHorizontalGroup(self, label=None, sizePolicy=None, align=None):
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getHorizontalLayout(), label, sizePolicy)

    def getFormLayout(self):
        return QFormLayout()

    def getHorizontalLayout(self):
        return QHBoxLayout()

    def getVerticalLayout(self):
        return QVBoxLayout()

    def setLayoutOfCurrentGroup(self, layout):
        self.groups[self.groupIndex].addLayout(layout)

class BaseRowGroupedLayout(BaseGroupedLayout):
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.TopToBottom, parent)


class BaseColumnGroupedLayout(BaseGroupedLayout):
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.LeftToRight, parent)



class AmountLayout(BaseRowGroupedLayout):
    def __init__(self, label, amount, parent=None):
        super().__init__(parent)
        self.createVerticalGroup(None, (QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout = self.getFormLayout()
        layout.addRow(label, amount)
        self.addToCurrentGroup(layout)
        self.finishGroup()


class AnalysisLayout(BaseRowGroupedLayout):
    def __init__(
        self,
        stockSelector,
        overview,
        averageValues,
        # highestValues,
        # lowestValues,
        # variationValues,
        parent=None
    ):
        super().__init__(parent)
        autoWidthFixedHeight = (QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.createVerticalGroup("Stock Selector", autoWidthFixedHeight)
        self.addToCurrentGroup(stockSelector)
        self.finishGroup()
        self.createVerticalGroup("Overview", autoWidthFixedHeight)
        self.addToCurrentGroup(overview)
        self.finishGroup()
        self.createVerticalGroup("Analysis", autoWidthFixedHeight)
        self.addToCurrentGroup(averageValues)
        self.finishGroup()
        self.setStretch(2, 0)


class CalendarLayout(BaseRowGroupedLayout):

    def __init__(self, name, label, calendar, parent=None):
        super().__init__(parent)
        self.createVerticalGroup(name, (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(label, calendar)
        self.finishGroup()


class GraphLayout(BaseRowGroupedLayout):
    def __init__(self, options, label, graph, parent=None):
        super().__init__()
        self.createHorizontalGroup("Graph Options", (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(*options.getOptions())
        self.finishGroup()
        self.createVerticalGroup("Graph", (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(label, graph)
        self.finishGroup()


class LoadingLayout(BaseRowGroupedLayout):

    def __init__(
        self,
        label,
        currentLoading,
        progress,
        parent=None
    ):
        super().__init__(parent)
        self.addWidget(label)
        self.createVerticalGroup(None, (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(currentLoading, progress)
        self.finishGroup()


class ProfitLayout(BaseRowGroupedLayout):
    def __init__(
        self,
        stockSelector,
        profitValue,
        parent=None
    ):
        super().__init__(parent)
        autoWidthFixedHeight = (QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.createVerticalGroup("Stock Selector", autoWidthFixedHeight, Qt.AlignTop)
        self.addToCurrentGroup(stockSelector)
        self.finishGroup()
        self.createVerticalGroup("Profits", autoWidthFixedHeight, Qt.AlignTop)
        self.addToCurrentGroup(profitValue)
        self.finishGroup()
        self.setAlignment(Qt.AlignTop)


class StockLayout(BaseRowGroupedLayout):

    def __init__(
        self,
        label,
        stockClear,
        stockFilter,
        stockList,
        parent=None
    ):
        super().__init__(parent)
        self.createVerticalGroup("Stock to purchase", (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(
            stockFilter,
            stockClear,
            label,
            stockList
        )
        self.finishGroup()
