from Drivers.ExcelCtrl import *
from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.ReadEthData import *
from Tests.commFunctions import *
from Drivers.conSSH import *
from Tests.all_init import *


class firstPrep(allInitDefinitions):
    def __init__(self):
        self.stop_thread = False
        self.temp_change = []
        self.time_to_test = 30
        super().__init__()

    def rcv_the_packets(self):
        ctime = time.time()
        for [data, addr] in self.rcvD.start_receiving():
            #logging.debug(f"data {data} addr {addr}")
            self.rcvD.updateFeildsFromInputMsg()
            if time.time() - ctime > 10:
                self.update_batstat_excel()
                ctime = time.time()
            if self.rcvD.all_strck.batParamRep["voltage"] == 0:
                continue
            elif self.rcvD.all_strck.batParamRep["voltage"] / 1000 < 10.9:
                self.stop_thread = True
                break
            if self.stop_thread:
                break
    
    def update_batstat_excel(self):
        if rcvD.all_strck.batParamRep["voltage"] != 0:
            self.ws1.append([self.rcvD.all_strck.batParamRep["voltage"] / 1000, self.rcvD.all_strck.batParamRep["current"] / 1000,
                        self.rcvD.all_strck.batParamRep["runTimeToEmpty"], self.rcvD.all_strck.batParamRep["avgTimeToFull"],
                        self.rcvD.all_strck.batParamRep["tempK"] / 10 - 273.15 , self.rcvD.all_strck.batParamRep["digTemp"],
                        self.all_strck.PICReadWriteMsg["data"]])
    
    def send_packets(self):
        time_to_wait = 1
        while True:
            self.rcvD.send_receive_order()
            self.all_strck = icd_strucks()
            # read rf temp
            self.all_strck.PICReadWriteMsg["cmd"] = self.iCD.SPI_READ
            self.all_strck.PICReadWriteMsg["addr"] = 8
            self.sdm.send_the_message("PICReadWriteMsg", all_strck.PICReadWriteMsg)
            time.sleep(time_to_wait)
            if self.stop_thread:
                break

    def sendReboot(self):
        A = ViMach(usernameProxy='tester', passwordProxy='root')
        A.Reset_VM()
        STA = SSH_Terminal(hostname="192.168.43.1", username='root', password='root', proxy=A.proxy,
                           usernameProxy='tester', passwordProxy='root')
        STA.Write('reboot')
        ping = CheckPingAllAngles('192.168.43.1', 2)
        while (ping == -1):
            time.sleep(5)
            ping = CheckPingAllAngles('192.168.43.1', 2)
        time.sleep(10)

    def currentConsumptionTest(self):
        turn_tx_off()
        # check bat status every 10 sec and upload to excel
        print("checking battery status ...")
        self.ws1.append(["bat Status: "])
        self.ws1.append(["voltage","current", "RunTime2Empty", "AvgTime2Full", "Temp", "Digital Temp", "Rf Temp"])
    
        self.stop_thread = False
        t1 = threading.Thread(target=self.rcv_the_packets)
        t1.start()
        t2 = threading.Thread(target=self.send_packets)
        t2.start()
        print("waiting for 10 minutes...")
        time.sleep(self.time_to_test) # here should wait 10 minutes
        self.stop_thread = True
        t1.join()
        t2.join()
        print('thread currentConsumptionTest killed')
        self.temp_change.append([self.rcvD.all_strck.batParamRep["tempK"] / 10 - 273.15 , self.rcvD.all_strck.batParamRep["digTemp"],
                        self.all_strck.PICReadWriteMsg["data"]])
        # unplug unit from external voltage
        # wait for 10 min - check voltage/ current graph
        return "Pass"
    
    def temptest(self):
        #asking user to unplug voltage wire from unit:
        input("Please unplug unit and press a key")
        # configuring terminal:
        turn_tx_on()
        self.all_strck.Lmx2592FreqMsg["val"] = 29001
        self.sdm.send_the_message("Lmx2592FreqMsg", self.all_strck.Lmx2592FreqMsg)
        time.sleep(1)
        print("checking temperature status ...")
        time.sleep(10)
        # taking temperature samples :
        self.stop_thread = False
        t1 = threading.Thread(target=self.rcv_the_packets)
        t1.start()
        t2 = threading.Thread(target=self.send_packets)
        t2.start()
        time.sleep(self.time_to_test) # here should wait 10 minutes
        self.stop_thread = True
        t1.join()
        t2.join()
        print('thread temptest killed')
        self.temp_change.append([self.rcvD.all_strck.batParamRep["tempK"] / 10 - 273.15, self.rcvD.all_strck.batParamRep["digTemp"],
                            self.all_strck.PICReadWriteMsg["data"]])
        turn_tx_off()
        return "Pass"

    def activate(self):
        print(datetime.now())
        print("Scan The unit with the barcode:")
        unitName = input()
        #unitName = 1117
        print("Hello unit number: , " , unitName)
        
        props = getHRprops(unitName)
        print(f"props are: {props}")

        self.ws1.append(["SN", "ssid_name", "SW_Ver"])
        self.ws1.append([unitName, props[0], props[1]])
        print("Check all colors: red, blue, green! ")
        print("Enter OK if all colors apeared !")
        colorsStatus = input() #'OK'
        self.ws1.append(["", "colorsStatus"])
        self.ws1.append(["", colorsStatus])
        self.ws1.append(["time rebooting...", datetime.now()])
        print("rebooting...")
        self.sendReboot()  # OK - SSH
        self.ws1.append(["time", datetime.now()])
        time.sleep(20) # unit is waking up ...
        # connect to unit wifi:
        checkWifi()
        ping = CheckPingAllAngles('192.168.43.1',5) #returns -1 if no ping
        self.ws1.append(["", "pingStatus"])
        self.ws1.append(["", round(ping*1000, 5), "msec"])
        print("current Consumption Test...")
        self.ws1.append(["time", datetime.now()])
        self.ws1.append(["", "current_Consumption_Test"])
        cct = self.currentConsumptionTest()
        #לכבות את המתח של היחידה ומוציא הכל לשידור וקליטה
        self.ws1.append(["current Consumption Test result:", cct])
        print("temp test...")
        self.ws1.append(["time", datetime.now()])
        self.ws1.append(["", "temp_test"])
        tempt = self.temptest()
        self.ws1.append(["temp test result: ", tempt])
        
        self.ws1.append(["time", datetime.now()])
        
        print(datetime.now())
        self.ws1.append(["temperature changes:"])
        self.ws1.append(temp_change)
        self.me.saveTheWorkBookWithtimestamp()
        print('Done first prep !')




