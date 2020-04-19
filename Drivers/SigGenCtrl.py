import pyvisa
import time


class MySignalGenerator():
    def __init__(self):
        self.rm = pyvisa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
        self.inst = 'TCPIP0::192.168.1.111::inst0::INSTR'
        try:
            self.N5183B = self.rm.open_resource(self.inst)
        except:
            print("Signal Generator was off, please turn it on.")
            r = input(print("is it on ? press yes and enter."))
            if r == "yes":
                self.N5183B = self.rm.open_resource(self.inst)

    def changeFreq(self, newFreq = 1.0):
        self.N5183B.write('SOURce:FREQuency:CW %G GHz' % (newFreq))

    def changeAmp(self, newAmp = 0.0):
        self.N5183B.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %G' % (newAmp))

    def turnRfOn(self):
        self.N5183B.write(':OUTPut:STATe %d' % (1))

    def turnRFOff(self):
        self.N5183B.write(':OUTPut:STATe %d' % (0))

    def turnModOff(self):
        self.N5183B.write(':OUTPut:MODulation:STATe %d' % (0))

    def closeConnection(self):
        self.turnRFOff()
        self.N5183B.close()
        self.rm.close()


if __name__ == "__main__":
    mySig = MySignalGenerator()
    mySig.changeFreq()
    mySig.changeAmp()
    mySig.turnRfOn()
    mySig.turnModOff()
    time.sleep(2)
    mySig.turnRFOff()
    mySig.closeConnection()

    print ('Done')

