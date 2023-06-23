import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://kind.krx.co.kr/disclosure/todaydisclosure.do'
payload = {
    'method': 'searchTodayDisclosureSub',
    'currentPageSize': '15',
    'pageIndex': '1',
    'orderMode': '0',
    'orderStat': 'D',
    'forward': 'todaydisclosure_sub',
    'chose': 'S',
    'todayFlag': 'N',
    'selDate': '2022-07-27'
}

data = rq.post(url, data=payload)
html = BeautifulSoup(data.content, 'html.parser')

# print(html)

html_unicode = html.prettify()
tbl = pd.read_html(html.prettify())

print(tbl[0].head())
