import sys
import PyQt5
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


def relativePath(folder, name="", ftype=""):
    # ФУНКЦИЯ ВОЗВРАЩАЕТ ОТНОСИТЕЛЬНЫЙ ПУТЬ К ФАЙЛУ ИЛИ ПАПКЕ
    path = os.path.abspath(os.path.join(os.path.dirname(
        os.getcwd()),  folder) + "\\" + name + ftype)
    return path


def deltatime(time):
    # ФУНКЦИЯ ВОЗВРАЩАЕТ ОТНОСИТЕЛЬНОЕ ВРЕМЯ
    HOUR, WEEK, MONTH, YEAR = 3600, 7, 31, 365

    # СРАВНИВАЕМ ТОЛЬКО ДАТЫ
    zerotimeNow = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)
    zerotimeThen = datetime.datetime.strptime(
        time, '%Y-%m-%d %H:%M:%S').replace(hour=0, minute=0, second=0)

    delta = zerotimeNow - zerotimeThen
    if delta.days < 1:
        curtime = datetime.datetime.now()
        deltaToday = curtime - \
            datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if deltaToday.seconds < HOUR:
            deltaToday = "Меньше часа назад"
        elif deltaToday.seconds > HOUR and deltaToday.seconds < 2 * HOUR:
            deltaToday = "Час назад"
        else:
            deltaToday = "Сегодня"
    elif delta.days == 1:
        deltaToday = "Вчера"
    elif delta.days > 1 and delta.days <= WEEK:
        deltaToday = "На этой неделе"
    elif delta.days > WEEK and delta.days < MONTH:
        deltaToday = "В этом месяце"
    elif delta.days >= MONTH and delta.days <= YEAR:
        deltaToday = "В этом году"
    else:
        deltaToday = "Больше года назад"
    return deltaToday


class MainWindow(QtWidgets.QMainWindow, MainDesigner.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.loadSettings()
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
        self.openSettings.clicked.connect(self.openPreferences)

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
        self.lineEdit.returnPressed.connect(self.startParsing)

        self.cfgCheck.toggled.connect(self.setName)
        self.dateCheck.toggled.connect(self.setName)

        self.relativetime.toggled.connect(self.setTime)
        self.exactTime.toggled.connect(self.setTime)

        # ФУНКЦИИ ОКНА ПРЕДПРОСМОТРА
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.tableWidget.itemDoubleClicked.connect(self.copy)

        # ОБЩИЕ ПЕРЕМЕННЫЕ
        self.months = {'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4, 'Май': 5, 'Июн': 6,
                       'Июл': 7, 'Авг': 8, 'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12}

        self.updateMain()

    def loadSettings(self):
        try:
            settings = configparser.ConfigParser()
            settings.read('settings.ini', encoding='utf-8-sig')
            configDict = settings._sections['settings']

            self.RELATIVETIME = True
            self.EXPORTCFGNAME = True

            if configDict['loadstg'] == "True":
                if configDict['savestg'] != "True":
                    self.saveStgCheck.setChecked(False)
                if configDict['exitapp'] != "True":
                    self.exitCheck.setChecked(False)
                if configDict['relativetime'] != "True":
                    self.exactTime.setChecked(True)
                    self.RELATIVETIME = False
                if configDict['cfgname'] != "True":
                    self.dateCheck.setChecked(True)
                    self.EXPORTCFGNAME = False
            else:
                self.loadStgCheck.setChecked(False)
        except:
            return
    # ФУНКЦИИ ГЛАВНОГО ОКНА

    def updateMain(self):
        # ОБНОВЛЯЕТ ФАЙЛЫ ОСНОВНОГО ОКНА
        def convert_size(size_bytes):
            # РАССЧИТЫВАЕТ РАЗМЕР ФАЙЛА
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])

        # ЗАПОЛНЕНИЕ ДЕРЕВА ЭКСПОРТИРОВАННЫХ ДАННЫХ
        self.exportbox.clear()

        path = relativePath("export")
        files = [file for file in glob.glob(path + "**/*.csv")]
        for file in files:
            filename = file.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]
            filesize = convert_size(os.path.getsize(file))
            with open(file,  encoding='utf-8-sig') as f:
                length = sum(1 for line in f) - 1
            if length == 0:
                length = "<Ничего не найдено>"
            f.close()

            item = QtWidgets.QTreeWidgetItem(self.exportbox)
            values = (filename, length, filesize)
            for i in range(len(values)):
                item.setText(i, str(values[i]))
                item.setTextAlignment(i, 4)

        for i in range(self.exportbox.columnCount()):
            self.exportbox.resizeColumnToContents(i)

        # ЗАПОЛНЕНИЕ ДЕРЕВА КОНФИГУРАЦИЙ
        path = relativePath("config")

        self.configFullListbox.clear()
        self.configbox.clear()

        files = [file for file in glob.glob(path + "**/*.ini")]
        for file in files:
            config = configparser.ConfigParser()
            config.read(file, encoding='utf-8-sig')
            configDict = config._sections['config']

            if self.RELATIVETIME == True:
                date = deltatime(configDict['last_used'])
            else:
                date = configDict['last_used']

            filename = file.split("\\")
            filename = filename[len(filename) - 1].split('.')[0]

            item = QtWidgets.QTreeWidgetItem(self.configFullListbox)
            values = (filename, date)
            for i in range(len(values)):
                item.setText(i, values[i])

            item = QtWidgets.QTreeWidgetItem(self.configbox)
            values = (filename, configDict['text'], configDict['topic'], configDict['fdate'],
                      configDict['tdate'],  configDict['author'],  configDict['receiver'], configDict['expanded'])
            for i in range(len(values)):
                item.setText(i, values[i])

        for i in range(self.configFullListbox.columnCount()):
            self.configFullListbox.resizeColumnToContents(i)

        for i in range(self.configbox.columnCount()):
            self.configbox.resizeColumnToContents(i)

    def startParsing(self):
        # ФУНКЦИЯ НАЧАЛА ПАРСИНГА
        # ПРОВЕРКА ВВОДА КОЛИЧЕСТВА СТРАНИЦ
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

        # ПРОВЕРКА НАЛИЧИЯ КОНФИГУРАЦИИ
        if self.configshow.topLevelItemCount() == 0:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Вы не выбрали конфигурацию!")
            return

        # ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(int(self.maxPage)+3)
        self.progresslbl.setText("Устанавливаю соединение...")
        try:
            requests.head("https://vif2ne.org/")
            pass
        except requests.ConnectionError:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Проверьте ваше подключение к интернету и доступность сайта")
            self.progresslbl.setText("Ошибка при установке соединения!")
            return
        self.progresslbl.setText("Соединение установлено!")
        self.progressBar.setValue(self.progressBar.value()+1)

        # СЧИТЫВАНИЕ ФАЙЛА
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
            QtWidgets.QMessageBox.about(
                self, "Файл конфигурации поврежден!")
            return
        # ЗАПУСК ТРЕДА ПАРСИНГА
        self.parser = parserMain.Parser(filename,
                                        int(self.maxPage), self.ctopic, self.ctext, self.cstrtDate, self.cendDate, self.cauthor, self.cadressed, str(self.cexpanded), self.EXPORTCFGNAME)
        self.parser.progress.connect(self.moveprogress)
        self.parser.done.connect(self.complete)
        self.parser.start()
        self.progresslbl.setText("Начинаю парсинг!")

    def moveprogress(self, value):
        # ОТВЕЧАЕТ ЗА ВИЗУАЛЬЗАЦИЮ ПРОГРЕССА ПАРСИНГА
        if value <= int(self.maxPage):
            self.progresslbl.setText(
                f"Парсинг: страница: {value}/{self.maxPage}")
            self.progressBar.setValue(self.progressBar.value()+1)
        else:
            self.progresslbl.setText(f"Создания файла с данными!")
            self.progressBar.setValue(self.progressBar.value()+1)

    def complete(self, done):
        # ОКОНЧАНИЕ ПАРСИНГА
        # ЗАПИСЫВАЕТ В КОНФИГУРАЦИЮ ВРЕМЯ ПОСЛЕДНЕГО ПАРСИНГА (ТЕКУЩЕЕ ВРЕМЯ)
        config = configparser.ConfigParser()
        config.read(self.cfgPATH, encoding='utf-8-sig')
        last_used = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        config['config'] = {'text': self.ctext, 'author': self.cauthor,
                            'receiver': self.cadressed, 'topic': self.ctopic, 'fdate': self.cstrtDate, 'tdate': self.cendDate, 'last_used': last_used, 'expanded': self.cexpanded}
        with open(self.cfgPATH, "w", encoding='utf-8-sig') as configfile:
            config.write(configfile)
            configfile.close()
        QtWidgets.QMessageBox.about(
            self, "Успешно!", "Парсинг окончен!")
        self.updateMain()
        # ВОЗВРАЩАЕТ В ИСХОДНОЕ ПОЛОЖЕНИЕ ЛЕЙБЛ И ПРОГРЕССБАР
        self.progresslbl.setText(f"Ожидание начала парсинга...")
        self.progressBar.setValue(0)
        self.parser.stop()

    def deleteExport(self):
        # ОТВЕЧАЕТ ЗА УДАЛЕНИЕ ФАЙЛА ЭКСПОРТА
        try:
            # ДЛЯ ВСЕХ ВЫБРАННЫХ ФАЙЛОВ
            for item in self.exportbox.selectedItems():
                # СОЗДАЕМ ИХ ПУТЬ И УДАЛЯЕМ
                filepath = relativePath('export',  item.text(0), '.csv')
                if os.path.exists(filepath):
                    os.remove(filepath)
                else:
                    QtWidgets.QMessageBox.about(
                        self, "Внимание!", "Не удалось удалить файл")
            # ОБНОВЛЯЕМ ГЛАВНОЕ ОКНО И ОЧИЩАЕМ ОКНА ПРЕДПРОСМОТРА
            self.updateMain()
            self.previewShowbox.clear()
            self.treeWidget.clear()
            self.label_16.setText("Выберите файл!")
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Выберите файл!")

    def renameExport(self):
        # ОТВЕЧАЕТ ЗА ПЕРЕИМЕНОВАНИЕ ФАЙЛА ЭКСПОРТА
        try:
            # СОЗДАЕТ ОКНО ДЛЯ ПЕРЕИМЕНОВАНИЯ ФАЙЛА
            renameWin = RenameWin(self.exportbox.selectedItems()[0].text(0))
            if renameWin.exec_():
                try:
                    self.newName = relativePath(
                        'export',  renameWin.text, '.csv')
                    current = relativePath(
                        'export',  self.exportbox.selectedItems()[0].text(0), '.csv')
                    os.rename(current, self.newName)
                    self.updateMain()
                    self.previewShowbox.clear()
                except:
                    QtWidgets.QMessageBox.about(
                        self, "Внимание!", "Некорректное имя!")
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Выберите файл!")

    def openmanager(self):
        # ОТКРЫВАЕТ МЕНЕДЖЕР НА ВТОРОЙ ВКЛАДКЕ
        self.tabWidget.setCurrentIndex(1)

    def openPreview(self):
        # ПЕРЕКЛЮЧАЕТ ВКЛАДКУ НА ВКЛАДКУ ПРЕДПРОСМОТРА
        self.tabWidget.setCurrentIndex(2)

    def openPreferences(self):
        # ОТКРЫВАЕТ НАСТРОЙКИ НА ЧЕТВЕРТОЙ ВКЛАДКЕ
        self.tabWidget.setCurrentIndex(3)

    def preview(self, it, colf):
        # ЗАГРУЖАЕТ ФАЙЛ В ОКНА ПРЕДПРОСМОТРА
        self.previewShowbox.clear()
        try:
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
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Не удалось открыть файл. Возможно он поврежден")

    def loadfromHst(self, it, col):
        # ЗАГРУЖАЕТ КОНФИГУРАЦИЮ ИЗ ОКНА КОНФИГУРАЦИЙ
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

        self.updateMain()

    # ФУНКЦИИ ОКНА КОНФИГУРАЦИИ
    def loadCfgFromList(self, it, col):
        # ЗАПОЛНЯЕТ ВСЕ ПОЗИЦИИ ОКНА КОНФИГУРАЦИИ ИЗ ФАЙЛА
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

        self.loadfromHst(it, col)

    def newConfig(self):
        # ОБНУЛЯЕТ ВСЕ ПОЛЯ КОНФИГУРАЦИИ
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
        # СОХРАНЯЕТ КОНФИГУРАЦИЮ
        self.savedflag = 0
        path = relativePath("config")
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
                                                'Выбрана конфигурация', f'Вы уверены, что хотите сохранить конфигурацию "{self.name}"', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
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

        path = relativePath("config")
        with open(path + '\\' + self.name + '.ini', 'w', encoding="utf-8-sig") as configfile:
            config.write(configfile)

        try:
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
            self.updateMain()

    def useConfig(self):
        # ИСПОЛЬЗУЕТ КОНФИГУРАЦИЮ
        self.saveConfig()
        if self.savedflag == 1:
            try:
                self.cfgPATH = relativePath(
                    'config',  self.name, '.ini')
                self.tabWidget.setCurrentIndex(0)
                self.updateMain()
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
                    f.close()

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
        #  УДАЛЯЕТ КОНФИГУРАЦИЮ
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
        self.updateMain()

    def renameConfig(self):
        # ПЕРЕИМЕНОВЫВАЕТ КОНФИГУРАЦИЮ
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
                self.updateMain()

                self.configbox.setCurrentItem(self.configbox.findItems(self.renameWintxt, Qt.Qt.MatchExactly)[
                    0])
                self.configbox.itemClicked.emit(
                    self.configbox.selectedItems()[0], 0)

            except:
                QtWidgets.QMessageBox.about(
                    self, "Внимание!", "Файл с таким именем уже существует!")

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
        f.close()

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

    def setName(self):
        if self.cfgCheck.isChecked():
            self.EXPORTCFGNAME = True
        else:
            self.EXPORTCFGNAME = False

    def setTime(self):
        if self.relativetime.isChecked():
            self.RELATIVETIME = True
        else:
            self.RELATIVETIME = False
        self.updateMain()

    def closeEvent(self, event):

        if self.exitCheck.isChecked():
            MsgBox = QtWidgets.QMessageBox.question(self,
                                                    'Завершение работы', 'Вы уверены, что хотите выйти?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if MsgBox == QtWidgets.QMessageBox.Yes:
                pass
            else:
                event.ignore()
                return
        try:
            if self.saveStgCheck.isChecked():

                if self.loadStgCheck.isChecked():
                    loadStg = 'True'
                else:
                    loadStg = 'False'

                if self.exitCheck.isChecked():
                    exitApp = 'True'
                else:
                    exitApp = 'False'

                if self.cfgCheck.isChecked():
                    cfgName = 'True'
                else:
                    cfgName = 'False'

                if self.relativetime.isChecked():
                    relativetime = 'True'
                else:
                    relativetime = 'False'

                settings = configparser.ConfigParser()
                settings['settings'] = {'saveStg': 'True', 'loadStg': loadStg,
                                        'exitApp': exitApp, 'cfgName': cfgName, 'relativeTime': relativetime}

                with open('settings.ini', 'w', encoding="utf-8-sig") as configfile:
                    settings.write(configfile)
            else:
                settings = configparser.ConfigParser()
                settings.read('settings.ini', encoding='utf-8-sig')
                configDict = settings._sections['settings']
                loadStg, exitApp, relativetime, cfgName = configDict['loadStg'], \
                    configDict['exitApp'],  configDict['relativetime'], configDict['cfgName']

                settings['settings'] = {'saveStg': 'False', 'loadStg': loadStg,
                                        'exitApp': exitApp, 'cfgName': cfgName, 'relativeTime': relativetime}

                with open('settings.ini', 'w', encoding="utf-8-sig") as configfile:
                    settings.write(configfile)
        except:
            QtWidgets.QMessageBox.about(
                self, "Ошибка!", "Ошибка при сохранении настроек!")
        event.accept()
