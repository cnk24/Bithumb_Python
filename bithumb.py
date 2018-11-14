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
        time = strftime("%Y-%m-%d", localtime())

        # 일별데이터 이므로 마지막 업데이트 day 와 현재의 day 비교
        if self.lastDay != time:
            self.lastDay = time
            self.oldData = pybithumb.get_ohlcv(ticker)

        return self.oldData

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
        price = pybithumb.get_current_price(ticker)
        return price

    # 모든 종목의 현재가 가져오기
    def getCurrentPriceAll(self):
        prices = dict()
        all = pybithumb.get_current_price('ALL')
        for ticker in self.tickers:
            newDict = {ticker: all[ticker]['closing_price']}
            prices.update(newDict)

        return prices

    # 종목의 호가정보 가져오기
    def getOrderBook(self, ticker):
        orderbook = pybithumb.get_orderbook(ticker)
        return orderbook

    # 이동 평균 구하기
    def CalMovingAverage(self, ticker, day):
        df = self.getBeforeData(ticker)
        ma = df['close'].rolling(window=day).mean()
        return ma

    # 상승장/하락장 판단하기
    def getMarketInfo(self, ticker, day):
        ma = self.CalMovingAverage(ticker, day)
        price = self.getCurrentPrice(ticker)
        last_ma = ma[-2]

        if price > last_ma:
            return True
        else:
            return False
    
