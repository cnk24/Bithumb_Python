import pybithumb

class Cbithumb:
    tickers = []

    # init 모든 종목 가져오기
    def __init__(self):
        self.tickers = pybithumb.get_tickers()

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
    
