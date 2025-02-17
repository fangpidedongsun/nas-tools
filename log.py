import logging
import os
import threading
from logging.handlers import TimedRotatingFileHandler
import settings

lock = threading.Lock()


class Logger:
    __instance = None

    def __init__(self):
        self.logger = logging.Logger(__name__)
        self.logger.setLevel(level=logging.INFO)
        logtype = settings.get("root.logtype")
        if logtype == "FILE":
            # 记录日志到文件
            logpath = settings.get("root.logpath")
            if not os.path.exists(logpath):
                os.makedirs(logpath)
            log_file_handler = TimedRotatingFileHandler(filename=logpath + "/" + __name__ + ".txt", when="D", interval=1,
                                                        backupCount=2)
            formatter = logging.Formatter(
                '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s')
            log_file_handler.setFormatter(formatter)
            self.logger.addHandler(log_file_handler)
        elif logtype == "SERVER":
            logserver = settings.get("root.logserver")
            logip = logserver.split(':')[0]
            logport = int(logserver.split(':')[1])
            log_server_handler = logging.handlers.SysLogHandler((logip, logport),
                                                                logging.handlers.SysLogHandler.LOG_USER)
            formatter = logging.Formatter('%(filename)s: %(message)s')
            log_server_handler.setFormatter(formatter)
            self.logger.addHandler(log_server_handler)
        else:
            # 记录日志到终端
            log_console_handler = logging.StreamHandler()
            self.logger.addHandler(log_console_handler)

    @staticmethod
    def get_instance():
        if Logger.__instance:
            return Logger.__instance
        try:
            lock.acquire()
            if not Logger.__instance:
                Logger.__instance = Logger()
        finally:
            lock.release()
        return Logger.__instance


def debug(text):
    return Logger.get_instance().logger.debug(text)


def info(text):
    return Logger.get_instance().logger.info(text)


def error(text):
    return Logger.get_instance().logger.error(text)
