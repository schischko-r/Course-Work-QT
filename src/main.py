import sys
from PyQt5 import QtWidgets
from PyQt5 import Qt

from MainWin import *
from ConfigWin import *

import configparser
import datetime
import glob
import os


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
