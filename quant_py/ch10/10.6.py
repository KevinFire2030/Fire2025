
# 패키지 불러오기

import pandas as pd
import numpy as np
import sqlite3

# DB 연결
con = sqlite3.connect("kor_ticker.db")
con2 = sqlite3.connect("kor_fs.db")

# 티커 리스트 불러오기
ticker_list = pd.read_sql("""
select * from kor_ticker
where 기준일 = (select max(기준일) from kor_ticker) 
and 종목구분 = '보통주';
""", con)

# 분기 재무제표 불러오기
kor_fs = pd.read_sql("""
select * from kor_fs
where 공시구분 = 'q'
and 계정 in ('당기순이익', '자본', '영업활동으로인한현금흐름', '매출액');
""", con2)



# TTM 구하기
kor_fs = kor_fs.sort_values(['종목코드', '계정', '기준일'])
kor_fs['ttm'] = kor_fs.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(
    window=4, min_periods=4).sum()['값']

# 자본은 평균 구하기
kor_fs['ttm'] = np.where(kor_fs['계정'] == '자본', kor_fs['ttm'] / 4,
                         kor_fs['ttm'])
kor_fs = kor_fs.groupby(['계정', '종목코드']).tail(1)

kor_fs_merge = kor_fs[['계정', '종목코드',
                       'ttm']].merge(ticker_list[['종목코드', '시가총액', '기준일']],
                                     on='종목코드')
kor_fs_merge['시가총액'] = kor_fs_merge['시가총액'].astype(float) / 100000000

kor_fs_merge['value'] = kor_fs_merge['시가총액'] / kor_fs_merge['ttm']
kor_fs_merge['value'] = kor_fs_merge['value'].round(4)
kor_fs_merge['지표'] = np.where(
    kor_fs_merge['계정'] == '매출액', 'PSR',
    np.where(
        kor_fs_merge['계정'] == '영업활동으로인한현금흐름', 'PCR',
        np.where(kor_fs_merge['계정'] == '자본', 'PBR',
                 np.where(kor_fs_merge['계정'] == '당기순이익', 'PER', None))))

kor_fs_merge.rename(columns={'value': '값'}, inplace=True)
kor_fs_merge = kor_fs_merge[['종목코드', '기준일', '지표', '값']]
kor_fs_merge = kor_fs_merge.replace([np.inf, -np.inf, np.nan], None)

# DB에 자장하기
con = sqlite3.connect("stock.db")
kor_fs_merge.to_sql('kor_value', con, if_exists='replace')

# 배당수익률 역시 kor_value 테이블에 upsert 방식으로 저장한 후, DB와의 연결을 종료한다.
ticker_list['값'] = ticker_list['주당배당금'].astype(float) / ticker_list['종가'].astype(float)
ticker_list['값'] = ticker_list['값'].round(4)
ticker_list['지표'] = 'DY'
dy_list = ticker_list[['종목코드', '기준일', '지표', '값']]
dy_list = dy_list.replace([np.inf, -np.inf, np.nan], None)
dy_list = dy_list[dy_list['값'] != 0]


dy_list.to_sql('kor_value', con, if_exists='append')

print('ok')