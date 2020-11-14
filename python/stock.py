import requests
import sys
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs


class Stock:
    url = 'http://finance.yahoo.com/quote/'
    financial_url = 'https://finance.yahoo.com/quote/{}/financials?p={}'
    properties = {
        'company_name': ('h1', {'class': 'D(ib) Fz(18px)'}),
        'price': ('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}),
    }

    def __init__(self, ticker):
        self.ticker = ticker
        self.data = self.get_info()
        self.set_property('company_name')
        self.set_property('price')

    # 검색한 종목 파싱하기
    def get_info(self):
        try:
            result = requests.get(self.url + self.ticker)
            bs_obj = bs(result.content, "html.parser")
        except HTTPError:
            return None
        except AttributeError:
            return None
        return bs_obj

    # 검색한 종목 회사명 가져오기
    def set_property(self, property_name):
        if property_name not in self.properties:
            return None
        setattr(self, property_name, None)
        try:
            setattr(self, property_name, self.data.find(*self.properties[property_name]).text)
        except:
            pass

    def refresh_price(self):
        self.data = self.get_info()
        self.set_property('price')


    # 검색한 종목 financial 파싱
    # def get_info_financial(self):
    #     url = self.financial_url.format(self.ticker, self.ticker)
    #     try:
    #         result = requests.get(url)
    #         bs_obj = bs(result.content, "html.parser")
    #     except HTTPError:
    #         return None
    #     except AttributeError:
    #         return None
    #     return bs_obj
    #
    # # 재무제표 매출 조회
    # def get_this_year_total_revenue():
    #     try:
    #         this_year_date = stock1_info_financial.find('div', {
    #             'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(ib) Fw(b)',
    #             })
    #         this_year_total_revenue = stock1_info_financial.find('div', {
    #             'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(tbc)',
    #             'data-reactid' : '86'})
    #     except AttributeError:
    #         return None
    #     return this_year_date, this_year_total_revenue
    #
    # def get_last_year_total_revenue():
    #     try:
    #         last_year_date = stock1_info_financial.find('div', {
    #             'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg D(ib) Fw(b) Bgc($lv1BgColor)',
    #             })
    #         last_year_total_revenue = stock1_info_financial.find('div', {
    #             'class': 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(140px)--pnclg Bgc($lv1BgColor) fi-row:h_Bgc($hoverBgColor) D(tbc)',
    #             'data-reactid' : '88'})
    #     except AttributeError:
    #         return None
    #     return last_year_date, last_year_total_revenue



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


    # 검색한 주식의 정보 저장 ㅣ info(파싱), company_name(회사명), now_price(현재 주가)
    stock1 = Stock(user_ticker)


    # 출력 부분 ㅣ None 값일 경우 조회 실패 메시지 출력
    if stock1.company_name:
        print(stock1.company_name + " 주식의 현재 주가는 : " + stock1.price + " 입니다.")
    else:
        print('입력한 코드는 종목 코드가 아닙니다.')

# stock1_info_financial = stock1.get_info_financial()
# this_year_date, this_year_total_revenue = Stock.get_this_year_total_revenue()
# last_year_date, last_year_total_revenue = Stock.get_last_year_total_revenue()
#
#
# if this_year_date and this_year_total_revenue is None:
#     print('입력한 코드는 종목 코드가 아닙니다.')
# else:
#     print("Total Revenue")
#     print(this_year_date.text + " : " + this_year_total_revenue.text)
#     print(last_year_date.text + " : " + last_year_total_revenue.text)

