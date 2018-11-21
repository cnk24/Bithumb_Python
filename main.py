import sys
from PyQt5 import QtWidgets
from MainWindow import CWindow
from SocketClient import CSocketClient


def main():

    #client = CSocketClient()
    #client.connect()
    #client.send('TEST')
    #client.close()



    app = QtWidgets.QApplication(sys.argv)
    w = CWindow()
    w.show()

    w.debug("LOG")
    #w.communicationLog('TEST', True)


    app.exec_()
    #sys.exit(app.exec())

if __name__ == '__main__':
    main()








