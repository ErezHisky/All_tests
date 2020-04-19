import pyvisa
import time


class MySA:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.N9010B = self.rm.open_resource('TCPIP0::192.168.1.35::hislip0::INSTR')
        self.N9010B.write(':FORMat:TRACe:DATA %s,%d' % ('REAL', 64))
        self.data_format = self.N9010B.query_ascii_values(':FORMat:TRACe:DATA?', converter='s')

    def change_freq(self, freq_hz=20000000000.0):
        self.N9010B.write(':SENSe:FREQuency:CENTer %G' % (freq_hz))

    def set_span(self, span=2000000.0):
        self.N9010B.write(':SENSe:FREQuency:SPAN %G' % (span))

    def set_res_bw(self, rbw = 1000000.0):
        self.N9010B.write(':SENSe:BWIDth:RESolution %G' % (rbw))

    def set_rbw_auto(self):
        self.N9010B.write(':SENSe:BWIDth:RESolution:AUTO %d' % (1))

    def set_marker_max(self):
        self.N9010B.write(':CALCulate:MARKer:MAXimum')

    def set_continue_peak_search_on(self):
        self.N9010B.write(':CALCulate:MARKer:CPSearch:STATe %d' % (1))

    def set_continue_peak_search_off(self):
        self.N9010B.write(':CALCulate:MARKer:CPSearch:STATe %d' % (0))

    def set_avg(self):
        self.N9010B.write(':SENSe:AVERage:STATe %d' % (1))

    def get_marker_mode(self):
        return self.N9010B.query(':CALCulate:MARKer:PEAK:SEARch:MODE?')

    def get_marker_power(self):
        time.sleep(2.5)
        temp_values = self.N9010B.query_ascii_values(':CALCulate:MARKer:Y?')
        return temp_values[0]

    def close_sa(self):
        self.N9010B.close()
        self.rm.close()


if __name__ == "__main__":
    sa = MySA()
    sa.change_freq()
    sa.set_span()
    sa.set_res_bw()
    sa.set_rbw_auto()
    sa.set_marker_max()
    sa.set_continue_peak_search_on()
    print(sa.get_marker_mode())
    sa.set_avg()
    print("marker mode is: ", sa.get_marker_mode())
    for n in range(1,6):
        print("power measured is: ", sa.get_marker_power())
    sa.close_sa()
    print('Done')
