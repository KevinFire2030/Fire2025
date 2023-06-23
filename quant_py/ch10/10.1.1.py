import requests as rq
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/sise_deposit.nhn'
data = rq.get(url)
data_html = BeautifulSoup(data.content)
parse_day = data_html.select_one(
    'div.subtop_sise_graph2 > ul.subtop_chart_note > li > span.tah').text

print(parse_day)

import re

biz_day = re.findall('[0-9]+', parse_day)
biz_day = ''.join(biz_day)

print(biz_day)

