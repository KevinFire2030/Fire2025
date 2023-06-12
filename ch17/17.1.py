import pandas as pd
import pandas_datareader.data as web
import sqlite3

df = web.DataReader('005930', 'naver', '2023-01-01', '2023-06-09')

con = sqlite3.connect("kospi.db")
df.to_sql('005930', con, if_exists='replace')

readed_df = pd.read_sql("SELECT * FROM '005930'", con, index_col = 'Date')
print(readed_df)