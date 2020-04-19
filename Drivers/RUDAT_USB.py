###################################################################################################
#
#  Python library file to use with Mini-Circuits programmable Attenuator (Product ID 0x23)
#  This library use Libusb , PyUSB libraries
#  To use under Linux, Windows, OS
#  For Windows:
#  1. pip install libusb
#  2. pip install pyusb
#  3. copy libusb-1.0.dll (amd64 or x86 version according to Python ver 32/64 to Sys folder System32 or SysWow64) or add the path of the dll.
#  For Linux:
#  1. pip install libusb
#  2. pip install pyusb
#
##################################################################################################
import sys
import platform
import time
import usb.core
import usb.util


class USBDAT():
    # 64 bit array to send to USB
    cmd1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0]  # 64 bit array to send to USB

    def __init__(self):
        # find the device
        self.dev = usb.core.find(idVendor=0x20ce, idProduct=0x0023)
        # was it found?
        if self.dev is None:
            raise ValueError('Device not found')
        # set the active configuration. with no args we use first config.
        #  for Linux only
        if (platform.system == 'Linux'):

            for configuration in self.dev:
                for interface in configuration:
                    ifnum = interface.bInterfaceNumber
                if not self.dev.is_kernel_driver_active(ifnum):
                    continue
                try:
                    # print "detach kernel driver from device %s: interface %s" % (dev, ifnum)
                    self.dev.detach_kernel_driver(ifnum)
                except usb.core.USBError:
                    pass

        self.dev.set_configuration()
        self.cmd1[0] = 41
        self.dev.write(0x01, self.cmd1)  # SN
        s = self.dev.read(0x81, 64)
        self.SerialNumber = ""
        i = 1
        while (s[i] > 0):
            self.SerialNumber = self.SerialNumber + chr(s[i])
            i = i + 1
        self.cmd1[0] = 40
        self.dev.write(0x01, self.cmd1)  # Model
        s = self.dev.read(0x81, 64)
        self.ModelName = ""
        i = 1
        while (s[i] > 0):
            self.ModelName = self.ModelName + chr(s[i])
            i = i + 1

    def ReadSN(self):
        return str(self.SerialNumber)

    def ReadMN(self):
        return str(self.ModelName)

    def Send_SCPI(self, SCPIcmd):
        # send SCPI commands (to supported firmware only!)
        self.cmd1[0] = 42
        l1 = 0
        l1 = len(SCPIcmd)
        indx = 1
        while (indx <= l1):
            self.cmd1[indx] = ord(SCPIcmd[indx - 1])
            indx = indx + 1
        self.cmd1[indx] = 0
        self.dev.write(0x01, self.cmd1)  # SCP Command up to 60 chars;
        s = self.dev.read(0x81, 64)
        i = 1
        RetStr = ""
        while (s[i] > 0):
            RetStr = RetStr + chr(s[i])
            i = i + 1
        return str(RetStr)

