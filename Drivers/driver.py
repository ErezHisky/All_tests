import os
import sys
import time
import telnetlib
import string
import threading


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


        #self.prompt1 = '~ #'
        self.prompt1 = b'~$'
        self.prompt2 = b'~#'
        self.prompt3 =b'-sh-4.2#'
        self.active = False
        if auto_connect:
            connected=self.Reconnect()

    def Connect_admin(self):
        if self.active:
            return
        self.tn = telnetlib.Telnet(self.proxy)
        self.tn.read_until("login: ")
        self.Write(self.usernameProxy)
        self.tn.read_until("Password: ")
        self.Write(self.passwordProxy)
        print ("Connected to proxy %s" % (self.proxy))
        self.Write("cd /home/tester/.ssh")
        self.Write("rm known_hosts")
        # connect to the device
        self.Write('ssh %s@%s' %(self.username, self.hostname))

        sshask_passwd = self.username + "@" + self.hostname + "'s password: "
        sshask_newkey = 'Are you sure you want to continue connecting (yes/no)?'
        noroutehost = 'No route to host'

        waitForPassword = False

        (i, ob, text) = self.tn.expect([sshask_newkey, sshask_passwd, noroutehost], self.timeout)
        if i == -1:
            print ("Timeout")
            self.tn.close()
        if i == 0:
            self.Write('yes')
            self.tn.read_until(sshask_passwd, self.timeout)
            waitForPassword = True
        if (i == 1) or (waitForPassword):
            self.Write(self.password)
        if i == 2:
            print ("No route to host")
            self.tn.close()

        import time
        time.sleep(3)
        print (self.tn.read_eager())
        self.Write('debug login')
        time.sleep(3)
        self.Write('root')
        time.sleep(3)
        self.Write('NemarLaki@34')
        time.sleep(3)
        self.tn.read_until(self.prompt3, self.timeout)
        self.tn.read_eager()
        self.Write('export tmout=0')
        print ("Connected to the device %s" %(self.hostname))
        self.active = True
        print("here")

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
        self.Write('ssh %s@%s' %(self.username, self.hostname))

        sshask_passwd = bytes(self.username + "@" + self.hostname + "'s password: ", 'ascii')
        sshask_newkey = b'Are you sure you want to continue connecting (yes/no)?'
        noroutehost = b'No route to host'

        waitForPassword = False

        (i, ob, text) = self.tn.expect([sshask_newkey, sshask_passwd, noroutehost], self.timeout)
        if i == -1:
            print ("Timeout")
            self.tn.close()
        if i == 0:
            self.Write('yes')
            self.tn.read_until(sshask_passwd, self.timeout)
            waitForPassword = True
        if (i == 1) or (waitForPassword):
            self.Write(self.password)
        if i == 2:
            print ("No route to host")
            self.tn.close()

        import time
        time.sleep(3)
        self.tn.read_until(self.prompt2, self.timeout)
        self.tn.read_eager()
        print ("Connected to the device %s" %(self.hostname))
        self.active = True
        print("benny test here")
        self.Write('reboot')

    def Reconnect(self):
        self.Close()
        tries=1
        while (not self.active) and (tries<10):
            try:
                if self.username == 'root':
                    self.Connect_root()
                elif self.username == 'admin':
                    self.Connect_admin()
            except EOFError:
                tries+=1
        if not self.active:
            print('connection failed - timeout')
            return (0)
        return tries

    def __del__(self):
        self.Close()

    def Close(self):
        if not self.active:
            return
        self.Write("exit")
        self.Write("exit")
        self.tn.close()
        self.active = False

    def Close_th(self):
        self.tn.close()
        self.active = False


    def Read(self, prompt = None, Override_timeout=0):
        if not Override_timeout:
            timeout=self.timeout
        else:
            timeout=Override_timeout

        if prompt == None:
            return self.tn.read_until(self.prompt1, timeout)
        else:
            return self.tn.read_until(prompt, timeout)

    def Write(self, command):
        self.tn.write(bytes(command, 'ascii') + b"\r\n")

    def CliCommand(self,cmd):
        self.flush_buffer()
        self.Write("cli")
        self.Read(self.prompt2)
        self.Write(cmd)
        data = self.Read(self.prompt2)
        self.Write("exit")
        return data

    def RF_temp(self):
        try:
            self.Write("cd /sys/kernel/debug/ieee80211/phy0/wil6210/")
            self.flush_buffer()
            temp = self.Read(self.prompt3)
            self.Write("cat temp")
            temp = self.Read(self.prompt3)
            BBtemp = temp.strip().split()[4]
            RFtemp = temp.strip().split()[7]
            if temp.strip().split()[2]== 'T_mac' and temp.strip().split()[5] == 'T_radio':
                temp_vec = []
                temp_vec.append(BBtemp)
                temp_vec.append(RFtemp)
                return temp_vec
            else:
                temp_vec = []
            temp_vec.append(10000)
            temp_vec.append(10000)
        except:
            temp_vec = []
            temp_vec.append(10000)
            temp_vec.append(10000)


    def Iperf_Server(self,port=5001):
        self.Write("iperf -s -p "+str(port)+" &") # activate iperf
        time.sleep(1)
        self.Write("") # add another Enter key
        print(self.Read(self.prompt3))


    def Iperf_Client(self,Server_sys,interval=2, traffic_time=600, port=5001):
        a=self.Write("iperf -c "+Server_sys+" -i"+str(interval)+" -t"+str(traffic_time)+" -p"+str(port)+" &")
        rest=self.Read(self.prompt3)
        print(rest)

    def Kill_Proces(self,Proces):
        self.flush_buffer()
        self.Read(self.prompt3)
        self.Write('killall %s'%(Proces))
        time.sleep(2)
        self.Write('killall %s'%(Proces))
        print('kiled the Process')

    def Stat_BF(self):
        try:
            self.Read(self.prompt3)
            self.Write("cd /sys/kernel/debug/ieee80211/phy0/wil6210/")
            scan=self.Read(self.prompt3)
            self.Write("cat bf")
            scan=self.Read(self.prompt3)
            RX_Sec=int(scan.splitlines()[6].split(':')[2].strip().split()[0])
            TX_Sec=int(scan.splitlines()[6].split(':')[3].strip())
            return RX_Sec,TX_Sec
        except:
            return 10000,10000

    def Link_status(self):
        try:
            self.flush_buffer()
            self.Read(self.prompt3)
            Link_status = self.CliCommand("show unit-debug")
            status = Link_status.strip().split()[17]
            if status == 'bf-ok':
                return 1
        except:
            return 0

    def modemd_2(self):
        try:
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write("modemd 2")
            modemdS=self.Read(self.prompt3)
            MCS_Avg=float(modemdS.splitlines()[1].split(',')[0].strip())
            if MCS_Avg > 13 or MCS_Avg < 0.5:
                return 10000
            else:
                return MCS_Avg
        except:
            return 10000

    def throughput(self):
        try:
            self.flush_buffer()
            self.Read(self.prompt3)
            time.sleep(2)
            modemdS=self.Read(self.prompt3)
            try:
                mod_a = modemdS.splitlines()[0].split(' ')[9].strip()
            except:
                mod_a = 0
            try:
                mod_b =modemdS.splitlines()[0].split(' ')[10].strip()
            except:
                mod_b = 0
            try:
                mod_c =modemdS.splitlines()[0].split(' ')[11].strip()
            except:
                mod_c = 0
            try:
                mod_d =modemdS.splitlines()[0].split(' ')[12].strip()
            except:
                mod_d = 0

                if mod_a =='Gbits/sec' or mod_a =='Mbits/sec' or mod_a =='Kbits/sec' or mod_a=='bits/sec':
                    throughput = float(modemdS.splitlines()[0].split(' ')[8].strip())
                    rate = modemdS.splitlines()[0].split(' ')[9].strip()

                elif mod_b =='Gbits/sec' or mod_b =='Mbits/sec' or mod_b =='Kbits/sec' or mod_b=='bits/sec':
                    throughput = float(modemdS.splitlines()[0].split(' ')[9].strip())
                    rate = modemdS.splitlines()[0].split(' ')[10].strip()

                elif mod_c =='Gbits/sec' or mod_c =='Mbits/sec' or mod_c =='Kbits/sec' or mod_c=='bits/sec':
                    throughput = float(modemdS.splitlines()[0].split(' ')[10].strip())
                    rate = modemdS.splitlines()[0].split(' ')[11].strip()

                elif mod_d =='Gbits/sec' or mod_d =='Mbits/sec' or mod_d =='Kbits/sec' or mod_d=='bits/sec':
                    throughput = float(modemdS.splitlines()[0].split(' ')[11].strip())
                    rate = modemdS.splitlines()[0].split(' ')[12].strip()

            if rate == 'Gbits/sec':
                throughput = throughput*1000
            elif rate == 'Kbits/sec':
                throughput = throughput/1000
            elif rate == 'bits/sec':
                throughput = throughput/1000000

            return throughput
        except:
            return 10000


    def SetRfCh(self,channel):
        try:
            tries=1
            channel_read =' '
            while (tries<5):
                print(tries)
                tries+=1
                cmd = 'set base-unit frequency channel-'+ str(channel)
                print('the channel is set')
                self.CliCommand(cmd)
                time.sleep(2)
                self.flush_buffer()
                self.Read(self.prompt3)
                self.Write("cd /tmp/modem/")
                self.Write("cat hostapd.conf")
                data=self.Read(self.prompt3)
                if (data.strip().split()[8]) == 'wpa=0':
                    channel_read = data.strip().split()[9]
                elif (data.strip().split()[9]) == 'wpa=0':
                    channel_read = data.strip().split()[10]
                elif (data.strip().split()[10]) == 'wpa=0':
                    channel_read = data.strip().split()[11]
                elif (data.strip().split()[11]) == 'wpa=0':
                    channel_read = data.strip().split()[12]
                elif (data.strip().split()[12]) == 'wpa=0':
                    channel_read = data.strip().split()[13]
                elif (data.strip().split()[13]) == 'wpa=0':
                    channel_read = data.strip().split()[14]

                if channel_read != 'channel=%s'%(channel) :
                    print('the ch isnt o.k')
                    print(channel_read)
                else:
                    break

            return channel_read
        except:
            return 10000

    def flush_buffer(self): # can change each self.Read('sdgbds',timeout) to this.
        scan=self.tn.read_very_eager() # flush register
        scan=scan + self.tn.read_very_eager() # flush register
        return scan

    def Set_Sys_To_EIRP(self):
        try:
            self.Write('export tmout=0')
            time.sleep(1)
            self.Kill_Proces('wpa_supplicant')
            time.sleep(1)
            self.Kill_Proces('hostapd')
            time.sleep(1)
            self.Kill_Proces('iperf')
            time.sleep(1)
            self.Write('ifconfig wlan0 down')
            time.sleep(1)
            self.Write('ifconfig wlan0 up')
            time.sleep(1)
            self.Write('wigig_remoteserver -p 2390 &')
            time.sleep(1)
        except:
            print ('please reboot the system')

    def Reset_System(self):
        try:
            self.CliCommand('reset system')
        except:
            print ('done')

    def Cw_Mode(self):
        try:
            self.Write('export tmout=0')
            #time.sleep(1)
            self.Kill_Proces('wpa_supplicant')
            #time.sleep(1)
            self.Kill_Proces('hostapd')
            #time.sleep(1)
            self.Kill_Proces('iperf')
            #time.sleep(1)
            self.Write('ifconfig wlan0 down')
            time.sleep(1)
            self.Write('ifconfig wlan0 up')
            #time.sleep(1)
            self.Write('cd /sys/kernel/debug/ieee80211/phy0/wil6210/')
            #time.sleep(1)
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write('cat set_cw')
            set_cw = self.Read(self.prompt3)
            return set_cw
        except:
            print ('need to fix please call benny')

    def Set_Freq(self,ch):
        try:
            cmd = 'echo %s > cw_config_freq'%str(ch)
            self.Write(cmd)
            self.Write('cat set_cw')
            #time.sleep(1)
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write('echo 0x883020 > mem_addr; cat mem_val')
            Set_freq = self.Read(self.prompt3)
            return Set_freq
        except:
            print ('need to fix please call benny')

    def Set_Sector(self,sector_num):
        try:
            cmd = 'echo %s > cw_config_sector'%str(sector_num)
            self.Write(cmd)
            #time.sleep(1)
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write('cat set_sector_gain')
            self.flush_buffer()
            set_sector = self.Read(self.prompt3)
            return set_sector
        except:
            print ('need to fix please call benny')

    def Set_Gain(self,gain_num):
        try:
            cmd = 'echo %s > cw_config_gain'%str(gain_num)
            self.Write(cmd)
            #time.sleep(1)
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write('cat set_sector_gain')
            self.flush_buffer()
            set_gain = self.Read(self.prompt3)
            return set_gain
        except:
            print ('need to fix please call benny')

    def Set_Etype_Phase_low_Phase_High(self,etype_num,phase_low,phase_high):
        try:
            cmd = 'echo %s > brd_config_etype'%str(etype_num)
            self.Write(cmd)
            cmd_low = 'echo %s > brd_config_psh_low'%str(phase_low)
            self.Write(cmd_low)
            cmd_high = 'echo %s > brd_config_psh_high'%str(phase_high)
            self.Write(cmd_high)
            self.flush_buffer()
            self.Read(self.prompt3)
            self.Write('cat write_sector')
            self.flush_buffer()
            set_etype = self.Read(self.prompt3)
            return set_etype
        except:
            print ('need to fix please call benny')


    def Config_Phase(self,default_phase):
        phase_l=0
        phase_h=0
        for ant in range(0,32,1):
            phase = default_phase[ant]
            if phase == 0:
                val = 0
            elif phase == 90:
                val = 1
            elif phase == 180:
                val = 2
            elif phase == 270:
                val = 3;

            if ant < 16:
                phase_l = phase_l + (val << (ant)*2)
            else:
                phase_h = phase_h + (val<<(ant-16)*2)

        return phase_l,phase_h

    def Config_Etype(self,default_Etype):
        Etype=0
        for ant in range(0,32,1):
            gain = default_Etype[ant]
            Etype = Etype + (gain << (ant)*1)

        return Etype

class VM:

    def __init__(self, proxy = 'picasso', usernameProxy = 'borism', passwordProxy = '1234'):

        self.timeout = 15
        self.usernameProxy = usernameProxy
        self.passwordProxy = passwordProxy
        self.proxy = proxy


        #self.prompt1 = '~ #'
        self.prompt1 = b'`$'
        self.prompt2 = b'>'
        self.prompt3 = b'-sh-4.2#'
        self.active = False

        self.tn = telnetlib.Telnet(self.proxy)
        self.tn.read_until(b"ubuntu login: ")
        self.Write(self.usernameProxy)
        self.tn.read_until(b"Password: ")
        self.Write(self.passwordProxy)
        print ("Connected to proxy %s" % (self.proxy))


    def Ping(self,UUT):
        ping =0
        tries=0
        fail_flag=1
        while ping!= 1 and (tries<20) :
            time.sleep(5)
            tries+=1
            self.flush_buffer()
            self.tn.read_until(self.prompt1, self.timeout)
            self.Write("ping %s -c 3" %UUT)
            a=self.tn.read_until(self.prompt1, self.timeout)
            print(a.strip().split()[15])
            if a.strip().split()[15]== 'icmp_seq=1':
                print('done')
                ping =1
                fail_flag=0

        if fail_flag==1:
            return 0
        else:
            return 1

    def flush_buffer(self): # can change each self.Read('sdgbds',timeout) to this.
        scan=self.tn.read_very_eager() # flush register
        scan=scan + self.tn.read_very_eager() # flush register
        return scan

    def Reset_VM(self):
        self.Write('sudo reboot')
        time.sleep(1)
        self.Write('root')
        time.sleep(15)
        self.tn = telnetlib.Telnet(self.proxy)
        self.tn.read_until(b"ubuntu login: ")
        self.Write(self.usernameProxy)
        self.tn.read_until(b"Password: ")
        self.Write(self.passwordProxy)
        print ("Connected to proxy %s" % (self.proxy))


    def Write(self, command):
        self.tn.write(bytes(command, 'ascii') + b"\r\n")


if __name__ == "__main__":
    A = VM(proxy = '192.168.192.130', usernameProxy = 'tester', passwordProxy = 'root')
    A.Reset_VM()

    STA = SSH_Terminal(hostname = "192.168.43.1", username = 'root', password = 'root', proxy = '192.168.192.130', usernameProxy = 'tester', passwordProxy = 'root')

