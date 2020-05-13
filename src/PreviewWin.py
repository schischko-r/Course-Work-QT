import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import Qt
from designer import PreviewDesigner

import csv


class PreviewWin(QtWidgets.QDialog, PreviewDesigner.Ui_Dialog):
    def __init__(self,  initName="", parent=None):
        super(PreviewWin, self).__init__()
        self.setupUi(self)
        self.initName = initName
        self.populateExport()

    def populateExport(self):
        with open(self.initName, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            try:
                for row in reader:
                    item = QtWidgets.QTreeWidgetItem(self.treeWidget)
                    values = (row['name'], row['msg'], row['time'],
                              row['link'], row['length'], row['expmsg'])
                    for i in range(len(values)):
                        item.setText(i, values[i])
            except:
                for row in reader:
                    item = QtWidgets.QTreeWidgetItem(self.treeWidget)
                    values = (row['name'], row['msg'], row['time'],
                              row['link'], row['length'], "")
                    for i in range(len(values)):
                        item.setText(i, values[i])
        for i in range(self.treeWidget.columnCount()):
            self.treeWidget.resizeColumnToContents(i)
