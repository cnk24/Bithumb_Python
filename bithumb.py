import pybithumb
from time import localtime, strftime

class Cbithumb:
    tickers = []

    lastDay = ""
    oldData = []

    # init 모든 종목 가져오기
    def __init__(self):
        self.tickers = pybithumb.get_tickers()

    # 과거 데이터 얻기
    def getBeforeData(self, ticker):
        try:
            time = strftime("%Y-%m-%d", localtime())

            # 일별데이터 이므로 마지막 업데이트 day 와 현재의 day 비교
            if self.lastDay != time:
                self.lastDay = time
                self.oldData = pybithumb.get_ohlcv(ticker)
            
            return self.oldData

        except Exception as ex:
            print('Error :', ex)
            return None

    # 전체 종목 이름 가져오기
    def getTickers(self):
        return self.tickers

    # 종목의 갯수 가져오기
    def getTickersLength(self):
        return len(self.tickers)
        
    # 종목 이름 가져오기
    def getTicker(self, no):
        return self.tickers[no]

    # 종목의 현재가 가져오기
    def getCurrentPrice(self, ticker):
        try:
            price = pybithumb.get_current_price(ticker)
            return price
        except Exception as ex:
            print('Error :', ex)
            return None

    # 모든 종목의 현재가 가져오기
    def getCurrentPriceAll(self):
        try:
            prices = dict()
            all = pybithumb.get_current_price('ALL')
            for ticker in self.tickers:
                newDict = {ticker: all[ticker]['closing_price']}
                prices.update(newDict)
            return prices
        except Exception as ex:
            print('Error :', ex)
            return None

    # 종목의 호가정보 가져오기
    def getOrderBook(self, ticker):
        try:
            orderbook = pybithumb.get_orderbook(ticker)
            return orderbook
        except Exception as ex:
            print('Error :', ex)
            return None

    # 이동 평균 구하기
    def CalMovingAverage(self, ticker, day):
        df = self.getBeforeData(ticker)
        ma = df['close'].rolling(window=day).mean()
        return ma

    # 변동성 돌파 전략 구하기
    def CalTarget(self, ticker):
        df = self.getBeforeData(ticker)
        yesterday = df.iloc[-2]
 
        today_open = float(yesterday['close'])
        yesterday_high = float(yesterday['high'])
        yesterday_low = float(yesterday['low'])
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        return target

    # 상승장/하락장 판단하기
    def getMarketInfo(self, ticker, day):
        ma = self.CalMovingAverage(ticker, day)
        price = self.getCurrentPrice(ticker)
        last_ma = ma[-2]

        if price > last_ma:
            return True
        else:
            return False
    




'''
[변동성 돌파 전략]
1) 가격 변동폭 구하기 : 투자하려는 가상화폐의 전일 고가(high)에서 전일 저가(low)를 빼서 가상화폐의 가격 변동폭을 구합니다.
2) 매수 기준: 당일 시간에서 (변동폭 * 0.5) 이상 상승하면 해당 가격에 바로 매수한다.
3) 매도 기준: 당일 종가에 매도한다.
'''


