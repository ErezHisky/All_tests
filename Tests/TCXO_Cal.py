import logging
import time
from datetime import datetime
from Drivers.ExcelCtrl import *
from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.ReadEthData import *
from Tests.commFunctions import *
from Drivers.StepEngineCtrl import *
from Drivers.DigAtt64bit import *
from Drivers.Spectrum_bb60c import *
from Drivers.SigGenCtrl import *
from Tests.all_init import *


class tcxo_cal(allInitDefinitions):
    def __init__(self):
        self.stop_thread = False
        self.Signal_freq = 26.0
        self.ang_x = self.ang_y = 0
        self.tpc_val = 0
        self.my_eng = MyStepEngine("azimuth")
        self.mybb60csa = bb60c_scpi()
        self.mySig = MySignalGenerator()
        super().__init__()

    def activate(self):
        try:
            self.mySig.changeFreq(self.Signal_freq)
            self.mySig.changeAmp(10.0)
            self.ySig.turnRfOn()
            self.mySig.turnModOff()

            my_date = datetime.datetime.now().date()
            t = time.localtime()
            current_time = time.strftime("%H_%M_%S", t)
            logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)

            #DigAtt - 30dB (for SA protection)
            self.myAtt.set_attenuation(30.0)

            open_Tx_pic()
            turn_tx_on()
            unit_Freq = 29000
            self.all_strck.Lmx2592FreqMsg["val"] = unit_Freq
            self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)
            time.sleep(1)

            # transmit LO (MB register)
            print("turn LO on...")
            self.all_strck.MxFEAxiRegMsg["addr"] = 0x71
            self.all_strck.MxFEAxiRegMsg["data"] = 0x0
            self.sdm.send_the_message("MxFEAxiRegMsg", self.all_strck.MxFEAxiRegMsg)
            time.sleep(1)
            # turn off modem (PIC register)
            print("turn off modem...")
            self.all_strck.PICReadWriteMsg["opcode"] = self.iCD.PIC_REG_SET_GET
            self.all_strck.PICReadWriteMsg["addr"] = 4
            self.all_strck.PICReadWriteMsg["data"] = 0x708
            self.sdm.send_the_message("PICReadWriteMsg", self.all_strck.PICReadWriteMsg)
            time.sleep(1)

            #set_TPC(tpc_val)

            #DigAtt - 5dB
            self.myAtt.set_attenuation(5.0)

            # check freq precision
            # peak search in narrow span
            print("configure bb60c sa...")
            span = 100.0*1e3
            sa_results = self.mybb60csa.get_peak_search(3.0*1e9, span)
            logging.info(sa_results)
            expected_freq_in_sa = unit_Freq/1000 - Signal_freq
            logging.debug(sa_results[0] - expected_freq_in_sa * 1e9)
            print(sa_results[0] - expected_freq_in_sa * 1e9)

            print("taking results...")
            for n in range(0,20):
                val2Dac = 1000 + n*1000
                self.all_strck.clkDacMsg["val"] = val2Dac
                print(f"value to clkDacMsg = {val2Dac}")
                self.sdm.send_the_message("clkDacMsg", self.all_strck.clkDacMsg)
                sa_results = self.mybb60csa.get_peak_search(expected_freq_in_sa*1e9, span)
                tcxo_res = sa_results[0] - expected_freq_in_sa * 1e9
                print(tcxo_res)
                logging.info(tcxo_res)
                time.sleep(1)

            print("Done tcxo cal process !")

        finally:
            turn_tx_off()
            self.mybb60csa.close_spike()
            self.my_eng.close_engine()
            #save results to excel
            print("saving to excel...")
            self.ws3.append(["X", "Y", "clkDac val", "Tpc", "Dig Temp"])
            self.ws3.append([float(self.ang_x), float(self.ang_y), float(val2Dac), float(self.tpc_val), ""])
            self.me.saveTheWorkBookWithtimestamp()


            self.mySig.closeConnection()