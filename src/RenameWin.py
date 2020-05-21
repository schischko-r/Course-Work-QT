import sys
import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5 import Qt

from designer import RenameDesigner


class RenameWin(QtWidgets.QDialog, RenameDesigner.Ui_Rename):
    def __init__(self,  initName="", parent=None):
        super(RenameWin, self).__init__()
        self.setupUi(self)
        self.lineEdit.returnPressed.connect(self.on_pushButtonOK_clicked)
        self.lineEdit.setText(initName)

    @QtCore.pyqtSlot()
    def on_pushButtonOK_clicked(self):
        self.text = self.lineEdit.text()
        if self.text != "":
            name = "".join(x for x in self.text if x.isalnum())
            if len(name) == 0 or "." in self.text:
                QtWidgets.QMessageBox.about(
                    self, "Ошибка!", "Некорректное имя!")
                self.close()
            else:
                self.accept()
                self.close()
        else:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Имя не может быть пустым!")
