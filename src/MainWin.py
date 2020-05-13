import sys
from PyQt5 import QtWidgets, Qt, QtCore

from designer import MainDesigner
from ConfigWin import ConfigWin
from RenameWin import RenameWin
from PreviewWin import PreviewWin

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


class MainWindow(QtWidgets.QMainWindow, MainDesigner.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.populateExport()
        self.managerBtn.clicked.connect(self.openmanager)
        self.startBtn.clicked.connect(self.startParsing)

        self.deleteBtn.clicked.connect(self.deleteExport)
        self.renameBtn.clicked.connect(self.renameExport)
        self.expandedBtn.clicked.connect(self.openPreview)

        self.exportbox.itemClicked.connect(self.preview)
        self.configFullListbox.itemClicked.connect(self.loadfromHst)

    def openmanager(self):
        self.PATH = ""
        manager = ConfigWin()
        if manager.exec_():
            self.cfgPATH = manager.PATH
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
                for i in range(self.configshow.columnCount()):
                    self.configshow.resizeColumnToContents(i)
                self.guidelbl.setText("Выбрано успешно!")
            except:
                QtWidgets.QMessageBox.about(
                    self, "Внимание!", "Конфигурация не выбрана!")

        self.populateExport()

    def populateExport(self):
        def convert_size(size_bytes):
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])

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
            date = self.deltatime(configDict['last_used'])
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

            self.progresslbl.setText("Конфигурация загружена успешно!")
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
        try:
            previewWin = PreviewWin(relativePath(
                'export',  self.exportbox.selectedItems()[0].text(0), '.csv'))
            if previewWin.exec_():
                pass
        except:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Выберите файл!")

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

    def deltatime(self, time):
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
