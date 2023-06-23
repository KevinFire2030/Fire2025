import requests as rq
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'
data = rq.get(url)
html = BeautifulSoup(data.content, 'html.parser')
html_select = html.select('dl > dd.articleSubject > a')

html_select[0:3]


[print(i['title']) for i in html_select]