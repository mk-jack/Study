import requests
import sys
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
import sqlite3
import datetime

# DB 생성 및 Auto Commit
conn = sqlite3.connect('./resource/stock_info.db', isolation_level=None)

# Cursor 연결
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS stock_info(id INTEGER PRIMARY KEY AUTOINCREMENT, date text, search text, company text, price INTEGER)")

class Stock:
    url = 'http://finance.yahoo.com/quote/'
    financial_url = 'https://finance.yahoo.com/quote/{}/financials?p={}'
    properties = {
        'company_name': ('h1', {'class': 'D(ib) Fz(18px)'}),
        'price': ('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}),
        'this_year_date': ('div', {'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(ib) Fw(b)'}),
        'last_year_date': ('div', {'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)'}),
        'this_year_total_revenue': ('div', {'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)','data-reactid' : '86'}),
        'last_year_total_revenue': ('div', {'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)', 'data-reactid' : '88'}),
    }

    def __init__(self, ticker):
        self.ticker = ticker
        self.data_summary = self.get_info_summary()
        self.data_financial = self.get_info_financial()
        self.set_property_summary('company_name')
        self.set_property_summary('price')
        self.set_property_financial('this_year_date')
        self.set_property_financial('this_year_total_revenue')
        self.set_property_financial('last_year_date')
        self.set_property_financial('last_year_total_revenue')

    # 검색한 종목 파싱하기
    def get_info_summary(self):
        try:
            result = requests.get(self.url + self.ticker)
            bs_obj = bs(result.content, "html.parser")
        except HTTPError:
            return None
        except AttributeError:
            return None
        return bs_obj

    def get_info_financial(self):
        url = self.financial_url.format(self.ticker, self.ticker)
        try:
            result = requests.get(url)
            bs_obj = bs(result.content, "html.parser")
        except HTTPError:
            return None
        except AttributeError:
            return None
        return bs_obj

    # 검색한 종목 회사명 가져오기
    def set_property_summary(self, property_name):
        if property_name not in self.properties:
            return None
        setattr(self, property_name, None)
        try:
            setattr(self, property_name, self.data_summary.find(*self.properties[property_name]).text)
        except:
            pass

    def set_property_financial(self, property_name):
        if property_name not in self.properties:
            return None
        setattr(self, property_name, None)
        try:
            setattr(self, property_name, self.data_financial.find(*self.properties[property_name]).text)
        except:
            pass

    def refresh_price(self):
        self.data = self.get_info()
        self.set_property('price')

if __name__ == '__main__':
    # 입력 부분 ㅣ 공백 입력 또는 CTRL+C 등 예외 처리 적용
    while True:
        try:
            print("""
정확한 종목 코드를 입력해주세요 :
[예시] 미국주식(티커) : AAPL ㅣ 코스피(코드.KS) : 005930.KS ㅣ 코스닥(코드.KQ) : 293490.KQ)
            """)
            user_ticker = input().replace(' ', '')
            if user_ticker == '':
                raise ValueError
            break
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print('입력한 코드는 종목 코드가 아닙니다.')


    # 검색한 주식의 정보 저장 ㅣ info(파싱)
    # company_name(회사명), price(현재 주가), this_year_date, last_year_date, this_year_total_revenue, last_year_total_revenue
    stock1 = Stock(user_ticker)

    # 기록 DB 삽입
    cursor.execute("INSERT INTO stock_info('date', 'search', 'company', 'price') VALUES (?, ?, ?, ?)",
                   (datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S'), user_ticker, stock1.company_name, stock1.price))

    # 출력 부분 ㅣ None 값일 경우 조회 실패 메시지 출력
    if stock1.company_name:
        print(stock1.company_name + " 주식의 현재 주가는 : " + stock1.price + " 입니다.")
        print()
    else:
        print('입력한 코드는 종목 코드가 아닙니다.')

    if stock1.this_year_date:
        print("[Financials Information]")
        print("Total Revenue")
        print(stock1.this_year_date + " : " + stock1.this_year_total_revenue)
        print(stock1.last_year_date + " : " + stock1.last_year_total_revenue)
    else:
        print('조회되는 정보가 없습니다.')


