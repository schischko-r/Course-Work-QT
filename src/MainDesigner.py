# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWin.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1427, 882)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1427, 882))
        MainWindow.setMaximumSize(QtCore.QSize(1427, 882))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(229, 240, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.menu = QtWidgets.QFrame(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(0, 0, 287, 882))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 20, 252))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 20, 252))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 20, 252))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.menu.setPalette(palette)
        self.menu.setAutoFillBackground(False)
        self.menu.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);")
        self.menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu.setObjectName("menu")
        self.menubase = QtWidgets.QFrame(self.menu)
        self.menubase.setGeometry(QtCore.QRect(17, 648, 253, 194))
        self.menubase.setAutoFillBackground(False)
        self.menubase.setStyleSheet("border: 2px solid rgb(177, 206, 240);")
        self.menubase.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menubase.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menubase.setObjectName("menubase")
        self.guidefrm = QtWidgets.QFrame(self.menubase)
        self.guidefrm.setGeometry(QtCore.QRect(0, 0, 253, 58))
        self.guidefrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.guidefrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.guidefrm.setObjectName("guidefrm")
        self.guidelbl = QtWidgets.QLabel(self.guidefrm)
        self.guidelbl.setGeometry(QtCore.QRect(20, 15, 228, 27))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.guidelbl.setFont(font)
        self.guidelbl.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.guidelbl.setObjectName("guidelbl")
        self.startBtn = QtWidgets.QPushButton(self.menubase)
        self.startBtn.setGeometry(QtCore.QRect(24, 137, 205, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.startBtn.setFont(font)
        self.startBtn.setStyleSheet("background-color: rgb(103, 169, 237);\n"
"color: rgb(255, 255, 255)")
        self.startBtn.setObjectName("startBtn")
        self.label_5 = QtWidgets.QLabel(self.menubase)
        self.label_5.setGeometry(QtCore.QRect(20, 70, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.menubase)
        self.lineEdit.setGeometry(QtCore.QRect(174, 76, 51, 21))
        self.lineEdit.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_6 = QtWidgets.QLabel(self.menu)
        self.label_6.setGeometry(QtCore.QRect(17, 40, 253, 239))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../design/ico/badge.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.configfrm = QtWidgets.QFrame(self.centralwidget)
        self.configfrm.setGeometry(QtCore.QRect(325, 40, 353, 305))
        self.configfrm.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);")
        self.configfrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configfrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configfrm.setObjectName("configfrm")
        self.configshow = QtWidgets.QTreeWidget(self.configfrm)
        self.configshow.setGeometry(QtCore.QRect(18, 45, 317, 239))
        self.configshow.setObjectName("configshow")
        self.configshow.header().setDefaultSectionSize(140)
        self.configshow.header().setMinimumSectionSize(90)
        self.label_3 = QtWidgets.QLabel(self.configfrm)
        self.label_3.setGeometry(QtCore.QRect(18, 10, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.exportfrm = QtWidgets.QFrame(self.centralwidget)
        self.exportfrm.setGeometry(QtCore.QRect(711, 471, 681, 367))
        self.exportfrm.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);")
        self.exportfrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.exportfrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.exportfrm.setObjectName("exportfrm")
        self.buttonfrm = QtWidgets.QFrame(self.exportfrm)
        self.buttonfrm.setGeometry(QtCore.QRect(14, 316, 649, 35))
        self.buttonfrm.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.buttonfrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttonfrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttonfrm.setObjectName("buttonfrm")
        self.renameBtn = QtWidgets.QPushButton(self.buttonfrm)
        self.renameBtn.setGeometry(QtCore.QRect(226, 7, 105, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(7)
        self.renameBtn.setFont(font)
        self.renameBtn.setStyleSheet("background-color: rgb(103, 169, 237);\n"
"color: rgb(255, 255, 255)")
        self.renameBtn.setObjectName("renameBtn")
        self.deleteBtn = QtWidgets.QPushButton(self.buttonfrm)
        self.deleteBtn.setGeometry(QtCore.QRect(348, 7, 75, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(7)
        self.deleteBtn.setFont(font)
        self.deleteBtn.setStyleSheet("background-color: rgb(103, 169, 237);\n"
"color: rgb(255, 255, 255)")
        self.deleteBtn.setObjectName("deleteBtn")
        self.label = QtWidgets.QLabel(self.exportfrm)
        self.label.setGeometry(QtCore.QRect(14, 10, 351, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.exportbox = QtWidgets.QTreeWidget(self.exportfrm)
        self.exportbox.setGeometry(QtCore.QRect(14, 45, 649, 271))
        self.exportbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.exportbox.setDragEnabled(True)
        self.exportbox.setIndentation(25)
        self.exportbox.setObjectName("exportbox")
        self.exportbox.header().setVisible(True)
        self.exportbox.header().setCascadingSectionResizes(False)
        self.exportbox.header().setDefaultSectionSize(200)
        self.exportbox.header().setMinimumSectionSize(150)
        self.configFullListfrm = QtWidgets.QFrame(self.centralwidget)
        self.configFullListfrm.setGeometry(QtCore.QRect(325, 379, 353, 463))
        self.configFullListfrm.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);\n"
"")
        self.configFullListfrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configFullListfrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configFullListfrm.setObjectName("configFullListfrm")
        self.configFullListbox = QtWidgets.QTreeWidget(self.configFullListfrm)
        self.configFullListbox.setGeometry(QtCore.QRect(18, 46, 317, 345))
        self.configFullListbox.setObjectName("configFullListbox")
        self.configFullListbox.header().setDefaultSectionSize(140)
        self.configFullListbox.header().setMinimumSectionSize(90)
        self.label_4 = QtWidgets.QLabel(self.configFullListfrm)
        self.label_4.setGeometry(QtCore.QRect(18, 10, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.managerBtn = QtWidgets.QPushButton(self.configFullListfrm)
        self.managerBtn.setGeometry(QtCore.QRect(74, 415, 205, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(7)
        self.managerBtn.setFont(font)
        self.managerBtn.setStyleSheet("background-color: rgb(103, 169, 237);\n"
"color: rgb(255, 255, 255)")
        self.managerBtn.setObjectName("managerBtn")
        self.previewfrm = QtWidgets.QFrame(self.centralwidget)
        self.previewfrm.setGeometry(QtCore.QRect(711, 40, 681, 385))
        self.previewfrm.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(177, 206, 240);\n"
"")
        self.previewfrm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.previewfrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.previewfrm.setObjectName("previewfrm")
        self.label_2 = QtWidgets.QLabel(self.previewfrm)
        self.label_2.setGeometry(QtCore.QRect(14, 10, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"")
        self.label_2.setObjectName("label_2")
        self.frame = QtWidgets.QFrame(self.previewfrm)
        self.frame.setGeometry(QtCore.QRect(14, 336, 649, 35))
        self.frame.setStyleSheet("background-color: rgb(229, 240, 249);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.expandedBtn = QtWidgets.QPushButton(self.frame)
        self.expandedBtn.setGeometry(QtCore.QRect(228, 7, 193, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(7)
        self.expandedBtn.setFont(font)
        self.expandedBtn.setStyleSheet("background-color: rgb(103, 169, 237);\n"
"color: rgb(255, 255, 255)")
        self.expandedBtn.setObjectName("expandedBtn")
        self.previewShowbox = QtWidgets.QTreeWidget(self.previewfrm)
        self.previewShowbox.setGeometry(QtCore.QRect(14, 45, 649, 293))
        self.previewShowbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.previewShowbox.setDragEnabled(True)
        self.previewShowbox.setObjectName("previewShowbox")
        self.previewShowbox.header().setDefaultSectionSize(200)
        self.previewShowbox.header().setMinimumSectionSize(150)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.guidelbl.setText(_translate("MainWindow", "Выберите конфигурацию!"))
        self.startBtn.setText(_translate("MainWindow", "Начать парсинг"))
        self.label_5.setText(_translate("MainWindow", "Количество страниц:\n"
"(1 страница = 100 запросов)"))
        self.configshow.headerItem().setText(0, _translate("MainWindow", "Ключ"))
        self.configshow.headerItem().setText(1, _translate("MainWindow", "Значение"))
        self.label_3.setText(_translate("MainWindow", "Конфигурация:"))
        self.renameBtn.setText(_translate("MainWindow", "Переименовать"))
        self.deleteBtn.setText(_translate("MainWindow", "Удалить"))
        self.label.setText(_translate("MainWindow", "Экспортированные файлы:"))
        self.exportbox.setSortingEnabled(True)
        self.exportbox.headerItem().setText(0, _translate("MainWindow", "Имя"))
        self.exportbox.headerItem().setText(1, _translate("MainWindow", "Кол-во записей"))
        self.exportbox.headerItem().setText(2, _translate("MainWindow", "Размер файла"))
        self.configFullListbox.setSortingEnabled(True)
        self.configFullListbox.headerItem().setText(0, _translate("MainWindow", "Имя"))
        self.configFullListbox.headerItem().setText(1, _translate("MainWindow", "Последний парсинг"))
        self.label_4.setText(_translate("MainWindow", "История:"))
        self.managerBtn.setText(_translate("MainWindow", "Открыть менеджер конфигураций"))
        self.label_2.setText(_translate("MainWindow", "Предпросмотр:"))
        self.expandedBtn.setText(_translate("MainWindow", "Расширенный предпросмотр"))
        self.previewShowbox.setSortingEnabled(True)
        self.previewShowbox.headerItem().setText(0, _translate("MainWindow", "Пользователь"))
        self.previewShowbox.headerItem().setText(1, _translate("MainWindow", "Сообщение"))
        self.previewShowbox.headerItem().setText(2, _translate("MainWindow", "Время"))
import ico_rc
