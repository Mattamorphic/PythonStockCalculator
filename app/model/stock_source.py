'''
    Stock Source
    Parent class for all stock sources

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''


class StockSource:
    '''
        Base class for the stock data sources

        Args:
            location (mixed):   The source location
    '''
    isReady = False

    def __init__(self, location=None):
        self.location = location

    def genLine(self):
        '''
            Generate a new line from the source

            Yields:
                (str)
        '''
        raise Exception("Only implemented in child classes")

    def genRow(self):
        '''
            Gen a row of data represented as headers and values

            Returns:
                (dict{str: mixed})
        '''
        if not self.isReady:
            raise RuntimeError("Can't load, no source")
        headers = [header.lower() for header in next(self.genLine())]
        for line in self.genLine():
            yield dict(zip(headers, line))

    def getLineSize(self):
        '''
            Getter for line size, should be overridden by child classes

            Returns:
                (int)
        '''
        return 0

    def getResourceSize(self):
        '''
            Getter for resource size, should be overridden by child classes

            Returns:
                (int)
        '''
        return 0
