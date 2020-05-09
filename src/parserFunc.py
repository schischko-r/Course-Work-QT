from bs4 import BeautifulSoup
import urllib.parse
from tkinter import messagebox

HOST = 'https://vif2ne.org/nvk/forum/'                       # ХОСТ
LIST = '0/index/list?text='                                  # ЛИСТ
TOPIC = '&topic='                                            # Рубрика
FDAY = '&fday='                                              # НАЧАЛЬНЫЙ ДЕНЬ
FMONTH = '&fmonth='                                          # НАЧАЛЬНЫЙ МЕСЯЦ
FYEAR = '&fyear='                                            # НАЧАЛЬНЫЙ ГОД
TDAY = '&tday='                                              # КОНЕЧНЫЙ ДЕНЬ
TMONTH = '&tmonth='                                          # КОНЕЧНЫЙ МЕСЯЦ
TYEAR = '&tyear='                                            # КОНЕЧНЫЙ ГОД
AUTHOR = '&author='                                          # АВТОР
TOAUTHOR = '&toauthor='                                      # АДРЕСАТ
FROM = '&from='                                              # ПЕРВАЯ СТРАНИЦА
TO = '&to='                                                  # ПОСЛЕДНЯЯ СТРАНИЦА
WIDE = '&wide='


def load_url(text, topic, strtDate, endDate, page, author, adressed, expanded, session):
    [fday, fmonth, fyear] = strtDate.split("-")
    [tday, tmonth, tyear] = endDate.split("-")

    strtdoc = 1 + int(page) * 100
    enddoc = (int(page) + 1) * 100
    text = encodestr(text)
    if topic == 'Все':
        topic = ""
    else:
        topic = encodestr(topic)
    topic = topic.replace("%", "")
    author = encodestr(author)
    adressed = encodestr(adressed)
    if expanded != "False":
        expanded = "on"
        url = HOST + LIST + text + TOPIC + topic + FDAY + fday + FMONTH + fmonth + FYEAR + fyear + TDAY \
            + tday + TMONTH + tmonth + TYEAR + tyear + WIDE + expanded + AUTHOR + author + TOAUTHOR + adressed \
            + FROM + str(strtdoc) + TO + str(enddoc)
    else:
        url = HOST + LIST + text + TOPIC + topic + FDAY + fday + FMONTH + fmonth + FYEAR + fyear + TDAY \
            + tday + TMONTH + tmonth + TYEAR + tyear + AUTHOR + author + TOAUTHOR + adressed \
            + FROM + str(strtdoc) + TO + str(enddoc)

    request = session.get(url)
    return request.text


def contain_forum_data(text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        line = soup.find('div', id='wrapper').find_all('table')
        return line is not None
    except:
        return


def getData(tables):
    parsed = []

    iter = 0
    for table_i in tables:
        try:
            iter += 1
            if iter % 2 != 0:
                dateTime = table_i.find('td').text
                textlink = HOST + table_i.find('a')['href'][3:]
                textlen = table_i.find_all('td')[1].text[6:]

                tmpdict2 = {'time': dateTime,
                            'link': textlink, 'length': textlen}
                tmpdict = {**tmpdict1, **tmpdict2}
                parsed.append(tmpdict)
                tmpdict = {}
            else:
                nickname = table_i.find('b').text
                message = table_i.find('a').text
                tmpdict1 = {'name': nickname, 'msg': message}
        except:
            pass
    return parsed


def getMsg(expMsg):
    parsed = []

    for table_i in expMsg:
        try:
            try:
                nickname = table_i.find('b').text
                message = table_i.find('a').text
                tmpdict1 = {'name': nickname, 'msg': message}
            except:
                pass
            else:
                iter = 0
            iter += 1
            if iter % 3 == 0:
                expanded = table_i.text
                tmpdict3 = {'expmsg': expanded}

                tmpdict = {**tmpdict1, **tmpdict2, **tmpdict3}
                parsed.append(tmpdict)
                tmpdict = {}
            if iter % 2 == 0:
                dateTime = table_i.find('td').text
                textlink = HOST + table_i.find('a')['href'][3:]
                textlen = table_i.find_all('td')[1].text[6:]

                tmpdict2 = {'time': dateTime,
                            'link': textlink, 'length': textlen}
            else:
                nickname = table_i.find('b').text
                message = table_i.find('a').text
                tmpdict1 = {'name': nickname, 'msg': message}

        except:
            pass
    return parsed


def encodestr(text):
    text = urllib.parse.quote_plus(text.encode('cp1251'))
    return text
