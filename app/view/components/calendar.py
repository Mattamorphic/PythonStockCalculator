'''
    Calendar
    Input widget handling dates

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import (pyqtSignal, QDate)
from PyQt5.QtWidgets import QCalendarWidget


class Calendar(QCalendarWidget):
    '''
        Date widget extends from QCalendarWidget
        Args:
            date (str):         Base value
            earliest (str):     Earliest date
            latest (str):       Latest date
            parent (QWidget):   The parent to attach the widget to
    '''

    onChange = pyqtSignal(str)

    def __init__(self, date: str, earliest=None, latest=None, parent=None):
        super().__init__(parent)
        self.setSelectedDate(Calendar.getQDate(date))
        if earliest is not None:
            self.setMinimumDate(earliest)
        if latest is not None:
            self.setMaximumDate(latest)
        self.clicked[QDate].connect(self.calendarChange)

    def calendarChange(self, date):
        '''
            On calendar change validate and emit custom signal

            Args:
                date (QDate): The date clicked
        '''
        # TODO: Validate payload
        dateString = date.toString(Constants.DATE_FORMAT)
        self.onChange.emit(dateString)

    def setMinimumDate(self, date: str):
        '''
            Set the minimum date on the calendar

            Args:
                date (str): Date string in yyyy-mm-dd format
        '''
        super().setMinimumDate(Calendar.getQDate(date))

    def setMaximumDate(self, date: str):
        '''
            Set the maximum date on the calendar

            Args:
                date (str): Date string in yyyy-mm-dd format
        '''
        super().setMaximumDate(Calendar.getQDate(date))

    @staticmethod
    def getQDate(date: str):
        '''
            A static helper method tto convert a string to QDate

            Args:
                date (str): Date string in yyyy-mm-dd format
        '''
        return QDate.fromString(date, Constants.DATE_FORMAT)
