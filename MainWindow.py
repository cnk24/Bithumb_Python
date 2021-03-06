from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from time import localtime, strftime
from logger import MyLogger

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class Worker(QtCore.QThread):
    # 사용자 정의 시그널 선언
    finished = QtCore.pyqtSignal(dict)

    def __init__(self, bithumb):
        super().__init__()
        self.bithumb = bithumb

    def run(self):
        while True:
            data = {}

            prices = self.bithumb.getCurrentPriceAll()
            for ticker in self.bithumb.getTickers():
                price = float(prices[ticker])
                data[ticker] = self.getMarketInfos(ticker, price, 7)

            self.finished.emit(data)
            self.msleep(500)

    def getMarketInfos(self, ticker, price, day):
        try:
            ma = self.bithumb.CalMovingAverage(ticker, day)
            last_ma = ma[-2] # 뒤에서 두번째

            state = None
            if price > last_ma:
                state = "상승장"
            else:
                state = "하락장"

            target_state = None
            target = self.bithumb.CalTarget(ticker)
            if price > target:
                target_state = "On"
            else:
                target_state = "Off"
 
            return (price, last_ma, state, target_state)
        except:
            return (None, None, None, None)


class CWindow(QtWidgets.QWidget):
    dicTarget = dict()

    def __init__(self, bithumb):
        super().__init__()
        uic.loadUi("MainForm.ui", self)

        self.bithumb = bithumb

        self.logger = MyLogger()
        self.logger.SetLogView(self.uiLog)

        self.viewMarketInfo.setColumnCount(5)
        self.viewMarketInfo.setRowCount(bithumb.getTickersLength())
        self.viewMarketInfo.setHorizontalHeaderLabels(["Name", "Price", "이동평균", "State", "Target"])
        self.viewMarketInfo.resizeColumnsToContents()
        self.viewMarketInfo.cellClicked.connect(self.tableCellClicked)

        self.initPlot()

        worker = Worker(bithumb)
        worker.finished.connect(self.updateMarketInfo)
        worker.start()

    def initPlot(self):
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layoutPlot.addWidget(self.canvas)

    def plotMACD(self, ticker):
        self.fig.clear()
        df = self.bithumb.getMACD(ticker)

        ax1 = self.fig.add_subplot(211, frame_on=False)
        ax1.set_title(ticker)
        ax1.plot(df.index.date, df['macd'], lw=1.0, color='blue', label='MACD')
        ax1.plot(df.index.date, df['macds'], lw=1.0, color='orange', label='signal')
        ax1.bar(df.index.date, df['macdo'], align='center', alpha=0.5, color='green', label='oscillator')
        ax1.legend(loc='upper left')
        
        ax2 = self.fig.add_subplot(212, frame_on=False)
        ax2.bar(df.index.date, df['volume'], align='center', alpha=0.5, color='red', label='volume')
        ax2.legend(loc='upper left')

        self.canvas.draw()

    def plotStochastic(self, ticker):
        self.fig.clear()
        df = self.bithumb.getStochastic(ticker)

        ax1 = self.fig.add_subplot(211, frame_on=False)
        ax1.set_title(ticker)
        ax1.plot(df.index.date, df['kdj_k'], lw=1.0, color='blue', label='Slow%K')
        ax1.plot(df.index.date, df['kdj_d'], lw=1.0, color='orange', label='Slow%D')
        ax1.legend(loc='upper left')
        
        ax2 = self.fig.add_subplot(212, frame_on=False)
        ax2.bar(df.index.date, df['volume'], align='center', alpha=0.5, color='red', label='volume')
        ax2.legend(loc='upper left')

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


    def tableCellClicked(self, row, column):
        if column == 0:
            item = self.viewMarketInfo.item(row, column)
            ticker = item.text()
            self.plotMACD(ticker)
        elif column == 1:
            item = self.viewMarketInfo.item(row, 0)
            ticker = item.text()
            self.plotStochastic(ticker)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)


    @QtCore.pyqtSlot(dict)    
    def updateMarketInfo(self, data):
        try:
            for ticker, infos in data.items():
                index = self.bithumb.getTickers().index(ticker)

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
        except:
            pass
        

        


        


