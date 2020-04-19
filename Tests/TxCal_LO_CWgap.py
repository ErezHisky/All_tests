from Drivers.SigGenCtrl import *
from Drivers.Spectrum_bb60c import *
from Drivers.StepEngineCtrl import *
from Drivers.Terminal.iCDs import *
from Drivers.ExcelCtrl import *
from Drivers.DigAtt64bit import *
from Drivers.Terminal.SendDataMsg import *
from Tests.commFunctions import *
from Tests.all_init import *
import logging


class TxCalib(allInitDefinitions):
    def __init__(self):
        self.mybb60csa = bb60c_scpi()
        self.mySig = MySignalGenerator()
        super().__init__()

    def activate(self):
        my_date = datetime.now().date()
        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        logging.basicConfig(filename=f"D:/TesterLogs/TesterLog_{my_date}_{current_time}.txt", level=logging.DEBUG)

        freq_s = [27500, 28000, 29000, 30000, 30500]
        angle_x = 0
        angle_y = 0
        res_cw = [0, -120]
        span = 0.5 * 1e6
        ref_lvl = -40

        # put Dig Atten on 30dB
        print("Dig Atten on 30dB")
        self.myAtt.set_attenuation(30.0)

        # turn on tx
        logging.info("turning Tx on...")
        turn_tx_on()
        open_Tx_pic() # only for static uut
        gap_between_tx_cal()

        logging.info("turning CW on...")
        set_cw()
        set_i_q(100, 100)
        # put Dig Atten on 5dB
        print("Dig Atten on 5dB")
        self.myAtt.set_attenuation(5.0)

        self.mySig.changeAmp(10.0)
        self.mySig.turnRfOn()
        self.mySig.turnModOff()

        logging.info("configuring the excel...")
        self.ws6.append(["X", "Y", "fre sig gen", "uut Freq(GHz)", "tpc", "freq cw", "Pout-cw",
                    "freq lo", "Pout lo", "freq iq", "Pout iq", "dalta cw-lo", "delta cw-iq"])

        logging.info(f"starts at {datetime.now()}")
        print(datetime.now())

        # TPC will be in p1dB point
        tpc_num = 30
        print(f"tpc is {tpc_num}")
        set_TPC(tpc_num)

        try:
            for freq_i in freq_s:
                self.all_strck.Lmx2592FreqMsg["val"] = freq_i
                self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)
                time.sleep(0.5)
                logging.info("config Sig Gen ...")
                sigFreq = freq_i/1000 - 3.0
                self.mySig.changeFreq(sigFreq)

                res_cw = [0, -120]
                print(type(res_cw))

                print("waiting after changing freq... ")
                look_index = 0
                while (res_cw[1] < -110):
                    res_cw = self.mybb60csa.get_peak_search(2.999 * 1e9, span, ref=-10)
                    print(res_cw[1])
                    time.sleep(1)
                    look_index += 1
                    if look_index > 20:
                        self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)
                        look_index = 0

                # measure Pout:
                logging.info("Read from sa...")
                res_cw = self.mybb60csa.get_peak_search(2.999 * 1e9, span, ref=-10)
                time.sleep(1)
                res_lo = self.mybb60csa.get_peak_search(3 * 1e9, span, ref_lvl)
                time.sleep(1)
                res_iq_emb = self.mybb60csa.get_peak_search(3.001 * 1e9, span, ref_lvl)
                time.sleep(1)
                self.ws6.append( [ angle_x, angle_y, float(sigFreq * 1e9), float(freq_i * 1e6), int(tpc_num), float(res_cw[0]),
                              float(res_cw[1]), float(res_lo[0]), float(res_lo[1]), float(res_iq_emb[0]), float(res_iq_emb[1]),
                              float(res_cw[0] - res_lo[0]), float(res_cw[0] - res_iq_emb[0]) ] )

            print('Done Tx calibration !')

        finally:
            print(datetime.now())
            logging.info(f"stoped at {datetime.now()}")
            turn_tx_off()
            self.mybb60csa.close_spike()
            self.mySig.closeConnection()

            self.me.saveTheWorkBookWithtimestamp()


