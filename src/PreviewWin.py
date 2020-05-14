import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import Qt
from designer import PreviewDesigner

import csv
import subprocess


class PreviewWin(QtWidgets.QDialog, PreviewDesigner.Ui_Dialog):
    def __init__(self,  initName="", parent=None):
        super(PreviewWin, self).__init__()
        self.setupUi(self)
        self.initName = initName
        self.populateExport()
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.tableWidget.itemDoubleClicked.connect(self.copy)

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

    def onItemClicked(self, it, col):
        self.tableWidget.clearContents()
        for i in range(self.tableWidget.rowCount() + 1):
            self.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(it.text(i)))

        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def copy(self, it):
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(it.text(), mode=cb.Clipboard)
        QtWidgets.QMessageBox.about(
            self, "Скопировано!", "Скопировано в буфер обмена!")
