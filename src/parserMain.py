import requests
from bs4 import BeautifulSoup
import datetime
import parserFunc as p
import itertools
import pandas as pd


def create_record(maxPage, topic, text, strtDate, endDate, author, adressed, expanded):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

    s = requests.session()
    s.headers.update(headers)

    page = 0
    records = []

    while page < maxPage:
        data = p.load_url(text, topic, strtDate, endDate,
                          page, author, adressed, expanded, s)
        if p.contain_forum_data(data):
            soup = BeautifulSoup(data, 'html.parser')
            if expanded == "False":
                tables = soup.find_all('table')
                records.append(p.getData(tables))
            else:
                expMsg = soup.find_all(['table', 'i'])
                records.append(p.getMsg(expMsg))

            page += 1
        else:
            break

    records = list(itertools.chain.from_iterable(records))
    listToSCV(records, expanded)


def listToSCV(records, expanded):
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
