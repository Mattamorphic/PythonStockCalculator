'''
    Stock Node Data Module
    A module holding classes for dealing with stock nodes

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from datetime import datetime, timedelta


class StockNode:
    '''
        A stock node represents a stock
    '''
    def __init__(self, label):
        self.data = {}
        self.label = label

    def getLabel(self):
        '''
            Return the label for the stock

            Returns:
                str
        '''
        return self.label

    def addData(self, date: str, stock_value):
        '''
            Add data to the stock node

            Args:
                date        (str):          The date for the data
                stock_value (StockValue):   The StockValue for the data
        '''
        if date not in self.data:
            self.data[date] = stock_value
        else:
            raise ValueError("No two entries can exist for the same date")

    def getValueForDate(self, date: str):
        '''
            Return a stock value for a specific date

            Args:
                date (str): The date to return the value for

            Returns:
                StockValue || None
        '''
        if date in self.data:
            return self.data[date]
        return None

    def getAverageValues(self, fromDate: str, toDate: str):
        '''
            Calculate the average values between two dates

            Args:
                fromDate    (str):  The from (buy) date
                toDate      (str):  The to (sell) date

            Returns:
                StockValue
        '''
        currentDate = datetime.strptime(fromDate, Constants.PY_DATE_FORMAT)
        endDate = datetime.strptime(toDate, Constants.PY_DATE_FORMAT)
        # Create a time delta to iterate with
        delta = timedelta(days=1)
        totalCount = 0
        open = 0.0
        high = 0.0
        low = 0.0
        close = 0.0

        while currentDate < endDate:
            node = self.getValueForDate(
                currentDate.strftime(Constants.PY_DATE_FORMAT))
            if node is not None:
                totalCount += 1
                open += node.getOpeningValue()
                high += node.getHighValue()
                low += node.getLowValue()
                close = node.getCloseValue()
            currentDate += delta
        return StockValue(round(open / totalCount, 2),
                          round(high / totalCount, 2),
                          round(low / totalCount, 2),
                          round(close / totalCount, 2))

    def getProfitValue(self, amount, fromDate, toDate):
        buyValue = self.getValueForDate(fromDate)
        sellValue = self.getValueForDate(toDate)
        if buyValue is None or sellValue is None:
            return None

        return StockProfit(amount, buyValue, sellValue)


class StockValue:
    '''
        Stock value represents the value for a stock on a given day

        Args:
            open    (float): The opening price on the given date
            high    (float): The high price on the given date
            low     (float): The low price on the given date
            close   (float): The close price on the given date
    '''
    def __init__(self, open: float, high: float, low: float, close: float):
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def getCloseValue(self):
        '''
            Getter for close value

            Returns:
                (float)
        '''
        return self.close

    def getHighValue(self):
        '''
            Getter for high value

            Returns:
                (float)
        '''
        return self.high

    def getLowValue(self):
        '''
            Getter for low value

            Returns:
                (float)
        '''
        return self.low

    def getOpeningValue(self):
        '''
            Getter for opening value

            Returns:
                (float)
        '''
        return self.open

    def getDayDiff(self):
        '''
            Determine the difference between the close and open

            Returns:
                (float)
        '''
        return self.close - self.open

    def getHighLowDiff(self):
        '''
            Determine the difference between the high and low

            Returns:
                (float)
        '''
        return self.high - self.low


def profitPreNoneCheck(func):
    '''
        Decorator for stock profit methods, as they have this preflight check

        Args:
            func   (class method)   The class method to trigger

        Returns:
            func
    '''
    def decorator(self, *args, **kwargs):
        '''
            Decorator function (with instance)

            Args:
                self        (self):     A class instance
                *args       (args):     Unnamed args
                **kwargs    (kwargs):   Keyed args

            Returns:
                (float)
        '''
        if self.buy is None or self.sell is None:
            return 0.0
        return func(self, *args, **kwargs)

    return decorator


class StockProfit:
    '''
        Stock profit class, used for profit related calculations
    '''
    def __init__(self, amount: int, buyValue=None, sellValue=None):
        '''
            Initialize the StockProfit class

            Args:
                amount      (int):           The amount of stock
                buyValue    (StockValue):    The stock value on buy date
                sellValue   (StockValue):    The stock value on sell date
        '''
        self.multiplier = amount
        self.buy = buyValue
        self.sell = sellValue

    @profitPreNoneCheck
    def getLowestMargin(self):
        '''
            Returns the lowest profit

            Returns:
                (float)
        '''
        return round((self.sell.getLowValue() - self.buy.getHighValue()) *
                     (self.multiplier / 1.0), 2)

    @profitPreNoneCheck
    def getHighestMargin(self):
        '''
            Returns the highest profit

            Returns:
                (float)
        '''
        return round((self.sell.getHighValue() - self.buy.getLowValue()) *
                     (self.multiplier / 1.0), 2)

    @profitPreNoneCheck
    def getAverageMargin(self):
        '''
            Get the average profit

            Returns:
                (float)
        '''
        return round((self.getHighestMargin() + self.getLowestMargin()) / 2, 2)

    @profitPreNoneCheck
    def getLowestBuyPrice(self):
        '''
            Returns the lowest buy price

            Returns:
                (float)
        '''
        return round(self.buy.getLowValue() * self.multiplier, 2)

    @profitPreNoneCheck
    def getHighestBuyPrice(self):
        '''
            Returns the highest buy price

            Returns:
                (float)
        '''
        return round(self.buy.getHighValue() * self.multiplier, 2)

    @profitPreNoneCheck
    def getAverageBuyPrice(self):
        '''
            Returns the average buy price
        '''
        return round(
            (self.getHighestBuyPrice() + self.getLowestBuyPrice()) / 2)

    @profitPreNoneCheck
    def getLowestSellPrice(self):
        '''
            Returns the lowest sell price

            Returns:
                (float)
        '''
        return round(self.sell.getLowValue() * self.multiplier, 2)

    @profitPreNoneCheck
    def getHighestSellPrice(self):
        '''
            Returns the highest sell price

            Returns:
                (float)
        '''
        return round(self.sell.getHighValue() * self.multiplier, 2)

    @profitPreNoneCheck
    def getAverageSellPrice(self):
        '''
            Returns the average sell price
        '''
        return round(
            (self.getHighestSellPrice() + self.getLowestSellPrice()) / 2)
