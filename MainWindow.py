from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from time import localtime, strftime
from bithumb import Cbithumb

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


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

            target_state = None
            target = xbithumb.CalTarget(ticker)
            if price > target:
                target_state = "On"
            else:
                target_state = "Off"
 
            return (price, last_ma, state, target_state)
        except:
            return (None, None, None, None)


class CWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("MainForm.ui", self)

        self.viewMarketInfo.setColumnCount(5)
        self.viewMarketInfo.setRowCount(xbithumb.getTickersLength())
        self.viewMarketInfo.setHorizontalHeaderLabels(["Name", "Price", "이동평균", "State", "Target"])
        self.viewMarketInfo.resizeColumnsToContents()

        self.initPlot()

        self.worker = Worker()
        self.worker.finished.connect(self.updateMarketInfo)
        self.worker.start()

    def initPlot(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layoutPlot.addWidget(self.canvas)

        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax2 = self.ax1.twinx()
        self.ax1.set_xlabel('Ticker')
        self.ax1.set_ylabel('Target')
        self.ax2.set_ylabel('Price')
        self.ax1.yaxis.label.set_color('red')
        self.ax2.yaxis.label.set_color('blue')

    def plotDraw(self):
        x = xbithumb.getTickers()
        prices = xbithumb.getCurrentPriceAll()

        y1 = []
        y2 = []
        for ticker in x:
            y1.append(xbithumb.CalTarget(ticker))
            y2.append(float(prices[ticker]))

        self.ax1.plot(x, y1, lw=0.5, color='r')
        self.ax2.plot(x, y2, lw=0.5, color='b')

        #self.ax1.grid()
        self.canvas.draw()


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
                self.viewMarketInfo.setItem(index, 4, QtWidgets.QTableWidgetItem(str(infos[3])))

                self.viewMarketInfo.resizeColumnsToContents()

            #self.plotDraw()
        except:
            pass
        

        


        


