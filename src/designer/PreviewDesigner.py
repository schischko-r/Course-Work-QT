# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreviewWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 800)
        Dialog.setMinimumSize(QtCore.QSize(1000, 800))
        Dialog.setMaximumSize(QtCore.QSize(1000, 800))
        Dialog.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.treeWidget = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 1000, 400))
        self.treeWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(160)
        self.treeWidget.header().setMinimumSectionSize(40)
        self.treeWidget.header().setSortIndicatorShown(True)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 410, 980, 380))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(2, 2, 976, 376))
        self.tableWidget.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(820)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Предпросмотр"))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "Пользователь"))
        self.treeWidget.headerItem().setText(1, _translate("Dialog", "Сообщение"))
        self.treeWidget.headerItem().setText(2, _translate("Dialog", "Время"))
        self.treeWidget.headerItem().setText(3, _translate("Dialog", "Ссылка"))
        self.treeWidget.headerItem().setText(4, _translate("Dialog", "Длина сообщения"))
        self.treeWidget.headerItem().setText(5, _translate("Dialog", "Развернутый вид"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "Пользователь"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "Сообщение"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "Время"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "Ссылка"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "Длина сообщения"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Dialog", "Развернутый вид"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Значение"))
