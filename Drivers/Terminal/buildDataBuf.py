from struct import *
import logging
import time
from datetime import datetime
import Drivers.Terminal.CreateHeader
from Drivers.Terminal.terminalStrucks import *


class DataBufBuilder:
    def __init__(self, structName, msgStruct):
        self.all_strck = icd_strucks()
        self.strFormats = self.all_strck.strFormats
        self.buf = Drivers.Terminal.CreateHeader.TheBuffer()
        self.Header = self.buf.getDataHeader()
        self.msgStruct = msgStruct
        self.bufToSend = self.Header
        self.struct_name = structName

    def calc_chsm(self, aBuf):
        chck_sum = 0
        for b in aBuf:
            chck_sum += b
        logging.info(f"checksum is:  {chck_sum}")
        a = chck_sum >> 8
        b = chck_sum & 0xff
        logging.info(f"a is {a}")
        logging.info(f"b is {b}")
        return b

    def get_data_buffer(self):
        packed = pack(self.strFormats[self.struct_name], *self.msgStruct.values())
        current_buf = [int(element) for element in packed]
        return current_buf

    def build_data_buffer(self):
        self.bufToSend[4:] = self.get_data_buffer()
        self.bufToSend.append(self.calc_chsm(self.bufToSend))
        self.buf.outSeqNum = self.buf.outSeqNum + 1
        return self.bufToSend

my_date = datetime.now().date()
t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)


if __name__ =="__main__":
    all_strck = icd_strucks()
    all_strck.setLmxTxFreqMsg["txFreq"] = 29050
    logging.info([v for k,v in locals().items() if v is all_strck])
    myDatB = DataBufBuilder("setLmxTxFreqMsg", all_strck.setLmxTxFreqMsg)
    logging.info(str(myDatB.build_data_buffer()))