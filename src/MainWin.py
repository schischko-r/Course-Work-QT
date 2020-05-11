import sys
from PyQt5 import QtWidgets
from PyQt5 import Qt

from designer import MainDesigner
from ConfigWin import ConfigWin
from RenameWin import RenameWin

from parsing import parserMain

import configparser
import threading
import requests
import datetime
import glob
import math
import os


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
                self.configshow.resizeColumnToContents(0)
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

    def startParsing(self):
        try:
            r = requests.head("https://vif2ne.org/")
            pass
        except requests.ConnectionError:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Проверьте ваше подключение к интернету и доступность сайта")
            return

        if self.configshow.topLevelItemCount() == 0:
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Вы не выбрали конфигурацию!")
            return
        maxPage = self.lineEdit.text()
        if maxPage == "":
            QtWidgets.QMessageBox.about(
                self, "Внимание!", "Укажите количество страниц!")
            return

        config = configparser.ConfigParser()
        config.read(self.cfgPATH, encoding='utf-8-sig')
        filename = self.cfgPATH.split("\\")
        filename = filename[len(filename) - 1].split('.')[0]
        configDict = config._sections['config']
        text, topic, strtDate, endDate, author, adressed, expanded = configDict['text'], configDict[
            'topic'], configDict['fdate'], configDict['tdate'],  configDict['author'],  configDict['receiver'], configDict['expanded']

        RECWRITING = threading.Thread(target=parserMain.create_record, args=(
            int(maxPage), topic, text, strtDate, endDate, author, adressed, str(expanded)))
        RECWRITING.start()
        RECWRITING.join()

        config = configparser.ConfigParser()
        config.read(self.cfgPATH, encoding='utf-8-sig')
        last_used = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        config['config'] = {'text': text, 'author': author,
                            'receiver': adressed, 'topic': topic, 'fdate': strtDate, 'tdate': endDate, 'last_used': last_used, 'expanded': expanded}
        with open(self.cfgPATH, "w", encoding='utf-8-sig') as configfile:
            config.write(configfile)
        self.populateExport()

    def deleteExport(self):
        for item in self.exportbox.selectedItems():
            filepath = os.path.abspath(os.path.join(os.path.dirname(
                "__file__"),  'export')) + "\\" + item.text(0) + ".csv"
            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                print("The file does not exist")
        self.populateExport()

    def renameExport(self):
        rename = RenameWin()
        if rename.exec_():
            try:
                self.newName = os.path.abspath(os.path.join(os.path.dirname(
                    "__file__"),  'export')) + "\\" + rename.text
                current = os.path.abspath(os.path.join(os.path.dirname(
                    "__file__"),  'export')) + "\\" + self.exportbox.selectedItems()[0].text(0) + ".csv"
                os.rename(current, self.newName)
                self.populateExport()
                self.previewShowbox.clear()
            except:
                messagebox.showinfo(
                    "Внимание!", "Ошибка!")

    def openPreview(self):
        pass

    def preview(self):
        pass

    def loadfromHst(self):
        pass

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
