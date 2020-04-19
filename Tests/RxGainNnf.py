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
import math
from datetime import *
import time



class rx_gain_nf(allInitDefinitions):

    def __init__(self):
        self.freq_s = [18500, 19000, 20500]
        self.stop_thread = False
        self.calib = 70 # estimated, will be measured
        self.rf_snr = self.bb_snr = self.rx_gain = self.nf = 0
        self.angle_x = 0
        self.angle_y = 0
        self.sum_noise_iq = 0
        self.i=0
        self.q=0
        self.mySig = MySignalGenerator()
        super().__init__()

    #read i, q
    def rcv_the_packets(self):
        for [data, addr] in self.rcvD.start_receiving():
            self.rcvD.updateFeildsFromInputMsg()
            self.update_i_q()
            if self.stop_thread:
                break


    def update_i_q(self):
        if self.rcvD.all_strck.modemRegCommandMsg["addr"] == 14:
            self.i = rcvD.all_strck.modemRegCommandMsg["data"]
        elif self.rcvD.all_strck.modemRegCommandMsg["addr"] == 15:
            self.q = rcvD.all_strck.modemRegCommandMsg["data"]


    def send_packets(self):
        time_to_wait = 2
        while True:
            #print("sending ...")
            self.all_strck.modemRegCommandMsg["opcode"] = self.all_strck.iCD.MODEM_REGISTER
            self.all_strck.modemRegCommandMsg["cmd"] = self.all_strck.iCD.SPI_READ
            self.all_strck.modemRegCommandMsg["addr"] = 15 # 15 (DEC) = 0xF (HEX)
            self.sdm.send_the_message("modemRegCommandMsg", self.all_strck.modemRegCommandMsg)
            time.sleep(0.5)
            self.all_strck.modemRegCommandMsg["addr"] = 14  # 14 (DEC) = 0xE (HEX)
            self.sdm.send_the_message("modemRegCommandMsg", self.all_strck.modemRegCommandMsg)
            time.sleep(time_to_wait)
            if self.stop_thread:
                break

    def activate(self):

        self.ws8.append(["X", "Y", "uut Freq(GHz)", "freq sig gen", "Calib", "Pin_sg", "Irms", "Qrms", "Rssi(I,Q)",
                    "Noise(I,Q)", "RF_SNR", "BB_SNR", "Rx_Gain", "NF"])


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
                self.sdm.send_the_message("Admv4420FreqMsg", self.all_strck.Admv4420FreqMsg)
                time.sleep(1)

                print("config Sig Gen ...")
                sigFreq = freq_i / 1000 + 1e-3
                ampSig = -100.0
                self.mySig.changeAmp(ampSig)
                self.mySig.changeFreq(sigFreq)

                print("sig pow off")
                self.mySig.turnRFOff()
                #calculate avg - noise_iq
                sum_noise_iq = 0
                for n in range(5):
                    time.sleep(3) # wait for i and q to update
                    noise_iq = math.sqrt(i + q)
                    if noise_iq == 0:
                        continue
                    self.sum_noise_iq = self.sum_noise_iq + noise_iq
                    print(f"--------noise is {noise_iq}")
                noise_iq = self.sum_noise_iq / 5

                print("sig pow on")
                self.mySig.turnRfOn()
                time.sleep(3)  # wait for i and q to update
                rssi_iq = math.sqrt(i + q)

                print(f"rssi_iq is {rssi_iq}, noise_iq is {noise_iq}")
                while rssi_iq < 120 or rssi_iq > 150:
                    print(f"rssi_iq is {rssi_iq}, noise_iq is {noise_iq}")
                    ampSig += 1
                    mySig.changeAmp(ampSig)
                    time.sleep(3)
                    rssi_iq = math.sqrt(i + q)

                # unit angle in boresight:
                time.sleep(3)
                print("changing angle to boresight (uut home)...")
                '''my_eng = MyStepEngine("azimuth")
                my_eng.check_communication()
                my_eng.'''
                #calculate:
                self.rf_snr = ampSig + 87 - self.calib
                self.bb_snr = 20* numpy.log(rssi_iq/noise_iq)
                self.nf = self.rf_snr - self.bb_snr
                self.rx_gain = 20*numpy.log(rssi_iq - 17 - (ampSig - self.calib))
                self.ws8.append([int(self.angle_x), int(self.angle_y), float(freq_i * 1e6),
                                 float(sigFreq * 1e9), float(self.calib), float(ampSig), float(math.sqrt(i)),
                                 float(math.sqrt(q)), float(rssi_iq), float(noise_iq), float(self.rf_snr),
                                 float(self.bb_snr), float(self.rx_gain), float(self.nf) ])
            print(datetime.now())

        finally:

            turn_tx_off()
            self.mySig.closeConnection()

            self.me.saveTheWorkBookWithtimestamp()

            self.stop_thread = True
            t1.join()
            t2.join()


        print('Done Rx Gain NF calculate !')


