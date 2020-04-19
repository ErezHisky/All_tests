from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.iCDs import *

all_strcks = icd_strucks()
my_strFormats = all_strcks.strFormats
sdm = Send_The_Data()

def C0_set_TPC(tpc_indx):

    tpc71val = TPC_VEC[tpc_indx][0]
    tpcPIC4val = TPC_VEC[tpc_indx][1]
    # send the tpc message:
    all_strcks.PICReadWriteMsg["addr"] = 4
    all_strcks.PICReadWriteMsg["data"] = tpcPIC4val
    sdm.send_the_message("PICReadWriteMsg", all_strcks.PICReadWriteMsg)
    time.sleep(1)
    all_strcks.MxFEAxiRegMsg["addr"] = 0x71
    all_strcks.MxFEAxiRegMsg["data"] = tpc71val
    sdm.send_the_message("MxFEAxiRegMsg", all_strcks.MxFEAxiRegMsg)
    time.sleep(1)


print(C0_set_TPC(3))