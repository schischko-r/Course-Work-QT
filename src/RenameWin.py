import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import Qt

from designer import RenameDesigner


class RenameWin(QtWidgets.QDialog, RenameDesigner.Ui_Rename):
    def __init__(self, parent=None):
        super(RenameWin, self).__init__()
        self.setupUi(self)
        self.lineEdit.returnPressed.connect(self.on_pushButtonOK_clicked)

    @QtCore.pyqtSlot()
    def on_pushButtonOK_clicked(self):
        self.text = self.lineEdit.text() + ".csv"
        self.accept()
        self.close()
