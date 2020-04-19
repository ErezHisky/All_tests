import socket
import logging
import time
from datetime import datetime
from Drivers.Terminal.terminalStrucks import *
from Drivers.Terminal.buildDataBuf import *


class Send_The_Data:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # For UDP
        self.udp_host = "192.168.43.1"  # Host IP
        self.udp_port = 8889  # specified port to connect
        all_strck = icd_strucks()
        all_strck.setLmxTxFreqMsg["txFreq"] = 28000
        self.myDatB = DataBufBuilder("setLmxTxFreqMsg", all_strck.setLmxTxFreqMsg)
        self.Buf = self.myDatB.build_data_buffer()

    def send_the_message(self, msgName, msgStruct):
        self.myDatB.msgStruct = msgStruct
        self.myDatB.struct_name = msgName
        self.Buf = self.myDatB.build_data_buffer()
        logging.info(self.Buf)
        self.sock.sendto(bytearray(self.Buf), (self.udp_host, self.udp_port))

my_date = datetime.now().date()
t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)

if __name__ == "__main__":
    iCD = Drivers.Terminal.iCDs
    all_strck = icd_strucks()
    sdm = Send_The_Data()
    all_strck.setLmxTxFreqMsg["txFreq"] = 27500
    sdm.send_the_message("setLmxTxFreqMsg", all_strck.setLmxTxFreqMsg)
    sdm.send_the_message("modemConfigMsg", all_strck.modemConfigMsg)
    all_strck.modemConfigMsg["opcode"] = iCD.IOT_MODEM_CONFIG
    sdm.send_the_message("modemConfigMsg", all_strck.modemConfigMsg)
    sdm.send_the_message("Admv4420FreqMsg", all_strck.Admv4420FreqMsg)
    sdm.send_the_message("ADMV4420RegMsg", all_strck.ADMV4420RegMsg)
    all_strck.ADMV4420RegMsg["cmd"] = iCD.SPI_READ
    sdm.send_the_message("ADMV4420RegMsg", all_strck.ADMV4420RegMsg)
    sdm.send_the_message("MAX2112RegMsg", all_strck.MAX2112RegMsg)
    all_strck.MAX2112RegMsg["cmd"] = iCD.SPI_READ
    sdm.send_the_message("MAX2112RegMsg", all_strck.MAX2112RegMsg)
    sdm.send_the_message("antPwrCtrlMsg", all_strck.antPwrCtrlMsg)
    all_strck.antPwrCtrlMsg["antType"] = 4
    sdm.send_the_message("antPwrCtrlMsg", all_strck.antPwrCtrlMsg)
    all_strck.antPwrCtrlMsg["pwrMode"] = 2
    sdm.send_the_message("antPwrCtrlMsg", all_strck.antPwrCtrlMsg)
    sdm.send_the_message("clkDacMsg", all_strck.clkDacMsg)
    sdm.send_the_message("MxFEAxiRegMsg", all_strck.MxFEAxiRegMsg)
    all_strck.MxFEAxiRegMsg["data"] = 0x3
    sdm.send_the_message("MxFEAxiRegMsg", all_strck.MxFEAxiRegMsg)
    sdm.send_the_message("PICReadWriteMsg", all_strck.PICReadWriteMsg)
    all_strck.PICReadWriteMsg["cmd"] = iCD.SPI_READ
    sdm.send_the_message("PICReadWriteMsg", all_strck.PICReadWriteMsg)
    sdm.send_the_message("phaseSetDynamicMsg", all_strck.phaseSetDynamicMsg)
    sdm.send_the_message("ADMV1013RegMsg", all_strck.ADMV1013RegMsg)
    all_strck.ADMV1013RegMsg["cmd"] = iCD.SPI_READ
    all_strck.ADMV1013RegMsg["data"] = 0
    sdm.send_the_message("ADMV1013RegMsg", all_strck.ADMV1013RegMsg)
    sdm.send_the_message("regReadWriteMsg", all_strck.regReadWriteMsg)
    all_strck.regReadWriteMsg["cmd"] = iCD.SPI_READ
    sdm.send_the_message("regReadWriteMsg", all_strck.regReadWriteMsg)
    # GENERAL - Registers : -----------------------------------------------------------
    sdm.send_the_message("modemRegCommandMsg", all_strck.modemRegCommandMsg)
    all_strck.modemRegCommandMsg["cmd"] = iCD.SPI_READ
    all_strck.modemRegCommandMsg["data"] = 0
    sdm.send_the_message("modemRegCommandMsg", all_strck.modemRegCommandMsg)
    all_strck.modemRegCommandMsg["cmd"] = iCD.SPI_WRITE
    all_strck.modemRegCommandMsg["opcode"] = iCD.MODEM_REGISTER
    all_strck.modemRegCommandMsg["data"] = 65535
    sdm.send_the_message("modemRegCommandMsg", all_strck.modemRegCommandMsg)
    all_strck.modemRegCommandMsg["cmd"] = iCD.SPI_READ
    all_strck.modemRegCommandMsg["data"] = 0
    sdm.send_the_message("modemRegCommandMsg", all_strck.modemRegCommandMsg)
    # ----------------- modemRegCommandMsg - Modem Signal / CW Select: ----------------
    '''
                        Modem Signal
    modemRegCommandMsg.cmd = 0xaa;
    modemRegCommandMsg.addr = 0x5;
    modemRegCommandMsg.data = 0x1;
    
                        CW Select
    modemRegCommandMsg.cmd = 0xaa;
    modemRegCommandMsg.addr = 0x5;
    modemRegCommandMsg.data = 0x2;
    regWriteEn = true;
    sendDataMsg(modemRegCommandMsg);'''


    
