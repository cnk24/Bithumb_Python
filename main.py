import sys
from PyQt5 import QtWidgets
from MainWindow import CWindow
from SocketClient import CSocketClient

def main():

    #bithumb = Cbithumb()

    #ticker = bithumb.getTicker(0)
    #price = bithumb.getCurrentPrice(ticker)
    #print(price)

    #orderbook = bithumb.getOrderBook(ticker)
    #bids = orderbook['bids']
    #asks = orderbook['asks']
    #print(bids)
    #print(asks)

    #prices = bithumb.getCurrentPriceAll()
    #for k, v in prices.items():
    #    print(k, v)

    

    #tickers = bithumb.getTickers()
    #for ticker in tickers:
    #    bull = bithumb.bull_market(ticker, 10)
    #    if bull:
    #        print("{} 상승".format(ticker))
    #    else:
    #        print("{} 하락".format(ticker))

    



    #client = CSocketClient()
    #client.connect()
    #client.send('TEST')
    #client.close()



    app = QtWidgets.QApplication(sys.argv)
    w = CWindow()
    w.show()

    #prices = bithumb.getCurrentPriceAll()
    #w.setTickerList(prices)

    #w.debugLog("LOG")
    #w.communicationLog('TEST', True)

    app.exec_()
    #sys.exit(app.exec())

if __name__ == '__main__':
    main()








