from Drivers.SigGenCtrl import *
from Drivers.Spectrum_bb60c import *
from Drivers.StepEngineCtrl import *
from Drivers.Terminal.iCDs import *
from Drivers.ExcelCtrl import *
from Drivers.DigAtt64bit import *
from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.ReadEthData import *
from Tests.commFunctions import *
from Tests.all_init import *
import logging
import json
import threading


class p1db(allInitDefinitions):
    def __init__(self):
        with open('D:/Documents/TestersDocs/tpc.json') as f:
          self.tpc_data = json.load(f)

        self.freq_s = [27000, 28000, 29000]  # [25000, 26000, 27000, 28000, 29000, 30000]
        self.tpc_data["cells"][2]["pwr tx"]["static"]["total freqs"] = len(self.freq_s)
        self.angle_x = 0
        self.angle_y = 0
        self.stop_thread = False
        self.real_line = []
        self.theor_line = []
        self.p1db_freq = []
        self.temp = [0, 0, 0]
        self.result = [-100, -90]
        self.result1 = [-100, -90]

        self.mybb60csa = bb60c_scpi()
        self.mySig = MySignalGenerator()
        super.__init__()

    def rcv_the_packets(self):
        for [data, addr] in self.rcvD.start_receiving():
            self.rcvD.updateFeildsFromInputMsg()
            self.update_temp()
            if self.stop_thread:
                break

    def update_temp(self):
        self.temp = [self.rcvD.all_strck.batParamRep["tempK"] / 10 - 273.15 , self.rcvD.all_strck.batParamRep["digTemp"],
                     self.rcvD.all_strck.PICReadWriteMsg["data"]]

    def send_packets(self):
        time_to_wait = 0.5
        while True:
            self.rcvD.send_receive_order()
            # read rf temp
            self.all_strck.PICReadWriteMsg["cmd"] = self.all_strck.iCD.SPI_READ
            self.all_strck.PICReadWriteMsg["addr"] = 8
            self.sdm.send_the_message("PICReadWriteMsg", self.all_strck.PICReadWriteMsg)
            time.sleep(time_to_wait)
            if self.stop_thread:
                break


    def activate(self):
        my_date = datetime.now().date()
        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)

        # put Dig Atten on 20dB
        print("Dig Atten on 20dB")
        self.myAtt.set_attenuation(20.0)

        open_Tx_pic() # only for static uut
        # turn on tx
        logging.info("turning Tx on...")
        turn_tx_on()

        # logging.info("turning CW on...")
        # set_cw()
        # put Dig Atten on 5dB
        print("Dig Atten on 5dB")
        self.myAtt.set_attenuation(5.0)

        self.mySig.changeAmp(10.0)
        self.mySig.turnRfOn()
        self.mySig.turnModOff()

        logging.info("configuring the excel...")
        self.ws5.append(["X", "Y", "uut Freq(GHz)", "fre sig gen", "freq sa", "TPC value", "Pout-sa", "tempK", "digTemp", "Rf temp"])

        logging.info(f"starts at {datetime.now()}")
        print(datetime.now())

        self.stop_thread = False
        t1 = threading.Thread(target=self.rcv_the_packets)
        t1.start()
        t2 = threading.Thread(target=self.send_packets)
        t2.start()

        ref_lvl = 0

        try:
            for freq_i in self.freq_s:
                self.all_strcks.Lmx2592FreqMsg["val"] = freq_i
                self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)

                logging.info("config Sig Gen ...")
                sigFreq = freq_i / 1000 - 3.0
                self.mySig.changeFreq(sigFreq)

                self.result = self.result1 = [0,0]
                print("waiting for freq changed ... ")
                self.mybb60csa.freq(3 * 1e9)
                self.mybb60csa.span(20 * 1e6)
                self.mybb60csa.rbw(3 * 1e6)
                self.mybb60csa.vbw(3 * 1e4)
                self.mybb60csa.ref_lvl(-20.0)
                time.sleep(3) # for the privious freq to disapear
                self.result1 = self.mybb60csa.peak_search()
                self.result = self.result1.copy()
                count = 0
                while (self.result[1] - self.result1[1] < 5.0):
                    self.result = self.mybb60csa.peak_search()
                    count += 1
                    time.sleep(1)
                    if count % 20 == 0:
                        self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)
                        self.result1 = self.mybb60csa.peak_search()
                        self.result = self.result1.copy()
                    if count > 30 and self.result[1] > -70:
                        break

                self.real_line.clear()
                # The start TPC will be from minimum Pout
                for tpc_num in range(76, -1, -1):
                    print(f"tpc is {tpc_num}")
                    logging.info(f"tpc is {tpc_num}")
                    set_TPC(tpc_num)
                    if tpc_num == 76:
                        set_TPC(tpc_num)
                        time.sleep(1)
                        self.result = self.mybb60csa.peak_search()

                    # measure Pout:
                    logging.info("Read from sa...")
                    ref_lvl = self.result[1] + 20
                    self.mybb60csa.ref_lvl(round(ref_lvl))
                    self.result = self.mybb60csa.peak_search()
                    self.ws5.append([self.angle_x, self.angle_y, float(freq_i * 1e6), float(sigFreq * 1e9), float(self.result[0]),
                                float(tpc_num), float(self.result[1]), float(self.temp[0]), float(self.temp[1]), float(self.temp[2])])
                    real_line.append([float(self.result[1]), tpc_num])

                p1db = calculate_p1db(self.real_line)
                self.p1db_freq.append(p1db)
                self.ws5.append(["p1db pout", p1db[0], "p1db tpc", p1db[1]])
                self.ws5.append([])  # add a blank raw between freq

            print(f"p1db_freq is {self.p1db_freq}")
            logging.info(f"freq list is {self.freq_s}")
            logging.info(f"p1db_freq is {self.p1db_freq}")
            all_tpc = []
            for n in self.p1db_freq:
                all_tpc.append(n[1])
            self.tpc_data["cells"][2]["pwr tx"]["static"]["temps"][0]["tcp num p1db"] = all_tpc

            print('Done p1db !')

        finally:
            self.stop_thread = True
            t1.join()
            t2.join()
            print(datetime.now())
            logging.info(f"stoped at {datetime.now()}")
            self.myAtt.set_attenuation(50.0)
            turn_tx_off()
            self.mybb60csa.close_spike()
            self.mybb60csa.close_device()
            self.mySig.closeConnection()

            with open(f'D:/Documents/TestersDocs/tpc_{my_date}_{current_time}.json', 'w') as json_file:
                json.dump(self.tpc_data, json_file, indent=4)

            self.me.saveTheWorkBookWithtimestamp()


