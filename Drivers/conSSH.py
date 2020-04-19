import os
import sys
import time
import telnetlib
import string
import threading
from Drivers.cmdArp import *
from Drivers.ConnectToWifi import *


class SSH_Terminal:
       def __init__(self, hostname, username = 'root', password = 'root', port = 22, proxy = 'tester', usernameProxy = 'root', passwordProxy = 'root', auto_connect = True):

              port = 22
              self.timeout = 15
              self.hostname = hostname
              self.username = username
              self.usernameProxy = usernameProxy
              self.password = password
              self.passwordProxy = passwordProxy
              self.proxy = proxy

              #check ip to unit:
              unit_ip = "192.168.43.1"
              unit_ping = CheckPingAllAngles(unit_ip, 3)
              print("unit ping ", unit_ping)
              if unit_ping == -1:
                     print("unit didn't respond to ping , trying to reconnect...")
                     myWifi = Wifi_Connection()
                     try:
                            net = myWifi.wifi_connect_to_terminal()
                            print(f"conneted to {net}")
                            time.sleep(5)
                     except:
                            print("Could not connect to unit, is it on ?")
                     print('Wifi is connected')

              self.prompt1 = b'~$'
              self.prompt2 = b'~#'
              self.prompt3 =b'-sh-4.2#'
              self.active = False
              if auto_connect:
                     connected=self.Connect_root()

       def Connect_root(self):
              if self.active:
                     return
              self.tn = telnetlib.Telnet(self.proxy)
              self.tn.read_until(b"ubuntu login: ")
              self.Write(self.usernameProxy)
              self.tn.read_until(b"Password: ")
              self.Write(self.passwordProxy)
              print("Connected to proxy %s" % (self.proxy))
              self.Write("cd /home/tester/.ssh")
              self.Write("rm known_hosts")
              self.flush_buffer()

              # connect to the device
              self.Write('ssh %s@%s' % (self.username, self.hostname))

              sshask_passwd = bytes(self.username + "@" + self.hostname + "'s password: ", 'ascii')
              sshask_newkey = b'Are you sure you want to continue connecting (yes/no)?'
              noroutehost = b'No route to host'

              waitForPassword = False

              (i, ob, text) = self.tn.expect([sshask_newkey, sshask_passwd, noroutehost], self.timeout)
              if i == -1:
                     print("Timeout")
                     self.tn.close()
              if i == 0:
                     self.Write('yes')
                     self.tn.read_until(sshask_passwd, self.timeout)
                     waitForPassword = True
              if (i == 1) or (waitForPassword):
                     self.Write(self.password)
              if i == 2:
                     print("No route to host")
                     self.tn.close()

              import time
              time.sleep(3)
              self.tn.read_until(self.prompt2, self.timeout)
              self.tn.read_eager()
              print("Connected to the device %s" % (self.hostname))
              self.active = True
              print("The commands starts here")
              time.sleep(2)
              #self.Write('reboot')
              #print(self.tn.read_until(b"2019):"))

       def Write(self, command):
              self.tn.write(bytes(command, 'ascii') + b"\r\n")

       def Read_until(self, word):
              return self.tn.read_until(bytes(word, 'ascii'), self.timeout)

       def change_in_file_Nsave(self, word, word_to_put):
              self.Read_until(word)
              self.Write('a')
              self.Write(word_to_put)
              self.tn.write( b"\x1b" ) #Esc
              self.Write(":x")


       def flush_buffer(self):  # can change each self.Read('sdgbds',timeout) to this.
              scan = self.tn.read_very_eager()  # flush register
              scan = scan + self.tn.read_very_eager()  # flush register
              return scan




class ViMach:
       def __init__(self, proxy = 'picasso', usernameProxy = 'borism', passwordProxy = '1234'):

              self.check_VMware()

              myCmd = sendCmd()
              myCmd.lookVimIp()
              proxyIp = myCmd.getVimIpPing()
              print(proxyIp)

              self.timeout = 15
              self.usernameProxy = usernameProxy
              self.passwordProxy = passwordProxy
              self.proxy = proxyIp

              self.prompt1 = b'~$'
              self.prompt2 = b'~#'
              self.prompt3 = b'-sh-4.2#'
              self.active = False

              try:
                     self.tn = telnetlib.Telnet(self.proxy)
                     self.tn.read_until(b"ubuntu login: ")
                     self.Write(self.usernameProxy)
                     self.tn.read_until(b"Password: ")
                     self.Write(self.passwordProxy)
                     print ("Connected to proxy %s" % (self.proxy))
              except:
                     print("connection to vim failed")

       def Reset_VM(self):
              self.Write('sudo reboot')
              time.sleep(1)
              self.Write('root')
              time.sleep(30)
              try:
                     self.tn = telnetlib.Telnet(self.proxy)
              except:
                     time.sleep(10)
                     self.tn = telnetlib.Telnet(self.proxy)
              self.tn.read_until(b"ubuntu login: ")
              self.Write(self.usernameProxy)
              self.tn.read_until(b"Password: ")
              self.Write(self.passwordProxy)
              print ("Connected to proxy %s" % (self.proxy))


       def Write(self, command):
              try:
                     self.tn.write(bytes(command, 'ascii') + b"\r\n")
              except:
                     print("writing to vim failed")


       def check_VMware(self):
              import psutil

              if not ("vmware.exe" in (p.name() for p in psutil.process_iter())):
                     print("Starting VMware...")
                     os.startfile("C:/Program Files (x86)/VMware/VMware Workstation/vmware.exe")
                     time.sleep(15)

       def close_VMware(self):
              import psutil

              if "vmware.exe" in (p.name() for p in psutil.process_iter()):
                     os.system("taskkill /f /im vmware.exe")
                     time.sleep(1)


if __name__ == "__main__":

       A = ViMach(usernameProxy='tester', passwordProxy='root')
       A.Reset_VM()

       STA = SSH_Terminal(hostname="192.168.43.1", username='root', password='root', proxy=A.proxy,
                          usernameProxy='tester', passwordProxy='root')
       '''STA.Write('vi /media/SDcard/config_db.json')
       print(STA.Read_until("modem").decode())
       STA.change_in_file_Nsave("_Static_Terminal_", "1")
       STA.Write(":x")
       time.sleep(2)'''
       STA.Write('reboot')

       print('Done')


