import socket
from struct import *
import Drivers.Terminal.CreateHeader
from Drivers.Terminal.terminalStrucks import *
# importing functools for reduce()
import functools

class TxFreqMsg:
    def __init__(self, strFormat='=BBxd', Freq=29000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # For UDP
        self.udp_host = "192.168.43.1"  # Host IP
        self.udp_port = 8888            # specified port to connect
        self.strformat = strFormat      # for setTxFreqMsg struct
        self.freq = Freq # Freq=29000 -- > 2900000000
        self.all_strck = icd_strucks()
        self.setTxFreqMsg = self.all_strck.setTxFreqMsg
        self.setTxFreqMsg["txFreq"] = int((self.freq - 26000) * 1e5)

        self.setLmxTxFreqMsg = self.all_strck.setLmxTxFreqMsg
        self.setLmxTxFreqMsg["txFreq"] = Freq

        self.getReportMsg = self.all_strck.getReportMsg

    def get_report_buffer(self):
        packed = pack(self.strformat, *self.getReportMsg.values())
        buf = [int(element) for element in packed]
        print("5 ",  buf)
        return buf

    def get_buffer(self):
        if self.freq < 27000 or self.freq > 32000:
            raise Exception("Please enter valid frequency.")
        print("freq is: ", self.setTxFreqMsg["txFreq"])
        #packed = pack(self.strformat, self.setTxFreqMsg["opcode"], self.setTxFreqMsg["rfBandWith"], self.setTxFreqMsg["txFreq"])
        packed = pack(self.strformat, self.setLmxTxFreqMsg["cmnd"], self.setLmxTxFreqMsg["opcode"],
                      self.setLmxTxFreqMsg["txFreq"])
        buf = [int(element) for element in packed]
        print("4 ", buf)
        return buf

    def calc_the_checksum(self, aBuf):
        chck_sum=0
        for b in aBuf:
            chck_sum += b
        print(chck_sum)
        a = chck_sum >> 8
        b = chck_sum & 0xff
        print("a is ", a)
        print("b is ", b)
        return b

    def build_the_array(self):
        buf = Drivers.Terminal.CreateHeader.TheBuffer()
        #msgToSend = buf.getHeader()
        msgToSend = buf.getDataHeader()
        print("1 ", msgToSend)
        #msgToSend[6:] = self.get_buffer()
        #msgToSend[4:] = self.get_buffer()[1:]
        msgToSend[6:] = self.get_report_buffer()
        print("2 ", msgToSend)
        msgToSend.append(self.calc_the_checksum(msgToSend))
        print("3 ", msgToSend)
        buf.outSeqNum = buf.outSeqNum + 1
        return msgToSend

    def build_msg_array(self):
        pass

    def build_data_msg_array(self):
        pass

    def send_the_message(self):
        msgToSendb = self.build_the_array()
        self.sock.sendto(bytearray(msgToSendb), (self.udp_host, self.udp_port))


if __name__ == "__main__":
    all_stcks = icd_strucks()
    my_strFormats = all_stcks.strFormats

    my_tx_freq_msg = TxFreqMsg(my_strFormats["setLmxTxFreqMsg"], 29050)
    my_tx_freq_msg.send_the_message()

    '''get_report = TxFreqMsg(my_strFormats["getReportMsg"])
    get_report.send_the_message()'''
