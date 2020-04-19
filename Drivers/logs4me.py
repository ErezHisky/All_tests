import time
from datetime import datetime
import logging
import os

class MyLog:
    def __init__(self):
        my_date = datetime.now().date()
        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        try:
            if not os.path.isdir('D:/TesterLogs'):
                os.mkdir("D:/TesterLogs")
        except OSError:
            print("Creation of the directory %s failed" % path)
        logging.basicConfig(filename=f'D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s')

    def write_debug_log(self, msg):
        logging.debug(msg)

    def write_info_log(self, msg):
        logging.info(msg)

    def write_warning(self, msg):
        logging.warning(msg)

if __name__ == "__main__":
    myLog =MyLog()
    myLog.write_debug_log("this is my debug")
    myLog.write_warning("this is my warning")
    myLog.write_info_log("this is my info")


