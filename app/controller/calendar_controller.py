'''
    Name:
        Calendar Controller
    Description:
        Controller for the returned calendar widget
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''

from app.view.components.calendar import Calendar
from app.view.components.labels import CalendarLabel
from app.view.layouts import CalendarLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class CalendarController(QWidget):
    '''
        Calendar controller handles delivering and monitoring a calendar widget
    '''
    update = pyqtSignal(str)

    def __init__(self, date, earliest=None, latest=None, name=None):
        '''
            Initialize the calendar component with an initial value

            Args:
                date        string  Initial Date in yyyy-mm-dd format
                earliest    string  Earliest Date in yyyy-mm-dd format
                latest      string  Latest Date in yyyy-mm-dd format
        '''
        super().__init__()
        # TODO : Add parameter validation
        self.date = date
        self.earliest = earliest
        self.latest = latest
        self.initUI(name)

    def initUI(self, name):
        '''
            Initializes the UI widgets for the calendar component view
        '''
        self.calendarComponent = Calendar(self.date, self.earliest, self.latest)
        self.calendarComponent.onChange.connect(self.updateDate)
        self.labelComponent = CalendarLabel(self.date)
        self.setLayout(CalendarLayout(
            name,
            self.labelComponent,
            self.calendarComponent
        ))

    def updateDate(self, date):
        '''
            Initialize the UI widget for the controller (the view)

            Args:
                date    string      Date in  yyyy-mm-dd format
        '''
        self.labelComponent.update(date)
        self.update.emit(date)

    def setEarliestDate(self, date):
        '''
            Set the earliest date for the calendar

            Args:
                date    string      Date in yyyy-mm-dd format
        '''
        self.earliest = date
        self.calendarComponent.setMinimumDate(date)

    def setLatestDate(self, date):
        '''
            Set the latest date for the calendar

            Args:
                date    string      Date in yyyy-mm-dd format
        '''
        self.latest = date
        self.calendarComponent.setMaximumDate(date)

    def getDate(self):
        '''
            Getter for the date instance variable value

            Returns:
                string
        '''
        return self.date
