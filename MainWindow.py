from PyQt5.QtWidgets import *
from PyQt5 import uic
from time import localtime, strftime

class CWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi("MainWindow.ui")
        self.ui.show()

    def setTickerList(self, prices):
        table = QTableWidget()
        table = self.ui.priceView
        table.setColumnCount(2)
        table.setRowCount(len(prices))
        table.setHorizontalHeaderLabels(["Name", "Price"])

        rowIndex = 0
        for k, v in prices.items():
            table.setItem(rowIndex,0, QTableWidgetItem(k))
            table.setItem(rowIndex,1, QTableWidgetItem(v))
            rowIndex += 1

        table.resizeColumnsToContents()

    def debugLog(self, msg):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        log = "[{0}] {1}".format(time, msg)

        logView = QListWidget()
        logView = self.ui.debugLog
        logView.addItem(QListWidgetItem(log))

    def communicationLog(self, msg, isRecv=False):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())

        title = ""
        if isRecv == True:
            title = "Client<--Server"
        else:
            title = "Client-->Server"

        log = "[{0}] [{1}] {2}".format(time, title, msg)

        logView = QListWidget()
        logView = self.ui.communicationLog
        logView.addItem(QListWidgetItem(log))
        

        


        


