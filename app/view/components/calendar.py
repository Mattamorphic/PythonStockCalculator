'''
    Name:
        Calendar
    Description:
        Input widget handling date strings
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import (pyqtSignal, QDate)
from PyQt5.QtWidgets import QCalendarWidget


class Calendar(QCalendarWidget):
    '''
        Date widget extends from QCalendarWidget
    '''

    onChange = pyqtSignal(str)

    def __init__(self, date, earliest=None, latest=None, parent=None):
        '''
            Initialize the widget

            Args:
                date   string     Base value
                parent  QWidget The parent to attach the widget to
        '''
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
                date QDate  The date clicked
        '''
        # TODO: Validate payload
        dateString = date.toString(Constants.DATE_FORMAT)
        self.onChange.emit(dateString)

    def setMinimumDate(self, date):
        super().setMinimumDate(Calendar.getQDate(date))

    def setMaximumDate(self, date):
        super().setMaximumDate(Calendar.getQDate(date))

    @staticmethod
    def getQDate(date):
        '''
            A static helper method tto convert a string to QDate

            Args:
                date    str     format 'yyyy-mm-dd'
        '''
        return QDate.fromString(date, Constants.DATE_FORMAT)
