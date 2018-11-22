import sys
from PyQt5 import QtWidgets
from Init import InitDialog
from MainWindow import CWindow
from bithumb import Cbithumb
from SocketClient import CSocketClient


def main():

    #client = CSocketClient()
    #client.connect()
    #client.send('TEST')
    #client.close()


    app = QtWidgets.QApplication(sys.argv)

    xbithumb = Cbithumb()

    dialog = InitDialog(xbithumb)
    dialog.exec_()

    w = CWindow(xbithumb)
    w.show()

    #w.debug("START")


    app.exec_()
    #sys.exit(app.exec())

if __name__ == '__main__':
    main()








