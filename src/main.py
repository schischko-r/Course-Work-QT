import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import Qt

from MainWin import MainWindow

import configparser
import datetime
import glob
import os


def main():
    # ЗАПУСК ОСНОВНОГО ОКНА
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
