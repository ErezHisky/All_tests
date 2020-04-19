
from Drivers.ExcelCtrl import *
from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.ReadEthData import *
from Drivers.Spectrum_bb60c import *
from Drivers.SigGenCtrl import *

class allInitDefinitions:

    log = logging.getLogger('start_receiving')
    all_strck = icd_strucks()
    iCD = Drivers.Terminal.iCDs
    sdm = Send_The_Data()

    rcvD = ReceiveData()
    rcvD.send_receive_order()

    me = MyExcel()
    ws1 = me.ws  # .my_sheet
    me.change_sheet_title(ws1, "first prep")
    ws2 = me.create_new_sheet("imuNgps")
    ws3 = me.create_new_sheet("TCXO cal")
    ws4 = me.create_new_sheet("EiRP_Tx")
    ws5 = me.create_new_sheet("p1dB")
    ws6 = me.create_new_sheet("Tx Cal")
    ws7 = me.create_new_sheet("EiRP_Rx")
    ws8 = me.create_new_sheet("Rx_Gain_NF")

    myAtt = DigAtt64()

    def __init__(self):
        pass
