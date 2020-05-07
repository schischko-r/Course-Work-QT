import sys
from PyQt5 import QtWidgets
from PyQt5 import Qt
from MainWin import *
from ConfigWin import *

import configparser
import glob
import os


class ConfigWin(QtWidgets.QMainWindow, Ui_CfgWindow):
    def __init__(self, parent=None):
        super(ConfigWin, self).__init__(parent)
        self.setupUi(self)
        self.configbox.itemClicked.connect(self.onItemClicked)
        self.newConfigBtn.clicked.connect(self.newConfig)
        self.saveConfigBtn.clicked.connect(self.saveConfig)
        self.delConfigBtn.clicked.connect(self.delConfig)
        self.useConfigBtn.clicked.connect(self.useConfig)

        self.loadConfigs()

    def loadConfigs(self):
        path = os.path.abspath(os.path.join(
            os.path.dirname("__file__"), 'config'))

        files = [file for file in glob.glob(path + "**/*.ini", recursive=True)]
        for file in files:
            config = configparser.ConfigParser()
            config.read(file, encoding='utf-8-sig')
            filename = file.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]
            configDict = config._sections['config']

            item = QtWidgets.QTreeWidgetItem(self.configbox)
            values = (filename, configDict['text'], configDict['topic'], configDict['fdate'],
                      configDict['tdate'],  configDict['author'],  configDict['receiver'], configDict['expanded'])
            for i in range(len(values)):
                item.setText(i, values[i])

    def onItemClicked(self, it, col):
        self.nameEntry.setText(it.text(0))
        self.textEntry.setText(it.text(1))
        items = self.topicbox.findItems(it.text(2), Qt.Qt.MatchExactly)[0]
        self.topicbox.setCurrentRow(self.topicbox.row(items))

        self.months = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Май': 5, 'Июн': 6,
                       'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12}

        self.fdayMenu.setCurrentIndex(self.fdayMenu.findText(
            it.text(3).split("-")[0], QtCore.Qt.MatchFixedString))
        self.fmonthMenu.setCurrentIndex(self.fmonthMenu.findText([key for (key, value) in self.months.items(
        ) if value == int(it.text(3).split("-")[1])][0], QtCore.Qt.MatchFixedString))
        self.fyearMenu.setCurrentIndex(self.fyearMenu.findText(
            it.text(3).split("-")[2], QtCore.Qt.MatchFixedString))

        self.tdayMenu.setCurrentIndex(self.tdayMenu.findText(
            it.text(4).split("-")[0], QtCore.Qt.MatchFixedString))
        self.tmonthMenu.setCurrentIndex(self.tmonthMenu.findText([key for (key, value) in self.months.items(
        ) if value == int(it.text(4).split("-")[1])][0], QtCore.Qt.MatchFixedString))
        self.tyearMenu.setCurrentIndex(self.tyearMenu.findText(
            it.text(4).split("-")[2], QtCore.Qt.MatchFixedString))
        self.authorEntry.setText(it.text(5))
        self.receiverEntry.setText(it.text(6))

        if (it.text(7)) == "True" and self.checkBox.isChecked() == False:
            self.checkBox.toggle()
        elif (it.text(7)) == "False" and self.checkBox.isChecked() == True:
            self.checkBox.toggle()

    def newConfig(self):
        self.nameEntry.setText("")
        self.textEntry.setText("")
        items = self.topicbox.findItems("Все", Qt.Qt.MatchExactly)[0]
        self.topicbox.setCurrentRow(self.topicbox.row(items))

        self.months = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Май': 5, 'Июн': 6,
                       'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12}

        self.fdayMenu.setCurrentIndex(0)
        self.fmonthMenu.setCurrentIndex(0)
        self.fyearMenu.setCurrentIndex(0)

        self.tdayMenu.setCurrentIndex(0)
        self.tmonthMenu.setCurrentIndex(0)
        self.tyearMenu.setCurrentIndex(20)
        self.authorEntry.setText("")
        self.receiverEntry.setText("")

        if self.checkBox.isChecked() == True:
            self.checkBox.toggle()

    def saveConfig(self):
        pass

    def delConfig(self):
        pass

    def useConfig(self):
        pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fillTrees()
        self.managerBtn.clicked.connect(self.openmanager)
        self.dialog = ConfigWin(self)

    def fillTrees(self):
        pass

    def openmanager(self):
        self.dialog.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
