from Drivers.SigGenCtrl import *
from Drivers.Spectrum_bb60c import *
from Drivers.StepEngineCtrl import *
from Drivers.Terminal.iCDs import *
from Drivers.ExcelCtrl import *
from Drivers.DigAtt64bit import *
from Drivers.Terminal.SendDataMsg import *
from Tests.commFunctions import *
from Tests.all_init import *


class eirp_tx(allInitDefinitions):
    def __init__(self):
        self.freq_s = [28500, 29000, 30500]
        self.angle_x = 0
        self.angle_y = 0
        self.my_eng = MyStepEngine("azimuth")
        self.mybb60csa = bb60c_scpi()
        self.mySig = MySignalGenerator()
        super.__init__()

    def activate(self):
        self.myAtt.set_attenuation(30.0)

        open_Tx_pic()
        turn_tx_on()

        # TPC at saturation:
        print("TPC at saturation...")
        tpc_num = 0
        set_TPC(tpc_num)

        self.ws4.append(["X", "Y", "uut Freq(GHz)", "fre sig gen", "freq sa", "Pout","TPC-value"])

        # put Dig Atten on 5dB
        print("Dig Atten on 5dB")
        self.myAtt.set_attenuation(5.0)

        try:
            self.mybb60csa.rbw(3 * 1e6)
            self.mybb60csa.vbw(3 * 1e4)
            self.mybb60csa.span(30.0 * 1e6)
            self.mybb60csa.ref_lvl(-40.0)
            print("entering the freq loop...")
            # every freq - configure frequency
            for freq_i in self.freq_s:
                self.all_strcks.Lmx2592FreqMsg["val"] = freq_i
                self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strcks.Lmx2592FreqMsg)
                time.sleep(1)
                self.mybb60csa.freq(freq_i * 1e6)

                #Read from sa
                print("config Sig Gen ...")
                sigFreq = freq_i/1000 - 3.0
                mySig.changeFreq(sigFreq)
                mySig.changeAmp(10.0)
                mySig.turnRfOn()
                mySig.turnModOff()

                #every angle - save to excel
                print("entering the angle loop...")
                self.my_eng.check_communication()
                #change unit angle between -30 to +30:
                for ang in range(-30, 31, 2):
                    time.sleep(3)
                    print("changing angle...")

                    self.my_eng.rotate_absolute(str(ang))

                    print("Read from sa...")
                    result = self.mybb60csa.peak_search()
                    self.ws4.append([int(ang), int(self.angle_y), float(freq_i*1e6), float(sigFreq*1e9), float(result[0]),
                                float(result[1]), float(tpc_num)])

                self.my_eng.get_to_home()
                self.my_eng.change_engine_type()
                self.angle_x = 0
                for ang in range(-30, 31, 2):
                    time.sleep(3)
                    print("changing angle...")

                    self.my_eng.rotate_absolute(str(ang))

                    print("Read from sa...")
                    result = self.mybb60csa.get_power_in_freq_rbw_vbw(3 * 1e9, 20 * 1e6)
                    self.ws4.append([int(self.angle_x), int(ang), float(freq_i * 1e6), float(sigFreq * 1e9), float(result[0]),
                                float(result[1]), float(tpc_num)])

                self.my_eng.get_to_home()
                self.my_eng.change_engine_type()
                self.angle_y = 0

            print('Done eirp tx test !')

        finally:
            turn_tx_off()
            self.mybb60csa.close_spike()
            self.mySig.closeConnection()
            self.my_eng.close_engine()
            self.me.saveTheWorkBookWithtimestamp()


