import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import Qt

from designer import ConfigDesigner
from RenameWin import RenameWin

import configparser
import datetime
import glob
import os


def relativePath(folder, name, ftype):
    return os.path.abspath(os.path.join(os.path.dirname(
        "__file__"),  folder)) + "\\" + name + ftype


class ConfigWin(QtWidgets.QDialog, ConfigDesigner.Ui_ConfigWin):
    def __init__(self, parent=None):
        super(ConfigWin, self).__init__()
        self.setupUi(self)
        self.configbox.itemClicked.connect(self.onItemClicked)
        self.configbox.itemDoubleClicked.connect(self.useConfig)
        self.newConfigBtn.clicked.connect(self.newConfig)
        self.renameConfigBtn.clicked.connect(self.renameConfig)
        self.delConfigBtn.clicked.connect(self.delConfig)
        self.useConfigBtn.clicked.connect(self.useConfig)

        self.nameEntry.returnPressed.connect(self.useConfig)
        self.textEntry.returnPressed.connect(self.useConfig)
        self.authorEntry.returnPressed.connect(self.useConfig)
        self.receiverEntry.returnPressed.connect(self.useConfig)
        self.populateConfig()

    def onItemClicked(self, it, col):
        self.selectedCfg = str(it.text(0))
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
        self.savedflag = 0
        path = os.path.abspath(os.path.join(
            os.path.dirname("__file__"), 'config'))
        if not os.path.exists(path):
            os.makedirs(path)
            print("DEBUG: CFG FOLDER CREATED")

        self.name = "".join(x for x in self.nameEntry.text()
                            if x.isalnum() or x == " ")
        if len(self.name) == 0:
            QtWidgets.QMessageBox.about(
                self, "Ошибка!", "Некорректное имя!")
            return

        MsgBox = QtWidgets.QMessageBox.question(self,
                                                'Выбрана конфигурация', f'Вы уверены, что хотите выбрать конфигурацию "{self.name}"', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if MsgBox == QtWidgets.QMessageBox.Yes:
            pass
        else:
            return

        text = self.textEntry.text()
        author = self.authorEntry.text()
        receiver = self.receiverEntry.text()
        try:
            topic = [item.text() for item in self.topicbox.selectedItems()][0]
        except:
            topic = 'Все'
        finally:
            pass

        fdate = str(self.fdayMenu.currentText()) + "-" + \
            str(self.months[str(self.fmonthMenu.currentText())]) + \
            "-" + str(self.fyearMenu.currentText())

        tdate = str(self.tdayMenu.currentText()) + "-" + \
            str(self.months[str(self.tmonthMenu.currentText())]) + \
            "-" + str(self.tyearMenu.currentText())
        if self.checkBox.isChecked() == True:
            expanded = "True"
        else:
            expanded = "False"

        last_used = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        config = configparser.ConfigParser()
        config['config'] = {'text': text, 'author': author,
                            'receiver': receiver, 'topic': topic, 'fdate': fdate, 'tdate': tdate, 'last_used': last_used, 'expanded': expanded}

        path = os.path.abspath(os.path.join(
            os.path.dirname("__file__"), 'config'))
        with open(path + '\\' + self.name + '.ini', 'w', encoding="utf-8-sig") as configfile:
            config.write(configfile)

        try:
            path = os.path.abspath(os.path.join(
                os.path.dirname("__file__"), 'config'))
            f = open(path + "\\" + self.name + '.ini')
        except IOError:
            QtWidgets.QMessageBox.about(
                self, "Ошибка!", "Некорректное имя!")
            return
        else:
            f.close()
            QtWidgets.QMessageBox.about(
                self, "Вы выбрали конфигурацию", f'Выбрана конфигурация "{self.name}"!')
            self.savedflag = 1
            print("DEBUG: CFG SAVED")
            self.populateConfig()

    def useConfig(self):
        self.saveConfig()
        if self.savedflag == 1:
            try:
                self.PATH = relativePath(
                    'config',  self.name, '.ini')
                self.accept()
                self.close()
            except:
                QtWidgets.QMessageBox.about(
                    self, "Error!", "Непредвиденная ошибка!")
                return
        else:
            pass

    def delConfig(self):
        name = self.nameEntry.text()

        MsgBox = QtWidgets.QMessageBox.question(self,
                                                'Удаление', f'Вы уверены, что хотите удалить конфигурацию {name}?',  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if MsgBox == QtWidgets.QMessageBox.Yes:
            pass
        else:
            return

        filepath = relativePath('config',  self.selectedCfg, '.ini')

        if os.path.exists(filepath):
            os.remove(filepath)
            self.newConfig()
        else:
            print("The file does not exist")
        self.populateConfig()

    def renameConfig(self):
        rename = RenameWin(initName=self.configbox.selectedItems()[0].text(0))
        if rename.exec_():
            try:
                self.renameWintxt = "".join(
                    x for x in rename.text if x.isalnum() or x == " ")
                self.newName = relativePath(
                    'config', self.renameWintxt, '.ini')
                current = relativePath(
                    'config',  self.configbox.selectedItems()[0].text(0), '.ini')

                os.rename(current, self.newName)
                self.populateConfig()

                self.configbox.setCurrentItem(self.configbox.findItems(self.renameWintxt, Qt.Qt.MatchExactly)[
                    0])
                self.configbox.itemClicked.emit(
                    self.configbox.selectedItems()[0], 0)

            except:
                QtWidgets.QMessageBox.about(
                    self, "Внимание!", "Файл с таким именем уже существует!")

    def populateConfig(self):
        self.configbox.clear()

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
        for i in range(self.configbox.columnCount()):
            self.configbox.resizeColumnToContents(i)
