'''
    Layouts for our views
    Each of the layouts extend from the base layouts

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFormLayout, QGroupBox, QBoxLayout, QHBoxLayout,
                             QLayout, QSizePolicy, QVBoxLayout, QWidget)


class BaseGroupedLayout(QBoxLayout):
    '''
        Base grouped layout for widgets as we tend to use groupings

        Args:
            direction (QBoxLayout.DIRECTION): The direction for the layout
    '''
    def __init__(self, direction, parent=None):
        super().__init__(direction, parent)
        self.groups = []
        self.groupIndex = 0
        self.currentGroupIndex = 0
        self.currentGroup = None

    def addToCurrentGroup(self, *components):
        '''
            Used to add components to the current group

            Args:
                components (iterable): Widgets/layouts to add to the group
        '''

        for component in components:
            # add widget is only available on a layout that we have added to the QGroupBox
            if isinstance(component, QWidget):
                self.groups[self.groupIndex].addWidget(component)
            elif isinstance(component, QLayout):
                self.groups[self.groupIndex].addLayout(component)

    def addToExistingGroup(self, index: int, component):
        '''
            Add a component to a different group

            Args:
                index (int):                    The existing group index
                component (QWidget/QLayout):    The component to aadd
        '''
        if index not in self.groups:
            raise IndexError("Group at index is not set")
        if isinstance(component, QWidget):
            self.groups[index].addWidget(component)
        elif isinstance(component, QLayout):
            self.groups[index].addLayout(component)

    def createGroup(self, layout, label=None, sizePolicy=None):
        '''
            Create a new group with a specific layout

            Args:
                layout (QBoxLayout):    A layout to use
                label (str):            A label for the group
                sizePolicy (tuple):     QSizePolicy for horizontal and vertical
        '''
        self.currentGroup = QGroupBox(label)
        if sizePolicy:
            self.currentGroup.setSizePolicy(*sizePolicy)
        self.groups.append(layout)

    def finishGroup(self):
        '''
            A finish method to build the layout
        '''
        self.currentGroup.setLayout(self.groups[self.groupIndex])
        self.addWidget(self.currentGroup)
        self.currentGroup = None
        self.groupIndex += 1

    def createVerticalGroup(self, label=None, sizePolicy=None, align=None):
        '''
            Create a new group with a vertical layout

            Args:
                label (str):         A label for the group
                sizePolicy (tuple):  QSizePolicy for horizontal and vertical
                align (QtAlign):     Align the contents
        '''
        layout = self.getVerticalLayout()
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getVerticalLayout(), label, sizePolicy)

    def createHorizontalGroup(self, label=None, sizePolicy=None, align=None):
        '''
            Create a new group with a horizontal layout

            Args:
                label (str):         A label for the group
                sizePolicy (tuple):  QSizePolicy for horizontal and vertical
                align (QtAlign):     Align the contents
        '''
        layout = self.getHorizontalLayout()
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getHorizontalLayout(), label, sizePolicy)

    def getFormLayout(self):
        '''
            Helper to create a new form layout

            Returns:
                (QFormLayout)
        '''
        return QFormLayout()

    def getHorizontalLayout(self):
        '''
            Helper to create a new horizontal layout

            Returns:
                (QHBoxLayout)
        '''
        return QHBoxLayout()

    def getVerticalLayout(self):
        '''
            Helper to create a new vertical layout

            Returns:
                (QVBoxLayout)
        '''
        return QVBoxLayout()

    def setLayoutOfCurrentGroup(self, layout):
        '''
            Helper to set the layout of the current group

            Args:
                layout (QBoxLayout): The Layout to set
        '''
        self.groups[self.groupIndex].addLayout(layout)


class BaseRowGroupedLayout(BaseGroupedLayout):
    '''
        Wrapper for BaseGroupedLayout
    '''
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.TopToBottom, parent)


class BaseColumnGroupedLayout(BaseGroupedLayout):
    '''
        Wrapper for BaseGroupedLayout
    '''
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.LeftToRight, parent)


class AmountLayout(BaseRowGroupedLayout):
    '''
        Amount controller layout
    '''
    def __init__(self, label, amount, parent=None):
        super().__init__(parent)
        self.createVerticalGroup(None,
                                 (QSizePolicy.Expanding, QSizePolicy.Fixed))
        layout = self.getFormLayout()
        layout.addRow(label, amount)
        self.addToCurrentGroup(layout)
        self.finishGroup()


class AnalysisLayout(BaseRowGroupedLayout):
    '''
        Analysis controller layout
    '''
    def __init__(self, stockSelector, overview, averageValues, parent=None):
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
    '''
        Calendar controller layout
    '''
    def __init__(self, name, label, calendar, parent=None):
        super().__init__(parent)
        self.createVerticalGroup(name,
                                 (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(label, calendar)
        self.finishGroup()


class GraphLayout(BaseRowGroupedLayout):
    '''
        Graph controller layout
    '''
    def __init__(self, options, label, graph, parent=None):
        super().__init__()
        self.createHorizontalGroup("Graph Options",
                                   (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(*options.getOptions())
        self.finishGroup()
        self.createVerticalGroup(
            "Graph", (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(label, graph)
        self.finishGroup()


class LoadingLayout(BaseRowGroupedLayout):
    '''
        Loading controller layout
    '''
    def __init__(self, label, currentLoading, progress, parent=None):
        super().__init__(parent)
        self.addWidget(label)
        self.createVerticalGroup(None,
                                 (QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.addToCurrentGroup(currentLoading, progress)
        self.finishGroup()


class ProfitLayout(BaseRowGroupedLayout):
    '''
        Profit controller layout
    '''
    def __init__(self, stockSelector, profitValue, parent=None):
        super().__init__(parent)
        autoWidthFixedHeight = (QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.createVerticalGroup("Stock Selector", autoWidthFixedHeight,
                                 Qt.AlignTop)
        self.addToCurrentGroup(stockSelector)
        self.finishGroup()
        self.createVerticalGroup("Profits", autoWidthFixedHeight, Qt.AlignTop)
        self.addToCurrentGroup(profitValue)
        self.finishGroup()
        self.setAlignment(Qt.AlignTop)


class StockLayout(BaseRowGroupedLayout):
    '''
        Stock controller layout
    '''
    def __init__(self, label, stockClear, stockFilter, stockList, parent=None):
        super().__init__(parent)
        self.createVerticalGroup(
            "Stock to purchase",
            (QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.addToCurrentGroup(stockFilter, stockClear, label, stockList)
        self.finishGroup()
