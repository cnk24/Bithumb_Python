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
                data[ticker] = self.getMarketInfos(ticker, price, 7)

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
    dicTarget = dict()

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

    def plotDraw(self, ticker):
        df = xbithumb.getMACD(ticker)

        #ax1 = self.fig.add_subplot(1, 1, 1)
        #self.ax2 = self.ax1.twinx()

        ax_macd = self.fig.add_subplot(211, frame_on=False)
        ax_macd.set_title(ticker)
        ax_macd.set_ylabel('MACD')
        ax_macd.yaxis.label.set_color('blue')
        ax_macd.plot(df.index.date, df['macd'], lw=0.5, color='blue')

        #ax_signal = ax_macd.twinx()
        #ax_signal.set_ylabel('Signal')
        #ax_signal.yaxis.label.set_color('orange')
        #ax_signal.plot(df.index.date, df['macds'], lw=0.5, color='orange', kind='bar')

        #ax_oscillator = ax_macd.twinx()
        #ax_oscillator.set_ylabel('oscillator')
        #ax_oscillator.yaxis.label.set_color('green')
        #ax_oscillator.plot(df.index.date, df['macdo'], lw=0.5, color='green')


        #ax_volume = self.fig.add_subplot(212, frame_on=False)
        #ax_volume.set_ylabel('volume')
        #ax_volume.yaxis.label.set_color('red')
        #ax_volume.plot(df.index.date, df['volume'], lw=0.5, color='red')

        self.canvas.draw()



    def TargetFind(self, ticker):
        val = self.dicTarget.get(ticker)
        if val is None:
            return False

        return True


    def TargetAdd(self, ticker, price):
        if self.TargetFind(ticker) == True:
            return

        newDict = {ticker: price}
        self.dicTarget.update(newDict)

        value = "[{0}] [{1}]".format(ticker, price)        

        listWidget = QtWidgets.QListWidget(self)
        listWidget = self.listTarget
        listWidget.addItem(QtWidgets.QListWidgetItem(value))

    def TargetRemove(self, ticker):
        if self.TargetFind(ticker) == False:
            return

        listWidget = QtWidgets.QListWidget(self)
        listWidget = self.listTarget
        listWidget.removeAll()

        del self.dicTarget[ticker]

        for item in self.dicTarget:
            value = "[{0}] [{1}]".format(item.key, item.value)
            listWidget.addItem(QtWidgets.QListWidgetItem(value))


        #model = listWidget.model()
        #for selectedItem in listWidget.selectedItems():
        #    qIndex = listWidget.indexFromItem(selectedItem)
            #print('removing : %s' %model.data(qIndex).toString())
        #    model.removeRow(qIndex.row())



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

                price = infos[0]
                last_ma = round(infos[1], 2)
                state = infos[2]
                target_state = infos[3]

                if state == "상승장" and target_state == "On":
                    self.TargetAdd(ticker, price)
                else:
                    self.TargetRemove(ticker)
 
                self.viewMarketInfo.setItem(index, 0, QtWidgets.QTableWidgetItem(ticker))
                self.viewMarketInfo.setItem(index, 1, QtWidgets.QTableWidgetItem(str(price)))
                self.viewMarketInfo.setItem(index, 2, QtWidgets.QTableWidgetItem(str(last_ma)))
                self.viewMarketInfo.setItem(index, 3, QtWidgets.QTableWidgetItem(str(state)))
                self.viewMarketInfo.setItem(index, 4, QtWidgets.QTableWidgetItem(str(target_state)))

                self.viewMarketInfo.resizeColumnsToContents()

            self.plotDraw('XRP')
        except:
            pass
        

        


        


