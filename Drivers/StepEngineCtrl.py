import serial
import threading
import time
import datetime


class MyStepEngine():
    def __init__(self, engine_type):
        try:
            self.ser = serial.Serial('COM3', baudrate=115200, timeout=None)
            print("Session serial with engine is now open.")
            self.read_from_engine = threading.Thread(target=self.thread_func)
            self.read_from_engine.start()
            self.engineType = engine_type
            self.stop_threads = False
            self.data_from_serial = ""
            self.location = 500
            self.finish_flag = False  # for all kinds of rotate
            self.home_flag = False
            self.location_flag = False
        except:
            print("turn engine ON... and press yes")
            ans = input()
            if ans.lower() == "yes":
                self.reconnect()
            else:
                print("press yes when told...")

    def reconnect(self):
        try:
            self.ser = serial.Serial('COM3', baudrate=115200, timeout=None)
        except:
            print("turn engine ON... and press yes")
            ans = input()
            if ans.lower() == "yes":
                self.reconnect()
            else:
                print("press yes when told...")

    def thread_func(self):
        while True:
            if self.ser.in_waiting:
                self.read_data()
            time.sleep(0.0000001)
            if self.stop_threads:
                break

    def read_data(self):
        if self.ser.in_waiting:
            self.data_from_serial = self.ser.readline().decode('utf-8')
            print(self.data_from_serial)

            if self.data_from_serial == "LOCATION1\r\n":
                self.location_flag = True
                self.location = self.ser.readline().decode('utf-8')
                print("the location is {}".format(self.location))

            if self.data_from_serial == "LOCATION2\r\n":
                self.location_flag = True
                self.location = self.ser.readline().decode('utf-8')
                print("the location is {}".format(self.location))

            if self.data_from_serial == "FINISHED1\r\n":
                self.finish_flag = True

            if self.data_from_serial == "NOW HOME1\r\n":
                self.home_flag = True

            if self.data_from_serial == "FINISHED2\r\n":
                self.finish_flag = True

            if self.data_from_serial == "NOW HOME2\r\n":
                self.home_flag = True

    def rotate_relative_cw(self, degrees):
        if self.engineType == "azimuth":
            cmd = "w"
        elif self.engineType == "elevation":
            cmd = "w".upper()
        else:
            print("No Engine !")
        try:
            self.finish_flag = False
            self.ser.write(cmd.encode())
            self.ser.write((degrees + '\n').encode())
            while not self.finish_flag:
                time.sleep(0.0001)
        except ValueError:
            print("some error", ValueError)

    def rotate_relative_ccw(self, degrees):
        if self.engineType == "azimuth":
            cmd = "x"
        elif self.engineType == "elevation":
            cmd = "x".upper()
        else:
            print("No Engine !")
        try:
            self.finish_flag = False
            self.ser.write(cmd.encode())
            self.ser.write((degrees+'\n').encode())
            while not self.finish_flag:
                time.sleep(0.0001)
        except ValueError:
            print("some error", ValueError)

    def rotate_absolute(self, degrees):
        if self.engineType == "azimuth":
            cmd = "a"
        elif self.engineType == "elevation":
            cmd = "a".upper()
        else:
            print("No Engine !")
        try:
            self.finish_flag = False
            self.ser.write(cmd.encode())
            self.ser.write((degrees + '\n').encode())
            while not self.finish_flag:
                time.sleep(0.0001)
        except ValueError:
            print("some error", ValueError)

    def stop(self):
        if self.engineType == "azimuth":
            cmd = "s"
        elif self.engineType == "elevation":
            cmd = "s".upper()
        else:
            print("No Engine !")
        try:
            self.ser.write(cmd.encode())
            time.sleep(1)
        except ValueError:
            print("some error", ValueError)

    def get_location(self):
        if self.engineType == "azimuth":
            cmd = "e"
        elif self.engineType == "elevation":
            cmd = "e".upper()
        else:
            print("No Engine !")
        try:
            self.location_flag = False
            self.ser.write(cmd.encode())
            while not self.location_flag:
                time.sleep(0.0001)

        except ValueError:
            print("some error", ValueError)

    def get_to_home(self):
        self.rotate_absolute("-10")
        if self.engineType == "azimuth":
            cmd = "h"
        elif self.engineType == "elevation":
            cmd = "h".upper()
        else:
            print("No Engine !")
        try:
            self.home_flag = False
            self.ser.write(cmd.encode())
            while not self.home_flag:
                time.sleep(0.0001)
        except ValueError:
            print("some error", ValueError)

    def set_zero(self):
        if self.engineType == "azimuth":
            cmd = "o"
        elif self.engineType == "elevation":
            cmd = "o".upper()
        else:
            print("No Engine !")
        try:
            self.ser.write(cmd.encode())
            print("Kaufman R&D", "Current Location\n   Is Set To 0.00")
            time.sleep(1)
        except ValueError:
            print("some error", ValueError)

    def set_speed(self, speed):
        if self.engineType == "azimuth":
            cmd = "d"
        elif self.engineType == "elevation":
            cmd = "d".upper()
        else:
            print("No Engine !")
        if int(speed) > 10 or int(speed) < 1:
            print("speed is only between 1 to 10.")
        try:
            self.ser.write(cmd.encode())
            self.ser.write((speed + '\n').encode())
            time.sleep(1)
        except ValueError:
            print("some error", ValueError)

    def check_communication(self):
        try:
            time.sleep(0.5)
            self.ser.write('q'.encode())
        except ValueError:
            print('some error', ValueError)

    def change_engine_type(self):
        if self.engineType == "azimuth":
            self.engineType = "elevation"
        elif self.engineType == "elevation":
            self.engineType = "azimuth"
        else:
            print("No Engine !")

    def Is_moving(self):
        self.get_location()
        a = float(self.location)
        time.sleep(1)
        self.get_location()
        b = float(self.location)
        return (a - b)

    def close_engine(self):
        time.sleep(2)
        self.stop_threads = True
        while self.read_from_engine.is_alive():
            time.sleep(0.01)
        self.read_from_engine.join()
        self.ser.close()
        print("Session with engine is now closed.")


def main():
    my_eng = MyStepEngine("azimuth")
    my_eng.check_communication()

    my_eng.get_to_home()

    '''ang = 0
    my_eng.get_location()
    while my_eng.location == 'aa':
        my_eng.get_location()
        time.sleep(0.1)
    while (float(my_eng.location) > float(ang + 0.2)) or (float(my_eng.location) < float(ang - 0.2)):
        my_eng.get_location()
        print(my_eng.location)
        print(f"i expect angle {float(ang)}")
    print(f"location : {my_eng.location}")'''

    # time.sleep(2)

    # my_eng.set_speed("10")
    '''my_eng.get_location()
    print("before")
    my_eng.rotate_relative_ccw("30")
    time.sleep(3)
    my_eng.get_location()
    print("after")'''
    # my_eng.rotate_relative_ccw("90")
    # my_eng.rotate_absolute(str(ang))
    # time.sleep(1)
    # time.sleep(2)
    # my_eng.stop()

    # for ang in range(0, 180, 2):
    #    my_eng.rotate_absolute(str(ang))
    #    now = datetime.datetime.now()
    #    print(now.strftime("%d/%m/%Y %H:%M:%S"))
    # while (float(my_eng.location) > float(ang + 0.2)) or (float(my_eng.location) < float(ang - 0.2)):
    '''for n in range(0,5):
        my_eng.get_location()
        print(my_eng.location)'''
        # print(float(ang))
        # print(f"location : {my_eng.location} arrived !")
    #    now = datetime.datetime.now()
    #    print(now.strftime("%d/%m/%Y %H:%M:%S"))

    '''for ang in range(-90, 91, 2):
        my_eng.rotate_absolute(str(ang))
        my_eng.get_location()
        while (float(my_eng.location) > float(ang + 0.2)) or (float(my_eng.location) < float(ang - 0.2)):
            my_eng.get_location()
            print(my_eng.location)
            print(f"i expect angle {float(ang)}")

    time.sleep(5)
    print(f"location : {my_eng.location} arrived !")'''

    # now = datetime.datetime.now()
    # print(now.strftime("%d/%m/%Y %H:%M:%S"))

    #my_eng.get_to_home()
    # my_eng.get_location()
    # my_eng.set_zero()
    # my_eng.set_speed("5")
    # for i in range(0,10):
    #     print("Is moving: ", my_eng.Is_moving())
    # time.sleep(2)
    '''my_eng.change_engine_type()
    print(my_eng.engineType)
    my_eng.location = 500
    my_eng.get_to_home()'''
    # my_eng.set_speed("5")
    # my_eng.rotate_relative_cw("25")
    # my_eng.rotate_relative_ccw("75")
    # my_eng.rotate_absolute("90")
    # time.sleep(1)
    #time.sleep(2)
    # my_eng.stop()
    #my_eng.get_location()
    #while my_eng.location == 'aa':
    #    my_eng.get_location()
    #    time.sleep(0.1)
    #for ang in range(0, 180, 2):
    #    my_eng.rotate_absolute(str(ang))
    #    now = datetime.datetime.now()
    #    print(now.strftime("%d/%m/%Y %H:%M:%S"))
    #    while (float(my_eng.location) > float(ang + 0.2)) or (float(my_eng.location) < float(ang - 0.2)):
    #        my_eng.get_location()
    #        print(my_eng.location)
    #        print(float(ang + 0.2))
    #    print(f"location : {my_eng.location} arrived !")
    #    now = datetime.datetime.now()
    #    print(now.strftime("%d/%m/%Y %H:%M:%S"))
    # my_eng.get_location()
    # my_eng.get_location()
    # my_eng.get_to_home()
    # my_eng.get_location()
    # my_eng.get_location()
    # my_eng.set_zero()
    # my_eng.set_speed("10") # -- limits are between 1 to 10
    '''for ang in range(-90, 91, 2):
        my_eng.rotate_absolute(str(ang))
        my_eng.get_location()
        while (float(my_eng.location) > float(ang + 0.2)) or (float(my_eng.location) < float(ang - 0.2)):
            my_eng.get_location()
            print(my_eng.location)
            print(f"i expect angle {float(ang)}")
'''
    # my_eng.check_communication()
    my_eng.close_engine()


if __name__ == "__main__":
    main()