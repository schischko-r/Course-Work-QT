import requests
from bs4 import BeautifulSoup
import datetime
from parsing import parserFunc as p
from PyQt5 import QtCore
import os
import itertools
import pandas as pd


def relativePath(folder, name="", ftype=""):
    # ФУНКЦИЯ ВОЗВРАЩАЕТ ОТНОСИТЕЛЬНЫЙ ПУТЬ К ФАЙЛУ ИЛИ ПАПКЕ
    path = os.path.abspath(os.path.join(os.path.dirname(
        "__file__"),  folder) + "\\" + name + ftype)
    return path


class Parser(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    done = QtCore.pyqtSignal(int)

    def __init__(self, filename, maxPage, topic, text, strtDate, endDate, author, adressed, expanded, EXPORTCFGNAME):
        QtCore.QThread.__init__(self)

        self.filename = filename
        self.maxPage = maxPage
        self.topic = topic
        self.text = text
        self.strtDate = strtDate
        self.endDate = endDate
        self.author = author
        self.adressed = adressed
        self.expanded = expanded
        self.EXPORTCFGNAME = EXPORTCFGNAME

    def stop(self):
        self.terminate()

    def run(self):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

        s = requests.session()
        s.headers.update(headers)

        page = 0
        records = []

        while page < self.maxPage:
            data = p.load_url(page, self.text, self.topic, self.strtDate, self.endDate,
                              self.author, self.adressed, self.expanded, s)
            if p.contain_forum_data(data):
                soup = BeautifulSoup(data, 'html.parser')
                if self.expanded == "False":
                    tables = soup.find_all('table')
                    records.append(p.getData(tables))
                else:
                    expMsg = soup.find_all(['table', 'i'])
                    records.append(p.getMsg(expMsg))

                page += 1
                self.sleep(1)
                self.progress.emit(page)
            else:
                break

        records = list(itertools.chain.from_iterable(records))
        self.listToCSV(records, self.expanded)
        self.progress.emit(page + 1)
        self.done.emit(1)

    def listToCSV(self, records, expanded):
        if self.EXPORTCFGNAME == False:
            csv_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        else:
            i = 0
            if os.path.exists(relativePath('export', self.filename, ".csv")):
                i += 1
            while os.path.exists(relativePath('export', f"{self.filename} ({i})", ".csv")):
                i += 1
            if i != 0:
                csv_name = f"{self.filename} ({i})"
            else:
                csv_name = self.filename

        if expanded == "False":
            df = pd.DataFrame(records, columns=[
                'name', 'msg', 'time', 'link', 'length'])
            df['time'] = pd.to_datetime(df['time'])

            df.to_csv(relativePath('export', csv_name, ".csv"),
                      index=False, encoding='utf-8-sig')
        else:
            df = pd.DataFrame(records, columns=[
                'name', 'msg', 'time', 'link', 'length', 'expmsg'])
            df['time'] = pd.to_datetime(df['time'])

            df.to_csv(relativePath('export', csv_name, ".csv"),
                      index=False, encoding='utf-8-sig')
