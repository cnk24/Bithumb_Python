'''
Creator : SeoJK
CreateTime : 2018.03.31

'''

import os
import logging
#from common import *


try:
    LOG_FILENAME = os.path.splitext(__file__)[0] + ".log"
except:
    LOG_FILENAME = __file__ + ".log"

class Singleton(object):
    """
    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class MyLogger(Singleton):
    def __init__(self):
        self._logger = logging.getLogger("Bithumb")
        self._logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s (%(funcName)s) %(message)s')

        log_dir = "log"
        import os
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        from datetime import date
        today = date.today()
        filename = log_dir + "/" + today.strftime("%Y%m%d") + ".log"

        fileHandler = logging.FileHandler(filename, "a", "utf-8")
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(self.formatter)
        streamHandler.setFormatter(self.formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def getLogger(self):
        return self._logger

    def debug(self, msg):
        self._logger.debug(msg)

    def error(self, msg):
        self._logger.error(msg)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def SetLogView(self, widget):
        logTextBox = QPlainTextEditLogger(widget)
        logTextBox.setFormatter(self.formatter)
        self._logger.addHandler(logTextBox)


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
