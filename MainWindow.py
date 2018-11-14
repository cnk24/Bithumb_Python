from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from time import localtime, strftime
from bithumb import Cbithumb

xbithumb = Cbithumb()

class Worker(QtCore.QThread):
    finished = QtCore.pyqtSignal(dict)

    def run(self):
        while True:
            data = {}

            prices = xbithumb.getCurrentPriceAll()
            for ticker in xbithumb.getTickers():
                price = float(prices[ticker])
                data[ticker] = self.getMarketInfos(ticker, price, 5)

            self.finished.emit(data)
            self.msleep(500)

    def getMarketInfos(self, ticker, price, day):
        try:
            ma = xbithumb.CalMovingAverage(ticker, day)
            last_ma = ma[-2]

            state = None
            if price > last_ma:
                state = "상승장"
            else:
                state = "하락장"
 
            return (price, last_ma, state)
        except:
            return (None, None, None)


class CWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("MainForm.ui", self)

        self.viewMarketInfo.setColumnCount(4)
        self.viewMarketInfo.setRowCount(xbithumb.getTickersLength())
        self.viewMarketInfo.setHorizontalHeaderLabels(["Name", "Price", "이동평균", "State"])
        self.viewMarketInfo.resizeColumnsToContents()

        self.worker = Worker()
        self.worker.finished.connect(self.updateMarketInfo)
        self.worker.start()

    def debugLog(self, msg):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        log = "[{0}] {1}".format(time, msg)

        listWidget = QtWidgets.QListWidget(self)
        listWidget = self.logWidget
        listWidget.addItem(QtWidgets.QListWidgetItem(log))

    def communicationLog(self, msg, isRecv=False):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        title = ""
        if isRecv == True:
            title = "Client<--Server"
        else:
            title = "Client-->Server"

        log = "[{0}] [{1}] {2}".format(time, title, msg)


    @QtCore.pyqtSlot(dict)
    def updateMarketInfo(self, data):
        try:
            for ticker, infos in data.items():
                index = xbithumb.getTickers().index(ticker)
 
                self.viewMarketInfo.setItem(index, 0, QtWidgets.QTableWidgetItem(ticker))
                self.viewMarketInfo.setItem(index, 1, QtWidgets.QTableWidgetItem(str(infos[0])))
                self.viewMarketInfo.setItem(index, 2, QtWidgets.QTableWidgetItem(str(infos[1])))
                self.viewMarketInfo.setItem(index, 3, QtWidgets.QTableWidgetItem(str(infos[2])))

                self.viewMarketInfo.resizeColumnsToContents()
        except:
            pass
        

        


        


