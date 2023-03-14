# Про этот проект

Цель данной работы — создать оконное приложение для парсинга форума. В работе используются запросы через поисковую систему самого форума, после чего полученная выдача обрабатывается через bs4. Оконное приложение написано на QT.

## В работе использовались
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)

## Примеры работы

- Входные параметры:
```ini
text = "Буран"
author = 
receiver = 
topic = Все
fdate = 01-01-2000
tdate = 17-06-2020
last_used = 2020-06-17 12:27:01
expanded = False
```
- Выходные параметры:
```csv
Mike,"Re: Mike, я especially for you",2000-06-14 23:20:00,https://vif2ne.org/nvk/forum/archive/words/1153?text=,2.50K
Илья Григоренко,"Ну-с, начнем? : )",2000-06-15 00:33:42,https://vif2ne.org/nvk/forum/archive/words/2309?text=,9.95K
...
```