from Drivers.ExcelCtrl import *
from Drivers.Terminal.SendDataMsg import *
from Drivers.Terminal.ReadEthData import *
from Tests.commFunctions import *
from Drivers.StepEngineCtrl import *
from datetime import *
from Tests.all_init import *
import time


class imuNgps(allInitDefinitions):
    def __init__(self):
        self.stop_thread = False
        self.ang_x = self.ang_y = 0
        self.speed = "10"
        self.end_ang = []
        self.my_eng = MyStepEngine("azimuth")
        super().__init__()

    #read imu - roll, pitch, yaw
    def rcv_the_packets(self):
        FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
        logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)

        v = [self.rcvD.all_strck.PointAntStruct["imuRoll"], self.rcvD.all_strck.PointAntStruct["imuPitch"],
                self.rcvD.all_strck.PointAntStruct["imuYaw"], self.rcvD.all_strck.dynPointParamMsg["status"],
             self.rcvD.all_strck.dynPointParamMsg["latitude"], float(self.rcvD.all_strck.dynPointParamMsg["longitude"]),
             self.rcvD.all_strck.dynPointParamMsg["altitude"]]

        ctime = time.time()
        try:
            for [data, addr] in self.rcvD.start_receiving():
                self.rcvD.updateFeildsFromInputMsg()
                if time.time() - ctime > 0.1:
                    self.update_batstat_excel()
                    ctime = time.time()
                if self.stop_thread:
                    break
        except ValueError:
            print("trying to connect to uut again...", ValueError)
            checkWifi()
            time.sleep(1)
            self.rcv_the_packets()


    def update_batstat_excel(self):
        if self.ang_x is None or self.ang_y is None:
            print(f"type ang_x is {type(self.ang_x)} type ang_y is {type(self.ang_y)}")
            print(f"ang_x is {self.ang_x} ang_y is {self.ang_y}")
        elif self.rcvD.all_strck.PointAntStruct["imuRoll"] != 0:
            self.ws2.append([float(self.ang_x), float(self.ang_y), self.rcvD.all_strck.PointAntStruct["imuRoll"],
                             self.rcvD.all_strck.PointAntStruct["imuPitch"], self.rcvD.all_strck.PointAntStruct["imuYaw"],
                             self.rcvD.all_strck.dynPointParamMsg["status"], self.rcvD.all_strck.dynPointParamMsg["latitude"],
                             self.rcvD.all_strck.dynPointParamMsg['longitude'] * 1e100, self.rcvD.all_strck.dynPointParamMsg["altitude"]])


    def moveEngine(self):
        self.ang_x = self.ang_y = 0
        self.my_eng.set_speed(self.speed)
        for ang in range(-90, 91, +2):
            self.my_eng.rotate_absolute(str(ang))
            if ang == 90 or ang == -90:
                # wait for unit to refresh:
                print("waiting for ang to refresh...")
                self.wait_unit_place_report()
            cur_ang = self.my_eng.location
            while abs(float(self.my_eng.location) - ang) != 0.0:
                time.sleep(0.01)
                self.my_eng.get_location()
            cur_ang = self.my_eng.location
            if self.my_eng.engineType == "azimuth":
                self.ang_x = cur_ang
            elif self.my_eng.engineType == "elevation":
                self.ang_y = cur_ang
        self.my_eng.get_to_home()
        if self.my_eng.engineType == "azimuth":
            self.ang_x = 0
        elif self.my_eng.engineType == "elevation":
            self.ang_y = 0


    def wait_unit_place_report(self):
        x = y = 0
        delta_x = delta_y = 10
        if self.my_eng.engineType == "azimuth":
            x = self.rcvD.all_strck.PointAntStruct["imuYaw"]
            print(f"PointAntStruct['imuYaw'] x is {self.rcvD.all_strck.PointAntStruct['imuYaw']}")
            while abs(delta_x) > 1:
                time.sleep(2)
                delta_x = self.rcvD.all_strck.PointAntStruct["imuYaw"] - x
                print(f"PointAntStruct['imuYaw'] x is {self.rcvD.all_strck.PointAntStruct['imuYaw']}")
                print(f"delta x is {delta_x}")
                time.sleep(0.1)
                x = self.rcvD.all_strck.PointAntStruct["imuYaw"]
            self.end_ang.append(x)
        elif self.my_eng.engineType == "elevation":
            y = self.rcvD.all_strck.PointAntStruct["imuPitch"]
            print(f"PointAntStruct['imuPitch'] y is {self.rcvD.all_strck.PointAntStruct['imuPitch']}")
            while abs(delta_y) > 1:
                time.sleep(2)
                delta_y = self.rcvD.all_strck.PointAntStruct["imuPitch"] - y
                print(f"PointAntStruct['imuPitch'] y is {self.rcvD.all_strck.PointAntStruct['imuPitch']}")
                print(f"delta y is {delta_y}")
                time.sleep(0.1)
                y = self.rcvD.all_strck.PointAntStruct["imuPitch"]
            self.end_ang.append(y)

    def check_imu(self):
        imu_x_delta = imu_y_delta = 0
        if len(self.end_ang) >= 2:
            imu_x_delta = self.end_ang[1] - self.end_ang[0]
            if abs(imu_x_delta) > 170:
                print("imu yaw is working as excected")
                self.ws2.append(["imu yaw Pass"])
            else:
                print("imu yaw is not working as excected")
                self.ws2.append(["imu yaw Fail"])
        else:
            print("no data from x axis to determine if imu yaw report from unit is correct.")
        if len(self.end_ang) >= 4:
            imu_y_delta = self.end_ang[3] - self.end_ang[2]
            if abs(imu_y_delta) > 170:
                print("imu pitch is working as excected")
                self.ws2.append(["imu pitch Pass"])
            else:
                print("imu pitch is not working as excected")
                self.ws2.append(["imu pitch Fail"])
        else:
            print("no data from y axis to determine if imu pitch report from unit is correct.")

    def activate(self):
        try:
            print(datetime.now())
            self.my_eng.check_communication()

            print(datetime.now())
            self.ws2.append(["time", datetime.now()])
            print("imu test ...")
            self.my_eng.engineType = "azimuth"
            self.ws2.append(["imU Test", "azimuth - X axis", ""])
            self.ws2.append(["X", "Y", "imuRoll", "imuPitch(y)", "imuYaw(x)", "gps Status", "latitude", "longitude * 1e100", "altitude"])

            self.stop_thread = False
            t1 = threading.Thread(target=rcv_the_packets)
            t1.start()
            #move the engine from -90 to +90 (azimuth - X axis)
            self.moveEngine()
            #always read

            self.ws2.append(["time", datetime.now()])
            self.my_eng.engineType = "elevation"
            self.ws2.append(["imU Test", "elevation - Y axis", ""])
            self.ws2.append(["X", "Y", "imuRoll", "imuPitch(y)", "imuYaw(x)", "gps Status", "latitude", "longitude * 1e100", "altitude"])

            #move the engine from -90 to +90 (elevation - Y axis)
            self.moveEngine()
            #always read

            self.stop_thread = True
            t1.join()

            self.check_imu()

            #GPS - check status = 1
            self.ws2.append(["time", datetime.now()])
            print("Gps test ...")
            self.my_eng.engineType = "azimuth"
            self.ws2.append(["GPs Test", "azimuth - X axis", ""])
            self.ws2.append(["X", "Y", "imuRoll", "imuPitch(y)", "imuYaw(x)", "gps Status", "latitude", "longitude * 1e100", "altitude"])

            self.stop_thread = False
            t2 = threading.Thread(target=rcv_the_packets)
            t2.start()
            #move the engine from -90 to +90 (azimuth - X axis)
            self.moveEngine()
            #always read GPS - check status = 1

            self.my_eng.engineType = "elevation"
            self.ws2.append(["time", datetime.now()])
            self.ws2.append(["GPs Test", "elevation - Y axis", ""])
            self.ws2.append(["X", "Y", "imuRoll", "imuPitch(y)", "imuYaw(x)", "gps Status", "latitude", "longitude * 1e100", "altitude"])
            #move the engine from -90 to +90 (elevation - Y axis)
            self.moveEngine()
            #always read GPS - check status = 1
            self.stop_thread = True
            t2.join()

            self.ws2.append(["time", datetime.now()])

            print('Done imu and gps test !')

        finally:
            self.ws2.append(["ends of ang:"])
            self.ws2.append(["imu_x_start", "imu_x_stop", "imu_y_start", "imu_y_stop", "gps_x_start", "gps_x_stop", "gps_y_start", "gps_y_stop"])
            self.ws2append(end_ang)
            self.me.saveTheWorkBookWithtimestamp()
            print(self.end_ang)
            print(datetime.now())
            self.my_eng.close_engine()

