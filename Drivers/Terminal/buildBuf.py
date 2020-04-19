from struct import *
import Drivers.Terminal.CreateHeader
from Drivers.Terminal.terminalStrucks import *


class BufBuilder:
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
        print("checksum is: ", chck_sum)
        a = chck_sum >> 8
        b = chck_sum & 0xff
        print("a is ", a)
        print("b is ", b)
        return [a,b]

    def get_buffer(self):
        packed = pack(self.strFormats[self.struct_name], *self.msgStruct.values())
        current_buf = [int(element) for element in packed]
        print(current_buf)
        return current_buf

    def build_buffer(self):
        self.bufToSend.append(self.buf.outSeqNum)
        self.bufToSend.append(self.buf.outSeqNum >> 8)
        self.bufToSend[6:] = self.get_buffer()
        self.bufToSend.extend(self.calc_chsm(self.bufToSend[4:]))
        self.buf.outSeqNum = self.buf.outSeqNum + 1
        return self.bufToSend


if __name__ =="__main__":
    all_strck = icd_strucks()
    myB = BufBuilder("setRxFreqMsg", all_strck.setRxFreqMsg)
    print(myB.build_buffer())