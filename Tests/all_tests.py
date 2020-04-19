from Tests.FirstPrep import *
from Tests.ImuNGps import *
from Tests.TCXO_Cal import *
from Tests.EIRP_Tx import *
from Tests.p1dB import *
from Tests.TxCal_LO_CWgap import *
from Tests.EIRP_Rx import *
from Tests.RxGainNnf import *



class all_tests():
    def __init__(self):
        ipusAll()

    # ==============================
    #       General
    # ==============================
    def first_prep(self):
        self.fp = firstPrep()
        self.fp.activate()

    def imu_gps(self):
        self.ig = imuNgps()
        self.ig.activate()

    def tcxo_cal(self):
        self.tc = tcxo_cal()
        self.tc.activate()
    #==============================
    #       Tx
    #==============================

    def eirp_tx(self):
        self.et = eirp_tx()
        self.et.activate()

    def p1db(self):
        self.p1 = p1db()
        self.p1.activate()

    def tx_cal_verification(self):
        self.tcv = TxCalib()
        self.tcv.activate()

    def TxActivate(self):
        print("Tx want to start ! if setup is ready - press yes")
        react = input()
        if react == "yes":
            self.eirp_tx()
            self.p1db()
            self.tx_cal_verification()
        else:
            self.TxActivate()
    # ==============================
    #       Rx
    # ==============================
    def eirp_rx(self):
        self.er = eirp_rx()
        self.er.activate()

    def rx_gain_nf(self):
        self.gnf = rx_gain_nf()
        self.gnf.activate()

    def RxActivate(self):
        print("Rx want to start ! if setup is ready - press yes")
        react = input()
        if react == "yes":
            self.eirp_rx()
            self.rx_gain_nf()
        else:
            self.RxActivate()

    # ==============================
    #       Link
    # ==============================
    def full_link(self):
        pass

    def activateAll(self):
        self.first_prep()
        self.imu_gps()
        self.tcxo_cal()
        self.TxActivate()
        self.RxActivate()
        self.full_link()


if __name__ == "__main__":
    my_all_test = all_tests()
    my_all_test.activateAll()