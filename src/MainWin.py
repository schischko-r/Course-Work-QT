import sys
from PyQt5 import QtWidgets, Qt, QtCore

from designer import MainDesigner
from RenameWin import RenameWin

from parsing import parserMain

import configparser
import requests
import datetime
import glob
import math
import csv
import os


def relativePath(folder, name, ftype):
    path = os.path.abspath(os.path.join(os.path.dirname(
        "__file__"),  folder) + "\\" + name + ftype)
    return path


def deltatime(time):
    zerotimeNow = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)
    zerotimeThen = datetime.datetime.strptime(
        time, '%Y-%m-%d %H:%M:%S').replace(hour=0, minute=0, second=0)
    delta = zerotimeNow - zerotimeThen
    if delta.days < 1:
        curtime = datetime.datetime.now()
        deltaToday = curtime - \
            datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if deltaToday.seconds < 3600:
            deltaToday = "Меньше часа назад"
        elif deltaToday.seconds > 3600 and deltaToday.seconds < 2 * 3600:
            deltaToday = "Час назад"
        else:
            deltaToday = "Сегодня"
    elif delta.days == 1:
        deltaToday = "Вчера"
    elif delta.days > 1 and delta.days <= 7:
        deltaToday = "На этой неделе"
    elif delta.days > 7 and delta.days < 31:
        deltaToday = "В этом месяце"
    elif delta.days >= 31 and delta.days <= 365:
        deltaToday = "В этом году"
    else:
        deltaToday = "Больше года назад"
    return deltaToday


class MainWindow(QtWidgets.QMainWindow, MainDesigner.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populateExport()

        # ФУНКЦИИ ГЛАВНОГО ОКНА
        self.tabWidget.setCurrentIndex(0)
        self.managerBtn.clicked.connect(self.openmanager)
        self.startBtn.clicked.connect(self.startParsing)

        self.deleteBtn.clicked.connect(self.deleteExport)
        self.renameBtn.clicked.connect(self.renameExport)
        self.expandedBtn.clicked.connect(self.openPreview)

        self.exportbox.itemClicked.connect(self.preview)
        self.exportbox.itemDoubleClicked.connect(self.openPreview)
        self.configFullListbox.itemClicked.connect(self.loadfromHst)

        # ФУНКЦИИ ОКНА КОНФИГУРАЦИИ
        self.configbox.itemClicked.connect(self.loadCfgFromList)
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

        # ФУНКЦИИ ОКНА ПРЕДПРОСМОТРА
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.tableWidget.itemDoubleClicked.connect(self.copy)

    # ФУНКЦИИ ГЛАВНОГО ОКНА
    def openmanager(self):
        self.tabWidget.setCurrentIndex(1)

    def populateExport(self):
        def convert_size(size_bytes):
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])

        self.months = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Май': 5, 'Июн': 6,
                       'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12}

        self.exportbox.clear()

        path = os.path.abspath(os.path.join(
            os.path.dirname("__file__"), 'export'))

        files = [file for file in glob.glob(path + "**/*.csv", recursive=True)]
        for file in files:
            filename = file.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]
            filesize = convert_size(os.path.getsize(file))
            with open(file,  encoding='utf-8-sig') as f:
                length = sum(1 for line in f) - 1
            if length == 0:
                length = "<Ничего не найдено>"

            item = QtWidgets.QTreeWidgetItem(self.exportbox)
            values = (filename, length, filesize)
            for i in range(len(values)):
                item.setText(i, str(values[i]))

        for i in range(self.exportbox.columnCount()):
            self.exportbox.resizeColumnToContents(i)

        path = os.path.abspath(os.path.join(
            os.path.dirname("__file__"), 'config'))

        self.configFullListbox.clear()

        files = [file for file in glob.glob(path + "**/*.ini", recursive=True)]
        for file in files:
            config = configparser.ConfigParser()
            config.read(file, encoding='utf-8-sig')
            configDict = config._sections['config']
            date = deltatime(configDict['last_used'])
            filename = file.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]

            item = QtWidgets.QTreeWidgetItem(self.configFullListbox)
            values = (filename, date)
            for i in range(len(values)):
                item.setText(i, values[i])

        for i in range(self.configFullListbox.columnCount()):
            self.configFullListbox.resizeColumnToContents(i)

    def startParsing(self):
        self.maxPage = self.lineEdit.text()
        if self.maxPage == "":
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Укажите количество страниц!")
            return
        try:
            int(self.maxPage)
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Неверное количество!")
            return

        self.progressBar.setValue(0)
        self.progressBar.setMaximum(int(self.maxPage)+3)
        self.progresslbl.setText("Устанавливаю соединение...")
        try:
            r = requests.head("https://vif2ne.org/")
            pass
        except requests.ConnectionError:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Проверьте ваше подключение к интернету и доступность сайта")
            self.progresslbl.setText("Ошибка при установке соединения!")
            return
        self.progresslbl.setText("Соединение установлено!")
        self.progressBar.setValue(self.progressBar.value()+1)

        if self.configshow.topLevelItemCount() == 0:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Вы не выбрали конфигурацию!")
            return

        try:
            config = configparser.ConfigParser()
            config.read(self.cfgPATH, encoding='utf-8-sig')
            filename = self.cfgPATH.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]
            configDict = config._sections['config']
            self.ctext, self.ctopic, self.cstrtDate, self.cendDate, self.cauthor, self.cadressed, self.cexpanded = configDict['text'], configDict[
                'topic'], configDict['fdate'], configDict['tdate'],  configDict['author'],  configDict['receiver'], configDict['expanded']

            self.progresslbl.setText("Конфигурация загружена!")
            self.progressBar.setValue(self.progressBar.value()+1)
        except:
            self.progresslbl.setText("Файл конфигурации поврежден!")
            return
        self.parser = parserMain.Parser(
            int(self.maxPage), self.ctopic, self.ctext, self.cstrtDate, self.cendDate, self.cauthor, self.cadressed, str(self.cexpanded))
        self.parser.progress.connect(self.moveprogress)
        self.parser.done.connect(self.complete)
        self.parser.start()
        self.progresslbl.setText("Начинаю парсинг!")

    def moveprogress(self, value):
        if value <= int(self.maxPage):
            self.progresslbl.setText(
                f"Парсинг: страница: {value}/{self.maxPage}")
            self.progressBar.setValue(self.progressBar.value()+1)
        else:
            self.progresslbl.setText(f"Создания файла с данными!")
            self.progressBar.setValue(self.progressBar.value()+1)

    def complete(self, done):
        config = configparser.ConfigParser()
        config.read(self.cfgPATH, encoding='utf-8-sig')
        last_used = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        config['config'] = {'text': self.ctext, 'author': self.cauthor,
                            'receiver': self.cadressed, 'topic': self.ctopic, 'fdate': self.cstrtDate, 'tdate': self.cendDate, 'last_used': last_used, 'expanded': self.cexpanded}
        with open(self.cfgPATH, "w", encoding='utf-8-sig') as configfile:
            config.write(configfile)
        QtWidgets.QMessageBox.about(
            self, "Успешно!", "Парсинг окончен!")
        self.populateExport()
        self.progresslbl.setText(f"Ожидание начала парсинга...")
        self.progressBar.setValue(0)

    def deleteExport(self):
        try:
            for item in self.exportbox.selectedItems():
                filepath = relativePath('export',  item.text(0), '.csv')
                if os.path.exists(filepath):
                    os.remove(filepath)
                else:
                    print("The file does not exist")
            self.populateExport()
            self.previewShowbox.clear()
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Выберите файл!")

    def renameExport(self):
        try:
            renameWin = RenameWin(self.exportbox.selectedItems()[0].text(0))
            if renameWin.exec_():
                try:
                    self.newName = relativePath(
                        'export',  renameWin.text, '.csv')
                    current = relativePath(
                        'export',  self.exportbox.selectedItems()[0].text(0), '.csv')
                    os.rename(current, self.newName)
                    self.populateExport()
                    self.previewShowbox.clear()
                except:
                    QtWidgets.QMessageBox.about(
                        self, "Внимание!", "Некорректное имя!")
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Выберите файл!")

    def openPreview(self):
        self.tabWidget.setCurrentIndex(2)

    def preview(self, it, colf):
        self.previewShowbox.clear()
        filepath = relativePath('export',  it.text(0), '.csv')
        with open(filepath, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                item = QtWidgets.QTreeWidgetItem(self.previewShowbox)
                values = (row['name'], row['msg'], row['time'])
                for i in range(len(values)):
                    item.setText(i, values[i])
        for i in range(self.previewShowbox.columnCount()):
            self.previewShowbox.resizeColumnToContents(i)
        self.populateExpandedExport(
            relativePath('export',  it.text(0), '.csv'))
        self.label_16.setText(it.text(0) + ".csv")

    def loadfromHst(self, it, col):
        self.cfgPATH = relativePath('config',  it.text(0), '.ini')
        try:
            with open(self.cfgPATH, encoding='utf-8-sig') as f:
                lines = f.readlines()

            self.configshow.clear()
            for line in lines[1:]:
                if line != "":
                    cfgtitle = line.split(" = ")[0]
                    try:
                        cfgvalue = line.split(" = ")[1]
                    except:
                        cfgvalue = ""
                    item = QtWidgets.QTreeWidgetItem(self.configshow)
                    values = (cfgtitle, cfgvalue)
                    for i in range(len(values)):
                        item.setText(i, values[i])
                        item.setTextAlignment(i, 4)
            for i in range(self.configshow.columnCount()):
                self.configshow.resizeColumnToContents(i)
            self.guidelbl.setText("Выбрано успешно!")

        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Конфигурация не выбрана!")

        self.populateExport()

    # ФУНКЦИИ ОКНА КОНФИГУРАЦИИ
    def loadCfgFromList(self, it, col):
        self.selectedCfg = str(it.text(0))
        self.nameEntry.setText(it.text(0))
        self.textEntry.setText(it.text(1))
        items = self.topicbox.findItems(it.text(2), Qt.Qt.MatchExactly)[0]
        self.topicbox.setCurrentRow(self.topicbox.row(items))

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
            self.populateExport()

    def useConfig(self):
        self.saveConfig()
        if self.savedflag == 1:
            try:
                self.cfgPATH = relativePath(
                    'config',  self.name, '.ini')
                self.tabWidget.setCurrentIndex(0)
                self.populateExport()
                try:
                    with open(self.cfgPATH, encoding='utf-8-sig') as f:
                        lines = f.readlines()

                    self.configshow.clear()
                    for line in lines[1:]:
                        if line != "":
                            cfgtitle = line.split(" = ")[0]
                            try:
                                cfgvalue = line.split(" = ")[1]
                            except:
                                cfgvalue = ""
                            item = QtWidgets.QTreeWidgetItem(self.configshow)
                            values = (cfgtitle, cfgvalue)
                            for i in range(len(values)):
                                item.setText(i, values[i])
                                item.setTextAlignment(i, 4)
                    for i in range(self.configshow.columnCount()):
                        self.configshow.resizeColumnToContents(i)
                    self.guidelbl.setText("Выбрано успешно!")

                except:
                    QtWidgets.QMessageBox.about(
                        self, "Внимание!", "Конфигурация не выбрана!")
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
        self.populateExport()

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
                self.populateExport()

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

    # ФУНКЦИИ ОКНА ПРЕДПРОСМОТРА
    def populateExpandedExport(self, file=""):
        with open(file, encoding='utf-8-sig') as f:
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
