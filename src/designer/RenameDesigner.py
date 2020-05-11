# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RenameWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Rename(object):
    def setupUi(self, Rename):
        Rename.setObjectName("Rename")
        Rename.resize(350, 100)
        Rename.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.frame = QtWidgets.QFrame(Rename)
        self.frame.setGeometry(QtCore.QRect(0, 0, 350, 100))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 310, 34))
        self.lineEdit.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 205, 27))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Rename)
        QtCore.QMetaObject.connectSlotsByName(Rename)

    def retranslateUi(self, Rename):
        _translate = QtCore.QCoreApplication.translate
        Rename.setWindowTitle(_translate("Rename", "Переименование"))
        self.label_3.setText(_translate("Rename", "Переименование:"))
