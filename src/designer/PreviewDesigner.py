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
        Dialog.resize(1000, 600)
        self.treeWidget = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(160)
        self.treeWidget.header().setMinimumSectionSize(40)
        self.treeWidget.header().setSortIndicatorShown(True)

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
