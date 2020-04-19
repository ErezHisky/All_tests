import logging
import socket
import time
import threading
from datetime import datetime
from Drivers.Terminal.terminalStrucks import *
from Drivers.Terminal.SendDataMsg import *
from Tests.commFunctions import *


class ReceiveData:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SO_BROADCAST  SO_REUSEADDR
        self.sock.settimeout(5)
        self.all_strck = icd_strucks()
        self.strFormats = self.all_strck.strFormats
        self.packet_size = 1500
        self.host=''
        self.port = 10088
        self.sock.bind((self.host, self.port))
        self.myDatB = DataBufBuilder("setLmxTxFreqMsg", self.all_strck.setLmxTxFreqMsg)
        self.Buf = self.myDatB.build_data_buffer()

    def send_receive_order(self, demandOpcodeNum=0xff):
        self.udp_host = "192.168.43.1"  # Host IP
        self.udp_port = 8889  # specified port to connect
        self.myDatB = DataBufBuilder("getReportMsg", self.all_strck.getReportMsg)
        self.all_strck.getReportMsg["reqMsgOpcode"] = demandOpcodeNum
        self.Buf = self.myDatB.build_data_buffer()
        logging.info(self.Buf)
        self.sock.sendto(bytearray(self.Buf), (self.udp_host, self.udp_port))

    def send_the_message(self, msgName, msgStruct):
        self.myDatB.msgStruct = msgStruct
        self.myDatB.struct_name = msgName
        self.Buf = self.myDatB.build_data_buffer()
        logging.info(self.Buf)
        self.sock.sendto(bytearray(self.Buf), (self.udp_host, self.udp_port))

    def start_receiving(self):
        log.info("Listening on udp %s:%s" % (self.host, self.port))
        try:
            while True:
                (self.data, addr) = self.sock.recvfrom(self.packet_size)
                time.sleep(0.01)
                yield [self.data, addr]
        except:
            checkWifi()
            time.sleep(2)
            self.start_receiving()

    def packet_into_strct(self, msgName):
        return unpack(self.strFormats[msgName], self.data)

    def updateFeildsFromInputMsg(self):
        if self.data[0] == 1:
            logging.info(f"registrationReqMsg length is {len(self.data)}")
        elif self.data[0] == 38:
            logging.info(f"modemParamMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["modemParamMsg"], self.data)
            self.all_strck.modemParamMsg["opcode"] = params_var[0]
            self.all_strck.modemParamMsg["modemSnr"] = params_var[1] / 16
            self.all_strck.modemParamMsg["modemEstFreq"] = params_var[2]
            self.all_strck.modemParamMsg["modemSync"] = params_var[3]
            self.all_strck.modemParamMsg["modemEnN0Rem"] = params_var[4]
            logging.info(self.all_strck.modemParamMsg)

        elif self.data[0] == 39:
            logging.info(f"modemRegCommandMsg -39 length is {len(self.data)}")
            params_var = unpack(self.strFormats["modemRegCommandMsg"], self.data)
            self.all_strck.modemRegCommandMsg["opcode"] = params_var[0]
            self.all_strck.modemRegCommandMsg["cmd"] = params_var[1]
            self.all_strck.modemRegCommandMsg["addr"] = params_var[2]
            self.all_strck.modemRegCommandMsg["data"] = params_var[3]
            logging.info(self.all_strck.modemRegCommandMsg)

        elif self.data[0] == 40:
            logging.info(f"aplVoiceOutputMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["aplVoiceOutputMsg"], self.data)
            logging.info(params_var)

        elif self.data[0] == 41:
            logging.info(f"aplVoiceInMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["aplVoiceInMsg"], self.data)
            logging.info(params_var)

        elif self.data[0] == 42:
            logging.info(f"aplThroughputMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["aplThroughputMsg"], self.data)
            logging.info(params_var)

        elif self.data[0] == 43:
            logging.info(f"inputThroughputMsg length is {len(self.data)}")

        elif self.data[0] == 80:
            logging.info(f"ad9364OpRepMsg length is {len(self.data)}")

        elif self.data[0] == 90:
            logging.info(f"dataStatusRepMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["dataStatusRepMsg"], self.data)

            self.all_strck.dataStatusRepMsg = {
                "opcode": params_var[0],
                "sentMsgCnt": params_var[1],
                "rcvMsgCnt": params_var[2],
                "crcErrCnt": params_var[3],
                "properPackCnt": params_var[4],
                "dropPackCnt": params_var[5],
                "function": params_var[6],
                "regDataRead": params_var[7],
                "rcvBytesCnt": params_var[8]
            }
            logging.info(self.all_strck.dataStatusRepMsg)

        elif self.data[0] == 129:
            logging.info(f"iotTDDMtMsg length is {len(self.data)}")

        elif self.data[0] == 143:
            logging.info(f"dynSoftRegMsg length is {len(self.data)}")

        elif self.data[0] == 153:
            logging.info(f"modemRegMsgReport - 153 length is {len(self.data)}")

        elif self.data[0] == 155:
            logging.info(f"MxFEAxiRegMsg length is {len(self.data)}")

        elif self.data[0] == 156:
            logging.info(f"MxFESpiRegMsg length is {len(self.data)}")

        elif self.data[0] == 159:
            logging.info(f"MxFESpiRegMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["MxFEAxiRegMsg"], self.data)

            self.all_strck.MxFEAxiRegMsg ={
                "opcode": params_var[0],
                "cmd": params_var[1],
                "addr": params_var[2],
                "data": params_var[3]  # 0x7 is ON, 0x3 is OFF
            }
            logging.info(self.all_strck.MxFEAxiRegMsg)

        elif self.data[0] == 161:
            logging.info(f"LMX2592RegWrReadMsg length is {len(self.data)}")

        elif self.data[0] == 162:
            logging.info(f"MAX2112RegMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["MAX2112RegMsg"], self.data)
            self.all_strck.MAX2112RegMsg = {
                "opcode": params_var[0],
                "cmd": params_var[1],
                "addr": params_var[2],
                "data": params_var[3]  # 0x7 is ON, 0x3 is OFF
            }
            logging.info(self.all_strck.MAX2112RegMsg)

        elif self.data[0] == 163:
            logging.info(f"ADMV1013RegMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["ADMV1013RegMsg"], self.data)
            self.all_strck.ADMV1013RegMsg = {
                "opcode": params_var[0],
                "cmd": params_var[1],
                "addr": params_var[2],
                "data": params_var[3]  # 0x7 is ON, 0x3 is OFF
            }
            logging.info(self.all_strck.ADMV1013RegMsg)

        elif self.data[0] == 168:
            logging.info(f"ADMV4420RegMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["ADMV4420RegMsg"], self.data)
            self.all_strck.ADMV4420RegMsg = {
                "opcode": params_var[0],
                "cmd": params_var[1],
                "addr": params_var[2],
                "data": params_var[3]  # 0x7 is ON, 0x3 is OFF
            }
            logging.info(self.all_strck.ADMV4420RegMsg)

        elif self.data[0] == 170:
            logging.info(f"PICReadWriteMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["PICReadWriteMsg"], self.data)
            self.all_strck.PICReadWriteMsg = {
                "opcode": params_var[0],
                "cmd": params_var[1],
                "addr": params_var[2],
                "data": params_var[3]  # 0x7 is ON, 0x3 is OFF
            }
            logging.info(self.all_strck.PICReadWriteMsg)

        elif self.data[0] == 173:
            logging.info(f"gpsMsgMsg length is {len(self.data)}")

        elif self.data[0] == 201:
            logging.info(f"pointAntMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["PointAntStruct"], self.data)

            self.all_strck.PointAntStruct = {
                "opcode": params_var[0],  # OPCODE 0xC9
                "imuRoll": params_var[1],
                "imuPitch": params_var[2],
                "imuYaw": params_var[3],
                "Longitude": params_var[4],
                "Latitude": params_var[5],
                "Altitude": params_var[6],
                "gpsStatus": params_var[7],
                "mta_hor": params_var[8],
                "mta_ver": params_var[9],
                "memsCalib": params_var[10],
                "heading": params_var[11],
                "mag_X": params_var[12],
                "mag_Y": params_var[13],
                "mag_Z": params_var[14],
                "EbNo": params_var[15] / 16,
                "FreqEst": params_var[16]
            }
            logging.info(self.all_strck.PointAntStruct)

        elif self.data[0] == 206:
            logging.info(f"dynPointParamMsg length is {len(self.data)}")
            params_var = unpack(self.strFormats["dynPointParamMsg"], self.data)

            self.all_strck.dynPointParamMsg = {
                "opcode": params_var[0],  # OPCODE 0xCE
                "intYaw": params_var[1],
                "intPitch": params_var[2],
                "intRoll": params_var[3],
                "extYaw": params_var[4],
                "extPitch": params_var[5],
                "extRoll": params_var[6],
                "status": params_var[7],  # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix
                "latitude": params_var[8],
                "nsIndicator": params_var[9],  # North/South Indicator.
                "longitude": params_var[10],
                "ewIndicator": params_var[11],  # East/West Indicator.
                "altitude": params_var[12],
                # === Belong to  DynamicMT\ATENNA POINTING folder ===
                "angHor": params_var[13],
                "angVer": params_var[14],
                "angEl": params_var[15],
                "angAz": params_var[16],
                # ===================================================
                "trackStat": params_var[17],
                "rssiAzOff": params_var[18],
                "rssiElOff": params_var[19],
                "northYawOff": params_var[20],
                "dummy1": params_var[21],
                "dummy2": params_var[22],
                "dummy3": params_var[23],
                "dummy4": params_var[24],
                "dummy5": params_var[25],
                "dummy6": params_var[26],
                "dummy7": params_var[27],
                "dummy8": params_var[28],
                "dummy9": params_var[29],
                "dummy10": params_var[30],
                "dummy11": params_var[31],
                "dummy12": params_var[32]
            }
            logging.info(self.all_strck.dynPointParamMsg)


        elif self.data[0] == 209:
            logging.info(f"iotRxAdmv4420RegRepMsg length is {len(self.data)}")
            #params_var = unpack(self.strFormats["iotRxAdmv4420RegRepMsg"], self.data)
            #logging.info(params_var)

        elif self.data[0] == 213:
            logging.info(f"iotRxAdmv4420RegRepMsg length is {len(self.data)}")
            #params_var = unpack(self.strFormats["iotRxAdmv4420RegRepMsg"], self.data)
            #logging.info(params_var)

        elif self.data[0] == 216:
            logging.info(f"iotRxAdmv4420RegRepMsg length is {len(self.data)}")
            #params_var = unpack(self.strFormats["iotRxAdmv4420RegRepMsg"], self.data)
            #logging.info(params_var)

        elif self.data[0] == 222:
            logging.info(f"batParamRep length is {len(self.data)}")
            params_var = unpack(self.strFormats["batParamRep"], self.data)
            logging.info(params_var)

            self.all_strck.batParamRep = {
                "opcode": params_var[0],
                "tempK": params_var[1],
                "voltage": params_var[2],
                "current": params_var[3],
                "avgCurrent": params_var[4],
                "remainingCapacity": params_var[5],
                "fullChargeCapacity": params_var[6],
                "runTimeToEmpty": params_var[7],
                "avgTimeToEmpty": params_var[8],
                "avgTimeToFull": params_var[9],
                # 0...65534 - remain predicted time to full charged, 65535 - battery is not being charged.
                "chargingCurrent": params_var[10],
                "chargingVoltage": params_var[11],
                "batteryStatus": params_var[12],  # See bq20z95_tech_manual.pdf page 80.
                "designCapacity": params_var[13],  # // Design capacity in units of mAh.
                # ------Calculated individual cell voltages, in mV. -------
                "cellVoltage3": params_var[14],
                "cellVoltage2": params_var[15],
                "cellVoltage1": params_var[16],
                "digTemp": params_var[17]
            }
            logging.info(self.all_strck.batParamRep)

        elif self.data[0] == 224:
            logging.info(f"dataConfigFileRepMsg length is {len(self.data)}")

        elif self.data[0] == 226:
            logging.info(f"iotTDDHubEventMsg length is {len(self.data)}")

        elif self.data[0] == 227:
            logging.info(f"modemRxConfigRepMsg length is {len(self.data)}")

        elif self.data[0] == 228:
            logging.info(f"modemRxConfigRepMsg length is {len(self.data)}")

        elif self.data[0] == 230:
            logging.info(f"modemToHubReportMsg length is {len(self.data)}")


#------------------------------------------------
#-----From Here will be in main :
# all wanted structs will be available by demand.
#------------------------------------------------

my_date = datetime.now().date()
t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
log = logging.getLogger('start_receiving')
logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)

def rcv_the_packets():
    FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
    #logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

    for [data, addr] in rcvD.start_receiving():
        log.debug(f"data {data} addr {addr}")
        logging.info(f"{data[0]}")
        rcvD.updateFeildsFromInputMsg()

def send_packets():
    time_to_wait = 2
    while True:
        print("sending ...")
        rcvD.send_receive_order()
        iCD = Drivers.Terminal.iCDs
        all_strck = icd_strucks()
        all_strck.PICReadWriteMsg["cmd"] = iCD.SPI_READ
        all_strck.PICReadWriteMsg["data"] = 0
        sdm = Send_The_Data()
        sdm.send_the_message("PICReadWriteMsg", all_strck.PICReadWriteMsg)
        all_strck.modemRegCommandMsg["opcode"] = iCD.MODEM_REGISTER
        all_strck.modemRegCommandMsg["cmd"] = iCD.SPI_READ
        all_strck.modemRegCommandMsg["addr"] = 15 # 14 (DEC) = 0xE (HEX)
        sdm.send_the_message("modemRegCommandMsg", all_strck.modemRegCommandMsg)
        time.sleep(time_to_wait)


if __name__ == "__main__":
    rcvD = ReceiveData()
    rcvD.send_receive_order()
    t1 = threading.Thread(target=rcv_the_packets, daemon=True)
    t1.start()
    t2 = threading.Thread(target=send_packets, daemon=True)
    t2.start()
    time.sleep(6)



