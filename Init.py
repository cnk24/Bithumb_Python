from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Worker(QtCore.QThread):
    # 사용자 정의 시그널 선언
    finished = QtCore.pyqtSignal()
    change_value = QtCore.pyqtSignal(int)

    def __init__(self, bithumb):
        super().__init__()
        self.bithumb = bithumb

    def run(self):
        while True:
            cnt = 0
            for ticker in self.bithumb.getTickers():
                self.bithumb.getBeforeData(ticker)

                cnt += 1
                pos = (cnt / self.bithumb.getTickersLength()) * 100
                self.change_value.emit(pos)

            self.finished.emit()
            break


class InitDialog(QtWidgets.QDialog):

    def __init__(self, bithumb):
        super().__init__()
        uic.loadUi("InitDialog.ui", self)

        worker = Worker(bithumb)
        worker.change_value.connect(self.progressBar.setValue)
        worker.finished.connect(self.Finish)
        worker.start()


    @QtCore.pyqtSlot()
    def Finish(self):
        self.close()
        

        