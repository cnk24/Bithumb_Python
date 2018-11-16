import pybithumb
import pandas as pd
from time import localtime, strftime



'''
[변동성 돌파 전략]
1) 가격 변동폭 구하기 : 투자하려는 가상화폐의 전일 고가(high)에서 전일 저가(low)를 빼서 가상화폐의 가격 변동폭을 구합니다.
2) 매수 기준: 당일 시간에서 (변동폭 * 0.5) 이상 상승하면 해당 가격에 바로 매수한다.
3) 매도 기준: 당일 종가에 매도한다.

MACD 란?
MACD는 Moving Average Convergence Divergence의 약어로써, 이동평균선(MA)이 수렴과 발산을 반복한다 는 원리를 이용해 단기이동평균선(12)과 장기이동평균선(26) 사이의 관계를 보여주는 Gerald Appel이 개발한 지표다. MACD에서 단기이동평균으로는 12일, 장기이동평균으로는 26일을 사용하고, MACD의 9일 이동평균선을 Signal이라고 하고, MACD와 Signal의 차이를 Oscillator라고한다.

MACD: 단기이동평균(12)와 장기이동평균선(26)의 차이값
    - 보통 주식HTS에서는 이값을 파라미터 값으로써 조정할 수 있게 되어있다. 우리나라 주식시장에 맞는 5일과 20일로 대체해서 사용하기도 한다.
Signal: MACD의 9일 이동평균값
    - 일반적으로 9일을 설정하여 MACD의 값들을 완충 및 일반화 하는 역할을 한다.
Oscillator: MACD값과 Signal값의 차이
    - MACD의 값이 Signal값보다 클때는 양의 막대, 작을 때는 음의 막대가 그려진다.
'''



class Cbithumb:
    tickers = []
    oldData = dict()

    # init 모든 종목 가져오기
    def __init__(self):
        self.tickers = pybithumb.get_tickers()
        for ticker in self.tickers:
            newDict = {ticker: None}
            self.oldData.update(newDict)

    # 과거 데이터 얻기
    def getBeforeData(self, ticker):
        try:
            time = strftime("%Y-%m-%d", localtime())

            # 일별데이터 이므로 마지막 업데이트 day 와 현재의 day 비교
            if self.oldData[ticker] is None:
                self.oldData[ticker] = pybithumb.get_ohlcv(ticker)
            else:
                df = self.oldData[ticker]
                timestamp = df.index[-1]
                lastTime = timestamp.strftime("%Y-%m-%d")
                if lastTime != time:
                    self.oldData[ticker] = pybithumb.get_ohlcv(ticker)
            
            return self.oldData[ticker]

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
    def CalMovingAverage(self, ticker, t):
        df = pd.DataFrame(self.getBeforeData(ticker))
        ma = df.close.ewm(span=t).mean()
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
    def getMarketInfo(self, ticker, t):
        ma = self.CalMovingAverage(ticker, t)
        price = self.getCurrentPrice(ticker)
        last_ma = ma[-2]

        if price > last_ma:
            return True
        else:
            return False


    # MACD 지표 구하기
    def getMACD(self, ticker, short=12, long=26, t=9):
        df = pd.DataFrame(self.getBeforeData(ticker))

        # 단기(12) EMA(지수이동평균)
        ma_short = df.close.ewm(span=short).mean()
        # 장기(26) EMA(지수이동평균)
        ma_long = df.close.ewm(span=long).mean()

        macd = ma_short - ma_long

        # Signal
        macds = macd.ewm(span=t).mean()
        # Oscillator
        macdo = macd - macds

        df = df.assign(macd=macd, macds=macds, macdo=macdo).dropna()
        return df

    # MACD 차트 그리기
    #def plotMACD(self, ticker):
    #    df = self.getMACD(ticker)

    #    macd = go.Scatter(x=df.index.date, y=df['macd'], name="MACD")
    #    signal = go.Scatter(x=df.index.date, y=df['macds'], name="Signal")
    #    oscillator = go.Bar(x=df.index.date, y=df['macdo'], name="oscillator")
    #    trade_volume = go.Bar(x=df.index.date, y=df['volume'], name="volume")

    #    data = [macd, signal, oscillator]

    #    layout = go.Layout(title='{} MACD 그래프'.format(ticker))
    #    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)

    #    for trace in data:
    #        fig.append_trace(trace, 1, 1)

    #    fig.append_trace(trade_volume, 2, 1)

    #    offline.iplot(fig)



