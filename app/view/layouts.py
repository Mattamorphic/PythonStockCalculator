from PyQt5.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout
)

class BaseGroupedLayout(QBoxLayout):

    def __init__(self, direction, parent=None):
        super().__init__(direction, parent)
        self.groups = []
        # Optimization - saves additional conditional check in create group
        self.groupIndex = -1

    def addToCurrentGroup(self, component):
        self.groups[self.groupIndex].addWidget(component)

    def addToExistingGroup(self, index, component):
        if self.groups[index]:
            self.groups[index].addWidget(component)
        else:
            raise IndexError("Group at index is not set")


    def createGroup(self, label=None, sizePolicy=None):
        group = QGroupBox(label)
        if sizePolicy:
            group.setSizePolicy(*sizePolicy)
        self.groups.append(group)
        self.addWidget(group)
        self.groupIndex += 1

    def getFormLayout(self):
        return QFormLayout()

    def getHorizontalLayout(self):
        return QHBoxLayout()

    def getVerticalLayout(self):
        return QVBoxLayout()

    def setLayoutOfCurrentGroup(self, layout):
        self.groups[self.groupIndex].setLayout(layout)

class BaseRowGroupedLayout(BaseGroupedLayout):
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.TopToBottom, parent)


class BaseColumnGroupedLayout(BaseGroupedLayout):
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.LeftToRight, parent)



class AmountLayout(BaseRowGroupedLayout):
    def __init__(self, label, amount, parent=None):
        super().__init__(parent)
        self.createGroup(None, (QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout = self.getFormLayout()
        layout.addRow(label, amount)
        self.setLayoutOfCurrentGroup(layout)


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
        self.createGroup("Stock Selector", autoWidthFixedHeight)
        self.addToCurrentGroup(stockSelector)
        self.createGroup("Overview", autoWidthFixedHeight)
        self.addToCurrentGroup(overview)
        self.addLayout(averageValues)


class CalendarLayout(BaseRowGroupedLayout):

    def __init__(self, name, label, calendar, parent=None):
        super().__init__(parent)
        self.createGroup(name, (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(label, calendar)


class GraphLayout(BaseRowGroupedLayout):
    def __init__(self, options, label, graph, parent=None):
        super().__init__()
        self.createGroup("Graph Options", (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(*options)
        self.createGroup("Graph", (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(label, graph)



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
        self.createGroup("Progress", (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(currentLoading, progress)


class ProfitLayout(QVBoxLayout):
    def __init__(
        self,
        stockSelector,
        profitValue,
        parent=None
    ):
        super().__init__(parent)
        autoWidthFixedHeight = (QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.createGroup("Stock Selector", autoWidthFixedHeight)
        self.addToCurrentGroup(stockSelector)
        self.addLayout(profitValue)
        self.addStretch(0)


class StockLayout(QVBoxLayout):

    def __init__(
        self,
        label,
        stockClear,
        stockFilter,
        stockList,
        parent=None
    ):
        super().__init__(parent)
        self.createGroup("Stock to purchase", (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(
            label,
            stockClear,
            stockFilter,
            stockList
        )
