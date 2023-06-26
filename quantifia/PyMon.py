
import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame
import datetime
import pandas_datareader.data as web
import pandas as pd
import numpy as np
import sqlite3

MARKET_KOSPI   = 0
MARKET_KOSDAQ  = 10

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        #self.get_code_list()
        self.krx_codes= self.read_krx_code()

        print('ok')

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=' \
              'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)

        krx['category'] = np.where(krx['company'].str.contains('스팩|제[0-9]+호'), '스팩',
                                      np.where(krx['code'].str[-1:] != '0', '우선주',
                                               np.where(krx['company'].str.endswith('리츠'), '리츠',
                                                        '보통주')))

        print(krx['category'].value_counts())

        # 감리구분
        """
        GetMasterConstruction(
            BSTR
        strCode // 종목코드
        }
        """

        krx['state'] = ''

        for i, code in enumerate(krx['code']):
            krx['state'][i] = self.kiwoom.get_master_construction(code)

        # DB에 저장
        con = sqlite3.connect("krx_code.db")
        krx.to_sql('krx_code', con, if_exists='replace')

        # 보통주만 리턴

        krx = krx.where((krx['category']=='보통주') & (krx['state']=='정상'))

        krx = krx.dropna()
        krx.reset_index(drop=True, inplace=True)

        #return krx.where(krx['category']=='보통주')

        return krx

    def get_ohlcv(self, code, end):

        """
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.ohlcv['date'])
        """
        #print(code)

        try:

            df = web.DataReader(code, 'naver', end=end)

            df['Open'] = df['Open'].astype(float)
            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            df['Close'] = df['Close'].astype(float)
            df['Volume'] = df['Volume'].astype(int)

            return df

        except:

            print(f"read error: {code}")

            return False



    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)

        volumes = df['Volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol > avg_vol20 * 10:
            return True

    def update_buy_list(self, buy_list):
        f = open("buy_list.txt", "wt", encoding='UTF8')
        for code in buy_list:
            f.writelines(["매수;", code, ";시장가;10;0;매수전\n"])
        f.close()

    def run(self):
        buy_list = []
        num = len(self.krx_codes)
        #codes = self.krx_codes['code']

        for i, code in enumerate(self.krx_codes['code']):

            #time.sleep(1)

            #print(code)

            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                print(f"종목코드: {code}, 종목명: {self.krx_codes['company'][i]}")
                buy_list.append(code)

        self.update_buy_list(buy_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()

