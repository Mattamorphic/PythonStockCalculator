'''
    Stock Calculator Entry Point
    Author: Matthew Barber<mfmbarber@gmail.com>
'''

import sys

from app.app import App
from app.model.stock_source_file import StockSourceFile
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # TODO : Read the stock path from the console, or from a config file
    ex = App(StockSourceFile('all_stocks_5yr.csv'))
    sys.exit(app.exec_())
