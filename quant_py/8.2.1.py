import requests as rq

from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'
quote = rq.get(url)

#print(quote)


quote_html = BeautifulSoup(quote.content, 'html.parser')
#print(quote_html.head())

quote_div = quote_html.find_all('div', class_='quote')

#print(quote_div[0])


quote_span = quote_div[0].find_all('span', class_='text')

#print(quote_span)


#[print(i.find_all('span', class_ ='text')[0].text) for i in quote_div]



quote_text = quote_html.select('div.quote > span.text')

quote_text_list = [i.text for i in quote_text]

for i in quote_text:
    print (i.text)

#print(quote_text_list)


quote_author = quote_html.select('div.quote > span > small.author')
quote_author_list = [i.text for i in quote_author]

#print(quote_author_list)

for i in quote_author:
    print (i.text)




