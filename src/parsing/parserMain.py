import requests
from bs4 import BeautifulSoup
import datetime
from parsing import parserFunc as p
from PyQt5 import QtCore
import itertools
import pandas as pd


class Parser(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    done = QtCore.pyqtSignal(int)

    def __init__(self, maxPage, topic, text, strtDate, endDate, author, adressed, expanded):
        QtCore.QThread.__init__(self)
        self.maxPage = maxPage
        self.topic = topic
        self.text = text
        self.strtDate = strtDate
        self.endDate = endDate
        self.author = author
        self.adressed = adressed
        self.expanded = expanded

    def __del__(self):
        self.wait()

    def run(self):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

        s = requests.session()
        s.headers.update(headers)

        page = 0
        records = []

        while page < self.maxPage:
            data = p.load_url(self.text, self.topic, self.strtDate, self.endDate,
                              page, self.author, self.adressed, self.expanded, s)
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
        self.listToSCV(records, self.expanded)
        self.progress.emit(page + 1)
        self.done.emit(1)

    def listToSCV(self, records, expanded):
        if expanded == "False":
            df = pd.DataFrame(records, columns=[
                'name', 'msg', 'time', 'link', 'length'])
            df['time'] = pd.to_datetime(df['time'])

            scv_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            df.to_csv('./export/' + scv_name + '.csv',
                      index=False, encoding='utf-8-sig')
        else:
            df = pd.DataFrame(records, columns=[
                'name', 'msg', 'time', 'link', 'length', 'expmsg'])
            df['time'] = pd.to_datetime(df['time'])

            scv_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            df.to_csv('./export/' + scv_name + '.csv',
                      index=False, encoding='utf-8-sig')
