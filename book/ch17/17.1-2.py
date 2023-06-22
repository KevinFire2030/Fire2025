import pandas_datareader.data as web

df = web.DataReader('005930', 'naver', start='2023-01-01', end='2023-06-09')

print(df)