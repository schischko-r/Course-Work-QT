from bs4 import BeautifulSoup
import urllib.parse


def load_url(page, text, topic, strtDate, endDate, author, adressed, expanded, session):
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
        url = f"https://vif2ne.org/nvk/forum/0/index/list?text={text}&topic={topic}&fday={fday}&fmonth={fmonth}&fyear={fyear}&tday={tday}&tmonth={tmonth}&tyear={tyear}&wide={expanded}&author={author}&toauthor={adressed}&from={str(strtdoc)}&to={str(enddoc)}"
    else:
        url = f"https://vif2ne.org/nvk/forum/0/index/list?text={text}&topic={topic}&fday={fday}&fmonth={fmonth}&fyear={fyear}&tday={tday}&tmonth={tmonth}&tyear={tyear}&author={author}&toauthor={adressed}&from={str(strtdoc)}&to={str(enddoc)}"

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

    i = 0
    for table_i in tables:
        try:
            i += 1
            if i % 2 != 0:
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
    i = 0
    for table_i in expMsg:
        try:
            try:
                nickname = table_i.find('b').text
                message = table_i.find('a').text
                tmpdict1 = {'name': nickname, 'msg': message}
            except:
                pass
            else:
                i = 0
            i += 1
            if i % 3 == 0:
                expanded = table_i.text
                tmpdict3 = {'expmsg': expanded}

                tmpdict = {**tmpdict1, **tmpdict2, **tmpdict3}
                parsed.append(tmpdict)
                tmpdict = {}
            if i % 2 == 0:
                dateTime = table_i.find('td').text
                textlink = "https://vif2ne.org/nvk/forum/" + \
                    table_i.find('a')['href'][3:]
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
