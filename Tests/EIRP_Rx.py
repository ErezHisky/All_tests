from Drivers.SigGenCtrl import *
from Drivers.Spectrum_bb60c import *
from Drivers.StepEngineCtrl import *
from Drivers.Terminal.iCDs import *
from Drivers.ExcelCtrl import *
from Drivers.DigAtt64bit import *
from Drivers.Terminal.SendDataMsg import *
from Tests.commFunctions import *
from Drivers.Terminal.ReadEthData import *
from Tests.all_init import *
from datetime import *


class eirp_rx(allInitDefinitions):
    def __init__(self):
        self.freq_s = [18500, 19000, 20500]
        self.stop_thread = False
        self.angle_x = 0
        self.angle_y = 0
        self.i=0
        self.q=0
        self.sum_i = self.sum_q = 0
        self.my_eng = MyStepEngine("azimuth")
        self.mySig = MySignalGenerator()
        super.__init__()

    # read i, q
    def rcv_the_packets(self):
        ctime = time.time()
        for [data, addr] in self.rcvD.start_receiving():
            self.rcvD.updateFeildsFromInputMsg()
            self.update_i_q()
            if self.stop_thread:
                break

    def update_i_q(self):
        if self.rcvD.all_strck.modemRegCommandMsg["addr"] == 14:
            self.i = self.rcvD.all_strck.modemRegCommandMsg["data"]
        elif self.rcvD.all_strck.modemRegCommandMsg["addr"] == 15:
            self.q = self.rcvD.all_strck.modemRegCommandMsg["data"]

    def send_packets(self):
        time_to_wait = 0.5
        while True:
            # print("sending ...")
            self.all_strck.modemRegCommandMsg["opcode"] = self.all_strck.iCD.MODEM_REGISTER
            self.all_strck.modemRegCommandMsg["cmd"] = self.all_strck.iCD.SPI_READ
            self.all_strck.modemRegCommandMsg["addr"] = 15  # 15 (DEC) = 0xF (HEX)
            self.sdm.send_the_message("modemRegCommandMsg", self.all_strck.modemRegCommandMsg)
            time.sleep(time_to_wait)
            self.all_strck.modemRegCommandMsg["addr"] = 14  # 14 (DEC) = 0xE (HEX)
            self.sdm.send_the_message("modemRegCommandMsg", all_strcks.modemRegCommandMsg)
            time.sleep(time_to_wait)
            if self.stop_thread:
                break

    def activate(self):

        self.ws7.append(["X", "Y", "uut Freq(GHz)", "freq sig gen", "Pin_sg", "Irms", "Qrms", "Rssi(I,Q)"])

        self.mySig.turnRfOn()
        self.mySig.turnModOff()

        self.stop_thread = False
        t1 = threading.Thread(target=self.rcv_the_packets)
        t1.start()
        t2 = threading.Thread(target=self.send_packets)
        t2.start()

        try:
            print(datetime.now())
            print("entering the freq loop...")
            # every freq - configure frequency
            for freq_i in self.freq_s:
                self.all_strck.Admv4420FreqMsg["rfFreq"] = freq_i
                self.sdm.send_the_message("Admv4420FreqMsg", all_strcks.Admv4420FreqMsg)
                time.sleep(1)

                #Read from sa
                print("config Sig Gen ...")
                sigFreq = freq_i/1000 + 1e-3
                ampSig = -10.0
                self.mySig.changeFreq(sigFreq)
                self.mySig.changeAmp(ampSig)

                #every angle - save to excel
                print("entering the angle loop...")
                self.my_eng.check_communication()
                #change unit angle between -30 to +30:
                #x axis
                for ang in range(-30, 31, 2):
                    time.sleep(3)
                    print("changing angle...")
                    self.my_eng.rotate_absolute(str(ang))
                    # Reading i,q:

                    for ii in range(5):
                        self.sum_i = self.sum_i + i
                        time.sleep(0.4)
                    avg_i = self.sum_i / 5
                    for qq in range(5):
                        self.sum_q = self.sum_q + q
                        time.sleep(0.4)
                    avg_i = self.sum_i / 5
                    avg_q = self.sum_q / 5
                    ws1.append([int(ang), int(angle_y), float(freq_i * 1e6), float(sigFreq * 1e9), float(ampSig),
                                float(numpy.sqrt(avg_i)), float(numpy.sqrt(avg_q)), float(numpy.sqrt(i + q))])
                self.my_eng.get_to_home()

                self.my_eng.change_engine_type()
                self.angle_x = 0
                #y axis
                for ang in range(-30, 31, 2):
                    time.sleep(3)
                    print("changing angle...")
                    self.my_eng.rotate_absolute(str(ang))
                    # Reading i,q:
                    for ii in range(5):
                        self.sum_i = self.sum_i + i
                        time.sleep(0.4)
                    avg_i = self.sum_i / 5
                    for qq in range(5):
                        self.sum_q = self.sum_q + q
                        time.sleep(0.4)
                    avg_i = self.sum_i / 5
                    avg_q = self.sum_q / 5
                    ws1.append([int(angle_x), int(ang), float(freq_i * 1e6), float(sigFreq * 1e9), float(ampSig),
                                float(numpy.sqrt(avg_i)), float(numpy.sqrt(avg_q)), float(numpy.sqrt(i + q))])
                self.my_eng.get_to_home()
                self.my_eng.change_engine_type()
                self.angle_y = 0
            print(datetime.now())

        finally:
            turn_tx_off()
            self.mySig.closeConnection()
            self.my_eng.close_engine()
            self.me.saveTheWorkBookWithtimestamp()

            self.stop_thread = True
            t1.join()
            t2.join()

        print('Done eirp rx !')


