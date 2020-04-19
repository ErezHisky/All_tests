import socket
from Drivers.Terminal.terminalStrucks import *
from Drivers.Terminal.buildBuf import *


class Send_Data:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # For UDP
        self.udp_host = "192.168.43.1"  # Host IP
        self.udp_port = 8888  # specified port to connect
        all_strck = icd_strucks()
        all_strck.setRxFreqMsg["rxFreq"] = 1400 * 1000000
        self.myB = BufBuilder("setRxFreqMsg", all_strck.setRxFreqMsg)
        self.Buf = self.myB.build_buffer()

    def send_the_message(self, msgName, msgStruct):
        self.myB.msgStruct = msgStruct
        self.myB.struct_name = msgName
        self.Buf = self.myB.build_buffer()
        print(self.Buf)
        self.sock.sendto(bytearray(self.Buf), (self.udp_host, self.udp_port))


if __name__ == "__main__":
    iCD = Drivers.Terminal.iCDs
    all_strck = icd_strucks()
    sdm = Send_Data()
    all_strck.setRxFreqMsg["rxFreq"] = 1450 * 1000000
    sdm.send_the_message("setRxFreqMsg", all_strck.setRxFreqMsg)
    sdm.send_the_message("setTxFreqMsg", all_strck.setTxFreqMsg)
