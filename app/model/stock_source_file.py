'''
    Name:
        Stock Source File Handler
    Description:
        A Stock Source File Handler
    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
import csv
import os
from .stock_source import StockSource


class StockSourceFile(StockSource):
    '''
        Stock source file reader
    '''
    handler = None

    def __init__(self, location):
        '''
            Instantiate the source

            Args:
                location (string) The location of the data
        '''
        super().__init__(location)
        if not os.path.exists(location):
            raise ValueError("%s doesn't exist" % location)
        self.size = os.path.getsize(location)
        self.__setHandler()
        self.isReady = True

    def genLine(self):
        '''
            Generate a new line from the resource

            Yields:
                list
        '''
        if self.handler is None:
            raise RuntimeError("Resource not open")
        for line in self.handler:
            self.currentLineSize = len(','.join(line).encode('utf-8'))
            yield line
        self.handler = None

    def getLineSize(self):
        '''
            Get the current line size

            Returns:
                int
        '''
        return self.currentLineSize

    def getResourceSize(self):
        '''
            Get the total resource size (bytes)

            Returns:
                int
        '''
        return self.size

    def __setHandler(self):
        '''
            Set the file handler on the instance for reading the data
        '''
        if self.handler is not None:
            self.handler.close()
        try:
            # TODO: validate source file mime type
            self.handler = csv.reader(
                open(
                    file=self.location,
                    mode='r',
                    encoding='utf-8'
                ),
                delimiter=',',
                quotechar='"'
            )
        except Exception:
            raise ValueError("Cannot open file: ", self.location)
