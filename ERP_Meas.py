from Drivers.DigAtt64bit import *
from Drivers.SigGenCtrl import *
from Drivers.Spectrum_bb60c import *
from Drivers.StepEngineCtrl import *
from Drivers.ExcelCtrl import *
from Drivers.SendTxFreqMsg import *
import Drivers.CreateHeader
from Drivers.logs4me import *

class TestErp:
    def __init__(self):
        self.myAtt = DigAtt64()
        self.myAtt.set_attenuation(0)
        self.currentAtt = self.myAtt.get_att()
        self.mySig = MySignalGenerator()
        self.mySig.changeFreq(26.0)
        self.mySig.changeAmp(15.0)
        self.mySig.turnRfOn()
        self.mySig.turnModOff()
        self.mybb60csa = My_bb60c_sa()
        self.mybb60csa.configure_device(3.0e9, 100e6, -30.0, 1.0e6, 1.0e6)
        self.mybb60csa.get_trace_info()
        self.my_eng = MyStepEngine("azimuth")
        self.me = MyExcel('D:/ExcelFiles/ERP/ERP_ATR.xlsx', 'ERP/ERP_Results')
        self.me.openSheet('Sheet1')

    def run_x(self):
        self.my_eng.check_communication()
        self.my_eng.get_location()
        self.my_eng.engineType = "azimuth" #x axis
        excel_rawindex = 2
        angle = -60
        target_angle = 60
        while (angle < target_angle - 1):
            time.sleep(1)
            self.my_eng.rotate_absolute(str(angle))
            self.me.enterToCell('A' + str(excel_rawindex), '3GHz')
            self.my_eng.engineType = "azimuth"
            self.my_eng.get_location()
            self.check_engine_angle_report(angle)
            self.me.enterToCell('B' + str(excel_rawindex), float(self.my_eng.location))
            self.me.enterToCell('C' + str(excel_rawindex), "0.0")
            self.me.enterToCell('D' + str(excel_rawindex), self.mybb60csa.get_sweep().max())
            self.me.enterToCell('E' + str(excel_rawindex), self.myAtt.get_att())
            angle = angle + 2
            excel_rawindex = excel_rawindex + 1
        self.my_eng.rotate_absolute("90")

        self.me.saveTheWorkBookWithtimestamp()

    def run_y(self):
        self.my_eng.engineType = "elevation"  # y axis
        angle = -60
        target_angle = 60
        while (angle < target_angle - 1):
            time.sleep(1)
            self.my_eng.rotate_absolute(str(angle))
            self.me.enterToCell('A' + str(excel_rawindex), '3GHz')
            self.my_eng.engineType = "elevation"
            self.my_eng.get_location()
            self.me.enterToCell('B' + str(excel_rawindex), "0.0")
            #self.check_engine_angle_report(angle)
            self.me.enterToCell('C' + str(excel_rawindex), float(self.my_eng.location))
            self.me.enterToCell('D' + str(excel_rawindex), self.mybb60csa.get_sweep().max())
            self.me.enterToCell('E' + str(excel_rawindex), self.myAtt.get_att())
            angle = angle + 2
            excel_rawindex = excel_rawindex + 1
        self.my_eng.rotate_absolute("90")
        self.my_eng.engineType = "azimuth"  # x axis
        self.my_eng.rotate_absolute("90")

        self.me.saveTheWorkBookWithtimestamp()

    def check_engine_angle_report(self, ang):
        while self.my_eng.location == 'aa':
            self.my_eng.get_location()
            time.sleep(0.1)

        while (float(self.my_eng.location) > float(ang + 0.2)) or (float(self.my_eng.location) < float(ang - 0.2)):
            self.my_eng.get_location()
            print(self.my_eng.location)
            print("waiting for angle: ", ang)
        print(f"location : {self.my_eng.location} arrived !")

    def close_everything(self):
        self.mySig.turnRFOff()
        self.mySig.closeConnection()
        self.mybb60csa.close_device()
        self.my_eng.close_engine()

class CheckEvm:
    def __init__(self):
        self.myAtt = DigAtt64()
        self.myAtt.set_attenuation(0)
        self.currentAtt = self.myAtt.get_att()
        self.mySig = MySignalGenerator()
        self.mySig.changeFreq(26.0)
        self.mySig.changeAmp(15.0)
        self.mySig.turnRfOn()
        self.mySig.turnModOff()
        self.mybb60csa = My_bb60c_sa()
        self.me = MyExcel('D:/ExcelFiles/EVM/EVM_ATR.xlsx', 'EVM/EVM_Results')
        self.me.openSheet('Sheet1')
        self.excel_rawindex = 2

    def run_evm_test(self, freq_ghz=3, RfLev_dbm=-20, sym_rate_mhz=2.24):
        evm = self.mybb60csa.get_evm(freq_ghz, RfLev_dbm, sym_rate_mhz)
        print(f"freq is: {freq_ghz}, evm is: {evm}")
        self.write_the_result(freq_ghz, EVM=evm)

    def write_the_result(self, freq, x="0.0", y="0.0", EVM=0, Atten=0):
        self.me.enterToCell('A' + str(self.excel_rawindex), f'{freq}GHz')
        self.me.enterToCell('B' + str(self.excel_rawindex), x)
        self.me.enterToCell('C' + str(self.excel_rawindex), y)
        self.me.enterToCell('D' + str(self.excel_rawindex), str(EVM))
        self.me.enterToCell('E' + str(self.excel_rawindex), self.myAtt.get_att())
        self.me.saveTheWorkBookWithtimestamp()
        self.excel_rawindex = self.excel_rawindex + 1

    def close_everything(self):
        self.mySig.turnRFOff()
        self.mySig.closeConnection()
        self.mybb60csa.close_device()


def config_unit(freq=29000):
    my_tx_freq_msg = TxFreqMsg('=BBxd', freq)
    my_tx_freq_msg.send_the_message()

if __name__ == "__main__":
    myLog = MyLog()
    myLog.write_debug_log("this is my ERPdebug")
    myLog.write_warning("this is my warning")
    myLog.write_info_log("this is my info")
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"))

    #ERP test :
    #test = TestErp()
    #test.run_x()
    #print(f"evm is: {test.get_evm(3, )}")
    #test.close_everything()

    #EVM test :
    '''evm_test = CheckEvm()

    config_unit(27000)
    evm_test.run_evm_test(1)

    config_unit(29000)
    evm_test.run_evm_test(3)

    config_unit(31500)
    evm_test.run_evm_test(5.5)

    evm_test.close_everything()
    
    now = datetime.now()
    print(now.strftime("%d/%m/%Y %H:%M:%S"))'''

    print('Done')
