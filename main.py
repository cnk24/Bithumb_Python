import sys
import threading
from PyQt5.QtWidgets import QApplication
from MainWindow import CWindow
from SocketClient import CSocketClient
from bithumb import Cbithumb


def main():

    bithumb = Cbithumb()

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



    #client = CSocketClient()
    #client.connect()
    #client.send('TEST')
    #client.close()



    app = QApplication(sys.argv)
    w = CWindow()

    prices = bithumb.getCurrentPriceAll()
    w.setTickerList(prices)

    w.debugLog('LOG')
    w.communicationLog('TEST', True)

    app.exec_()
    #sys.exit(app.exec())

if __name__ == '__main__':
    main()








